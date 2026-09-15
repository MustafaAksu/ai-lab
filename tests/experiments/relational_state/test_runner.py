"""S4 runner tests with an injected fake provider (no SDK, no network)."""

import hashlib
import json
import random
from dataclasses import dataclass
from pathlib import Path

import pytest

from ai_lab.experiments.relational_state import INTEGRATION_EFFECT, runner
from ai_lab.experiments.relational_state.render import FRAME_SHA256


@dataclass
class FakeOutcome:
    text: str
    stop_reason: str = "completed"
    stop_reason_field: str = "status"
    input_tokens: int = 100
    output_tokens: int = 10


class FakeProvider:
    """Answers from the oracle with arm-dependent accuracy; records every prompt."""

    def __init__(self, acc_arm1=0.5, acc_arm2=0.9, model="gpt-5.6-luna", fail_on=None, reasoning_effort="low"):
        self.name, self.model = "Fake", model
        self._reasoning_effort = reasoning_effort
        self.acc = {1: acc_arm1, 2: acc_arm2}
        self.prompts: list[str] = []
        self.rng = random.Random(0)
        self.fail_on = fail_on or set()

    def ask_with_outcome(self, prompt: str):
        self.prompts.append(prompt)
        if len(self.prompts) in self.fail_on:
            raise RuntimeError("simulated provider error")
        arm = 2 if "\nINDEX\n" in prompt else 1
        target = prompt.rsplit("belongs to ", 1)[1].rstrip("?")
        # recover the truth from the clue table via the oracle-free trick: the
        # runner records omega; here we simply parse persons/items and solve.
        from ai_lab.experiments.relational_state.model import Clue, Puzzle
        from ai_lab.experiments.relational_state.oracle import oracle_status

        lines = prompt.splitlines()
        persons = tuple(h.strip() for h in lines[1][len("Persons: "):-1].split(","))
        items = tuple(h.strip() for h in lines[2][len("Items: "):-1].split(","))
        clues = tuple(Clue.parse(ln) for ln in lines if ln[:1] == "C" and " " in ln and ln.split()[1] in ("EQUAL", "NOT_EQUAL"))
        status, omega = oracle_status(Puzzle(persons, items, clues), target)
        if self.rng.random() < self.acc[arm]:
            return FakeOutcome(json.dumps({"status": status, "answer": list(omega)}))
        return FakeOutcome(json.dumps({"status": "unique", "answer": [items[0] if omega and items[0] != omega[0] else items[1]]}))


def _factory(prov):
    return lambda prof: prov


def _reload_settings(monkeypatch, model="gpt-5.6-luna", effort="low"):
    monkeypatch.setenv("AI_LAB_OPENAI_MODEL", model)
    if effort is None:
        monkeypatch.delenv("AI_LAB_OPENAI_REASONING_EFFORT", raising=False)
    else:
        monkeypatch.setenv("AI_LAB_OPENAI_REASONING_EFFORT", effort)
    import importlib

    from ai_lab.providers import settings

    importlib.reload(settings)


def _profile(tmp_path, monkeypatch):
    _reload_settings(monkeypatch)
    return runner.cmd_profile(tmp_path, "openai", seed=11)


def test_artifacts_identify_the_frozen_prereg_version(tmp_path, monkeypatch):
    from ai_lab.experiments.relational_state import PREREG_VERSION

    assert PREREG_VERSION == "v0.4"
    _profile(tmp_path, monkeypatch)
    prof = json.loads((tmp_path / "campaign_execution_profile.json").read_text())
    assert prof["prereg"] == "PREREG-RS-0001 v0.4"
    runner.cmd_calibration(tmp_path, _factory(FakeProvider()))
    man = json.loads((tmp_path / "campaign_manifest.json").read_text())
    assert man["prereg"] == "PREREG-RS-0001 v0.4"


def test_profile_is_frozen_once_and_carries_membrane_fields(tmp_path, monkeypatch):
    path = _profile(tmp_path, monkeypatch)
    prof = json.loads(path.read_text())
    assert prof["integration_effect"] == INTEGRATION_EFFECT == "none"
    assert prof["frame_sha256"] == FRAME_SHA256
    assert prof["model"] == "gpt-5.6-luna" and prof["reasoning_effort"] == "low"   # v0.4 amended subject
    assert prof["temperature"] == "provider_default" and prof["role"] == "primary"
    with pytest.raises(SystemExit):
        runner.cmd_profile(tmp_path, "openai", seed=11)


@pytest.mark.parametrize("provider,model,effort", [
    ("claude", "gpt-5.6-luna", "low"),          # wrong provider for the primary role
    ("openai", "gpt-5.6-terra", "low"),         # superseded v0.3.3 model
    ("openai", "gpt-5.6-luna", "medium"),       # superseded v0.3.3 effort
    ("openai", "gpt-5.6-luna", None),           # missing reasoning effort
])
def test_primary_profile_refuses_non_frozen_subject(tmp_path, monkeypatch, provider, model, effort):
    _reload_settings(monkeypatch, model=model, effort=effort)
    prov = FakeProvider()
    with pytest.raises(SystemExit):
        runner.cmd_profile(tmp_path, provider, seed=1)
    assert not (tmp_path / "campaign_execution_profile.json").exists()
    assert prov.prompts == []


def test_provider_is_built_from_frozen_profile_not_environment(tmp_path, monkeypatch):
    _profile(tmp_path, monkeypatch)
    # environment drifts to `high` after freezing; the factory must still receive `low`
    _reload_settings(monkeypatch, effort="high")
    seen = {}

    def factory(prof):
        seen.update(prof)
        return FakeProvider(reasoning_effort=prof["reasoning_effort"])

    runner.cmd_calibration(tmp_path, factory)
    assert seen["reasoning_effort"] == "low" and seen["model"] == "gpt-5.6-luna"


def test_effort_mismatch_on_built_provider_aborts_before_any_call(tmp_path, monkeypatch):
    _profile(tmp_path, monkeypatch)
    prov = FakeProvider(reasoning_effort="high")
    with pytest.raises(SystemExit):
        runner.cmd_calibration(tmp_path, _factory(prov))
    assert prov.prompts == []


def test_stage_requires_profile_and_matching_model(tmp_path, monkeypatch):
    with pytest.raises(SystemExit):
        runner.cmd_calibration(tmp_path, _factory(FakeProvider()))
    _profile(tmp_path, monkeypatch)
    with pytest.raises(SystemExit):
        runner.cmd_calibration(tmp_path, _factory(FakeProvider(model="other-model")))


def test_frame_drift_aborts_before_any_call(tmp_path, monkeypatch):
    _profile(tmp_path, monkeypatch)
    monkeypatch.setattr(runner, "FRAME_SHA256", "0" * 64)
    prov = FakeProvider()
    with pytest.raises(SystemExit):
        runner.cmd_calibration(tmp_path, _factory(prov))
    assert prov.prompts == []


def test_arm_order_is_sha_parity_and_balanced():
    tids = [hashlib.sha256(str(i).encode()).hexdigest() for i in range(400)]
    orders = [runner._arm_order(t) for t in tids]
    assert all(o in ((1, 2), (2, 1)) for o in orders)
    frac = sum(o == (1, 2) for o in orders) / len(orders)
    assert 0.4 < frac < 0.6
    assert runner._arm_order("x") == runner._arm_order("x")


def test_full_pipeline_with_fake_provider(tmp_path, monkeypatch):
    _profile(tmp_path, monkeypatch)
    prov = FakeProvider(acc_arm1=0.80, acc_arm2=0.90)   # discordance ~0.26 -> N_req within budget
    # --- calibration: Arm 1 only, 10 unique + 10 ambiguous per populated (n, d)
    cal = runner.cmd_calibration(tmp_path, _factory(prov))
    rows = runner._rows(tmp_path / "calibration.jsonl")
    assert all(r["arm"] == 1 and r["stage"] == "calibration" for r in rows)
    assert all(r["integration_effect"] == "none" for r in rows)
    prof = json.loads((tmp_path / "campaign_execution_profile.json").read_text())
    assert all(r["execution_profile_ref"] == "campaign_execution_profile.json" and len(r["execution_profile_sha256"]) == 64
               and r["source_git_commit"] == prof["git_commit"] and "source_git_dirty" in r for r in rows)
    for key, cell in cal["cells"].items():
        assert 1 <= cell["total"] <= cell["requested"] == 10, key
    assert cal["cells"]["n=3,d=1,ambiguous"]["total"] == 9   # tiny stratum: only 9 distinct puzzles exist; recorded
    assert cal["N_main"] is not None and len(cal["N_main"]) == 3
    assert min(cal["N_main"]) >= 6   # only triples with all 24 strata populated are eligible
    man = json.loads((tmp_path / "campaign_manifest.json").read_text())
    assert man["stages"]["calibration"]["sha256"] == hashlib.sha256((tmp_path / "calibration.jsonl").read_bytes()).hexdigest()
    # --- pilot: both arms, back-to-back per trial, blinding sequence
    n_calls_before = len(prov.prompts)
    # tampering with a hashed stage file is detected before the next stage runs
    calfile = tmp_path / "calibration.jsonl"
    original = calfile.read_bytes()
    calfile.write_bytes(original + b"\n")
    with pytest.raises(SystemExit):
        runner.cmd_pilot(tmp_path, _factory(prov))
    calfile.write_bytes(original)
    assert len(prov.prompts) == n_calls_before
    pil = runner.cmd_pilot(tmp_path, _factory(prov))
    prows = runner._rows(tmp_path / "pilot.jsonl")
    assert len(prows) == 3 * 4 * 2 * 10 * 2
    for i in range(0, len(prows), 2):
        assert prows[i]["trial_id"] == prows[i + 1]["trial_id"] and {prows[i]["arm"], prows[i + 1]["arm"]} == {1, 2}
        assert (prows[i]["arm"], prows[i + 1]["arm"]) == runner._arm_order(prows[i]["trial_id"])
    assert pil["N_req"] >= 1200 and pil["N_req"] % 24 == 0
    man = json.loads((tmp_path / "campaign_manifest.json").read_text())
    assert man["direction_unlocked"] is True and man["manifest_hash_at_freeze"] == pil["manifest_hash_before_unlock"]
    assert "delta_hat_pilot" not in man and "q_blinded" in man     # direction never enters the manifest
    assert man["looks"][-1] == man["N_req"] and len(man["z_k"]) == len(man["looks"])
    # --- main: stages in order; look adjudication only at preregistered looks
    with pytest.raises(SystemExit):
        runner.cmd_main(tmp_path, _factory(prov), 2)
    r1 = runner.cmd_main(tmp_path, _factory(prov), 1)
    assert r1["look"] is False and "verdict" not in r1
    reports = {1: r1}
    for k in range(2, 7):
        reports[k] = runner.cmd_main(tmp_path, _factory(prov), k)
        man = json.loads((tmp_path / "campaign_manifest.json").read_text())
        if man.get("closure"):
            break
    looks = [k for k, r in reports.items() if r["look"]]
    assert looks and all(reports[k]["cumulative_trials"] in man["looks"] for k in looks)
    assert reports[3]["look"] is True and reports[3]["cumulative_trials"] == 720
    assert man["closure"]["verdict"] == "POSITIVE" and man["closure"]["at_trials"] in man["looks"]
    closed_at_stage = max(reports)
    assert all(f"main-stage-{k:02d}" in man["stages"] for k in range(1, closed_at_stage + 1))
    with pytest.raises(SystemExit):
        runner.cmd_main(tmp_path, _factory(prov), closed_at_stage + 1)
    with pytest.raises(SystemExit):
        runner.cmd_close_inconclusive(tmp_path, "already closed")
    # no puzzle leaks from pilot into main, and no duplicate puzzles across main stages
    pids_pilot = {r["puzzle_id"] for r in prows}
    pids_main = [r["puzzle_id"] for k in range(1, closed_at_stage + 1) for r in runner._rows(tmp_path / f"main-stage-{k:02d}.jsonl")]
    assert not (pids_pilot & set(pids_main))
    assert len(set(pids_main)) == len(pids_main) // 2
    # every prompt the provider saw was admitted, and frame-headed
    assert all(p.startswith("You are given a logic puzzle.") for p in prov.prompts)
    assert len(prov.prompts) - n_calls_before == len(prows) + len(pids_main)


def test_provider_error_is_retried_once_then_recorded_as_missing(tmp_path, monkeypatch):
    _profile(tmp_path, monkeypatch)
    from ai_lab.experiments.relational_state.generator import generate

    inst = generate(4, 1, "unique", 1)
    prov = FakeProvider(fail_on={1, 2})
    prof = runner._load_profile(tmp_path)
    row = runner.run_trial_arm(inst, 1, prov, "t", prof)
    assert row.error and row.attempts == 2 and not row.correct and row.response == ""
    prov2 = FakeProvider(fail_on={1})
    row2 = runner.run_trial_arm(inst, 1, prov2, "t", prof)
    assert row2.error is None and row2.attempts == 2


def test_calibration_provider_failures_are_missing_not_wrong(tmp_path, monkeypatch):
    _profile(tmp_path, monkeypatch)
    # first call fails twice (retry exhausted) -> missing; must not enter any denominator
    prov = FakeProvider(acc_arm1=1.0, fail_on={1, 2})
    cal = runner.cmd_calibration(tmp_path, _factory(prov))
    rows = runner._rows(tmp_path / "calibration.jsonl")
    assert sum(1 for r in rows if r["error"]) == 1 and cal["missing_after_retry"] == 1
    assert sum(c["total"] for c in cal["cells"].values()) == len(rows) - 1
    # realized counts the puzzle that was generated and called even though its
    # observation is missing; total (the accuracy denominator) does not
    assert sum(c["realized"] for c in cal["cells"].values()) == len(rows)
    assert all(v["acc"] == 1.0 for v in cal["surface_by_n"].values())


def test_voluntary_close_records_inconclusive_at_last_completed_look(tmp_path, monkeypatch):
    _profile(tmp_path, monkeypatch)
    prov = FakeProvider(acc_arm1=0.80, acc_arm2=0.90)
    runner.cmd_calibration(tmp_path, _factory(prov))
    runner.cmd_pilot(tmp_path, _factory(prov))
    runner.cmd_main(tmp_path, _factory(prov), 1)
    closure = runner.cmd_close_inconclusive(tmp_path, "budget")
    assert closure["verdict"] == "INCONCLUSIVE" and closure["voluntary"] and closure["completed_trials"] == 240
    assert closure["at_last_completed_look"] is None      # no look completed yet
    with pytest.raises(SystemExit):
        runner.cmd_main(tmp_path, _factory(prov), 2)


def test_pilot_stops_when_required_n_exceeds_budget(tmp_path, monkeypatch):
    _profile(tmp_path, monkeypatch)
    prov = FakeProvider(acc_arm1=0.55, acc_arm2=0.85)   # discordance ~0.47 -> N_req > N_max
    runner.cmd_calibration(tmp_path, _factory(prov))
    res = runner.cmd_pilot(tmp_path, _factory(prov))
    assert res["STOP"] and res["N_req"] > runner.N_MAX
    man = json.loads((tmp_path / "campaign_manifest.json").read_text())
    assert man["STOP"] and man["direction_unlocked"] is False and "delta_hat_pilot" not in man
    with pytest.raises(SystemExit):
        runner.cmd_main(tmp_path, _factory(prov), 1)
