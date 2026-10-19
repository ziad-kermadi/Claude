"""Figures for staging/gap_B.json (gap batch B: generating functions, coupling, optimal stopping).

Every plotted number is computed here, never typed in.
"""
import math
import numpy as np
from matplotlib.patches import Rectangle
from qcfig import *


def _f(s):
    """Offspring PGF f(s) = (1+s+s^2)/3 (offspring uniform on {0,1,2})."""
    return (1 + s + s * s) / 3


@figure("fgB_branch_fixed", w=4.4, h=3.3)
def _(ax):
    # Cobweb of f_n(0) -> 1: f touches the diagonal only at s = 1 (double root)
    s = np.linspace(0, 1, 400)
    ax.plot(s, _f(s), color=BLUE, lw=2.0, label=r"$f(s)=\frac{1+s+s^2}{3}$")
    ax.plot(s, s, color=INK, lw=1.2, ls="--", label=r"$y=s$")
    x, y = 0.0, 0.0
    xs, ys = [0.0], [0.0]
    for _ in range(7):
        y = _f(x)                     # up to the curve
        xs += [x, x]; ys += [y, y]
        x = y                         # across to the diagonal
        xs.append(x); ys.append(x)
    ax.plot(xs, ys, color=ORANGE, lw=1.3)
    ax.plot([1], [1], "o", color=GREEN, ms=7, zorder=5)
    ax.annotate("only fixed point in $[0,1]$: $q=1$\n(double root)", xy=(0.97, 0.97), xytext=(0.5, 0.22),
                fontsize=9, color=GREEN, arrowprops=dict(arrowstyle="-", color=GREEN, lw=0.9))
    ax.text(0.5, 0.06, "orange: cobweb of $f_n(0)$", color=ORANGE, fontsize=8.5)
    ax.set_xlim(0, 1.05); ax.set_ylim(0, 1.05)
    ax.set_xlabel("$s$"); ax.set_ylabel("$f(s)$")
    ax.legend(loc="upper left", fontsize=8.5, frameon=False)


@figure("fgB_dominance_flips", w=5.4, h=2.1, axis=False)
def _(ax):
    # One sequence of 12 flips: X = heads in flips 1-10, Y = heads in all 12.
    flips = ["H", "T", "T", "H", "T", "T", "T", "H", "T", "H", "H", "T"]  # example outcome
    X = sum(1 for f_ in flips[:10] if f_ == "H")
    Y = sum(1 for f_ in flips if f_ == "H")
    for i, f_ in enumerate(flips):
        fc = LIGHT_BLUE if i < 10 else LIGHT_ORANGE
        ax.add_patch(Rectangle((i, 0), 0.92, 0.9, fc=fc if f_ == "H" else "white", ec=INK, lw=1.0))
        ax.text(i + 0.46, 0.45, f_, ha="center", va="center", fontsize=10)
        ax.text(i + 0.46, -0.22, str(i + 1), ha="center", va="center", fontsize=8, color=GREY)
    ax.plot([0, 10], [1.25, 1.25], color=BLUE, lw=1.6)
    ax.text(5.0, 1.45, f"shared by $X$ and $Y$: $X={X}$", ha="center", fontsize=9.5, color=BLUE)
    ax.plot([10, 12], [1.25, 1.25], color=ORANGE, lw=1.6)
    ax.text(11.0, 1.45, f"extra for $Y$: $Y={Y}$", ha="center", fontsize=9.5, color=ORANGE)
    ax.text(6.0, -0.75, "$Y=X+$(heads in flips 11, 12), so $Y\\geq X$ on every outcome",
            ha="center", fontsize=9, color=GREY)
    frame(ax, -0.2, 12.2, -1.0, 1.9)


@figure("fgB_cftp_paths", w=4.8, h=2.9)
def _(ax):
    # Four paths driven by the same uniforms; search a short pattern that merges all four by time 0
    T = 4

    def step(x, u):
        return min(x + 1, 3) if u < 0.5 else max(x - 1, 0)

    pattern = None
    for bits in range(2 ** T):
        us = [0.2 if (bits >> i) & 1 == 0 else 0.8 for i in range(T)]
        ends = []
        for x0 in range(4):
            x = x0
            for u in us:
                x = step(x, u)
            ends.append(x)
        if len(set(ends)) == 1 and pattern is None:
            # require the merge to happen before the last step, so the picture shows a merge
            mid = []
            for x0 in range(4):
                x = x0
                for u in us[:-1]:
                    x = step(x, u)
                mid.append(x)
            if len(set(mid)) > 1:
                pattern = us
    us = pattern
    cols = [BLUE, ORANGE, GREEN, RED]
    for x0 in range(4):
        xs, ys = [0], [x0]
        x = x0
        for t, u in enumerate(us, start=1):
            x = step(x, u)
            xs.append(t); ys.append(x)
        ax.plot(np.array(xs) - T, ys, color=cols[x0], lw=1.7, marker="o", ms=4)
    for t, u in enumerate(us):
        ax.text(t - T + 0.5, 3.55, "U<0.5" if u < 0.5 else "U>0.5", ha="center", fontsize=7.5, color=GREY)
    ax.set_xlim(-T - 0.2, 0.3); ax.set_ylim(-0.3, 3.9)
    ax.set_yticks([0, 1, 2, 3])
    ax.set_xticks(range(-T, 1))
    ax.set_xlabel("time")
    ax.set_ylabel("state")
    ax.set_title("same uniforms $U_{-4},\\dots,U_{-1}$ drive all four paths; all merge by time 0",
                 fontsize=8.5, color=GREY)


@figure("fgB_tv_overlap", w=5.0, h=3.0)
def _(ax):
    # Bin(4,1/2) vs Bin(4,1/3): common mass sum min(p,q); TV = mass not shared
    from fractions import Fraction as Fr
    from math import comb
    P = [Fr(comb(4, k), 16) for k in range(5)]
    Q = [Fr(comb(4, k) * 2 ** (4 - k), 81) for k in range(5)]
    Mn = [min(a, b) for a, b in zip(P, Q)]
    tv = sum(abs(a - b) for a, b in zip(P, Q)) / 2
    k = np.arange(5)
    w = 0.38
    ax.bar(k - w / 2, [float(v) for v in P], width=w, color=BLUE, label=r"$P(X=k)$, $\mathrm{Bin}(4,\frac{1}{2})$")
    ax.bar(k + w / 2, [float(v) for v in Q], width=w, color=ORANGE, label=r"$P(Y=k)$, $\mathrm{Bin}(4,\frac{1}{3})$")
    ax.bar(k, [float(v) for v in Mn], width=0.2, color=GREEN, alpha=0.9, label=r"common mass $\min(p_k,q_k)$")
    ax.set_xticks(k)
    ax.set_xlabel("$k$")
    ax.set_ylabel("probability")
    ax.set_ylim(0, 0.55)
    ax.legend(fontsize=8, frameon=False, loc="upper right")
    ax.text(-0.4, 0.5, f"TV $= {tv.numerator}/{tv.denominator}$", fontsize=9.5, color=INK)


@figure("fgB_house_gain", w=4.6, h=3.0)
def _(ax):
    # Reservation price: the gain from one more look, (1-w)^2/2, equals the look cost c
    c = 0.02
    w = np.linspace(0, 1, 400)
    gain = (1 - w) ** 2 / 2
    ax.plot(w, gain, color=BLUE, lw=2.0, label=r"gain from one more offer $\frac{(1-w)^2}{2}$")
    ax.axhline(c, color=ORANGE, lw=1.6, label=r"look cost $c$")
    wstar = 1 - math.sqrt(2 * c)
    ax.plot([wstar], [c], "o", color=GREEN, ms=7, zorder=5)
    ax.axvline(wstar, color=GREEN, lw=1.0, ls="--")
    ax.text(wstar - 0.02, 0.2, f"$w={wstar:.2f}$", ha="right", fontsize=9.5, color=GREEN)
    ax.text(0.03, 0.09, "gain $>c$: keep looking", fontsize=8.5, color=GREY)
    ax.set_xlim(0, 1); ax.set_ylim(0, 0.5)
    ax.set_xlabel("reservation price $w$")
    ax.set_ylabel("value")
    ax.legend(fontsize=8, frameon=False, loc="upper right")


@figure("fgB_lookahead_tree", w=5.2, h=2.9, axis=False)
def _(ax):
    # Decision tree: colleague's stop at t=1 (red) versus the optimal continuation (green)
    ax.plot([0.4, 1.9], [0.0, 1.1], color=INK, lw=1.0)
    box(ax, (0.0, 0.0), "t=1\ndecide", w=1.1, h=0.7, fs=8.5, fc=LIGHT_BLUE, ec=BLUE)
    box(ax, (2.2, 1.1), "stop: 1", w=1.1, h=0.55, fs=8.5, fc=LIGHT_RED, ec=RED)
    box(ax, (2.2, -0.9), "continue", w=1.1, h=0.55, fs=8.5, fc=LIGHT_GREEN, ec=GREEN)
    arrow(ax, (0.55, 0.12), (1.65, 1.0), color=RED, shrink=2)
    arrow(ax, (0.55, -0.12), (1.65, -0.85), color=GREEN, shrink=2)
    # chance node R2
    box(ax, (4.2, -0.9), "$R_2$", w=0.8, h=0.55, fs=8.5)
    arrow(ax, (2.8, -0.9), (3.8, -0.9), color=INK, shrink=2)
    # outcomes
    box(ax, (5.6, -0.2), "$R_2=0$, p=0.7\ncontinue: 2", w=1.6, h=0.7, fs=7.8, fc=LIGHT_GREEN, ec=GREEN)
    box(ax, (5.6, -1.7), "$R_2=3$, p=0.3\nstop: 3", w=1.6, h=0.7, fs=7.8, fc=LIGHT_GREEN, ec=GREEN)
    arrow(ax, (4.6, -0.75), (4.95, -0.3), color=INK, shrink=2, label=None)
    arrow(ax, (4.6, -1.05), (4.95, -1.6), color=INK, shrink=2, label=None)
    e_cont = 0.7 * 2 + 0.3 * 3
    ax.text(3.5, -2.45, f"value of continuing $=0.7\\cdot2+0.3\\cdot3={e_cont:.1f}$", ha="center",
            fontsize=8.5, color=GREEN)
    frame(ax, -0.9, 6.6, -2.7, 1.8)


@figure("fgB_odds_tail", w=5.0, h=2.9)
def _(ax):
    # Odds r_k = 1/k; tail sums T_s = sum_{k>=s} r_k; the threshold is the largest s with T_s >= 1
    n = 10
    r = {k: 1 / k for k in range(1, n + 1)}
    T = {s: sum(r[k] for k in range(s, n + 1)) for s in range(1, n + 1)}
    s_star = max(s for s in range(1, n + 1) if T[s] >= 1)
    xs = np.arange(1, n + 1)
    cols = [ORANGE if s == s_star else BLUE for s in xs]
    ax.bar(xs, [T[s] for s in xs], color=cols, width=0.62)
    ax.axhline(1, color=GREY, ls="--", lw=1.2)
    ax.text(10.4, 1.03, "1", color=GREY, fontsize=9, ha="left")
    for s in xs:
        ax.text(s, T[s] + 0.03, f"{T[s]:.2f}", ha="center", fontsize=7.5, color=INK)
    ax.set_xticks(xs)
    ax.set_xlabel("$s$ (first index at which you may stop)")
    ax.set_ylabel(r"$\sum_{k\geq s} r_k$")
    ax.set_ylim(0, 3.2)
    ax.text(s_star + 1.0, 2.6, f"$s^*={s_star}$: last $T_s\\geq 1$", color=ORANGE, fontsize=9)
