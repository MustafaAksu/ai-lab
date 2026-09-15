"""S4 runner: the only module that invokes a provider (PREREG-RS-0001 v0.3.2 §3, §8, §9.1).

Membrane: imports ai_lab.providers.* only (WARR-20260912-0001 cond. 6).
Provenance: Option S — no InvocationRecords; one JSONL per stage with
content-addressed rows, each completed stage's digest entered in the campaign
manifest. INTEGRATION_EFFECT = "none" on every artifact.

Stages (each a CLI sub-command; nothing runs implicitly):
  profile      resolve and FREEZE campaign_execution_profile.json before any call
  calibration  Arm 1 only, 10 unique + 10 ambiguous per populated (n, d); STOP rule
  pilot        both arms, 10 per stratum on N_main; direction-blinded N_req, looks,
               z_k written to the manifest and hashed BEFORE direction is unlocked
  main         one block per invocation; adjudication only at preregistered looks
Every provider call is preceded by admit_instance() and by the FRAME_SHA256 check.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable, Protocol

from . import INTEGRATION_EFFECT, PLAN_ID, PREREG_ID, PREREG_VERSION, WARRANT_ID
from .equivalence import admit_instance
from .generator import Instance, generate_stratum, populated
from .oracle import oracle_status
from .render import FLAT_VERSION, FRAME_SHA256, FRAME_VERSION, RM_VERSION, prompt
from .scoring import Paired, adjudicate, parse_output, required_pairs, score
from .sequential import blocks, look_schedule, schedule_for

# ---- frozen operator values (PREREG v0.3.2 §7, §8.1) -----------------------
SESOI = 0.03
N_MIN, N_MAX = 1200, 2616
BLOCK = 240
CAL_WINDOW = (0.30, 0.80)
CAL_CENTRE = 0.55
CAL_N_RANGE = tuple(range(3, 10))
CAL_D_RANGE = tuple(range(1, 7))
CAL_PER_STATE = 10
PILOT_PER_STRATUM = 10
MAIN_D = (1, 2, 3, 4)
STATES = ("unique", "ambiguous")


class ProviderLike(Protocol):
    name: str
    model: str

    def ask_with_outcome(self, prompt: str): ...


ProviderFactory = Callable[[str], ProviderLike]


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _sha_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git(*args: str) -> str:
    try:
        return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout.strip()
    except Exception:  # noqa: BLE001 - provenance is best-effort but recorded honestly
        return "unavailable"


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime())


def _write_json(path: Path, obj: object) -> None:
    path.write_text(json.dumps(obj, indent=1, sort_keys=True) + "\n", encoding="utf-8")


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def default_provider_factory(provider: str) -> ProviderLike:
    """Real providers; imported lazily so the zero-API modules never need the SDKs."""
    if provider == "openai":
        from ai_lab.providers.openai_provider import OpenAIProvider

        return OpenAIProvider()
    if provider == "claude":
        from ai_lab.providers.claude_provider import ClaudeProvider

        return ClaudeProvider()
    raise ValueError(provider)


# ---- profile ----------------------------------------------------------------

def resolve_profile(provider: str, seed: int) -> dict:
    """Execution profile from configured settings; provider-managed or
    unexposed parameters are recorded as provider_default (PREREG §3)."""
    from ai_lab.providers import settings

    if provider == "openai":
        model, effort, max_tokens = settings.OPENAI_MODEL, settings.OPENAI_REASONING_EFFORT, None
    elif provider == "claude":
        model, effort, max_tokens = settings.CLAUDE_MODEL, settings.CLAUDE_EFFORT, settings.CLAUDE_MAX_TOKENS
    else:
        raise ValueError(provider)
    return {
        "prereg": f"{PREREG_ID} {PREREG_VERSION}",
        "plan_id": PLAN_ID,
        "warrant_id": WARRANT_ID,
        "integration_effect": INTEGRATION_EFFECT,
        "provider": provider,
        "model": model,
        "reasoning_effort": effort if effort else "provider_default",
        "max_output_tokens": max_tokens if max_tokens is not None else "provider_default",
        "temperature": "provider_default",
        "seed_param": "provider_default",
        "frame_version": FRAME_VERSION,
        "frame_sha256": FRAME_SHA256,
        "serializers": {"arm1": FLAT_VERSION, "arm2": RM_VERSION},
        "campaign_seed": seed,
        "sesoi": SESOI,
        "n_min": N_MIN,
        "n_max": N_MAX,
        "block": BLOCK,
        "git_commit": _git("rev-parse", "HEAD"),
        "git_dirty": bool(_git("status", "--porcelain")) if _git("rev-parse", "HEAD") != "unavailable" else "unavailable",
        "frozen_at": _now(),
    }


def cmd_profile(out: Path, provider: str, seed: int) -> Path:
    out.mkdir(parents=True, exist_ok=True)
    path = out / "campaign_execution_profile.json"
    if path.exists():
        raise SystemExit("profile already frozen; refusing to overwrite")
    _write_json(path, resolve_profile(provider, seed))
    return path


def _load_profile(out: Path) -> dict:
    path = out / "campaign_execution_profile.json"
    if not path.exists():
        raise SystemExit("no frozen profile: run `profile` first")
    prof = _read_json(path)
    if prof["frame_sha256"] != FRAME_SHA256:
        raise SystemExit("FRAME_SHA256 mismatch: prompt frame drifted since the profile was frozen")
    if prof["integration_effect"] != INTEGRATION_EFFECT:
        raise SystemExit("integration_effect mismatch")
    return prof


def _check_provider_matches(prof: dict, prov: ProviderLike) -> None:
    if getattr(prov, "model", None) != prof["model"]:
        raise SystemExit(f"provider model {getattr(prov, 'model', None)!r} != frozen {prof['model']!r}")


# ---- one call ---------------------------------------------------------------

@dataclass(frozen=True)
class Row:
    stage: str
    puzzle_id: str
    trial_id: str
    arm: int
    n: int
    depth: int
    target_state: str
    target: str
    omega: tuple[str, ...]
    serializer: str
    prompt_sha256: str
    prompt_chars: int
    response: str
    response_sha256: str
    parsed_status: str | None
    parsed_answer: tuple[str, ...]
    parse_ok: bool
    correct: bool
    stop_reason: str | None
    input_tokens: int | None
    output_tokens: int | None
    attempts: int
    error: str | None
    started_at: str
    finished_at: str
    integration_effect: str = INTEGRATION_EFFECT


def run_trial_arm(inst: Instance, arm: int, prov: ProviderLike, stage: str, retries: int = 1) -> Row:
    pz, target = inst.trial.puzzle, inst.trial.target
    adm = admit_instance(pz)
    if not adm.ok:
        raise RuntimeError(f"instance not admitted: {adm.failed}")  # caller filters before calling
    text = prompt(inst.trial, arm)
    started = _now()
    err, out, attempts = None, None, 0
    while attempts <= retries and out is None:
        attempts += 1
        try:
            out = prov.ask_with_outcome(text)
        except Exception as e:  # noqa: BLE001 - recorded, retried once, then a missing pair
            err = f"{type(e).__name__}: {e}"
    status, omega = oracle_status(pz, target)
    if out is None:
        return Row(stage, pz.puzzle_id(), inst.trial.trial_id(), arm, inst.n, inst.depth, inst.target_state, target, omega,
                   FLAT_VERSION if arm == 1 else RM_VERSION, _sha(text), len(text), "", _sha(""), None, (), False, False,
                   None, None, None, attempts, err, started, _now())
    parsed = parse_output(out.text)
    return Row(stage, pz.puzzle_id(), inst.trial.trial_id(), arm, inst.n, inst.depth, inst.target_state, target, omega,
               FLAT_VERSION if arm == 1 else RM_VERSION, _sha(text), len(text), out.text, _sha(out.text),
               parsed.status, parsed.answer, parsed.ok, score(parsed, status, omega),
               getattr(out, "stop_reason", None), getattr(out, "input_tokens", None), getattr(out, "output_tokens", None),
               attempts, None, started, _now())


def _arm_order(trial_id: str) -> tuple[int, int]:
    """A->B when the low byte of SHA-256(trial_id) is even, else B->A."""
    return (1, 2) if hashlib.sha256(trial_id.encode("utf-8")).digest()[-1] % 2 == 0 else (2, 1)


def _append_row(path: Path, row: Row) -> None:
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(asdict(row), sort_keys=True) + "\n")


def _rows(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(ln) for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]


def _admitted(instances: list[Instance], log: list[dict]) -> list[Instance]:
    keep = []
    for inst in instances:
        res = admit_instance(inst.trial.puzzle)
        if res.ok:
            keep.append(inst)
        else:
            log.append({"puzzle_id": inst.trial.puzzle.puzzle_id(), "failed": list(res.failed)})
    return keep


# ---- calibration ------------------------------------------------------------

def calibration_instances(seed: int) -> list[Instance]:
    out: list[Instance] = []
    for n in CAL_N_RANGE:
        for d in CAL_D_RANGE:
            for st in STATES:
                if populated(n, d, st):
                    out.extend(generate_stratum(n, d, st, CAL_PER_STATE, seed + 1000 * n + 100 * d + (0 if st == "unique" else 50)))
    return out


def select_n_main(surface: dict[int, tuple[int, int]]) -> tuple[list[int] | None, dict]:
    """Deterministic rule (PREREG §8.1): among consecutive triples with pooled
    Arm-1 accuracy in CAL_WINDOW, the one nearest CAL_CENTRE; ties -> smaller n."""
    cands = []
    for n0 in CAL_N_RANGE:
        triple = [n0, n0 + 1, n0 + 2]
        if not all(n in surface for n in triple):
            continue
        # every main stratum (n, d in MAIN_D, state) must be populated (v0.3.2 §4.2: n >= 6)
        if not all(populated(n, d, st) for n in triple for d in MAIN_D for st in STATES):
            continue
        c = sum(surface[n][0] for n in triple)
        t = sum(surface[n][1] for n in triple)
        acc = c / t if t else 0.0
        if CAL_WINDOW[0] <= acc <= CAL_WINDOW[1]:
            cands.append((abs(acc - CAL_CENTRE), n0, triple, acc))
    if not cands:
        return None, {"eligible": [], "note": "no consecutive triple with all 24 strata populated has pooled Arm-1 accuracy in the window"}
    cands.sort()
    return cands[0][2], {"eligible": [{"triple": c[2], "pooled_acc": c[3]} for c in cands]}


def cmd_calibration(out: Path, factory: ProviderFactory) -> dict:
    prof = _load_profile(out)
    prov = factory(prof["provider"])
    _check_provider_matches(prof, prov)
    path = out / "calibration.jsonl"
    done = {(r["trial_id"]) for r in _rows(path)}
    excluded: list[dict] = []
    insts = _admitted(calibration_instances(prof["campaign_seed"]), excluded)
    rng = random.Random(f"cal|{prof['campaign_seed']}")
    rng.shuffle(insts)
    for inst in insts:
        if inst.trial.trial_id() in done:
            continue
        _append_row(path, run_trial_arm(inst, 1, prov, "calibration"))
    rows = _rows(path)
    surface: dict[int, tuple[int, int]] = {}
    cells: dict[str, dict] = {}
    for r in rows:
        c, t = surface.get(r["n"], (0, 0))
        surface[r["n"]] = (c + int(r["correct"]), t + 1)
        key = f"n={r['n']},d={r['depth']},{r['target_state']}"
        cc = cells.setdefault(key, {"correct": 0, "total": 0, "requested": CAL_PER_STATE})
        cc["correct"] += int(r["correct"])
        cc["total"] += 1  # may fall short of `requested` when the stratum has fewer distinct puzzles (recorded, not hidden)
    n_main, detail = select_n_main(surface)
    report = {
        "stage": "calibration", "evidential": False, "integration_effect": INTEGRATION_EFFECT,
        "arm": 1, "rows": len(rows), "excluded_at_admission": excluded,
        "surface_by_n": {str(n): {"correct": c, "total": t, "acc": c / t} for n, (c, t) in sorted(surface.items())},
        "cells": cells, "selection": detail,
        "N_main": n_main, "STOP": n_main is None,
        "stage_sha256": _sha_file(path), "completed_at": _now(),
    }
    _write_json(out / "calibration_report.json", report)
    _manifest_update(out, "calibration", path)
    return report


# ---- manifest ---------------------------------------------------------------

def _manifest_update(out: Path, stage: str, path: Path, extra: dict | None = None) -> dict:
    mpath = out / "campaign_manifest.json"
    m = _read_json(mpath) if mpath.exists() else {
        "prereg": f"{PREREG_ID} {PREREG_VERSION}", "integration_effect": INTEGRATION_EFFECT,
        "frame_sha256": FRAME_SHA256, "stages": {},
    }
    m["stages"][stage] = {"file": path.name, "sha256": _sha_file(path), "rows": len(_rows(path)), "completed_at": _now()}
    if extra:
        m.update(extra)
    m["manifest_sha256_excluding_self"] = _sha(json.dumps({k: v for k, v in m.items() if k != "manifest_sha256_excluding_self"}, sort_keys=True))
    _write_json(mpath, m)
    return m


# ---- pilot ------------------------------------------------------------------

def stratum_instances(n_main: list[int], per_stratum: int, seed: int, tag: str, exclude_pids: set[str]) -> list[Instance]:
    out: list[Instance] = []
    for n in n_main:
        for d in MAIN_D:
            for st in STATES:
                got: list[Instance] = []
                s = seed + int(_sha(f"{tag}|{n}|{d}|{st}")[:6], 16)
                while len(got) < per_stratum:
                    batch = generate_stratum(n, d, st, per_stratum + 20, s)
                    s += 10_000
                    for inst in batch:
                        pid = inst.trial.puzzle.puzzle_id()
                        if pid in exclude_pids or any(pid == g.trial.puzzle.puzzle_id() for g in got):
                            continue
                        got.append(inst)
                        if len(got) == per_stratum:
                            break
                    if not batch:
                        raise RuntimeError(f"generator exhausted for stratum {(n, d, st)}")
                out.extend(got)
    return out


def _run_pairs(insts: list[Instance], prov: ProviderLike, stage: str, path: Path, seed: int) -> None:
    done = {(r["trial_id"], r["arm"]) for r in _rows(path)}
    order = list(insts)
    random.Random(f"{stage}|{seed}").shuffle(order)
    for inst in order:
        tid = inst.trial.trial_id()
        for arm in _arm_order(tid):
            if (tid, arm) in done:
                continue
            _append_row(path, run_trial_arm(inst, arm, prov, stage))


def paired_from_rows(rows: list[dict]) -> tuple[Paired, dict]:
    by: dict[str, dict[int, dict]] = {}
    for r in rows:
        by.setdefault(r["trial_id"], {})[r["arm"]] = r
    b = c = n = missing = 0
    fcr = {1: [0, 0], 2: [0, 0]}
    for tid, arms in by.items():
        if 1 not in arms or 2 not in arms or arms[1]["error"] or arms[2]["error"]:
            missing += 1
            continue
        n += 1
        a1, a2 = arms[1]["correct"], arms[2]["correct"]
        b += int(a2 and not a1)
        c += int(a1 and not a2)
        if len(arms[1]["omega"]) == 2:
            for arm in (1, 2):
                fcr[arm][1] += 1
                fcr[arm][0] += int(arms[arm]["parse_ok"] and len(arms[arm]["parsed_answer"]) == 1)
    return Paired(max(n, 1), b, c), {"pairs": n, "missing_pairs": missing,
                                    "fcr_arm1": (fcr[1][0] / fcr[1][1]) if fcr[1][1] else None,
                                    "fcr_arm2": (fcr[2][0] / fcr[2][1]) if fcr[2][1] else None}


def cmd_pilot(out: Path, factory: ProviderFactory) -> dict:
    prof = _load_profile(out)
    cal = _read_json(out / "calibration_report.json")
    if cal["STOP"] or not cal["N_main"]:
        raise SystemExit("calibration STOP: no eligible N_main; pilot not authorized")
    prov = factory(prof["provider"])
    _check_provider_matches(prof, prov)
    path = out / "pilot.jsonl"
    excluded: list[dict] = []
    insts = _admitted(stratum_instances(cal["N_main"], PILOT_PER_STRATUM, prof["campaign_seed"], "pilot", set()), excluded)
    _run_pairs(insts, prov, "pilot", path, prof["campaign_seed"])
    rows = _rows(path)
    paired, extra = paired_from_rows(rows)
    # --- blinding sequence: (1) b+c, (2) N_req + looks + z_k, (3) manifest hash, (4) unlock direction
    q = (paired.b + paired.c) / paired.n
    n_req = required_pairs(q)
    if n_req > N_MAX:
        _manifest_update(out, "pilot", path, {"q_blinded": q, "N_req": n_req, "STOP": "N_req exceeds N_max", "direction_unlocked": False})
        _write_json(out / "pilot_report.json", {"stage": "pilot", "evidential": False, "q": q, "N_req": n_req, "STOP": True, "direction_unlocked": False})
        return {"STOP": True, "q": q, "N_req": n_req}
    sched = schedule_for(n_req)
    manifest = _manifest_update(out, "pilot", path, {
        "q_blinded": q, "N_req": n_req, "N_main": cal["N_main"], "blocks": list(blocks(n_req)),
        "looks": list(sched.looks), "spending_times": list(sched.t), "z_k": list(sched.z),
        "pilot_puzzle_ids": sorted({r["puzzle_id"] for r in rows}), "direction_unlocked": False,
    })
    frozen_hash = manifest["manifest_sha256_excluding_self"]
    # (4) direction is displayed only now, and only in the pilot report (non-evidential)
    report = {
        "stage": "pilot", "evidential": False, "integration_effect": INTEGRATION_EFFECT,
        "rows": len(rows), "excluded_at_admission": excluded, "q": q, "N_req": n_req,
        "looks": list(sched.looks), "z_k": list(sched.z), "manifest_hash_before_unlock": frozen_hash,
        "direction_unlocked": True, "delta_hat_pilot": paired.delta_hat, "b": paired.b, "c": paired.c, **extra,
        "completed_at": _now(),
    }
    _write_json(out / "pilot_report.json", report)
    m = _read_json(out / "campaign_manifest.json")
    m["direction_unlocked"] = True
    m["manifest_hash_at_freeze"] = frozen_hash
    _write_json(out / "campaign_manifest.json", m)
    return report


# ---- main campaign ----------------------------------------------------------

def cmd_main(out: Path, factory: ProviderFactory, stage_index: int) -> dict:
    prof = _load_profile(out)
    m = _read_json(out / "campaign_manifest.json")
    if "N_req" not in m or m.get("STOP"):
        raise SystemExit("no frozen N_req in manifest; run pilot first")
    if m.get("closure"):
        raise SystemExit(f"campaign already closed: {m['closure']}")
    blks = m["blocks"]
    if not 1 <= stage_index <= len(blks):
        raise SystemExit(f"stage index must be in 1..{len(blks)}")
    prev = f"main-stage-{stage_index - 1:02d}"
    if stage_index > 1 and prev not in m["stages"]:
        raise SystemExit(f"{prev} not completed/hashed; stages run in order")
    prov = factory(prof["provider"])
    _check_provider_matches(prof, prov)
    stage = f"main-stage-{stage_index:02d}"
    path = out / f"{stage}.jsonl"
    per = blks[stage_index - 1] // 24
    exclude = set(m["pilot_puzzle_ids"])
    for k in range(1, stage_index):
        exclude |= {r["puzzle_id"] for r in _rows(out / f"main-stage-{k:02d}.jsonl")}
    excluded: list[dict] = []
    insts = _admitted(stratum_instances(m["N_main"], per, prof["campaign_seed"], stage, exclude), excluded)
    _run_pairs(insts, prov, stage, path, prof["campaign_seed"] + stage_index)
    _manifest_update(out, stage, path)
    # cumulative paired statistic
    all_rows: list[dict] = []
    for k in range(1, stage_index + 1):
        all_rows += _rows(out / f"main-stage-{k:02d}.jsonl")
    paired, extra = paired_from_rows(all_rows)
    cum = sum(blks[:stage_index])
    report = {"stage": stage, "cumulative_trials": cum, "pairs": extra["pairs"], "missing_pairs": extra["missing_pairs"],
              "b_plus_c": paired.b + paired.c, "excluded_at_admission": excluded, "look": False,
              "integration_effect": INTEGRATION_EFFECT, "completed_at": _now()}
    if cum in m["looks"]:
        k = m["looks"].index(cum)
        z = m["z_k"][k]
        verdict = adjudicate(paired, z, SESOI)
        lo, hi = paired.wald_ci(z)
        report.update({"look": True, "look_index": k + 1, "z": z, "delta_hat": paired.delta_hat, "ci": [lo, hi],
                       "verdict": verdict, "mcnemar_p": paired.mcnemar_p(), **extra})
        if verdict != "INCONCLUSIVE" or cum == m["N_req"]:
            mm = _read_json(out / "campaign_manifest.json")
            mm["closure"] = {"verdict": verdict, "at_trials": cum, "look_index": k + 1, "closed_at": _now()}
            _write_json(out / "campaign_manifest.json", mm)
    _write_json(out / f"{stage}_report.json", report)
    return report


# ---- CLI --------------------------------------------------------------------

def main(argv: list[str] | None = None, factory: ProviderFactory = default_provider_factory) -> int:
    ap = argparse.ArgumentParser(prog="relational_state.runner")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("profile"); p.add_argument("--out", required=True); p.add_argument("--provider", choices=("openai", "claude"), required=True); p.add_argument("--seed", type=int, required=True)
    c = sub.add_parser("calibration"); c.add_argument("--out", required=True)
    q = sub.add_parser("pilot"); q.add_argument("--out", required=True)
    mn = sub.add_parser("main"); mn.add_argument("--out", required=True); mn.add_argument("--stage", type=int, required=True)
    a = ap.parse_args(argv)
    out = Path(a.out)
    if a.cmd == "profile":
        print(cmd_profile(out, a.provider, a.seed))
    elif a.cmd == "calibration":
        r = cmd_calibration(out, factory); print(json.dumps({k: r[k] for k in ("rows", "N_main", "STOP", "surface_by_n")}, indent=1))
    elif a.cmd == "pilot":
        r = cmd_pilot(out, factory); print(json.dumps({k: r.get(k) for k in ("q", "N_req", "STOP", "looks")}, indent=1))
    elif a.cmd == "main":
        r = cmd_main(out, factory, a.stage); print(json.dumps({k: r.get(k) for k in ("stage", "cumulative_trials", "look", "verdict")}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
