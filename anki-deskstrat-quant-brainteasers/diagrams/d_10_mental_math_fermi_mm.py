"""Figures for cards/10_mental_math_fermi_mm.json.

Only cards where a picture shows a mechanism are illustrated: market-making quotes and
adverse selection, inventory skew, the Kelly growth curve, Fermi decomposition trees,
extremal and tail-sum geometry, the log/sqrt error plots and Newton/remainder iterations.
Every number a figure states is recomputed here and asserted against the card's answer.
"""
import numpy as np
from math import comb, log, sqrt
from scipy.stats import norm
from scipy.integrate import quad
from scipy.optimize import brentq
from qcfig import *


# ---------- market making on the sum of two fair dice ----------

@figure("f10_mm_dice_quote", w=5.0, h=2.8)
def _(ax):
    s = np.arange(2, 13)
    p = np.array([sum(1 for a in range(1, 7) for b in range(1, 7) if a + b == k) for k in s]) / 36
    mean = (s * p).sum()
    sd = sqrt(((s - mean) ** 2 * p).sum())
    assert abs(mean - 7) < 1e-12 and abs(sd - 2.4152) < 1e-3
    inside = np.abs(s - mean) <= sd
    ax.bar(s, 100 * p, width=0.8, color=[BLUE if i else GREY for i in inside], alpha=0.85)
    ax.vlines([6, 8], 0, 17.0, colors=ORANGE, lw=1.8)
    ax.text(5.8, 17.5, "bid 6", ha="right", va="center", color=ORANGE, fontsize=10)
    ax.text(8.2, 17.5, "ask 8", ha="left", va="center", color=ORANGE, fontsize=10)
    ax.vlines(7, 0, 18.6, colors=INK, ls="--", lw=1.1)
    ax.text(7, 19.4, "mid 7", ha="center", va="center", fontsize=10)
    ax.set_xticks(s)
    ax.set_xlim(1.4, 12.6)
    ax.set_ylim(0, 21.5)
    ax.set_xlabel("sum S of two dice")
    ax.set_ylabel("probability (%)")
    ax.set_title(r"$\sigma = 2.42$; blue = within 1$\sigma$ of 7 (24/36 = two thirds)", fontsize=10)


@figure("f10_mm_winners_curse", w=5.0, h=2.6)
def _(ax):
    dens = 1 / 100
    # ask 50 is filled only if V > 50; conditional mean of V given a fill
    cond_mean = (50 + 100) / 2
    assert cond_mean == 75 and 50 - cond_mean == -25
    ax.plot([0, 100], [dens, dens], color=INK, lw=1.6)
    ax.fill_between([50, 100], 0, dens, color=LIGHT_ORANGE, zorder=1)
    ax.vlines(50, 0, dens * 1.05, colors=ORANGE, lw=1.8, zorder=3)
    ax.text(50, dens * 1.22, "your ask 50", ha="center", va="bottom", color=ORANGE, fontsize=10)
    ax.vlines(cond_mean, 0, dens * 1.05, colors=BLUE, lw=1.8, ls="--", zorder=3)
    ax.text(cond_mean, dens * 1.22, r"E[V | fill] = 75", ha="center", va="bottom", color=BLUE, fontsize=10)
    ax.text(62, 0.0045, "filled only if\nV > 50", ha="center", va="center", fontsize=10)
    ax.text(25, 0.0045, "no fill if V < 50", ha="center", va="center", color=GREY, fontsize=10)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 0.0175)
    ax.set_yticks([])
    ax.set_xlabel(r"true value $V \sim U[0,100]$")
    ax.set_title(r"P&L per fill $= 50 - 75 = -25$", fontsize=10)


@figure("f10_mm_reveal_fair", w=4.8, h=2.6)
def _(ax):
    d = np.arange(1, 7)
    fair = d + 3.5  # E[S | first die = d]
    assert fair[4] == 8.5 and fair[5] == 9.5
    ax.fill_between(d, 8, fair, where=fair > 8, color=LIGHT_RED, zorder=1, interpolate=True)
    ax.axhline(7, color=GREY, ls="--", lw=1.1)
    ax.text(0.8, 7.12, "no information: 7", color=GREY, va="bottom", fontsize=9.5)
    ax.axhline(8, color=ORANGE, lw=1.6)
    ax.text(0.8, 8.12, "your ask 8", color=ORANGE, va="bottom", fontsize=9.5)
    ax.plot(d, fair, "o-", color=BLUE, ms=6, zorder=3)
    for x, y in zip(d, fair):
        ax.text(x, y + 0.28, f"{y:.1f}", ha="center", va="bottom", fontsize=9.5, color=BLUE)
    ax.set_xticks(d)
    ax.set_xlim(0.6, 6.4)
    ax.set_ylim(4.0, 10.5)
    ax.set_xlabel("first die shown to the buyer, $d_1$")
    ax.set_ylabel(r"fair value $E[S \mid d_1]$")
    ax.set_title(r"$E[S \mid d_1] = d_1 + 3.5$; red: ask below fair", fontsize=10)


# ---------- inventory skew ----------

@figure("f10_inventory_skew", w=4.8, h=2.6)
def _(ax):
    mid, c = 100.0, 0.1  # c = gamma sigma^2 (T - t) per unit
    q = np.linspace(-5, 5, 101)
    r = mid - c * q
    assert abs((mid - c * 5) - 99.5) < 1e-12
    ax.fill_between(q, r - 1, r + 1, color=LIGHT_BLUE, alpha=0.8, zorder=1)
    ax.plot(q, r, color=BLUE, lw=2, zorder=3)
    ax.axhline(mid, color=GREY, ls="--", lw=1.0)
    ax.text(-4.9, mid + 0.06, "mid 100", color=GREY, va="bottom", fontsize=9.5)
    ax.plot([5], [mid - c * 5], "o", color=ORANGE, ms=7, zorder=4)
    ax.text(0.6, 101.0, "long 5: r = 99.5, so bid and ask both drop 0.5", fontsize=9.5, color=ORANGE,
            ha="center", va="center")
    ax.set_xlim(-5.2, 5.2)
    ax.set_ylim(98.4, 101.6)
    ax.set_xlabel("inventory q (contracts)")
    ax.set_ylabel("price")
    ax.set_title(r"reservation price $r = \mathrm{mid} - 0.1\,q$; band = bid/ask $\pm 1$", fontsize=10)


# ---------- Kelly ----------

def _g(f, p):
    return p * np.log(1 + f) + (1 - p) * np.log(1 - f)


@figure("f10_kelly_growth", w=5.2, h=2.9)
def _(ax):
    f_star = 2 * 0.6 - 1  # p - q for even money
    g_star = _g(f_star, 0.6)
    f0 = brentq(lambda f: _g(f, 0.6), 0.2, 0.99)
    assert abs(f_star - 0.2) < 1e-12 and abs(g_star - 0.0201) < 5e-5
    assert abs(_g(0.4, 0.6) - (-0.0024)) < 5e-5 and abs(_g(0.1, 0.6) - 0.0150) < 5e-5
    assert abs(f0 - 0.389) < 5e-4
    assert abs(_g(0.2, 0.5) - (-0.0204)) < 5e-5
    f = np.linspace(0.0, 0.45, 400)
    ax.axvspan(f0, 0.45, color=LIGHT_RED, alpha=0.6, zorder=0)
    ax.axhline(0, color=INK, lw=0.8)
    ax.plot(f, _g(f, 0.6), color=BLUE, lw=2, zorder=3)
    fp = np.linspace(0.0, 0.3, 300)
    ax.plot(fp, _g(fp, 0.5), color=GREY, ls="--", lw=1.4, zorder=2)
    ax.plot([f_star], [g_star], "o", color=BLUE, ms=6, zorder=4)
    ax.text(f_star, g_star + 0.0045, "f* = 0.2, g* = 0.0201", ha="center", va="bottom", fontsize=9.5, color=BLUE)
    ax.plot([0.1], [_g(0.1, 0.6)], "o", color=BLUE, ms=5, zorder=4)
    ax.text(0.12, 0.0055, "half-Kelly 0.1: 0.0150", ha="left", va="center", fontsize=9.5, color=BLUE)
    ax.plot([0.4], [_g(0.4, 0.6)], "o", color=RED, ms=6, zorder=4)
    ax.text(0.42, -0.0215, "f = 0.4\ng = -0.0024", ha="center", va="center", fontsize=9.5, color=RED)
    ax.plot([f0], [0], "x", color=RED, ms=7, mew=2, zorder=4)
    ax.text(0.415, 0.0225, f"zero growth\n$f_0 \\approx {f0:.2f}$", ha="center", va="center",
            fontsize=9.5, color=RED)
    ax.plot([0.2], [_g(0.2, 0.5)], "o", color=ORANGE, ms=6, zorder=4)
    ax.text(0.17, -0.0265, "true p = 0.5:\ng(0.2) = -0.0204", ha="right", va="center", fontsize=9.5,
            color=ORANGE)
    ax.text(0.27, -0.0330, "p = 0.5 (no edge)", ha="left", va="center", fontsize=9.5, color=GREY)
    ax.set_xlim(0, 0.46)
    ax.set_ylim(-0.036, 0.03)
    ax.set_xlabel(r"bet fraction $f$")
    ax.set_ylabel(r"$g(f) = p\ln(1+f)+q\ln(1-f)$")
    ax.set_title(r"even money, $p = 0.6$: growth per bet, maximised at $f^* = p - q$", fontsize=10)


@figure("f10_fractional_kelly", w=4.6, h=2.6)
def _(ax):
    lam = np.linspace(0, 2.1, 300)
    rel = 2 * lam - lam ** 2  # g(lambda f*) / g* in the continuous model
    assert abs((2 * 0.5 - 0.25) - 0.75) < 1e-12 and abs((2 * 0.25 - 0.0625) - 0.4375) < 1e-12
    ax.axvspan(1, 2.1, color=LIGHT_RED, alpha=0.6, zorder=0)
    ax.axhline(0, color=INK, lw=0.8)
    ax.plot(lam, rel, color=BLUE, lw=2, zorder=3)
    for x, y, lab, dy in [(0.25, 0.4375, "quarter: 44%", 0.12),
                          (0.5, 0.75, "half: 75%", 0.07),
                          (1.0, 1.0, "full Kelly: 100%", 0.08)]:
        ax.plot([x], [y], "o", color=BLUE, ms=5.5, zorder=4)
        ax.text(x + 0.03, y + dy, lab, ha="left", va="bottom", fontsize=9.5, color=BLUE)
    ax.plot([2.0], [0], "x", color=RED, ms=7, mew=2, zorder=4)
    ax.text(1.62, 0.09, r"$\lambda = 2$: zero growth", ha="center", va="bottom", fontsize=9.5, color=RED)
    ax.text(1.5, 0.45, "over-betting", ha="center", va="center", fontsize=9.5, color=RED)
    ax.set_xlim(0, 2.1)
    ax.set_ylim(-0.12, 1.22)
    ax.set_xticks([0, 0.5, 1, 1.5, 2])
    ax.set_xlabel(r"fraction $\lambda$ of Kelly, bet $= \lambda f^*$")
    ax.set_ylabel(r"$g(\lambda f^*)\, /\, g^*$")
    ax.set_title(r"continuous model: ratio $= 2\lambda - \lambda^2$", fontsize=10)


@figure("f10_kelly_paths", w=5.0, h=2.9)
def _(ax):
    f, p, n_bets, n_paths = 0.2, 0.6, 100, 6
    rng = np.random.default_rng(4)
    steps = np.where(rng.random((n_paths, n_bets)) < p, 1 + f, 1 - f)
    W = np.hstack([np.ones((n_paths, 1)), np.cumprod(steps, axis=1)])
    touched = (W <= 0.5).any(axis=1)
    assert touched.any() and (~touched).any()
    t = np.arange(n_bets + 1)
    ax.axhline(0.5, color=RED, ls="--", lw=1.2, zorder=1)
    ax.text(n_bets * 0.98, 0.52, r"$W = 1/2$", ha="right", va="bottom", color=RED, fontsize=9.5)
    ax.axhline(1.0, color=GREY, lw=0.8, zorder=1)
    for i in range(n_paths):
        col = RED if touched[i] else BLUE
        ax.plot(t, W[i], color=col, lw=1.3, alpha=0.9 if touched[i] else 0.7, zorder=3)
    ax.set_yscale("log")
    ax.set_yticks([0.5, 1, 2, 5, 20])
    ax.set_yticklabels(["1/2", "1", "2", "5", "20"])
    ax.set_xlim(0, n_bets)
    ax.set_ylim(0.3, 30)
    ax.set_xlabel("bet n")
    ax.set_ylabel(r"bankroll $W_n$ (log scale)")
    ax.set_title(r"$P(\min_n W_n \leq 1/2) \leq 1/2$; red paths touch $1/2$", fontsize=10)


# ---------- Fermi decomposition ----------

@figure("f10_fermi_bus_tree", w=5.4, h=2.9, axis=False)
def _(ax):
    fleet, mass = 9000, 11
    assert fleet * mass == 99000
    assert 6000 * 8 == 48000 and 12000 * 13 == 156000
    assert abs(9000 * 7 * 1.5 - 94500) < 1e-9
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    box(ax, (5, 5.15), r"Total mass $\approx 10^{8}$ kg", w=4.0, h=0.72, fs=10.5, fc=LIGHT_BLUE, ec=BLUE)
    box(ax, (2.5, 3.35), "Fleet count  N ≈ 9,000", w=3.6, h=0.72, fs=10)
    box(ax, (7.5, 3.35), "Mass per bus  m ≈ 11 t", w=3.6, h=0.72, fs=10)
    ax.text(5, 3.35, r"$\times$", ha="center", va="center", fontsize=15)
    arrow(ax, (3.9, 4.6), (2.9, 3.75), shrink=2)
    arrow(ax, (6.1, 4.6), (7.1, 3.75), shrink=2)
    ax.text(2.5, 2.42, "range 6,000 to 12,000", ha="center", va="center", fontsize=9, color=GREY)
    ax.text(7.5, 2.42, "range 8 to 13 t", ha="center", va="center", fontsize=9, color=GREY)
    ax.text(5, 1.45, r"central: $9{,}000 \times 11\,\mathrm{t} = 9.9\times10^{4}\,\mathrm{t} \approx 10^{8}$ kg",
            ha="center", va="center", fontsize=9.5)
    ax.text(5, 0.75, r"bounds: $4.8\times10^{4}$ t to $1.6\times10^{5}$ t (about a factor of 2 either way)",
            ha="center", va="center", fontsize=9.5)
    ax.text(5, 0.1, "cross-check: a bus is about 7 cars by mass, so 63,000 cars ≈ $10^{5}$ t",
            ha="center", va="center", fontsize=9, color=GREY)


@figure("f10_fermi_fx_routes", w=5.4, h=2.6, axis=False)
def _(ax):
    bottom_up = 400 * 250 * 10e6
    top_down = 7.5e12 * 0.38
    geo = sqrt(bottom_up * top_down)
    assert abs(bottom_up - 1.0e12) < 1 and abs(top_down - 2.85e12) < 1e6
    assert abs(geo / 1e12 - 1.69) < 0.01
    ax.set_xlim(-0.3, 10.3)
    ax.set_ylim(-0.1, 5.0)
    box(ax, (3.1, 3.5), "Bottom-up\n400 desks × 250 trades/day\n× $10m average size\n= $1.0tn a day",
        w=6.2, h=1.75, fs=9.5, fc=LIGHT_BLUE, ec=BLUE)
    box(ax, (3.1, 1.25), "Top-down\nglobal turnover $7.5tn\n× London share 38%\n= $2.85tn a day",
        w=6.2, h=1.75, fs=9.5, fc=LIGHT_BLUE, ec=BLUE)
    arrow(ax, (6.3, 3.5), (7.2, 2.75), shrink=2, color=BLUE)
    arrow(ax, (6.3, 1.25), (7.2, 2.25), shrink=2, color=BLUE)
    box(ax, (8.6, 2.5), "Geometric mean\n√(1.0 × 2.85)\n≈ $1.7tn", w=2.7, h=1.3, fs=9.5,
        fc=LIGHT_ORANGE, ec=ORANGE)
    ax.text(5, -0.05, "two routes to one quantity; a gap of about 3 is typical for Fermi estimates",
            ha="center", va="center", fontsize=9, color=GREY)


@figure("f10_mm_pnl_chain", w=5.4, h=2.8, axis=False)
def _(ax):
    notional = 1e6 * 10
    captured = 0.05 * notional
    edge_day = 0.0005 * captured
    gross = edge_day * 252
    net = 0.5 * gross
    assert notional == 1e7 and captured == 5e5 and abs(edge_day - 250) < 1e-9
    assert abs(gross - 63000) < 1e-6 and abs(net - 31500) < 1e-6
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    w, h = 2.2, 0.9
    row1, row2 = 3.5, 1.3
    xs = [1.5, 5.0, 8.5]
    box(ax, (xs[0], row1), "1m shares/day", w=w, h=h, fs=9.5)
    box(ax, (xs[1], row1), "£10m/day\nnotional", w=w, h=h, fs=9.5)
    box(ax, (xs[2], row1), "£0.5m/day\ncaptured", w=w, h=h, fs=9.5)
    box(ax, (xs[2], row2), "£250/day\nedge", w=w, h=h, fs=9.5, fc=LIGHT_BLUE, ec=BLUE)
    box(ax, (xs[1], row2), "£63k/yr\ngross", w=w, h=h, fs=9.5, fc=LIGHT_BLUE, ec=BLUE)
    box(ax, (xs[0], row2), "£31k/yr\nnet", w=w, h=h, fs=9.5, fc=LIGHT_ORANGE, ec=ORANGE)
    ax.annotate("", xy=(xs[1] - w / 2 - 0.05, row1), xytext=(xs[0] + w / 2 + 0.05, row1),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.2))
    ax.text((xs[0] + xs[1]) / 2, row1 + 0.32, "× £10", ha="center", va="center", fontsize=9.5)
    ax.annotate("", xy=(xs[2] - w / 2 - 0.05, row1), xytext=(xs[1] + w / 2 + 0.05, row1),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.2))
    ax.text((xs[1] + xs[2]) / 2, row1 + 0.32, "× 5%", ha="center", va="center", fontsize=9.5)
    ax.annotate("", xy=(xs[2], row2 + h / 2 + 0.05), xytext=(xs[2], row1 - h / 2 - 0.05),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.2))
    ax.text(xs[2] + 0.2, (row1 + row2) / 2, "× 5 bp", ha="left", va="center", fontsize=9.5)
    ax.annotate("", xy=(xs[1] + w / 2 + 0.05, row2), xytext=(xs[2] - w / 2 - 0.05, row2),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.2))
    ax.text((xs[1] + xs[2]) / 2, row2 + 0.32, "× 252", ha="center", va="center", fontsize=9.5)
    ax.annotate("", xy=(xs[0] + w / 2 + 0.05, row2), xytext=(xs[1] - w / 2 - 0.05, row2),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.2))
    ax.text((xs[0] + xs[1]) / 2, row2 + 0.32, "× 0.5", ha="center", va="center", fontsize=9.5)
    ax.text(5, 0.2, "gross P&L is linear in every input; adverse selection halves the edge",
            ha="center", va="center", fontsize=9, color=GREY)


# ---------- Fermi uncertainty, extremes, tails ----------

@figure("f10_fermi_band", w=5.0, h=2.6)
def _(ax):
    s_ind = log(2) / sqrt(3) * sqrt(5)           # five independent factors, each log-sd ln2/sqrt3
    s_cor = sqrt(0.96)                           # pair with rho = 0.5 plus three independent
    assert abs(np.exp(s_ind) - 2.45) < 0.01 and abs(np.exp(s_cor) - 2.66) < 0.01
    # plot the density of ln(product): a normal with sd s; tick labels show the factor
    y = np.linspace(-2.6, 2.6, 500)
    def pdf(s):
        return norm.pdf(y / s) / s
    ax.plot(y, pdf(s_ind), color=BLUE, lw=2, label=r"independent: $\div$, $\times$ 2.45")
    ax.plot(y, pdf(s_cor), color=ORANGE, lw=2, ls="--", label=r"correlated pair: $\div$, $\times$ 2.66")
    for s, c in [(s_ind, BLUE), (s_cor, ORANGE)]:
        ax.axvline(-s, color=c, lw=0.9, ls=":")
        ax.axvline(s, color=c, lw=0.9, ls=":")
    ticks = [np.log(0.25), np.log(0.5), 0, np.log(2), np.log(4)]
    ax.set_xticks(ticks)
    ax.set_xticklabels(["0.25", "0.5", "1", "2", "4"])
    ax.set_xlim(-2.6, 2.6)
    ax.set_ylim(0, 0.5)
    ax.set_yticks([])
    ax.set_xlabel("product of five factors (median 1)")
    ax.legend(frameon=False, fontsize=9.5, loc="upper right")
    ax.set_title(r"1$\sigma$ band of the product: dotted lines at $\pm\sigma$ in log space", fontsize=10)


@figure("f10_extremal_max", w=5.0, h=2.6)
def _(ax):
    def emax(N):
        return quad(lambda x: x * N * norm.pdf(x) * norm.cdf(x) ** (N - 1), -12, 12)[0]
    Ns = np.unique(np.round(np.logspace(np.log10(2), 3, 45)).astype(int))
    E = np.array([emax(N) for N in Ns])
    assert abs(emax(5) - 1.163) < 1e-3 and abs(emax(1000) - 3.2414) < 1e-3
    ax.semilogx(Ns, E, color=BLUE, lw=2, label="exact expected max")
    ax.semilogx(Ns, np.sqrt(2 * np.log(Ns)), color=GREY, ls="--", lw=1.3, label=r"$\sqrt{2\ln N}$ (asymptote)")
    ax.plot([5], [emax(5)], "o", color=ORANGE, ms=6, zorder=4)
    ax.text(5 * 1.15, emax(5) - 0.5, "N = 5: 1.16", color=ORANGE, fontsize=9.5, va="center")
    ax.plot([1000], [emax(1000)], "o", color=ORANGE, ms=6, zorder=4)
    ax.text(600, emax(1000) - 0.75, "N = 1000: 3.24", color=ORANGE, fontsize=9.5, va="center", ha="right")
    ax.set_xlim(2, 1200)
    ax.set_ylim(0, 4.2)
    ax.set_xlabel("number of i.i.d. draws N (log scale)")
    ax.set_ylabel("expected max (sd units)")
    ax.legend(frameon=False, fontsize=9.5, loc="upper left")
    ax.set_title(r"the asymptote $\sqrt{2\ln N}$ overshoots at small $N$", fontsize=10)


@figure("f10_max_tail_area", w=5.0, h=2.5)
def _(ax):
    x = np.linspace(0, 1, 300)
    area = quad(lambda t: 1 - t ** 2, 0, 1)[0]
    assert abs(area - 2 / 3) < 1e-9
    ax.fill_between(x, 0, 1 - x ** 2, color=LIGHT_BLUE, zorder=1)
    ax.plot(x, 1 - x ** 2, color=BLUE, lw=2, zorder=3)
    ax.text(0.45, 0.2, r"area $= E[\max] = 2/3$", ha="center", va="center", fontsize=10, zorder=4)
    ax.text(0.5, 0.52, r"$P(\max > x) = 1 - x^2$", ha="center", va="center", fontsize=9.5, color=BLUE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.05)
    ax.set_xlabel("x")
    ax.set_yticks([0, 0.5, 1])
    ax.set_yticklabels(["0", "0.5", "1"])
    ax.set_ylabel(r"$P$")
    ax.set_title(r"$E[\max] = \int_0^1 P(\max > x)\,dx$", fontsize=10)


# ---------- approximation error and convergence ----------

@figure("f10_log_series_error", w=4.8, h=2.7)
def _(ax):
    r = np.logspace(-3, np.log10(0.2), 200)
    e1 = np.abs(np.log1p(r) - r)
    e2 = np.abs(np.log1p(r) - (r - r ** 2 / 2))
    assert abs(log(1.1) - 0.0953102) < 1e-6
    assert abs((0.1 - log(1.1)) - 0.0046898) < 1e-6
    ax.loglog(r, e1, color=BLUE, lw=2, label=r"$\ln(1+r) \approx r$")
    ax.loglog(r, e2, color=ORANGE, lw=2, label=r"$\ln(1+r) \approx r - r^2/2$")
    ax.loglog(r, r ** 2 / 2, color=GREY, ls=":", lw=1.1)
    ax.loglog(r, r ** 3 / 3, color=GREY, ls="-.", lw=1.1)
    ax.text(0.0035, 0.00035, r"$r^2/2$", color=GREY, fontsize=9.5)
    ax.text(0.0035, 0.00001, r"$r^3/3$", color=GREY, fontsize=9.5)
    for x, lab in [(0.01, "r = 0.01"), (0.05, "r = 0.05"), (0.1, "r = 0.1")]:
        ax.axvline(x, color=INK, lw=0.6, ls=":", alpha=0.6)
        ax.text(x, 0.45, lab, ha="center", va="bottom", fontsize=9, color=INK)
    ax.set_xlim(1e-3, 0.2)
    ax.set_ylim(1e-7, 1)
    ax.set_xlabel("r")
    ax.set_ylabel("absolute error")
    ax.legend(frameon=False, fontsize=9, loc="lower right")
    ax.set_title("truncation error of the log series", fontsize=10)


@figure("f10_sd_error_loglog", w=4.6, h=2.6)
def _(ax):
    rng = np.random.default_rng(10)
    ns = np.unique(np.round(np.logspace(1, 4, 16)).astype(int))
    sim = []
    for n in ns:
        reps = max(300, int(2e6 / n))
        samples = rng.standard_normal((reps, n))
        sim.append(samples.std(axis=1, ddof=1).std(ddof=1))
    sim = np.array(sim)
    th = 1 / np.sqrt(2 * (np.logspace(1, 4, 300)))
    assert abs(1 / np.sqrt(2 * 50) - 0.10) < 1e-12 and abs(1 / np.sqrt(2 * 5000) - 0.01) < 1e-3
    ax.loglog(np.logspace(1, 4, 300), th, color=BLUE, lw=2, label=r"$1/\sqrt{2n}$")
    ax.loglog(ns, sim, "o", color=GREY, ms=4, label="simulated")
    ax.plot([50], [0.10], "o", color=ORANGE, ms=6, zorder=4)
    ax.text(50 * 1.25, 0.10 * 1.12, "n = 50: 10%", color=ORANGE, fontsize=9.5, va="bottom")
    ax.plot([5000], [0.01], "o", color=ORANGE, ms=6, zorder=4)
    ax.text(3300, 0.0066, "n = 5000: 1%", color=ORANGE, fontsize=9.5, va="center", ha="right")
    ax.set_xlim(8, 1.3e4)
    ax.set_ylim(0.005, 0.4)
    ax.set_xlabel("sample size n (days)")
    ax.set_ylabel(r"relative error of $\hat\sigma$")
    ax.legend(frameon=False, fontsize=9, loc="upper right")
    ax.set_title("precision costs the inverse square of the error", fontsize=10)


@figure("f10_ncdf_tangent", w=4.6, h=2.6)
def _(ax):
    d = np.linspace(-1.5, 1.5, 400)
    N = norm.cdf(d)
    T = 0.5 + 0.4 * d
    assert abs(norm.cdf(0.25) - 0.5987) < 5e-5 and abs(norm.cdf(0.5) - 0.6915) < 5e-5
    assert abs((0.5 + 0.4 * 0.5) - 0.70) < 1e-12
    ax.fill_between(d, N, T, color=LIGHT_ORANGE, alpha=0.7, zorder=1)
    ax.plot(d, N, color=BLUE, lw=2, zorder=3)
    ax.plot(d, T, color=ORANGE, lw=1.6, ls="--", zorder=3)
    ax.plot([0], [0.5], "o", color=INK, ms=4, zorder=4)
    ax.text(0.05, 0.42, "tangent at d = 0", fontsize=9, color=INK, va="center")
    ax.plot([0.25], [norm.cdf(0.25)], "o", color=BLUE, ms=4, zorder=4)
    ax.annotate("d = 0.25\n0.5987 vs 0.600", xy=(0.25, norm.cdf(0.25)), xytext=(-0.5, 0.80),
                fontsize=9, va="center", arrowprops=dict(arrowstyle="-", color=GREY, lw=0.8))
    ax.plot([0.5], [norm.cdf(0.5)], "o", color=BLUE, ms=4, zorder=4)
    ax.annotate("d = 0.5\n0.6915 vs 0.700", xy=(0.5, norm.cdf(0.5)), xytext=(0.72, 0.27),
                fontsize=9, va="center", arrowprops=dict(arrowstyle="-", color=GREY, lw=0.8))
    ax.text(-1.4, 0.84, r"$N(d)$", color=BLUE, fontsize=10)
    ax.text(-1.4, 0.2, r"$0.5 + 0.4\,d$", color=ORANGE, fontsize=10)
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(0.1, 0.92)
    ax.set_xlabel("d")
    ax.set_ylabel(r"$N(d)$")
    ax.set_title("error grows past $|d| = 0.5$ (0.008)", fontsize=10)


# ---------- state diagrams and iterations ----------

@figure("f10_rem_cycle_7", w=3.6, h=3.1, axis=False)
def _(ax):
    # remainder r -> 10 r mod 7, digit = floor(10 r / 7); period 6 for 1/7
    seq = [1, 3, 2, 6, 4, 5]
    digits = [(10 * r) // 7 for r in seq]
    nxt = [(10 * r) % 7 for r in seq]
    assert nxt == [3, 2, 6, 4, 5, 1] and digits == [1, 4, 2, 8, 5, 7]
    R = 1.55
    pos = {}
    for i, r in enumerate(seq):
        th = np.deg2rad(90 - 60 * i)
        pos[r] = (R * np.cos(th), R * np.sin(th))
    frame(ax, -2.35, 2.35, -2.2, 2.25)
    for i, r in enumerate(seq):
        s = seq[(i + 1) % 6]
        arrow(ax, pos[r], pos[s], label=f"digit {digits[i]}", rad=-0.22, color=INK, shrink=17, fs=9, lw=1.2)
    for r in seq:
        node(ax, pos[r], str(r), r=0.3, fs=11, fc=LIGHT_ORANGE if r == 1 else "white",
             ec=ORANGE if r == 1 else INK)
    ax.text(0, 0.0, "r ↦ 10r mod 7", ha="center", va="center", fontsize=9.5, color=GREY)
    caption(ax, "period 6: digits 142857", fs=9.5)


@figure("f10_newton_recip_error", w=4.8, h=2.5)
def _(ax):
    def iterate(x0, n):
        xs = [x0]
        for _ in range(n):
            xs.append(xs[-1] * (2 - 7 * xs[-1]))
        return np.array(xs)
    bad, good = iterate(0.3, 5), iterate(0.14, 5)
    assert np.allclose(bad[:5], [0.3, -0.03, -0.0663, -0.16339, -0.51371], atol=2e-4)
    assert abs(good[1] - 0.1428) < 1e-12
    target = 1 / 7
    k = np.arange(6)
    ax.semilogy(k, np.abs(bad - target), "o-", color=RED, lw=1.8, ms=5, label=r"$x_0 = 0.3$ (outside basin)")
    ax.semilogy(k, np.abs(good - target) + 1e-12, "o-", color=BLUE, lw=1.8, ms=5,
                label=r"$x_0 = 0.14$ (inside $0<x_0<2/7$)")
    ax.set_xlim(-0.2, 5.2)
    ax.set_ylim(1e-9, 30)
    ax.set_xlabel("iteration k")
    ax.set_ylabel(r"$|x_k - 1/7|$")
    ax.legend(frameon=False, fontsize=9, loc="center right")
    ax.set_title(r"$x_{k+1} = x_k(2-7x_k)$: error grows outside the basin", fontsize=10)
