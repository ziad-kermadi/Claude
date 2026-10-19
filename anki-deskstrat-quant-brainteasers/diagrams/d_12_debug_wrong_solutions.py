"""Figures for cards/12_debug_wrong_solutions.json (find-the-flaw cards). Figures go on the back."""
import math
from itertools import combinations
from math import comb
from statistics import NormalDist
import numpy as np
from qcfig import *

_N = NormalDist()


def _bs_call(S, K, r, s, T):
    d1 = (math.log(S / K) + (r + s * s / 2) * T) / (s * math.sqrt(T))
    d2 = d1 - s * math.sqrt(T)
    return S * _N.cdf(d1) - K * math.exp(-r * T) * _N.cdf(d2)


def _p_gt(k):
    """P(T > k) for the simple walk hitting +1: equals P(S_k in {0, 1})."""
    if k == 0:
        return 1.0
    j = k // 2 if k % 2 == 0 else (k + 1) // 2
    return math.exp(math.lgamma(k + 1) - math.lgamma(j + 1) - math.lgamma(k - j + 1) - k * math.log(2))


# ---------- card 0: urn, equally likely objects are subsets ----------
@figure("f12_urn_subsets", w=5.0, h=2.6)
def _(ax):
    cnt = [comb(3, k) * comb(4, 3 - k) for k in range(4)]  # size-3 subsets with k blue balls
    tot = sum(cnt)
    assert tot == comb(7, 3) == 35 and cnt[1] == 18
    pr = [c / tot for c in cnt]
    ks = np.arange(4)
    ax.bar(ks, pr, width=0.55, color=[LIGHT_BLUE, LIGHT_ORANGE, LIGHT_BLUE, LIGHT_BLUE],
           ec=[BLUE, ORANGE, BLUE, BLUE], lw=1.3, zorder=2)
    ax.hlines([0.25] * 4, ks - 0.4, ks + 0.4, colors=RED, linestyles="--", lw=1.6, zorder=3)
    for k in ks:
        ax.text(k, pr[k] + 0.025, f"{cnt[k]}/35", ha="center", fontsize=10)
    ax.text(2.4, 0.64, "dashed red: wrong 1/4 each", color=RED, fontsize=9.5, ha="center")
    ax.set_xticks(ks)
    ax.set_xticklabels([f"{k} blue" for k in ks])
    ax.set_ylim(0, 0.7)
    ax.set_ylabel("probability")
    ax.set_title("35 equally likely subsets, grouped by blue count", fontsize=10)


# ---------- card 1: two dice, ordered outcomes ----------
@figure("f12_dice_grid", w=4.8, h=3.3, axis=False)
def _(ax):
    doubles = sum(1 for a in range(1, 7) for b in range(1, 7) if a == b)
    assert doubles == 6 and 36 == 6 * 6
    for a in range(1, 7):          # first die: row (top = 1)
        for b in range(1, 7):      # second die: column
            x, y = b, 7 - a
            if a == b:
                fc, ec = LIGHT_GREEN, GREEN
            elif {a, b} == {1, 2}:
                fc, ec = LIGHT_RED, RED
            else:
                fc, ec = "white", GREY
            ax.add_patch(Rectangle((x - 0.45, y - 0.45), 0.9, 0.9, fc=fc, ec=ec, lw=1.1, zorder=2))
            ax.text(x, y, f"{a},{b}", ha="center", va="center", fontsize=9, zorder=3)
    for b in range(1, 7):
        ax.text(b, 7.1, str(b), ha="center", va="bottom", fontsize=10, color=GREY)
    for a in range(1, 7):
        ax.text(0.2, 7 - a, str(a), ha="right", va="center", fontsize=10, color=GREY)
    ax.text(3.5, 7.7, "36 ordered rolls (die 1 row, die 2 column)", ha="center", fontsize=10)
    ax.text(0.5, -0.75, r"right: doubles $\frac{6}{36}=\frac{1}{6}$ (green)", color=GREEN, fontsize=10)
    ax.text(0.5, -1.45, r"wrong: $\frac{6}{21}$ over 21 unordered pairs", color=RED, fontsize=10)
    ax.text(0.5, -2.15, "red pair {1,2}: 2 cells, a double: 1 cell", color=INK, fontsize=9.5)
    frame(ax, -0.6, 6.7, -2.6, 8.2)


# ---------- card 2: five-card hand, witness overcount ----------
@figure("f12_witness_overcount", w=5.2, h=2.1)
def _(ax):
    true_n = comb(52, 5) - comb(48, 5)
    wit = 4 * comb(51, 4)
    extra = wit - true_n
    assert true_n == 886656 and wit == 999600 and extra == 112944
    assert extra == sum((k - 1) * comb(4, k) * comb(48, 5 - k) for k in range(1, 5))
    t, e = true_n / 1e3, extra / 1e3
    ax.barh(1, t, height=0.5, color=LIGHT_BLUE, ec=BLUE, lw=1.2)
    ax.barh(0, t, height=0.5, color=LIGHT_BLUE, ec=BLUE, lw=1.2)
    ax.barh(0, e, left=t, height=0.5, color=LIGHT_RED, ec=RED, lw=1.2, hatch="///")
    ax.text(t / 2, 1, "886 656 hands", ha="center", va="center", fontsize=10)
    ax.text(t / 2, 0, "each hand once", ha="center", va="center", fontsize=10)
    ax.text(t + e + 12, 0, "+112 944: hands with\n2, 3 or 4 aces", va="center", fontsize=9.5)
    ax.set_yticks([1, 0])
    ax.set_yticklabels(["true count", "witness count"], fontsize=10)
    ax.set_xlim(0, 1700)
    ax.set_xlabel("hands (thousands)")


# ---------- card 8: medical test, counts ----------
@figure("f12_medical_counts", w=5.2, h=2.4)
def _(ax):
    sick, tp, healthy = 100, 99, 99900
    fp = round(0.05 * healthy)
    assert fp == 4995
    pos = tp + fp
    assert pos == 5094
    assert abs(tp / sick - 0.99) < 1e-12
    r2 = tp / pos
    assert abs(r2 - 0.0194) < 1e-4
    # top row: among the sick, the test is positive 99% of the time (the wrong reading)
    ax.barh(1, 0.99, height=0.5, color=LIGHT_BLUE, ec=BLUE, lw=1.2)
    ax.barh(1, 0.01, left=0.99, height=0.5, color="white", ec=GREY, lw=1.0)
    ax.text(0.495, 1, "99 of 100 sick test positive", ha="center", va="center", fontsize=9.5)
    # bottom row: among the positives, only 99 of 5094 are sick (the answer)
    ax.barh(0, r2, height=0.5, color=LIGHT_BLUE, ec=BLUE, lw=1.2)
    ax.barh(0, 1 - r2, left=r2, height=0.5, color=LIGHT_RED, ec=RED, lw=1.2)
    ax.text(0.62, 0, "4995 healthy positives", ha="center", va="center", fontsize=9.5)
    ax.text(0.02, 0.42, "99 sick of 5094 positives", ha="left", va="bottom", fontsize=9.5, color=BLUE)
    ax.text(0.5, 1.42, r"$P(+\mid \mathrm{sick})=0.99$ (wrong answer)", ha="center", fontsize=10, color=RED)
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.5, 1.7)
    ax.set_yticks([1, 0])
    ax.set_yticklabels(["sick people", "positive tests"], fontsize=10)
    ax.set_xticks([])
    ax.spines["bottom"].set_visible(False)
    ax.set_title(r"$P(\mathrm{sick}\mid +)=\frac{99}{5094}\approx0.0194$", fontsize=10)


# ---------- card 9: Monty Hall, reveal likelihood ----------
@figure("f12_monty_tree", w=5.4, h=3.0, axis=False)
def _(ax):
    p_car = 1 / 3
    p_open3 = {1: 1 / 2, 2: 1.0, 3: 0.0}   # host can open door 3 only if it is not the pick or the car
    joint = {c: p_car * p_open3[c] for c in (1, 2, 3)}
    assert abs(joint[1] - 1 / 6) < 1e-12 and abs(joint[2] - 1 / 3) < 1e-12
    post2 = joint[2] / sum(joint.values())
    post1 = joint[1] / sum(joint.values())
    assert abs(post2 - 2 / 3) < 1e-12 and abs(post1 - 1 / 3) < 1e-12
    root = (0.0, 0.0)
    lvl1 = {1: (2.0, 1.2), 2: (2.0, 0.0), 3: (2.0, -1.2)}
    leaf = {1: (4.3, 1.2), 2: (4.3, 0.0), 3: (4.3, -1.2)}
    box(ax, root, "car door", w=1.4, h=0.42, fs=10)
    for c in (1, 2, 3):
        box(ax, lvl1[c], f"car {c}", w=0.9, h=0.42, fs=10,
            ec=ORANGE if c == 2 else INK)
        arrow(ax, (0.55, 0.0), (lvl1[c][0] - 0.45, lvl1[c][1]), "1/3",
              shrink=0, fs=10, label_offset=(0, 0.12 if c != 2 else -0.12))
    for c in (1, 2):
        arrow(ax, (lvl1[c][0] + 0.45, lvl1[c][1]), (leaf[c][0] - 0.42, leaf[c][1]),
              "open 3", shrink=0, fs=9.5, label_offset=(0, 0.2))
    box(ax, leaf[1], "1/6", w=0.8, h=0.42, fs=10)
    box(ax, leaf[2], "1/3", w=0.8, h=0.42, fs=10, fc=LIGHT_ORANGE, ec=ORANGE)
    box(ax, (4.3, -1.2), "0", w=0.8, h=0.42, fs=10, ec=RED)
    ax.text(4.3, -1.85, "host cannot\nopen door 3", ha="center", va="center", fontsize=9, color=RED)
    ax.text(5.35, 1.2, "joint: P(car 1) P(open 3 | car 1)", fontsize=9.5, va="center")
    ax.text(5.35, 0.0, "given open 3: car 2 = (1/3)/(1/2) = 2/3", fontsize=10,
            va="center", color=ORANGE)
    ax.text(5.35, -0.8, "car 1 = (1/6)/(1/2) = 1/3", fontsize=10, va="center")
    ax.text(5.35, -1.6, "wrong: 'two doors left, 1/2 each'", fontsize=9.5, va="center", color=RED)
    ax.set_xlim(-0.8, 8.4)
    ax.set_ylim(-2.3, 2.0)


# ---------- card 12: two children, selection of a child ----------
@figure("f12_family_selection", w=5.0, h=2.7)
def _(ax):
    fams = ["BB", "BG", "GB", "GG"]
    pick_boy = {"BB": 1.0, "BG": 0.5, "GB": 0.5, "GG": 0.0}
    wrong = np.array([1.0, 1.0, 1.0, 0.0])
    wrong = wrong / wrong.sum()
    joint = np.array([0.25 * pick_boy[f] for f in fams])
    correct = joint / joint.sum()
    assert abs(correct[0] - 0.5) < 1e-12 and abs(wrong[0] - 1 / 3) < 1e-12
    x = np.arange(4)
    w = 0.38
    ax.bar(x - w / 2, wrong, w, color=LIGHT_RED, ec=RED, lw=1.1, label="wrong: families with a boy")
    ax.bar(x + w / 2, correct, w, color=LIGHT_BLUE, ec=BLUE, lw=1.1,
           label="right: family times P(picked child is a boy)")
    for i in range(4):
        ax.text(x[i] - w / 2, wrong[i] + 0.02, f"{wrong[i]:.2f}" if wrong[i] else "0", ha="center", fontsize=9.5)
        ax.text(x[i] + w / 2, correct[i] + 0.02, f"{correct[i]:.2f}" if correct[i] else "0", ha="center", fontsize=9.5)
    ax.set_xticks(x)
    ax.set_xticklabels(fams)
    ax.set_ylim(0, 1.0)
    ax.set_ylabel("probability")
    ax.set_xlabel("family (first child, second child)")
    ax.legend(fontsize=9, frameon=False, loc="upper right")
    ax.set_title("P(other is a boy | picked child is a boy) = 1/2, not 1/3", fontsize=10)


# ---------- card 14: uniform prior, one head ----------
@figure("f12_bias_posterior", w=5.0, h=2.6)
def _(ax):
    p = np.linspace(0, 1, 401)
    post = 2 * p
    assert abs(post.mean() - 1) < 1e-3          # integrates to 1 on [0,1]
    m = p > 0.5
    ax.fill_between(p[m], 0, np.ones(m.sum()), color=GREY, alpha=0.25, lw=0)
    ax.fill_between(p[m], 0, post[m], color=LIGHT_BLUE, lw=0)
    ax.plot(p, np.ones_like(p), color=GREY, ls="--", lw=1.6, label="prior: flat")
    ax.plot(p, post, color=BLUE, lw=2.0, label=r"posterior $\propto p$ (after heads)")
    ax.text(0.75, 0.42, r"$\frac{3}{4}$", color=BLUE, fontsize=12, ha="center")
    ax.text(0.75, 1.12, r"prior area $\frac{1}{2}$", color=GREY, fontsize=9.5, ha="center")
    ax.set_xlabel("bias p")
    ax.set_ylabel("density")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 2.4)
    ax.legend(fontsize=9, frameon=False, loc="upper left")


# ---------- card 17: Jensen, reciprocal ----------
@figure("f12_jensen_reciprocal", w=5.0, h=2.8)
def _(ax):
    x = np.linspace(0.7, 6.3, 300)
    ax.plot(x, 1 / x, color=INK, lw=1.4, label=r"$y=1/x$")
    k = np.arange(1, 7)
    ax.vlines(k, 0, 1 / k, colors=GREY, lw=0.8, ls=":")
    ax.plot(k, 1 / k, "o", color=BLUE, ms=5, label=r"the six values $1/X$")
    mean_inv = float(np.mean(1 / k))
    assert abs(mean_inv - 49 / 120) < 1e-12
    ax.axhline(mean_inv, color=BLUE, ls="--", lw=1.2)
    ax.plot(3.5, 1 / 3.5, "o", color=RED, mfc="white", ms=7, mew=1.6,
            label=r"wrong: $1/E[X]=2/7$ at $E[X]=3.5$")
    ax.text(6.25, mean_inv + 0.02, r"$E[1/X]=\frac{49}{120}\approx0.408$", ha="right", va="bottom",
            fontsize=10, color=BLUE)
    ax.set_xlim(0.5, 6.5)
    ax.set_ylim(0, 1.25)
    ax.set_xlabel("x")
    ax.set_ylabel("1/x")
    ax.legend(fontsize=9, frameon=False, loc="upper right")


# ---------- card 55: call payoff, Jensen ----------
@figure("f12_option_chord", w=5.0, h=2.7)
def _(ax):
    S = np.linspace(60, 140, 400)
    ax.plot(S, np.maximum(S - 100, 0), color=INK, lw=1.8)
    ax.plot([80, 120], [0, 20], color=BLUE, ls="--", lw=1.2)
    ax.plot([80, 120], [0, 20], "o", color=BLUE, ms=5)
    avg = (0 + 20) / 2
    assert avg == 10
    ax.plot(100, avg, "o", color=BLUE, ms=6)
    ax.plot(100, 0, "o", mfc="white", mec=RED, ms=7, mew=1.8)
    ax.text(80.5, 14.0, r"$E[(S-100)^+]=10$", color=BLUE, fontsize=10, va="bottom")
    ax.text(101.5, -3.0, "wrong: payoff at E[S]=100 is 0", color=RED, fontsize=10, va="center")
    ax.text(79, 2.5, "S=80", fontsize=9.5, ha="right")
    ax.text(121, 20, "S=120", fontsize=9.5, va="center")
    ax.set_xlim(60, 140)
    ax.set_ylim(-4.5, 24)
    ax.set_xticks([80, 100, 120])
    ax.set_xlabel(r"$S_T$")
    ax.set_ylabel("payoff")


# ---------- card 24: simple walk, optional stopping fails ----------
@figure("f12_hitting_truncated", w=5.0, h=2.7)
def _(ax):
    assert abs(_p_gt(1) - 0.5) < 1e-12 and abs(_p_gt(3) - 0.375) < 1e-12
    N = 10000
    pg = np.array([_p_gt(k) for k in range(N)])
    ET = np.cumsum(pg)                   # ET[n-1] = E[min(T, n)]
    n = np.arange(1, N + 1)
    ax.loglog(n, ET, color=BLUE, lw=1.8, label=r"$E[T\wedge n]$ (exact)")
    ax.loglog(n, 2 * np.sqrt(2 * n / np.pi), color=GREY, ls=":", lw=1.3,
              label=r"$2\sqrt{2n/\pi}$")
    ax.axhline(1, color=RED, ls="--", lw=1.4, label="claimed $E[T]=1$")
    ax.plot([N], [ET[-1]], "o", color=ORANGE, ms=6)
    ax.text(N * 0.9, ET[-1] * 1.35, f"{ET[-1]:.0f} at n=10000", ha="right", fontsize=9.5, color=ORANGE)
    ax.set_xlabel("n (steps allowed)")
    ax.set_ylabel(r"$E[T\wedge n]$")
    ax.set_ylim(0.8, 600)
    ax.legend(fontsize=9, frameon=False, loc="upper left")


# ---------- card 26: gambler's ruin, drift ratio ----------
@figure("f12_ruin_ratio", w=5.0, h=2.7)
def _(ax):
    N = 10
    k = np.arange(0, N + 1)
    r = 1 / 2                                  # q/p
    corr = (1 - r ** k) / (1 - r ** N)
    wrong = (1 - 2.0 ** k) / (1 - 2.0 ** N)    # uses p/q = 2
    assert abs(corr[3] - 896 / 1023) < 1e-12 and abs(wrong[3] - 7 / 1023) < 1e-12
    ax.plot(k, corr, "o-", color=BLUE, ms=4, label=r"$r=\frac{q}{p}=\frac{1}{2}$ (correct)")
    ax.plot(k, wrong, "s--", color=RED, ms=4, label=r"$r=\frac{p}{q}=2$ (wrong)")
    ax.plot([3], [corr[3]], "o", color=ORANGE, ms=8)
    ax.text(3.3, 0.6, f"correct, r=q/p: {corr[3]:.3f} at k=3", color=BLUE, fontsize=9.5)
    ax.text(3.3, 0.3, f"wrong, r=p/q: {wrong[3]:.4f}", color=RED, fontsize=9.5)
    ax.set_xlabel("start k (absorbing at 0 and 10)")
    ax.set_ylabel(r"$P(\mathrm{hit}\ 10\ \mathrm{first})$")
    ax.set_ylim(-0.05, 1.12)
    ax.set_xticks(k)


# ---------- card 29: reflection principle for Brownian motion ----------
@figure("f12_reflection", w=5.2, h=2.8)
def _(ax):
    n = 1000
    dt = 1.0 / n
    for seed in range(1, 2000):
        rng = np.random.default_rng(seed)
        W = np.concatenate([[0.0], np.cumsum(rng.standard_normal(n) * math.sqrt(dt))])
        if W.max() >= 1 and -0.4 < W[-1] < 0.4:
            break
    else:
        raise RuntimeError("no seed found")
    tau = int(np.argmax(W >= 1))
    t = np.arange(n + 1) * dt
    ax.plot(t[: tau + 1], W[: tau + 1], color=BLUE, lw=1.3)
    ax.plot(t[tau:], W[tau:], color=BLUE, lw=0.9, alpha=0.35)
    ax.plot(t[tau:], 2 - W[tau:], color=RED, lw=1.2, ls="--")
    ax.axhline(1, color=ORANGE, lw=1.1, ls=":")
    ax.plot(t[tau], 1, "o", color=ORANGE, ms=5)
    ax.plot([1], [W[-1]], "o", color=BLUE, ms=5)
    ax.plot([1], [2 - W[-1]], "o", color=RED, ms=5)
    ax.text(0.98, W[-1] - 0.25, r"$W_1<1$", ha="right", color=BLUE, fontsize=10)
    ax.text(0.98, 2 - W[-1] + 0.15, r"reflected: $2-W_1$", ha="right", color=RED, fontsize=10)
    ax.text(0.02, 1.12, "level 1", color=ORANGE, fontsize=9.5)
    p_true = 2 * (1 - _N.cdf(1))
    assert abs(p_true - 0.3173) < 1e-4
    ax.set_xlim(0, 1.02)
    ax.set_ylim(-1.6, 2.9)
    ax.set_xlabel("t")
    ax.set_ylabel(r"$W_t$")
    ax.set_title(r"$P(\max W\geq1)=2(1-\Phi(1))\approx0.317$, not $0.159$", fontsize=10)


# ---------- card 35: broken stick, density of ordered pair ----------
@figure("f12_broken_stick", w=3.8, h=3.1)
def _(ax):
    ax.add_patch(Polygon([(0, 0), (1, 1), (0, 1)], closed=True, fc=LIGHT_BLUE, ec="none", alpha=0.45, zorder=1))
    ax.add_patch(Polygon([(0, 0.5), (0.5, 0.5), (0.5, 1.0)], closed=True, fc=LIGHT_GREEN, ec=GREEN, lw=1.2, zorder=2))
    ax.add_patch(Polygon([(0.5, 0), (0.5, 0.5), (1.0, 0.5)], closed=True, fc=LIGHT_GREEN, ec=GREEN, lw=1.2, zorder=2))
    ax.plot([0, 1], [0, 1], color=GREY, ls="--", lw=1.0, zorder=3)
    ax.plot([0, 1, 1, 0, 0], [0, 0, 1, 1, 0], color=INK, lw=1.0, zorder=3)
    area_half = 1 / 8
    assert abs(2 * area_half - 1 / 4) < 1e-12
    ax.text(0.06, 0.9, r"$X<Y$", fontsize=10, color=BLUE)
    ax.text(0.72, 0.05, r"$Y<X$", fontsize=10, color=GREY)
    frame(ax, -0.1, 1.1, -0.1, 1.1)
    ax.set_xlabel("first break X")
    ax.set_ylabel("second break Y")
    ax.set_xticks([0, 0.5, 1])
    ax.set_yticks([0, 0.5, 1])
    ax.set_title(r"green: area $\frac{1}{8}$ each half; density 2 gives $P=\frac{1}{4}$", fontsize=9.5)


# ---------- card 38: uniform point in the disc ----------
@figure("f12_disc_radius", w=5.0, h=2.7, axis=False)
def _(ax):
    radii = np.arange(0.1, 1.01, 0.1)
    for cx, inner_col, label, sub in [
        (-1.3, GREY, "wrong: R uniform\n(5 of 10 equal rings)", r"$P=\frac{1}{2}$"),
        (1.3, BLUE, "right: shaded area\nr < 1/2 of the disc", r"$P=\frac{1}{4}$"),
    ]:
        ax.add_patch(Circle((cx, 0), 1.0, fc="white", ec=INK, lw=1.1, zorder=1))
        for rr in radii[:-1]:
            ax.add_patch(Circle((cx, 0), rr, fc="none", ec=GREY, lw=0.6, zorder=2))
        if inner_col == GREY:
            ax.add_patch(Circle((cx, 0), 0.5, fc="none", ec=GREY, lw=1.8, ls="--", zorder=3))
        else:
            ax.add_patch(Circle((cx, 0), 0.5, fc=LIGHT_BLUE, ec=BLUE, lw=1.4, zorder=3))
        ax.text(cx, -1.25, label, ha="center", va="top", fontsize=9.5,
                color=inner_col if inner_col != GREY else RED)
        ax.text(cx, -2.0, sub, ha="center", va="top", fontsize=11,
                color=inner_col if inner_col != GREY else RED)
    assert abs((0.5 ** 2) - 0.25) < 1e-12
    frame(ax, -2.7, 2.7, -2.4, 1.3)


# ---------- card 39: nim with moves 1..3 ----------
@figure("f12_nim_positions", w=5.2, h=2.3, axis=False)
def _(ax):
    def losing(n):
        return n % 4 == 0
    xs = {n: 0.55 * n for n in range(11)}
    for n in range(11):
        L = losing(n)
        node(ax, (xs[n], 0), str(n), r=0.22, fc=LIGHT_RED if L else LIGHT_BLUE,
             ec=RED if L else BLUE, fs=10)
    for n in (3, 6, 9):
        ax.add_patch(Circle((xs[n], 0), 0.3, fc="none", ec=GREY, lw=1.0, ls="--", zorder=2))
    ax.annotate("", xy=(xs[8] + 0.02, 0.27), xytext=(xs[10] - 0.02, 0.27), zorder=6,
                arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=1.5, connectionstyle="arc3,rad=0.8",
                                shrinkA=0, shrinkB=0))
    ax.text(xs[9], 0.85, "take 2: 10 to 8", color=ORANGE, fontsize=10, ha="center", va="center")
    ax.text(xs[0], -0.8, "red = losing for the player to move (0, 4, 8)", fontsize=9.5, color=RED, ha="left")
    ax.text(xs[0], -1.25, "dashed grey = wrong rule, multiples of 3", fontsize=9.5, color=GREY, ha="left")
    frame(ax, -0.4, 6.1, -1.5, 1.6)


# ---------- card 43: first to three wins ----------
@figure("f12_race_to_three", w=4.6, h=3.0)
def _(ax):
    p = 0.6
    p_ge3 = sum(comb(5, j) * p ** j * (1 - p) ** (5 - j) for j in range(3, 6))
    assert abs(p_ge3 - 0.68256) < 1e-6
    assert abs(3 * p * p * (1 - p) + p ** 3 - 0.648) < 1e-9
    for a in range(4):
        for b in range(4):
            if a == 3 and b == 3:
                continue                   # the match ends before both reach 3
            if a == 3:
                fc, ec = LIGHT_GREEN, GREEN
            elif b == 3:
                fc, ec = LIGHT_RED, RED
            elif a + b == 3:
                fc, ec = LIGHT_ORANGE, ORANGE
            else:
                fc, ec = "white", GREY
            ax.scatter([a], [b], s=900, c=fc, edgecolors=ec, linewidths=1.4, zorder=3)
            ax.text(a, b, f"{a}-{b}", ha="center", va="center", fontsize=9.5, zorder=4)
    ax.set_xlim(-0.6, 6.4)
    ax.set_ylim(-0.6, 3.6)
    ax.set_xticks([0, 1, 2, 3])
    ax.set_yticks([0, 1, 2, 3])
    ax.set_xlabel("rounds A has won")
    ax.set_ylabel("rounds B has won")
    ax.text(3.6, 3.0, "B has 3: B wins", color=RED, fontsize=9.5, ha="left", va="center")
    ax.text(3.6, 2.0, "A has 3: A wins", color=GREEN, fontsize=9.5, ha="left", va="center")
    ax.text(3.6, 1.0, "orange: undecided\nafter 3 rounds", color=ORANGE, fontsize=9.5, ha="left", va="center")
    ax.set_title(r"$P(A)=P(\mathrm{Bin}(5,0.6)\geq3)=0.68256$ (2-2 still open)", fontsize=9.5)


# ---------- card 54: American call, no dividends ----------
@figure("f12_american_bound", w=5.0, h=2.8)
def _(ax):
    S = np.linspace(50, 140, 300)
    K, r, s, T = 80.0, 0.05, 0.2, 1.0
    bs = np.array([_bs_call(x, K, r, s, T) for x in S])
    lower = np.maximum(S - K * math.exp(-r * T), 0)
    intrinsic = np.maximum(S - K, 0)
    v100 = _bs_call(100.0, K, r, s, T)
    assert abs(v100 - 24.59) < 0.01
    assert abs((100 - K * math.exp(-r * T)) - 23.90) < 0.01
    ax.plot(S, intrinsic, color=GREY, ls="--", lw=1.4, label="intrinsic $(S-K)^+$ (wrong)")
    ax.plot(S, lower, color=ORANGE, ls=":", lw=1.6, label=r"lower bound $S-Ke^{-rT}$")
    ax.plot(S, bs, color=BLUE, lw=1.9, label="call value (Black-Scholes)")
    ax.plot([100], [20], "o", mfc="white", mec=RED, ms=7, mew=1.6)
    ax.plot([100], [v100], "o", color=BLUE, ms=6)
    ax.text(102, v100 + 2.5, f"{v100:.2f}", color=BLUE, fontsize=10)
    ax.text(102, 14.5, "20 (wrong)", color=RED, fontsize=10)
    ax.set_xlim(50, 140)
    ax.set_ylim(-3, 62)
    ax.set_xlabel(r"$S$ (with $K=80$, $r=5\%$, $\sigma=20\%$, $T=1$)")
    ax.set_ylabel("value")
    ax.legend(fontsize=9, frameon=False, loc="upper left")


# ---------- card 65: sampling without replacement ----------
@figure("f12_fpc_variance", w=5.0, h=2.6)
def _(ax):
    pop = list(range(1, 11))
    N = 10
    sig2 = sum((x - 5.5) ** 2 for x in pop) / N
    assert abs(sig2 - 8.25) < 1e-12
    means5 = [sum(c) / 5 for c in combinations(pop, 5)]
    assert len(means5) == 252
    v5 = float(np.var(means5))
    assert abs(v5 - 11 / 12) < 1e-9
    n = np.arange(1, N + 1)
    corr = sig2 / n * (N - n) / (N - 1)
    wrong = sig2 / n
    ax.plot(n, wrong, "s--", color=RED, ms=4, label=r"wrong: $\sigma^2/n$")
    ax.plot(n, corr, "o-", color=BLUE, ms=4, label=r"right: $\frac{\sigma^2}{n}\cdot\frac{N-n}{N-1}$")
    ax.plot([5], [corr[4]], "o", color=ORANGE, ms=8)
    ax.text(2.6, 0.45, f"n=5: {corr[4]:.3f}", color=BLUE, fontsize=10)
    ax.text(5.6, wrong[4] + 0.35, f"n=5: {wrong[4]:.2f}", color=RED, fontsize=10)
    ax.set_xlabel("sample size n (N = 10, without replacement)")
    ax.set_ylabel(r"$\mathrm{Var}(\bar X)$")
    ax.set_xticks(n)
    ax.set_ylim(-0.2, 9.0)
    ax.legend(fontsize=9, frameon=False, loc="upper right")


# ---------- card 66: regression to the mean ----------
@figure("f12_regression_mean", w=4.8, h=3.0)
def _(ax):
    rng = np.random.default_rng(12)
    M = 20000
    th = rng.standard_normal(M)
    X = th + rng.standard_normal(M)
    q = float(np.quantile(X, 0.99))
    top = X >= q
    z = _N.inv_cdf(0.99)
    ex_top = math.sqrt(2) * _N.pdf(z) / 0.01            # E[X | top 1%] analytically
    assert abs(ex_top - 3.77) < 0.02 and abs(ex_top / 2 - 1.88) < 0.02
    ax.scatter(X[::20], th[::20], s=4, color=GREY, alpha=0.35, lw=0)
    ax.scatter(X[top], th[top], s=7, color=ORANGE, alpha=0.7, lw=0)
    xx = np.linspace(-4, 5, 100)
    ax.plot(xx, xx, color=RED, ls="--", lw=1.2, label=r"wrong: skill $=$ score")
    ax.plot(xx, xx / 2, color=BLUE, lw=1.9, label=r"$E[\theta\mid X]=X/2$")
    ax.plot([ex_top], [ex_top / 2], "o", color=BLUE, ms=7)
    ax.plot([ex_top], [ex_top], "o", mfc="white", mec=RED, ms=7, mew=1.6)
    ax.text(4.0, -0.9, r"skill $\approx1.88$", color=BLUE, fontsize=10)
    ax.text(ex_top - 2.6, ex_top + 0.55, "wrong: 3.77", color=RED, fontsize=10)
    ax.set_xlim(-4, 5.5)
    ax.set_ylim(-4, 5)
    ax.set_xlabel(r"observed score $X=\theta+\varepsilon$")
    ax.set_ylabel(r"skill $\theta$")
    ax.legend(fontsize=9, frameon=False, loc="lower right")


# ---------- card 68: explicit heat scheme stability ----------
@figure("f12_heat_stability", w=5.0, h=2.6)
def _(ax):
    dx = 0.1
    th = np.linspace(0, math.pi, 300)
    r6, r5 = 0.006 / dx ** 2, 0.005 / dx ** 2
    assert abs(r6 - 0.6) < 1e-12
    g6 = 1 - 4 * r6 * np.sin(th / 2) ** 2
    g5 = 1 - 4 * r5 * np.sin(th / 2) ** 2
    ax.axhspan(-1, 1, color=LIGHT_GREEN, alpha=0.6, lw=0)
    ax.plot(th, g6, color=RED, lw=1.9, label=r"$r=0.6$ (wrong: stable)")
    ax.plot(th, g5, color=BLUE, lw=1.6, ls="--", label=r"$r=0.5$")
    ax.plot([math.pi], [1 - 4 * r6], "o", color=RED, ms=6)
    ax.text(2.35, -1.55, f"g(pi) = {1 - 4 * r6:.1f}", ha="left", color=RED, fontsize=9.5)
    ax.text(1.75, 0.8, "|g| <= 1 (stable)", color=GREEN, fontsize=9.5)
    ax.set_xticks([0, math.pi / 2, math.pi])
    ax.set_xticklabels(["0", r"$\pi/2$", r"$\pi$"])
    ax.set_xlabel(r"$k\,\Delta x$")
    ax.set_ylabel("amplification g")
    ax.set_xlim(0, math.pi)
    ax.set_ylim(-1.7, 1.3)
    ax.legend(fontsize=9, frameon=False, loc="lower left")


# ---------- card 69: Monte Carlo error vs N ----------
@figure("f12_mc_loglog", w=4.8, h=2.7)
def _(ax):
    Ns = np.logspace(3, 6, 100)
    se = np.sqrt(0.25 / Ns)
    assert abs(math.sqrt(0.25 / 1e4) - 0.005) < 1e-12
    se2 = math.sqrt(0.25 / 2e4)
    assert abs(se2 - 0.00354) < 1e-5
    ax.loglog(Ns, se, color=INK, lw=1.4)
    ax.plot([1e4], [0.005], "o", color=BLUE, ms=6)
    ax.plot([2e4], [0.0025], "o", mfc="white", mec=RED, ms=7, mew=1.6)
    ax.plot([2e4], [se2], "o", color=BLUE, ms=6)
    ax.plot([4e4], [math.sqrt(0.25 / 4e4)], "o", color=ORANGE, ms=7)
    ax.axhline(0.0025, color=GREY, ls=":", lw=1.1)
    ax.text(1.1e3, 0.0030, "halve the error: 0.0025", color=GREY, fontsize=9.5)
    ax.text(1.3e5, 0.0042, "2x: 0.0035", color=BLUE, fontsize=9.5, ha="left")
    ax.text(1.3e5, 0.0031, "4x: 0.0025", color=ORANGE, fontsize=9.5, ha="left")
    ax.set_xlabel("sample size N")
    ax.set_ylabel("standard error")
    ax.set_xlim(1e3, 1e6)
    ax.set_ylim(5e-4, 0.02)


# ---------- card 70: Cholesky by hand, variance as squared length ----------
@figure("f12_cholesky_vectors", w=4.4, h=3.0, axis=False)
def _(ax):
    rho = 0.6
    c_good = math.sqrt(1 - rho ** 2)
    c_bad = math.sqrt(1 - rho)
    assert abs(c_good - 0.8) < 1e-12
    assert abs(rho ** 2 + c_bad ** 2 - 0.76) < 1e-12
    ax.annotate("", xy=(1, 0), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.8))
    ax.annotate("", xy=(rho, c_good), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.9))
    ax.annotate("", xy=(rho, c_bad), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.5, ls="--"))
    ax.text(1.04, -0.08, r"$Z_1$", fontsize=10)
    ax.text(0.62, 0.86, r"right: $c=0.8$, length 1", color=BLUE, fontsize=9.5, ha="left")
    ax.text(0.68, 0.5, r"wrong: $c^2=1-\rho$, length 0.87", color=RED, fontsize=9.5, ha="left")
    ax.text(-0.2, -0.45, r"$\mathrm{Var}=0.36+c^2$: wrong $0.76$, right $1$", fontsize=9.5, ha="left")
    ax.text(-0.2, -0.7, r"$\mathrm{Corr}=\rho/\sqrt{\mathrm{Var}}$, so only length 1 gives $\rho=0.6$", fontsize=9.5, ha="left")
    frame(ax, -0.25, 1.6, -0.9, 1.1)


# ---------- card 72: OLS with an intercept ----------
@figure("f12_ols_intercept", w=4.8, h=2.8)
def _(ax):
    x = np.array([1.0, 2.0, 3.0])
    y = np.array([3.0, 5.0, 7.0])
    slope0 = float(np.sum(x * y) / np.sum(x * x))
    assert abs(slope0 - 34 / 14) < 1e-12
    xc = x - x.mean()
    b1 = float(np.sum(xc * (y - y.mean())) / np.sum(xc * xc))
    b0 = float(y.mean() - b1 * x.mean())
    assert abs(b1 - 2) < 1e-12 and abs(b0 - 1) < 1e-12
    xx = np.linspace(0, 3.8, 50)
    ax.plot(xx, slope0 * xx, color=RED, ls="--", lw=1.4,
            label=rf"no intercept: slope {slope0:.2f}")
    ax.plot(xx, b1 * xx + b0, color=BLUE, lw=1.9, label=r"with intercept: $y=2x+1$")
    ax.plot(x, y, "o", color=INK, ms=6, zorder=5)
    ax.set_xlim(0, 3.9)
    ax.set_ylim(0, 10)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend(fontsize=9, frameon=False, loc="lower right")


# ---------- card 74: Kelly, net odds ----------
@figure("f12_kelly_growth", w=5.0, h=2.7)
def _(ax):
    p, q = 0.6, 0.4
    f = np.linspace(0.0, 0.8, 400)

    def G(b, ff):
        return p * np.log(1 + b * ff) + q * np.log(1 - ff)

    fstar = (2 * p - q) / 2
    assert abs(fstar - 0.4) < 1e-12
    wrong_f = (3 * p - q) / 3
    assert abs(wrong_f - 0.4667) < 1e-3
    ax.plot(f, G(2, f), color=BLUE, lw=1.9, label=r"net odds $b=2$ (right)")
    ax.plot(f, G(3, f), color=RED, lw=1.3, ls="--", label=r"decimal 3 used as $b$ (wrong)")
    ax.plot([fstar], [G(2, fstar)], "o", color=BLUE, ms=7)
    ax.plot([wrong_f], [G(2, wrong_f)], "o", mfc="white", mec=RED, ms=7, mew=1.6)
    ax.text(fstar + 0.02, G(2, fstar) + 0.012, r"$f^*=0.4$", color=BLUE, fontsize=10)
    ax.text(wrong_f + 0.03, 0.05, r"$f=0.467$ (wrong)", color=RED, fontsize=9.5)
    ax.axhline(0, color=GREY, lw=0.8)
    ax.set_xlabel("fraction staked f")
    ax.set_ylabel("expected log growth")
    ax.set_xlim(0, 0.8)
    ax.set_ylim(-0.1, 0.32)
    ax.legend(fontsize=9, frameon=False, loc="lower left")
