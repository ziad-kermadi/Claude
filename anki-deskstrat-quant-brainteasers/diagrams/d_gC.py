"""Figures for staging/gap_C.json (Poisson, Wald/Doob, Brownian bridge and arcsine, concentration)."""
import numpy as np
from scipy.stats import norm, binom
from qcfig import *


@figure("fgC_thinning", w=5.6, h=2.4, axis=False)
def _(ax):
    # Thinning: a Poisson(12 per hour) stream, each arrival kept as "large" with p = 1/4.
    lam, p = 12.0, 0.25
    box(ax, (0, 0), "Poisson stream\nrate 12 per hour", w=2.3, h=0.9, fc=LIGHT_BLUE, ec=BLUE, fs=10)
    box(ax, (4.3, 0.85), "large arrivals\nPoisson(%d per hour)" % round(lam * p), w=2.4, h=0.8,
        fc=LIGHT_ORANGE, ec=ORANGE, fs=10)
    box(ax, (4.3, -0.85), "small arrivals\nPoisson(%d per hour)" % round(lam * (1 - p)), w=2.4, h=0.8,
        fc=LIGHT_GREEN, ec=GREEN, fs=10)
    ax.text(2.0, 0.62, "large, p = 1/4", color=ORANGE, fontsize=9.5, ha="center", va="bottom",
            rotation=20)
    ax.text(2.0, -0.62, "small, 1 - p = 3/4", color=GREEN, fontsize=9.5, ha="center", va="top",
            rotation=-20)
    arrow(ax, (1.2, 0.25), (3.0, 0.8), None, color=ORANGE, shrink=2)
    arrow(ax, (1.2, -0.25), (3.0, -0.8), None, color=GREEN, shrink=2)
    frame(ax, -1.4, 5.9, -1.5, 1.5)


@figure("fgC_race_all_fired", w=5.0, h=2.7)
def _(ax):
    # Three independent Poisson processes (rates 1, 2, 3 per hour) started at 0; one simulated sample.
    rng = np.random.default_rng(11)
    rates = [1.0, 2.0, 3.0]
    cols = [BLUE, ORANGE, GREEN]
    horizon = 2.6
    firsts = []
    for j, (lam, c) in enumerate(zip(rates, cols)):
        t, times = 0.0, []
        while True:
            t += rng.exponential(1.0 / lam)
            if t > horizon:
                break
            times.append(t)
        firsts.append(times[0])
        y = len(rates) - j
        for k, s in enumerate(times):
            ax.plot(s, y, "o", ms=5.5, mfc=c if k == 0 else "white", mec=c, mew=1.3, zorder=3)
        ax.plot([0, horizon], [y, y], color=c, lw=0.9, alpha=0.5, zorder=1)
    t_all = max(firsts)
    ax.axvline(t_all, color=RED, ls="--", lw=1.2)
    ax.text(t_all + 0.05, 3.45, "all three have fired", color=RED, fontsize=9, va="center")
    ax.set_yticks([3, 2, 1]); ax.set_yticklabels(["rate 1", "rate 2", "rate 3"])
    ax.set_ylim(0.4, 3.8); ax.set_xlim(-0.05, horizon)
    ax.set_xlabel("time (hours)")
    ax.set_title("filled dot = first event; the wait ends at the latest first event", fontsize=9.5)


@figure("fgC_interval_containing_t", w=5.0, h=2.0)
def _(ax):
    # Waiting-time paradox: the gap containing t splits into age A (elapsed) and residual R (to come).
    arrivals = [0.0, 3.0, 11.5, 16.0]          # illustrative sample; the process starts at 0
    t = 5.0
    before = max(a for a in arrivals if a <= t)
    after = min(a for a in arrivals if a > t)
    A, R = t - before, after - t
    ax.axhline(0, color=INK, lw=1.0)
    ax.plot([0, 16], [0, 0], color=INK, lw=1.0)
    for a in arrivals[1:]:
        ax.plot(a, 0, "o", color=INK, ms=5)
    ax.plot(t, 0, "o", color=RED, ms=6)
    ax.annotate("", xy=(before, 0.55), xytext=(after, 0.55),
                arrowprops=dict(arrowstyle="<->", color=INK, lw=1.0))
    ax.text((before + after) / 2, 0.8, "gap containing t: length L = A + R", ha="center", fontsize=9)
    ax.fill_between([before, t], -0.22, 0.22, color=BLUE, alpha=0.35, lw=0)
    ax.fill_between([t, after], -0.22, 0.22, color=GREEN, alpha=0.35, lw=0)
    ax.text((before + t) / 2, -0.5, "A (age)", color=BLUE, ha="center", fontsize=9)
    ax.text((t + after) / 2, -0.5, "R (residual)", color=GREEN, ha="center", fontsize=9)
    ax.text(t, 0.25, "t", color=RED, ha="center", fontsize=10)
    ax.set_xlim(-0.5, 16.5); ax.set_ylim(-0.9, 1.15)
    ax.set_yticks([]); ax.set_xlabel("time (minutes)")
    ax.spines["left"].set_visible(False)
    ax.text(16.3, 0.9, "L = %.1f" % (A + R), fontsize=8, color=GREY, ha="right")


@figure("fgC_bridge_reflection", w=5.0, h=2.8)
def _(ax):
    # Reflection for a bridge pinned to c = 1 at t = 1: reflect the path after its first hit of a = 2.
    a, c, tau = 2.0, 1.0, 0.4
    t1 = np.linspace(0, tau, 120)
    y1 = a * np.sin(np.pi / 2 * t1 / tau)
    t2 = np.linspace(tau, 1.0, 200)
    u = (t2 - tau) / (1.0 - tau)
    y2 = a + (c - a) * u + 0.25 * np.sin(9 * (t2 - tau)) * np.sin(np.pi * u)
    ax.plot(np.r_[t1, t2], np.r_[y1, y2], color=BLUE, lw=1.6)
    ax.plot(t2, 2 * a - y2, color=ORANGE, lw=1.4, ls="--")
    ax.axhline(a, color=RED, ls=":", lw=1.1)
    ax.plot(tau, a, "o", color=RED, ms=5)
    ax.text(0.02, a + 0.08, "level a = 2", color=RED, fontsize=9)
    ax.plot(1.0, c, "o", color=BLUE, ms=5); ax.plot(1.0, 2 * a - c, "o", color=ORANGE, ms=5)
    ax.text(0.62, c - 0.3, "original end: c = 1", color=BLUE, fontsize=9)
    ax.text(0.62, 2 * a - c + 0.12, "reflected end: 2a - c = 3", color=ORANGE, fontsize=9)
    ax.text(tau - 0.02, a - 0.45, r"$\tau$", ha="right", fontsize=10)
    ax.set_xlim(-0.03, 1.05); ax.set_ylim(-0.2, 3.5)
    ax.set_xlabel("t"); ax.set_ylabel("path")
    ax.set_title("bridge 0 to 1: after the hit, the reflected path ends at 2a - c", fontsize=9.5)


@figure("fgC_arcsine_density", w=4.8, h=2.6)
def _(ax):
    # Arcsine density of the occupation time A of (0, infinity) on [0, 1]; shaded tail P(A >= 3/4).
    x = np.linspace(0.002, 0.998, 800)
    f = 1 / (np.pi * np.sqrt(x * (1 - x)))
    ax.plot(x, f, color=BLUE, lw=1.6)
    xs = np.linspace(0.75, 0.998, 300)
    ax.fill_between(xs, 0, 1 / (np.pi * np.sqrt(xs * (1 - xs))), color=LIGHT_ORANGE, lw=0)
    ax.plot(xs, 1 / (np.pi * np.sqrt(xs * (1 - xs))), color=ORANGE, lw=1.2)
    p_tail = 1 - 2 / np.pi * np.arcsin(np.sqrt(0.75))
    ax.text(0.42, 2.3, "shaded: P(A >= 3/4) = %.3f" % p_tail, color=ORANGE, fontsize=9.5)
    ax.set_xlim(0, 1); ax.set_ylim(0, 3.2)
    ax.set_xlabel("a"); ax.set_ylabel("density")
    ax.set_title(r"$f(a)=\frac{1}{\pi\sqrt{a(1-a)}}$", fontsize=10)


@figure("fgC_running_max_median", w=4.8, h=2.6)
def _(ax):
    # Density of M_1 = max of standard BM on [0, 1] is 2*phi(m); the median splits it into halves.
    m_star = norm.ppf(0.75)
    m = np.linspace(0, 3.0, 400)
    f = 2 * norm.pdf(m)
    ax.fill_between(m[m <= m_star], 0, f[m <= m_star], color=LIGHT_BLUE, lw=0)
    ax.fill_between(m[m >= m_star], 0, f[m >= m_star], color=LIGHT_ORANGE, lw=0)
    ax.plot(m, f, color=INK, lw=1.5)
    ax.axvline(m_star, color=RED, ls="--", lw=1.1)
    ax.text(m_star + 0.06, 1.25, "median = %.4f" % m_star, color=RED, fontsize=9)
    ax.text(0.25, 0.25, "1/2", color=BLUE, fontsize=10)
    ax.text(1.6, 0.25, "1/2", color=ORANGE, fontsize=10)
    ax.set_xlim(0, 3.0); ax.set_ylim(0, 1.7)
    ax.set_xlabel("m"); ax.set_ylabel("density of $M_1$")


@figure("fgC_tail_bounds", w=5.0, h=2.5)
def _(ax):
    # Four bounds versus the exact tail P(X >= 60) for X ~ Binomial(100, 1/2), log scale.
    n, k = 100, 60
    p_exact = float(binom.sf(k - 1, n, 0.5))
    D = 0.6 * np.log(1.2) + 0.4 * np.log(0.8)              # Bernoulli KL, D(0.6 || 0.5)
    vals = [("Markov   E[X]/60", 50 / 60, GREY),
            ("Chebyshev   Var/10^2", 25 / 100, GREY),
            ("Chernoff   exp(-n D)", float(np.exp(-n * D)), BLUE),
            ("Hoeffding   exp(-2*10^2/n)", float(np.exp(-2.0)), BLUE),
            ("exact tail", p_exact, GREEN)]
    for i, (lab, v, c) in enumerate(vals):
        ax.barh(i, v, color=c, alpha=0.85, height=0.6)
        ax.text(v * 1.12, i, "%.4f" % v, va="center", fontsize=9)
    ax.set_yticks(range(len(vals))); ax.set_yticklabels([v[0] for v in vals], fontsize=9)
    ax.set_xscale("log"); ax.set_xlim(1e-2, 2.0)
    ax.set_xlabel("bound on P(X >= 60)  (log scale)")


@figure("fgC_chebyshev_tight", w=4.8, h=2.6)
def _(ax):
    # Equality case of Chebyshev: mean 0, variance 1, mass only at 0 and +-2.
    vals, probs = np.array([-2.0, 0.0, 2.0]), np.array([1 / 8, 3 / 4, 1 / 8])
    assert abs(float(np.sum(vals * probs))) < 1e-12
    assert abs(float(np.sum(vals ** 2 * probs)) - 1.0) < 1e-12
    ax.vlines(vals, 0, probs, color=BLUE, lw=3)
    ax.plot(vals, probs, "o", color=BLUE, ms=6)
    for v, p in zip(vals, probs):
        ax.text(v + (0.18 if v >= 0 else -0.18), p + 0.04, "P = %s" % ("1/8" if p < 0.5 else "3/4"),
                ha="left" if v >= 0 else "right", fontsize=9)
    for v in (-2, 2):
        ax.axvline(v, color=RED, ls="--", lw=1.0)
    ax.plot(0, 0, "x", color=ORANGE, ms=8, mew=2)
    ax.text(0, -0.09, "mean 0", color=ORANGE, ha="center", fontsize=9, va="top")
    ax.text(2.1, 0.5, "|Y| >= 2:\nprob 1/4", color=RED, fontsize=9, va="center")
    ax.set_xlim(-3.2, 3.6); ax.set_ylim(-0.15, 0.95)
    ax.set_xlabel("y"); ax.set_ylabel("probability")
