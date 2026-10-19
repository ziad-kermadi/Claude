"""Figures for staging/gap_F.json (gap batch F: Kyle, square-root impact, Almgren-Chriss,
Avellaneda-Stoikov, Glosten-Milgrom)."""
import math
import numpy as np
from qcfig import *


def _edge(ax, A, B, rA=0.34, rB=0.34, label=None, color=INK, off=(0, 0), fs=9):
    A = np.array(A, float); B = np.array(B, float)
    d = B - A
    u = d / np.hypot(*d)
    arrow(ax, tuple(A + u * rA), tuple(B - u * rB), label, rad=0.0, color=color,
          shrink=0, fs=fs, label_offset=off)


# ---------- 1. Kyle: the price is the regression of v on y (card 0 back) ----------

@figure("fgF_kyle_regression", w=5.0, h=2.9)
def _(ax):
    sv, su = 2.0, 1.0
    lam = sv / (2 * su)
    rng = np.random.default_rng(5)
    n = 4000
    v = sv * rng.standard_normal(n)
    u = su * rng.standard_normal(n)
    y = (v / 2) + u                       # insider x = beta v, beta = su/sv = 1/2
    slope = np.cov(v, y, bias=True)[0, 1] / np.var(y)
    assert abs(slope - lam) < 0.05, slope
    ax.scatter(y, v, s=4, color=GREY, alpha=0.35, lw=0, label="simulated $(y, v)$")
    g = np.linspace(-4.5, 4.5, 50)
    ax.plot(g, lam * g, color=BLUE, lw=1.9, label=r"price $p=\lambda y$, $\lambda=1$")
    ax.axhline(0, color=INK, lw=0.6)
    ax.set_xlim(-4.5, 4.5); ax.set_ylim(-5.5, 5.5)
    ax.set_xlabel(r"total order flow $y=x+u$"); ax.set_ylabel(r"value $v$")
    ax.legend(frameon=False, fontsize=8.5, loc="upper left")
    ax.set_title(r"$E[v\mid y]$ is linear in $y$, so $p=\lambda y$", fontsize=10)


# ---------- 2. Kyle: doubling noise trading (card 2 back) ----------

@figure("fgF_kyle_sigma_u", w=5.0, h=2.7)
def _(ax):
    sv = 2.0
    su = np.logspace(math.log10(0.25), math.log10(4.0), 200)
    lam = sv / (2 * su)
    prof = su * sv / 2
    ax.loglog(su, lam, color=BLUE, lw=1.8, label=r"price impact $\lambda=\frac{\sigma_v}{2\sigma_u}$")
    ax.loglog(su, prof, color=ORANGE, lw=1.8, label=r"insider profit $\frac{\sigma_u\sigma_v}{2}$")
    for s0 in (1.0, 2.0):
        ax.plot(s0, sv / (2 * s0), "o", color=BLUE, ms=5)
        ax.plot(s0, s0 * sv / 2, "o", color=ORANGE, ms=5)
    ax.set_xticks([0.25, 0.5, 1, 2, 4]); ax.set_xticklabels(["0.25", "0.5", "1", "2", "4"])
    ax.minorticks_off()
    ax.set_yticks([0.25, 0.5, 1, 2, 4]); ax.set_yticklabels(["0.25", "0.5", "1", "2", "4"])
    ax.set_xlabel(r"noise-trader volatility $\sigma_u$ (dots at $\sigma_u=1,2$)"); ax.set_ylabel("value")
    ax.set_ylim(0.2, 4.2)
    ax.legend(frameon=False, fontsize=8.5, loc="upper center")
    ax.set_title(r"$\sigma_v=2$: impact halves, profit doubles; $\mathrm{Var}(p)=2$ throughout",
                 fontsize=9.5)


# ---------- 3. Square-root splitting: cost of n equal children (card 5 back) ----------

@figure("fgF_split_cost", w=5.0, h=2.7)
def _(ax):
    Q, V, sg = 1.0, 1.0, 1.0

    def whole():
        return sg * Q * math.sqrt(Q / V)

    def children(n):
        q = Q / n
        return n * q * sg * math.sqrt(q / V)

    ns = np.arange(1, 9)
    sq = np.array([children(n) / whole() for n in ns])
    lin = 1.0 / ns                                  # linear impact: cost ratio 1/n
    assert abs(sq[3] - 0.5) < 1e-12 and abs(lin[3] - 0.25) < 1e-12
    ax.plot(ns, lin, "o--", color=GREY, lw=1.3, ms=4, label=r"linear impact: $1/n$")
    ax.plot(ns, sq, "o-", color=BLUE, lw=1.8, ms=4, label=r"square-root impact: $n^{-1/2}$")
    ax.plot(4, 0.25, "o", color=GREY, ms=7, zorder=5)
    ax.plot(4, 0.5, "o", color=ORANGE, ms=7, zorder=5)
    ax.annotate(r"$n=4$: $\frac{1}{4}$", (4, 0.25), xytext=(5.0, 0.12), fontsize=9, color=GREY,
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.8))
    ax.annotate(r"$n=4$: $\frac{1}{2}$", (4, 0.5), xytext=(5.2, 0.62), fontsize=9, color=ORANGE,
                arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.8))
    ax.set_xlim(0.7, 8.3); ax.set_ylim(0, 1.08)
    ax.set_xticks(range(1, 9))
    ax.set_xlabel("number of equal children $n$"); ax.set_ylabel("total cost / whole cost")
    ax.legend(frameon=False, fontsize=8.5, loc="upper right")
    ax.set_title("concave impact: splitting saves less than $n$", fontsize=10)


# ---------- 4. Almgren-Chriss schedule (cards 6 and 8 back) ----------

@figure("fgF_ac_sinh", w=5.0, h=2.8)
def _(ax):
    s = np.linspace(0, 1, 400)                     # s = t/T
    def sched(kT):
        return np.sinh(kT * (1 - s)) / np.sinh(kT)
    ax.plot(s, sched(0.01), color=GREY, ls="--", lw=1.3, label=r"$\kappa T\to0$: TWAP")
    ax.plot(s, sched(2.0), color=BLUE, lw=1.9, label=r"$\kappa T=2$")
    ax.plot(s, sched(4.0), color=ORANGE, lw=1.5, label=r"$\kappa T=4$")
    mid = math.sinh(1.0) / math.sinh(2.0)          # kT=2 at t=T/2
    q3 = math.sinh(1.5) / math.sinh(2.0)           # kT=2 at t=T/4
    assert abs(mid - 0.3240) < 5e-4 and abs(q3 - 0.5871) < 5e-4
    ax.plot(0.5, mid, "o", color=BLUE, ms=5)
    ax.plot(0.25, q3, "o", color=BLUE, ms=5)
    ax.annotate(rf"${mid:.3f}$", (0.5, mid), xytext=(0.56, 0.12), fontsize=9, color=BLUE)
    ax.annotate(rf"${q3:.3f}$", (0.25, q3), xytext=(0.30, 0.66), fontsize=9, color=BLUE)
    ax.set_xlim(0, 1); ax.set_ylim(-0.02, 1.04)
    ax.set_xlabel(r"$t/T$"); ax.set_ylabel(r"$x(t)/X$ shares left")
    ax.legend(frameon=False, fontsize=8.5, loc="upper right")
    ax.set_title(r"$x(t)/X=\frac{\sinh(\kappa(T-t))}{\sinh(\kappa T)}$", fontsize=10)


# ---------- 5. Avellaneda-Stoikov quotes with and without inventory (card 9 back) ----------

@figure("fgF_as_ladder", w=4.6, h=3.0)
def _(ax):
    s, gam, sig, tau, k = 100.0, 0.1, 0.5, 2.0, 1.5
    spread = gam * sig ** 2 * tau + (2 / gam) * math.log(1 + gam / k)
    cases = [(0, GREY, 0.0), (3, ORANGE, 0.0)]
    for x0, (q, col, _) in zip([0.0, 1.0], [(0, GREY, 0), (3, ORANGE, 0)]):
        r = s - q * gam * sig ** 2 * tau
        bid, ask = r - spread / 2, r + spread / 2
        ax.plot([x0, x0], [bid, ask], color=col, lw=5, alpha=0.35, solid_capstyle="butt")
        ax.plot(x0, r, "o", color=col, ms=7, zorder=4)
        ax.plot([x0 - 0.22, x0 + 0.22], [bid, bid], color=col, lw=1.6)
        ax.plot([x0 - 0.22, x0 + 0.22], [ask, ask], color=col, lw=1.6)
        ax.text(x0 + 0.3, ask, f"ask {ask:.3f}", va="center", fontsize=8.5, color=col)
        ax.text(x0 + 0.3, bid, f"bid {bid:.3f}", va="center", fontsize=8.5, color=col)
        ax.text(x0 - 0.3, r + 0.13, f"$r={r:.2f}$", va="center", ha="right", fontsize=8.5, color=col,
                bbox=dict(fc="white", ec="none", pad=1.0), zorder=6)
    ax.axhline(s, color=INK, ls=":", lw=1.0)
    ax.text(1.85, s + 0.06, "mid $s=100$", fontsize=8, color=GREY, ha="right")
    ax.set_xlim(-0.9, 1.9); ax.set_ylim(98.8, 101.2)
    ax.set_xticks([0, 1]); ax.set_xticklabels([r"$q=0$", r"$q=+3$"])
    ax.set_ylabel("price")
    ax.set_title("the reservation price shifts, the width does not", fontsize=9.5)


# ---------- 6. Glosten-Milgrom probability tree (card 12 back) ----------

@figure("fgF_gm_tree", w=5.2, h=2.7, axis=False)
def _(ax):
    mu = 0.25
    pbuy_H = mu + (1 - mu) / 2          # 5/8
    pbuy_L = (1 - mu) / 2               # 3/8
    root, H, L = (0.0, 0.0), (2.0, 0.9), (2.0, -0.9)
    leaves = {"Hb": (4.6, 1.45), "Hs": (4.6, 0.35), "Lb": (4.6, -0.35), "Ls": (4.6, -1.45)}
    node(ax, root, "V", r=0.3)
    box(ax, H, r"$V_H=110$", w=1.3, h=0.5, fc=LIGHT_BLUE, ec=BLUE)
    box(ax, L, r"$V_L=90$", w=1.3, h=0.5, fc=LIGHT_ORANGE, ec=ORANGE)
    _edge(ax, root, H, label=r"$\frac{1}{2}$", color=BLUE, off=(-0.25, 0.25))
    _edge(ax, root, L, label=r"$\frac{1}{2}$", color=ORANGE, off=(-0.25, -0.25))
    labels = {"Hb": ("buy", pbuy_H, BLUE), "Hs": ("sell", 1 - pbuy_H, GREY),
              "Lb": ("buy", pbuy_L, BLUE), "Ls": ("sell", 1 - pbuy_L, GREY)}
    for key, (lab, pr, col) in labels.items():
        src = H if key[0] == "H" else L
        box(ax, leaves[key], lab, w=0.7, h=0.42, fc=LIGHT_BLUE if lab == "buy" else "white",
            ec=col, fs=9.5)
        frac = {0.625: r"$\frac{5}{8}$", 0.375: r"$\frac{3}{8}$"}[round(pr, 3)]
        _edge(ax, src, leaves[key], rB=0.4, label=frac, color=col, fs=9.5,
              off=(0.0, 0.32 if key in ("Hb", "Lb") else -0.32))
    ax.text(0.5, -2.2, r"$E[V\mid \mathrm{buy}]=110\cdot\frac{5}{8}+90\cdot\frac{3}{8}=102.5$",
            ha="center", fontsize=9.5, color=INK)
    frame(ax, -0.6, 5.4, -2.5, 2.1)
