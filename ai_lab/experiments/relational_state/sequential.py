"""Lan-DeMets O'Brien-Fleming-type alpha spending and group-sequential
critical values (PREREG §7, staged execution).

alpha(t) = 2 [1 - Phi(z_{1-alpha/2} / sqrt(t))], two-sided alpha = 0.05.
Spending times t_k = n_k / N_req are prospective (trial fraction as the
planned information proxy). Critical values are computed by the standard
recursion over the joint distribution of the partial-sum statistic on a
numerical grid (Armitage-McPherson-Rowe), standard library only.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

ALPHA = 0.05
Z_HALF = 1.959963984540054  # z_{0.975}


def phi(x: float) -> float:
    return math.exp(-0.5 * x * x) / math.sqrt(2 * math.pi)


def Phi(x: float) -> float:
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def Phi_inv(p: float) -> float:
    lo, hi = -40.0, 40.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if Phi(mid) < p:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def spending(t: float, alpha: float = ALPHA) -> float:
    if t <= 0:
        return 0.0
    if t >= 1:
        return alpha
    return 2 * (1 - Phi(Phi_inv(1 - alpha / 2) / math.sqrt(t)))


@dataclass(frozen=True)
class Schedule:
    looks: tuple[int, ...]      # cumulative trials at each look
    n_req: int
    z: tuple[float, ...]        # critical values per look

    @property
    def t(self) -> tuple[float, ...]:
        return tuple(n / self.n_req for n in self.looks)


def look_schedule(n_req: int, block: int = 240, look_blocks: tuple[int, ...] = (3, 6, 9)) -> tuple[int, ...]:
    """Looks after blocks 3, 6, 9 that fall strictly below n_req, plus n_req."""
    looks = [b * block for b in look_blocks if b * block < n_req]
    return tuple(looks + [n_req])


def blocks(n_req: int, block: int = 240) -> tuple[int, ...]:
    """Balanced blocks of `block` trials with a final balanced partial block."""
    full, rem = divmod(n_req, block)
    out = [block] * full
    if rem:
        out.append(rem)
    return tuple(out)


def critical_values(t: tuple[float, ...], alpha: float = ALPHA, grid: int = 801, span: float = 8.0) -> tuple[float, ...]:
    """Sequential critical values c_k on the Z scale for spending times t."""
    if not t or any(b <= a for a, b in zip(t, t[1:])) or t[-1] > 1 + 1e-12:
        raise ValueError("t must be strictly increasing and <= 1")
    alphas = [spending(tk, alpha) for tk in t]
    cs: list[float] = []
    # density of the partial-sum S_k = sqrt(t_k) Z_k restricted to the continuation region
    xs: list[float] = []
    f: list[float] = []
    for k, tk in enumerate(t):
        inc = alphas[k] - (alphas[k - 1] if k else 0.0)
        sd_k = math.sqrt(tk)
        if k == 0:
            xs = [-span * sd_k + i * (2 * span * sd_k) / (grid - 1) for i in range(grid)]
            f = [phi(x / sd_k) / sd_k for x in xs]
        else:
            dt = tk - t[k - 1]
            sd = math.sqrt(dt)
            new_xs = [-span * sd_k + i * (2 * span * sd_k) / (grid - 1) for i in range(grid)]
            h = xs[1] - xs[0]
            new_f = []
            for s in new_xs:
                acc = 0.0
                for i, u in enumerate(xs):
                    w = 0.5 if i in (0, len(xs) - 1) else 1.0
                    acc += w * f[i] * phi((s - u) / sd) / sd
                new_f.append(acc * h)
            xs, f = new_xs, new_f
        # find c_k with P(|S_k| > c_k sd_k, continued so far) = inc
        h = xs[1] - xs[0]

        def tail(c: float) -> float:
            lim = c * sd_k
            acc = 0.0
            for i, x in enumerate(xs):
                if abs(x) > lim:
                    w = 0.5 if i in (0, len(xs) - 1) else 1.0
                    acc += w * f[i]
            return acc * h

        lo, hi = 0.0, 10.0
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            if tail(mid) > inc:
                lo = mid
            else:
                hi = mid
        c = 0.5 * (lo + hi)
        cs.append(c)
        # restrict density to the continuation region for the next look
        lim = c * sd_k
        f = [fi if abs(x) <= lim else 0.0 for x, fi in zip(xs, f)]
    return tuple(cs)


def schedule_for(n_req: int, block: int = 240) -> Schedule:
    looks = look_schedule(n_req, block)
    t = tuple(n / n_req for n in looks)
    return Schedule(looks, n_req, critical_values(t))
