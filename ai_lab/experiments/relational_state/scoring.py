"""Output parsing, per-trial scoring and the primary/secondary statistics.

PREREG §5.5, §7. Correct = status matches the oracle AND the answer set equals
Omega_q. Unparseable output = incorrect in the primary analysis (a sensitivity
analysis excludes it). `inconsistent` on this family is a false alarm.
"""

from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass

STATUSES = ("unique", "ambiguous", "inconsistent")


@dataclass(frozen=True)
class Parsed:
    ok: bool
    status: str | None
    answer: tuple[str, ...]
    raw: str


_JSON_RE = re.compile(r"\{.*?\}", re.S)


def parse_output(text: str) -> Parsed:
    """The first JSON object in the response is scored; strict shape."""
    for m in _JSON_RE.finditer(text):
        try:
            obj = json.loads(m.group(0))
        except json.JSONDecodeError:
            continue
        if not isinstance(obj, dict):
            continue
        status, answer = obj.get("status"), obj.get("answer")
        if status in STATUSES and isinstance(answer, list) and all(isinstance(a, str) for a in answer):
            return Parsed(True, status, tuple(sorted(set(a.strip() for a in answer))), text)
        return Parsed(False, None, (), text)
    return Parsed(False, None, (), text)


def score(parsed: Parsed, oracle_status: str, omega: tuple[str, ...]) -> bool:
    if not parsed.ok:
        return False
    return parsed.status == oracle_status and parsed.answer == tuple(sorted(omega))


# --- paired statistics -------------------------------------------------------

@dataclass(frozen=True)
class Paired:
    n: int   # pairs
    b: int   # arm2 correct, arm1 wrong
    c: int   # arm1 correct, arm2 wrong

    @property
    def delta_hat(self) -> float:
        return (self.b - self.c) / self.n

    def wald_ci(self, z: float) -> tuple[float, float]:
        """Paired Wald interval, variance ((b+c) - (b-c)^2/n) / n^2, no continuity correction."""
        var = max(0.0, ((self.b + self.c) - (self.b - self.c) ** 2 / self.n)) / self.n**2
        half = z * math.sqrt(var)
        return self.delta_hat - half, self.delta_hat + half

    def mcnemar_p(self) -> float:
        """Exact two-sided McNemar (binomial on discordant pairs); descriptive only."""
        d = self.b + self.c
        if d == 0:
            return 1.0
        k = min(self.b, self.c)
        p = sum(math.comb(d, i) for i in range(0, k + 1)) / 2**d
        return min(1.0, 2 * p)


def adjudicate(paired: Paired, z: float, sesoi: float) -> str:
    lo, hi = paired.wald_ci(z)
    if lo >= sesoi:
        return "POSITIVE"
    if hi < sesoi:
        return "NEGATIVE"
    return "INCONCLUSIVE"


def required_pairs(q: float, sesoi: float = 0.03, alt: float = 0.06, n_min: int = 1200, block: int = 24) -> int:
    """N_req = ceil(q (z_.975 + z_.80)^2 / (alt - sesoi)^2), rounded up to a
    multiple of `block`, floored at n_min. Frozen; only q comes from data.

    Precision convention: the quantiles enter as the two-decimal values used
    in the preregistration's own arithmetic (1.96 + 0.84 = 2.80), so that the
    frozen illustrative values (q=0.30 -> 2613 -> 2616 = N_max) are
    reproduced exactly. With full-precision quantiles q=0.30 would give 2640,
    exceeding N_max; the convention is recorded so the reviewing executor can
    confirm it rather than discover it."""
    z = 1.96 + 0.84
    n = math.ceil(q * z * z / (alt - sesoi) ** 2)
    n = max(n_min, n)
    return -(-n // block) * block


def fcr(pairs: list[tuple[int, str, tuple[str, ...]]]) -> float | None:
    """False-certainty rate: P(|answer| == 1 | oracle ambiguous), given
    (omega_size, parsed status, parsed answer) rows for one arm."""
    amb = [(s, a) for size, s, a in pairs if size == 2]
    if not amb:
        return None
    return sum(1 for s, a in amb if len(a) == 1) / len(amb)
