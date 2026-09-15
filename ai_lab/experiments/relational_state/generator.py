"""Puzzle family generator (PREREG §4).

Family: n persons x n items, clue atoms EQUAL / NOT_EQUAL only, declared
one-to-one rule. Instances are CONSTRUCTED for their stratum and then
VERIFIED by the oracle and by PROP-RS-0 (F3: both target states and every
depth are populated by a named mechanism, not by rejection on failures).

Construction. A hidden assignment sigma and a random chain of persons
p_0, ..., p_d. p_0 receives an EQUAL clue (fixed at round 0). Each p_k
(k >= 1) receives NOT_EQUAL clues for every item except sigma[p_{k-1}] and
sigma[p_k], so p_k becomes a singleton exactly when p_{k-1} does, one round
later (R1). Random consistent noise clues are then added.

* unique    -- p_d is the target; accepted iff the oracle finds exactly one
               solution and PROP-RS-0 labels the target singleton at round d.
* ambiguous -- p_d is a non-target person; the target T and a partner Q stay
               unconstrained relative to each other, sigma' = sigma with T and
               Q swapped, and every clue is consistent with both sigma and
               sigma'. Accepted iff the oracle finds exactly {sigma, sigma'}
               and PROP-RS-0 reaches its fixed point at round d with the
               target row non-singleton.

Occupancy bound (PROP-RS-0 = R1-only, PREREG v0.3.2): a unique-target chain
of depth d needs d + 1 persons (n >= d + 1); an ambiguous instance needs the
chain p_0..p_{d-1} plus the pair T, Q (n >= d + 2). See `populated`.

Handles are positional and never deduplicated by descriptor (A5).
"""

from __future__ import annotations

import random
from dataclasses import dataclass

from .depth import depth
from .model import ITEM_VOCAB, N_MAX_VOCAB, PERSON_VOCAB, Clue, Puzzle, Trial
from .oracle import solutions

TARGET_STATES = ("unique", "ambiguous")


@dataclass(frozen=True)
class Instance:
    trial: Trial
    n: int
    depth: int
    depth_kind: str
    target_state: str
    omega: tuple[str, ...]
    seed: int


def populated(n: int, d: int, target_state: str) -> bool:
    """Occupancy bound under PROP-RS-0 = R1-only (v0.3.2)."""
    if d < 1:
        return False
    return n >= d + 1 if target_state == "unique" else n >= d + 2


def _consistent(clue: tuple[str, str, str], sigmas: list[dict[str, str]]) -> bool:
    rel, p, it = clue
    if rel == "EQUAL":
        return all(s[p] == it for s in sigmas)
    return all(s[p] != it for s in sigmas)


def _build(
    rng: random.Random,
    n: int,
    d: int,
    target_state: str,
) -> tuple[Puzzle, str, list[dict[str, str]]]:
    persons = tuple(PERSON_VOCAB[:n])
    items = tuple(ITEM_VOCAB[:n])
    perm = list(items)
    rng.shuffle(perm)
    sigma = dict(zip(persons, perm))
    order = list(persons)
    rng.shuffle(order)
    raw: list[tuple[str, str, str]] = []

    def keep_only(p: str, keep: set[str]) -> None:
        for it in items:
            if it not in keep:
                raw.append(("NOT_EQUAL", p, it))

    if target_state == "unique":
        chain = order[: d + 1]
        free = order[d + 1 :]
        target = chain[-1]
        sigmas = [sigma]
        raw.append(("EQUAL", chain[0], sigma[chain[0]]))
        for k in range(1, len(chain)):
            keep_only(chain[k], {sigma[chain[k - 1]], sigma[chain[k]]})
        protected: set[str] = set()
    else:
        target, partner = order[0], order[1]
        chain = order[2 : d + 2]
        free = order[d + 2 :]
        sigma2 = dict(sigma)
        sigma2[target], sigma2[partner] = sigma[partner], sigma[target]
        sigmas = [sigma, sigma2]
        raw.append(("EQUAL", chain[0], sigma[chain[0]]))
        for k in range(1, len(chain)):
            keep_only(chain[k], {sigma[chain[k - 1]], sigma[chain[k]]})
        last = sigma[chain[-1]]
        for p in (target, partner):  # T and Q keep {sigma_T, sigma_Q, last}
            keep_only(p, {sigma[target], sigma[partner], last})
        protected = {target, partner}
    for p in free:  # noise on free persons: consistent, random
        if rng.random() < 0.5:
            raw.append(("EQUAL", p, sigma[p]))
        else:
            for it in items:
                if it != sigma[p] and rng.random() < 0.4:
                    raw.append(("NOT_EQUAL", p, it))
    raw = list(dict.fromkeys(raw))
    rng.shuffle(raw)
    clues = tuple(Clue(f"C{i + 1}", rel, p, it) for i, (rel, p, it) in enumerate(raw))
    return Puzzle(persons, items, clues), target, sigmas


def generate(n: int, d: int, target_state: str, seed: int, max_attempts: int = 200) -> Instance | None:
    """One verified instance of stratum (n, d, target_state), or None."""
    if not 2 <= n <= N_MAX_VOCAB:
        raise ValueError(f"n must be in [2, {N_MAX_VOCAB}]")
    if target_state not in TARGET_STATES:
        raise ValueError(target_state)
    if not populated(n, d, target_state):
        return None
    rng = random.Random(f"RS-0001|{n}|{d}|{target_state}|{seed}")
    for _ in range(max_attempts):
        puzzle, target, sigmas = _build(rng, n, d, target_state)
        puzzle.validate()
        sols = solutions(puzzle, limit=2)
        if len(sols) != len(sigmas):
            continue
        if sorted(map(sorted, (s.items() for s in sols))) != sorted(map(sorted, (s.items() for s in sigmas))):
            continue
        dd, kind = depth(puzzle, target)
        want_kind = "singleton" if target_state == "unique" else "fixed_point"
        if dd != d or kind != want_kind:
            continue
        omega = tuple(sorted({s[target] for s in sols}))
        if target_state == "ambiguous" and len(omega) != 2:
            continue
        return Instance(Trial(puzzle, target), n, dd, kind, target_state, omega, seed)
    return None


def generate_stratum(n: int, d: int, target_state: str, count: int, base_seed: int) -> list[Instance]:
    """`count` distinct-puzzle instances (by puzzle_id); seeds advance as needed."""
    out: list[Instance] = []
    seen: set[str] = set()
    seed, misses = base_seed, 0
    while len(out) < count and misses < 50:
        inst = generate(n, d, target_state, seed)
        seed += 1
        if inst is None:
            misses += 1
            continue
        pid = inst.trial.puzzle.puzzle_id()
        if pid in seen:
            continue
        seen.add(pid)
        out.append(inst)
    return out
