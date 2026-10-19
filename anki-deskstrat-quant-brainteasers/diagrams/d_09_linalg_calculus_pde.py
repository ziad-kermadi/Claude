"""Figures for cards/09_linalg_calculus_pde.json."""
import math
import numpy as np
from qcfig import *

SQ2 = math.sqrt(2.0)


# ---------- linear algebra: ellipses ----------

@figure("f09_chol_ellipse", w=4.4, h=3.0)
def _(ax):
    # X = LZ maps the unit circle to the 1-sigma contour of Sigma = LL^T
    L = np.array([[1.0, 0.0], [0.6, 0.8]])
    Sig = L @ L.T
    assert np.allclose(Sig, [[1, 0.6], [0.6, 1]])
    th = np.linspace(0, 2 * np.pi, 400)
    Z = np.vstack([np.cos(th), np.sin(th)])
    X = L @ Z
    ax.plot(Z[0], Z[1], ls="--", color=GREY, lw=1.2)
    ax.plot(X[0], X[1], color=BLUE, lw=2.0)
    for z, c in [((1.0, 0.0), ORANGE), ((0.0, 1.0), GREEN)]:
        z = np.array(z)
        x = L @ z
        ax.plot(*z, "o", color=c, ms=5)
        ax.plot(*x, "o", color=c, ms=5)
        ax.annotate("", xy=x, xytext=z,
                    arrowprops=dict(arrowstyle="-|>", color=c, lw=1.3, shrinkA=6, shrinkB=6))
    ax.text(1.1, 0.6, r"$(Z_1,Z_2)=(1,0)$" "\n" r"$\mapsto (1,\,0.6)$", color=ORANGE, fontsize=9,
            va="center")
    ax.text(0.1, 1.12, r"$(0,1)\mapsto(0,\,0.8)$", color=GREEN, fontsize=9)
    ax.text(-1.45, -1.55, "grey: $Z$ on the unit circle\nblue: $X=LZ$ (contour of $\\Sigma$)",
            color=INK, fontsize=9, va="bottom")
    ax.set_xlim(-1.5, 2.3)
    ax.set_ylim(-1.7, 1.45)
    ax.set_aspect("equal")
    ax.set_xlabel(r"$X_1$")
    ax.set_ylabel(r"$X_2$")
    ax.set_title(r"$X_1=Z_1,\quad X_2=0.6\,Z_1+0.8\,Z_2$", fontsize=10)


def _eig_base(ax):
    A = np.array([[2.0, 1.0], [1.0, 2.0]])
    vals = np.linalg.eigvalsh(A)
    assert np.allclose(vals, [1, 3])
    v_top = np.array([1.0, 1.0]) / SQ2
    v_bot = np.array([1.0, -1.0]) / SQ2
    assert np.allclose(A @ v_top, 3 * v_top) and np.allclose(A @ v_bot, v_bot)
    th = np.linspace(0, 2 * np.pi, 400)
    C = np.vstack([np.cos(th), np.sin(th)])
    E = A @ C
    ax.plot(C[0], C[1], ls="--", color=GREY, lw=1.2)
    ax.plot(E[0], E[1], color=BLUE, lw=2.0)
    ax.plot([0, 3 * v_top[0]], [0, 3 * v_top[1]], color=ORANGE, lw=1.6)
    ax.plot([0, v_bot[0]], [0, v_bot[1]], color=GREEN, lw=1.6)
    ax.plot(*v_top, "o", color=ORANGE, ms=4)
    ax.plot(*v_bot, "o", color=GREEN, ms=4)
    ax.text(3 * v_top[0] + 0.15, 3 * v_top[1] + 0.1, r"$\lambda=3$", color=ORANGE, fontsize=10)
    ax.text(v_bot[0] + 0.25, v_bot[1] + 0.2, r"$\lambda=1$", color=GREEN, fontsize=10)
    ax.set_xlim(-3.4, 3.4)
    ax.set_ylim(-3.0, 3.0)
    ax.set_aspect("equal")
    ax.set_xlabel(r"$x_1$")
    ax.set_ylabel(r"$x_2$")


@figure("f09_eig_ellipse", w=4.4, h=3.0)
def _(ax):
    _eig_base(ax)
    ax.set_title(r"image $\{Ax:\ \|x\|=1\}$ of the unit circle", fontsize=9.5)


@figure("f09_rayleigh_line", w=4.4, h=3.0)
def _(ax):
    _eig_base(ax)
    # constraint line x1+x2=0 is the span of (1,-1); it meets the unit circle at +-(1,-1)/sqrt2
    ax.plot([-3 / SQ2, 3 / SQ2], [3 / SQ2, -3 / SQ2], color=RED, ls="--", lw=1.3)
    u = np.array([1.0, -1.0]) / SQ2
    ax.plot(*u, "o", color=RED, ms=6)
    ax.plot(*(-u), "o", color=RED, ms=6)
    ax.plot(*(np.array([1.0, 1.0]) / SQ2), "x", color=GREY, ms=8, mew=2)
    ax.set_title("red: $x_1+x_2=0$, optimum $(1,-1)/\\sqrt{2}$\n"
                 r"value $x^{\mathsf{T}}Ax=1$; grey $\times$: top eigenvector, infeasible",
                 fontsize=9)


# ---------- two-asset minimum variance ----------

@figure("f09_minvar_parabola", w=4.6, h=2.7)
def _(ax):
    S = np.array([[0.04, 0.03], [0.03, 0.09]])  # sigma1=0.2, sigma2=0.3, rho=0.5
    one = np.ones(2)
    y = np.linalg.solve(S, one)
    wstar = y / y.sum()
    vstar = math.sqrt(1.0 / (one @ np.linalg.solve(S, one)))
    assert np.allclose(wstar, [6 / 7, 1 / 7]) and abs(vstar ** 2 - 27 / 700) < 1e-12
    t = np.linspace(-0.4, 1.4, 400)
    vol = np.array([math.sqrt(np.array([x, 1 - x]) @ S @ np.array([x, 1 - x])) for x in t])
    ax.axvspan(-0.4, 0, color=GREY, alpha=0.14, lw=0)
    ax.axvspan(1, 1.4, color=GREY, alpha=0.14, lw=0)
    ax.text(-0.2, 0.47, "short", color=GREY, fontsize=9, ha="center")
    ax.text(1.2, 0.47, "short", color=GREY, fontsize=9, ha="center")
    ax.plot(t, vol, color=BLUE, lw=2.0)
    ax.plot(0, 0.3, "o", color=GREY, ms=5)
    ax.plot(1, 0.2, "o", color=GREY, ms=5)
    ax.text(0.04, 0.315, r"asset 2 only", fontsize=9, color=INK)
    ax.text(1.03, 0.2, r"asset 1 only", fontsize=9, color=INK, va="center")
    ax.plot(wstar[0], vstar, "o", color=ORANGE, ms=6)
    ax.annotate(r"min: $w_1=\frac{6}{7}$, $\sigma=\sqrt{\frac{27}{700}}\approx0.1964$",
                xy=(wstar[0], vstar), xytext=(0.12, 0.37), fontsize=9,
                arrowprops=dict(arrowstyle="-", color=ORANGE, lw=1))
    ax.set_xlim(-0.4, 1.4)
    ax.set_ylim(0.15, 0.5)
    ax.set_xlabel(r"$w_1$  ($w_2=1-w_1$)")
    ax.set_ylabel(r"volatility $\sigma(w)$")


@figure("f09_minvar_rho", w=4.6, h=2.6)
def _(ax):
    def w1(r):
        S = np.array([[0.04, 0.06 * r], [0.06 * r, 0.09]])
        y = np.linalg.solve(S, np.ones(2))
        return y[0] / y.sum()
    assert abs(w1(0.0) - 9 / 13) < 1e-12
    formula = lambda r: (0.09 - r * 0.06) / (0.13 - 2 * r * 0.06)
    assert abs(w1(0.7) - formula(0.7)) < 1e-12
    rho = np.linspace(-1.0, 0.995, 300)
    ax.plot(rho, [w1(r) for r in rho], color=BLUE, lw=2.0)
    ax.axhline(3, color=GREEN, ls="--", lw=1.1)
    ax.axhline(1, color=GREY, ls=":", lw=1.1)
    ax.text(-0.98, 3.12, r"$\rho\to1$: $w_1\to3$", color=GREEN, fontsize=9)
    ax.text(0.35, 1.08, r"$w_2=0$", color=GREY, fontsize=9)
    ax.plot(0, 9 / 13, "o", color=ORANGE, ms=6)
    ax.annotate(r"$\rho=0$: $w_1=\frac{9}{13}$", xy=(0, 9 / 13), xytext=(-0.85, 2.0),
                fontsize=9, arrowprops=dict(arrowstyle="-", color=ORANGE, lw=1))
    ax.set_xlim(-1.0, 1.0)
    ax.set_ylim(0.0, 3.5)
    ax.set_xlabel(r"correlation $\rho$")
    ax.set_ylabel(r"$w_1$ (min variance)")


@figure("f09_minvar_long_only", w=4.6, h=2.7)
def _(ax):
    S = np.array([[0.04, 0.05], [0.05, 0.25]])  # sigma1=0.2, sigma2=0.5, rho=0.5
    y = np.linalg.solve(S, np.ones(2))
    wu = y / y.sum()
    assert np.allclose(wu, [20 / 19, -1 / 19])
    t = np.linspace(-0.3, 1.45, 400)
    vol = np.array([math.sqrt(np.array([x, 1 - x]) @ S @ np.array([x, 1 - x])) for x in t])
    ax.axvspan(0, 1, color=LIGHT_GREEN, alpha=0.8, lw=0)
    ax.text(0.5, 0.66, "long-only: $0\\leq w_1\\leq1$", color=GREEN, fontsize=9, ha="center")
    ax.plot(t, vol, color=BLUE, lw=2.0)
    vu = math.sqrt(1 / (np.ones(2) @ y))
    ax.plot(wu[0], vu, "o", mfc="white", mec=GREY, ms=7, mew=1.5)
    ax.text(wu[0] + 0.03, vu - 0.035, r"unconstrained $w_1=\frac{20}{19}$", color=GREY, fontsize=9)
    ax.plot(1, 0.2, "o", color=ORANGE, ms=6)
    ax.annotate(r"constrained: $w=(1,0)$, $\sigma=0.2$", xy=(1, 0.2), xytext=(0.2, 0.3),
                fontsize=9, color=ORANGE, arrowprops=dict(arrowstyle="-", color=ORANGE, lw=1))
    ax.set_xlim(-0.3, 1.45)
    ax.set_ylim(0.15, 0.7)
    ax.set_xlabel(r"$w_1$  ($w_2=1-w_1$)")
    ax.set_ylabel(r"volatility $\sigma(w)$")


# ---------- Gaussian integral ----------

@figure("f09_complete_square", w=4.4, h=2.5)
def _(ax):
    x = np.linspace(-1.5, 3.5, 600)
    g = np.exp(-x ** 2 + 2 * x)
    assert np.allclose(g, math.e * np.exp(-(x - 1) ** 2))
    xx = np.linspace(-12, 14, 40001)
    area = np.trapezoid(np.exp(-xx ** 2 + 2 * xx), xx)
    assert abs(area - math.sqrt(math.pi) * math.e) < 1e-6
    ax.fill_between(x, 0, g, color=LIGHT_BLUE, lw=0)
    ax.plot(x, g, color=BLUE, lw=2.0)
    ax.axvline(1, color=ORANGE, ls="--", lw=1.1)
    ax.plot(1, math.e, "o", color=ORANGE, ms=5)
    ax.text(1.1, math.e + 0.05, r"peak $e$ at $x=1$", color=ORANGE, fontsize=9)
    ax.text(-1.4, 2.85, r"$-x^2+2x=1-(x-1)^2$", fontsize=9.5)
    ax.text(2.1, 0.35, r"area $=\sqrt{\pi}\,e\approx4.818$", fontsize=9.5)
    ax.set_xlim(-1.5, 3.5)
    ax.set_ylim(0, 3.2)
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$e^{-x^2+2x}$")


# ---------- Ornstein-Uhlenbeck ----------

@figure("f09_ou_halflife", w=4.4, h=2.5)
def _(ax):
    kappa = 0.2
    t = np.linspace(0, 12, 300)
    d = np.exp(-kappa * t)  # (X_0 - mu) = 1
    th = math.log(2) / kappa
    assert abs(th - 3.4657) < 1e-3
    ax.plot(t, d, color=BLUE, lw=2.0)
    ax.axhline(0.5, color=GREY, ls="--", lw=1.0)
    ax.axvline(th, color=ORANGE, ls="--", lw=1.0)
    ax.plot(th, 0.5, "o", color=ORANGE, ms=5)
    ax.text(th + 0.25, 0.78, r"$t_{1/2}=\frac{\ln 2}{\kappa}\approx3.47$", color=ORANGE, fontsize=9.5)
    ax.text(7.0, 0.85, r"$E[X_t]-\mu=(X_0-\mu)\,e^{-\kappa t}$", fontsize=9.5)
    ax.text(7.0, 0.73, r"$\kappa=0.2$, $X_0-\mu=1$", fontsize=9, color=GREY)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 1.05)
    ax.set_xlabel(r"$t$ (years)")
    ax.set_ylabel(r"$E[X_t]-\mu$")


@figure("f09_ou_variance", w=4.4, h=2.6)
def _(ax):
    t = np.linspace(0, 30, 400)
    v_fast = (1 - np.exp(-2 * 0.2 * t)) / (2 * 0.2)
    v_slow = (1 - np.exp(-2 * 0.02 * t)) / (2 * 0.02)
    assert abs(1 / (2 * 0.2) - 2.5) < 1e-12
    ax.plot(t, t, color=GREY, ls="--", lw=1.2)
    ax.plot(t, v_slow, color=ORANGE, lw=2.0)
    ax.plot(t, v_fast, color=BLUE, lw=2.0)
    ax.axhline(2.5, color=BLUE, ls=":", lw=1.0)
    ax.text(12.0, 3.6, r"$\sigma^2/(2\kappa)=2.5$ ($\kappa=0.2$)", color=BLUE, fontsize=9)
    ax.text(14.0, 26.0, r"$\sigma^2 t$ (Brownian)", color=GREY, fontsize=9)
    ax.text(20.5, 7.5, r"$\kappa=0.02$", color=ORANGE, fontsize=9)
    ax.set_xlim(0, 30)
    ax.set_ylim(0, 31)
    ax.set_xlabel(r"$t$")
    ax.set_ylabel(r"$\mathrm{Var}\,X_t$  ($\sigma=1$, $X_0=0$)")


# ---------- Jensen and growth ----------

@figure("f09_jensen_chord", w=4.6, h=2.8)
def _(ax):
    x = np.linspace(0.5, 3.5, 300)
    ax.plot(x, 1 / x, color=GREY, lw=2.0)
    ax.plot([1, 3], [1, 1 / 3], color=BLUE, lw=1.6)
    ax.plot([1, 3], [1, 1 / 3], "o", color=BLUE, ms=5)
    chord2 = (1 + 1 / 3) / 2
    assert abs(chord2 - 2 / 3) < 1e-12
    ax.axvline(2, color=INK, ls=":", lw=0.9)
    ax.plot(2, chord2, "o", color=ORANGE, ms=6)
    ax.plot(2, 0.5, "o", color=GREEN, ms=6)
    ax.text(2.1, chord2 + 0.04, r"$E[1/X]=\frac{2}{3}$ (chord)", color=ORANGE, fontsize=9.5)
    ax.text(1.0, 0.8, r"$X=1$", fontsize=9, ha="center", color=BLUE)
    ax.text(3.0, 0.2, r"$X=3$", fontsize=9, ha="center", color=BLUE)
    ax.text(1.15, 0.3, r"$1/E[X]=\frac{1}{2}$ (curve)", color=GREEN, fontsize=9.5)
    ax.text(0.6, 1.9, r"$g(x)=\frac{1}{x}$ (convex)", color=GREY, fontsize=9.5)
    ax.set_xlim(0.5, 3.5)
    ax.set_ylim(0, 2.1)
    ax.set_xlabel(r"$x$")


@figure("f09_growth_p", w=4.6, h=2.7)
def _(ax):
    p = np.linspace(0, 1, 400)
    arith = 100 * (0.5 * p + (-0.4) * (1 - p))
    geo = 100 * (np.exp(p * math.log(1.5) + (1 - p) * math.log(0.6)) - 1)
    pstar = math.log(1 / 0.6) / (math.log(1.5) + math.log(1 / 0.6))
    assert abs(pstar - 0.5575) < 1e-4
    ax.axhline(0, color=INK, lw=0.8)
    ax.plot(p, arith, color=BLUE, lw=2.0)
    ax.plot(p, geo, color=ORANGE, lw=2.0)
    ax.axvline(pstar, color=GREY, ls="--", lw=1.0)
    for pp in (0.5, 0.6):
        a = 100 * (0.5 * pp - 0.4 * (1 - pp))
        g = 100 * (math.exp(pp * math.log(1.5) + (1 - pp) * math.log(0.6)) - 1)
        ax.plot([pp, pp], [g, a], color=GREY, lw=0.8)
        ax.plot(pp, a, "o", color=BLUE, ms=4)
        ax.plot(pp, g, "o", color=ORANGE, ms=4)
    ax.text(0.12, 14, "arithmetic (linear in $p$)", color=BLUE, fontsize=9, va="center")
    ax.text(0.3, -30, "geometric (concave)", color=ORANGE, fontsize=9, va="center")
    ax.text(pstar + 0.02, -41, r"$p\approx0.5575$", color=GREY, fontsize=9)
    box = dict(fc="white", ec="none", pad=1.0)
    ax.text(0.02, 52, r"$p=0.5$: arithmetic $+5\%$, geometric $-5.1\%$", fontsize=9, bbox=box)
    ax.text(0.02, 44, r"$p=0.6$: arithmetic $+14\%$, geometric $+4.0\%$", fontsize=9, bbox=box)
    ax.set_xlim(0, 1)
    ax.set_ylim(-45, 58)
    ax.set_xlabel(r"up-move probability $p$")
    ax.set_ylabel(r"per-period return (%)")


# ---------- heat equation ----------

@figure("f09_heat_spread", w=4.6, h=2.6)
def _(ax):
    D = 0.5
    x = np.linspace(-6, 6, 601)
    cols = [BLUE, GREY, ORANGE]
    for t, c in zip([0.5, 1.0, 2.0], cols):
        u = 1 / math.sqrt(4 * math.pi * D * t) * np.exp(-x ** 2 / (4 * D * t))
        mass = np.trapezoid(u, x)
        assert abs(mass - 1) < 1e-4
        ax.plot(x, u, color=c, lw=2.0, label=f"$t={t:g}$")
    ax.set_xlim(-6, 6)
    ax.set_ylim(0, 0.85)
    ax.legend(frameon=False, fontsize=9, loc="upper right")
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$u(x,t)$")
    ax.set_title(r"$u=\frac{1}{\sqrt{4\pi Dt}}\,e^{-x^2/(4Dt)}$, $D=\frac{1}{2}$, variance $2Dt=t$",
                 fontsize=9.5)


@figure("f09_heat_modes", w=4.6, h=2.6)
def _(ax):
    x = np.linspace(0, math.pi, 400)
    def u(t):
        return math.e ** (-t) * np.sin(x) + 3 * math.e ** (-9 * t) * np.sin(3 * x)
    assert np.allclose(u(0.0), np.sin(x) + 3 * np.sin(3 * x))
    for t, c in zip([0.0, 0.1, 0.5], [GREY, BLUE, ORANGE]):
        ax.plot(x, u(t), color=c, lw=2.0, label=f"$t={t:g}$")
    ax.axhline(0, color=INK, lw=0.7)
    ax.set_xlim(0, math.pi)
    ax.set_xticks([0, math.pi / 2, math.pi], ["0", r"$\frac{\pi}{2}$", r"$\pi$"])
    ax.set_ylim(-3.2, 3.6)
    ax.legend(frameon=False, fontsize=9, loc="lower left", ncol=3)
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$u(x,t)$")
    ax.set_title(r"$u_t=u_{xx}$ on $(0,\pi)$: mode $n$ decays as $e^{-n^2t}$", fontsize=9.5)


# ---------- finite differences ----------

@figure("f09_fd_amplification", w=4.6, h=2.6)
def _(ax):
    th = np.linspace(0, math.pi, 300)
    G = lambda r: 1 - 4 * r * np.sin(th / 2) ** 2
    assert abs(G(0.5)[-1] + 1) < 1e-12 and abs(G(0.6)[-1] + 1.4) < 1e-12
    ax.axhspan(-1, 1, color=LIGHT_GREEN, alpha=0.6, lw=0)
    ax.axhline(1, color=GREY, ls="--", lw=0.9)
    ax.axhline(-1, color=GREY, ls="--", lw=0.9)
    ax.axhline(0, color=INK, lw=0.6)
    ax.plot(th, G(0.5), color=BLUE, lw=2.0)
    ax.plot(th, G(0.6), color=RED, lw=2.0)
    ax.plot(math.pi, -1, "o", color=BLUE, ms=5)
    ax.plot(math.pi, -1.4, "o", color=RED, ms=5)
    ax.text(1.45, 0.62, r"$r=\frac{1}{2}$: $G(\pi)=-1$ (marginal)", color=BLUE, fontsize=9)
    ax.text(0.2, -1.35, r"$r=0.6$: $G(\pi)=-1.4$", color=RED, fontsize=9)
    ax.text(0.1, 1.12, r"$|G|\leq1$ band", color=GREEN, fontsize=9)
    ax.set_xticks([0, math.pi / 2, math.pi], ["0", r"$\frac{\pi}{2}$", r"$\pi$"])
    ax.set_xlim(0, math.pi)
    ax.set_ylim(-1.7, 1.35)
    ax.set_xlabel(r"grid angle $\theta$")
    ax.set_ylabel(r"$G(\theta)=1-4r\sin^2(\theta/2)$")


@figure("f09_stencil", w=5.2, h=2.5, axis=False)
def _(ax):
    frame(ax, -1.2, 9.4, -1.0, 3.5)
    r = 0.37
    fs = 9
    # explicit FTCS: the new value at (j, n+1) is built from three known values at t^n
    ex = {"-": (0.5, 0.0), "0": (1.7, 0.0), "+": (2.9, 0.0)}
    top_e = (1.7, 2.2)
    for k, lab in [("-", r"$j-1$"), ("0", r"$j$"), ("+", r"$j+1$")]:
        arrow(ax, ex[k], top_e, color=GREY, shrink=20, lw=1.0)
    for k, lab in [("-", r"$j-1$"), ("0", r"$j$"), ("+", r"$j+1$")]:
        node(ax, ex[k], lab, r=r, fs=fs, fc=LIGHT_BLUE, ec=BLUE)
    node(ax, top_e, r"$j$", r=r, fs=fs, fc=LIGHT_ORANGE, ec=ORANGE)
    ax.text(1.7, 3.05, "explicit (FTCS)", fontsize=fs, ha="center")
    ax.text(1.7, -0.65, "no solve", fontsize=fs, ha="center", color=GREY)
    # implicit backward Euler: three new values are coupled and solved together
    tp = {"-": (5.4, 2.2), "0": (6.6, 2.2), "+": (7.8, 2.2)}
    bot_i = (6.6, 0.0)
    ax.plot([5.4, 7.8], [2.2, 2.2], color=ORANGE, lw=1.0, zorder=1)
    arrow(ax, bot_i, tp["0"], color=GREY, shrink=20, lw=1.0)
    for k, lab in [("-", r"$j-1$"), ("0", r"$j$"), ("+", r"$j+1$")]:
        node(ax, tp[k], lab, r=r, fs=fs, fc=LIGHT_ORANGE, ec=ORANGE)
    node(ax, bot_i, r"$j$", r=r, fs=fs, fc=LIGHT_BLUE, ec=BLUE)
    ax.text(6.6, 3.05, "implicit (backward Euler)", fontsize=fs, ha="center")
    ax.text(6.6, -0.65, "tridiagonal solve", fontsize=fs, ha="center", color=ORANGE)
    # row labels shared by both panels
    ax.text(-0.9, 2.2, r"$t^{n+1}$", fontsize=fs, va="center", color=ORANGE)
    ax.text(-0.9, 0.0, r"$t^{n}$", fontsize=fs, va="center", color=BLUE)


# ---------- Monte Carlo ----------

@figure("f09_mc_halfwidth", w=4.6, h=2.8)
def _(ax):
    N = np.logspace(2, 7, 200)
    hw = 1.96 * np.sqrt(0.25 / N)
    assert abs(1.96 * math.sqrt(0.25 / 1e4) - 0.0098) < 1e-4
    assert abs(1.96 * math.sqrt(0.25 / 960400) - 0.001) < 1e-6
    ax.loglog(N, hw, color=BLUE, lw=2.0)
    ax.plot(1e4, 1.96 * math.sqrt(0.25 / 1e4), "o", color=ORANGE, ms=6)
    ax.plot(960400, 0.001, "o", color=GREEN, ms=6)
    ax.annotate(r"$N=10^4$: $\pm0.0098$", xy=(1e4, 0.0098), xytext=(2e2, 0.0012), fontsize=9,
                color=ORANGE, arrowprops=dict(arrowstyle="-", color=ORANGE, lw=1))
    ax.annotate(r"$\pm0.001$ needs $N\approx9.6\times10^5$", xy=(960400, 0.001),
                xytext=(3e4, 0.0003), fontsize=9, color=GREEN,
                arrowprops=dict(arrowstyle="-", color=GREEN, lw=1))
    ax.text(3e2, 0.09, r"slope $-\frac{1}{2}$", fontsize=9.5, color=INK)
    ax.set_xlim(1e2, 1e7)
    ax.set_ylim(2e-4, 0.2)
    ax.set_xlabel(r"samples $N$")
    ax.set_ylabel(r"95% half-width")
    ax.set_title(r"$p=\frac{1}{2}$: half-width $1.96\sqrt{p(1-p)/N}$", fontsize=9.5)


# ---------- variance reduction ----------

@figure("f09_antithetic_mono", w=4.4, h=2.5)
def _(ax):
    u = np.linspace(0, 1, 300)
    mean = math.e - 1
    ax.plot(u, np.exp(u), color=GREY, lw=2.0)
    ax.axhline(mean, color=INK, ls=":", lw=1.0)
    ax.text(0.02, mean + 0.06, r"$E[e^U]=e-1$", fontsize=9)
    f1, f2 = math.exp(0.1), math.exp(0.9)
    ax.plot([0.1, 0.9], [f1, f2], "o", color=BLUE, ms=6)
    ax.plot([0.1, 0.1], [mean, f1], color=BLUE, lw=1.2, ls="--")
    ax.plot([0.9, 0.9], [mean, f2], color=ORANGE, lw=1.2, ls="--")
    ax.text(0.12, f1 - 0.2, r"$f(0.1)$ below mean", color=BLUE, fontsize=9)
    ax.text(0.84, f2 + 0.12, r"$f(0.9)$ above", color=ORANGE, fontsize=9, ha="right")
    ax.set_xlim(0, 1)
    ax.set_ylim(0.9, 2.8)
    ax.set_xlabel(r"$u$")
    ax.set_ylabel(r"$f(u)=e^{u}$")
    ax.set_title("monotone $f$: partners land on opposite sides of the mean", fontsize=9.5)


@figure("f09_antithetic_sym", w=4.4, h=2.5)
def _(ax):
    u = np.linspace(0, 1, 300)
    ax.plot(u, (u - 0.5) ** 2, color=GREY, lw=2.0)
    ax.axhline(1 / 12, color=INK, ls=":", lw=1.0)
    ax.text(0.5, 1 / 12 + 0.02, r"$E[f]=\frac{1}{12}$", fontsize=9, ha="center")
    f = (0.1 - 0.5) ** 2
    assert abs(f - (0.9 - 0.5) ** 2) < 1e-12
    ax.plot([0.1, 0.9], [f, f], "o", color=BLUE, ms=6)
    ax.plot([0.1, 0.9], [f, f], color=BLUE, lw=1.0, ls="--")
    ax.text(0.5, f + 0.035, r"$f(0.1)=f(0.9)$", color=BLUE, fontsize=9, ha="center")
    ax.text(0.02, 0.285, r"$C=V$: second draw adds nothing", fontsize=9, color=INK, va="top")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 0.3)
    ax.set_xlabel(r"$u$")
    ax.set_ylabel(r"$f(u)=(u-\frac{1}{2})^2$")
    ax.set_title("symmetric about $\\frac{1}{2}$: $f(1-u)=f(u)$", fontsize=9.5)


@figure("f09_control_variate", w=4.6, h=2.6)
def _(ax):
    u = np.linspace(0, 1, 300)
    b = 12 * (1 - (math.e - 1) / 2)  # Cov(e^U,U)/Var U
    assert abs(b - 1.6906) < 1e-3
    line = (math.e - 1) + b * (u - 0.5)
    ax.fill_between(u, line, np.exp(u), color=LIGHT_BLUE, alpha=0.7, lw=0)
    ax.plot(u, np.exp(u), color=GREY, lw=2.0, label=r"$e^{u}$")
    ax.plot(u, line, color=BLUE, lw=1.6, ls="--", label=r"regression on $U$")
    ax.set_xlim(0, 1)
    ax.set_ylim(0.9, 2.8)
    ax.legend(frameon=False, fontsize=9, loc="lower right")
    ax.text(0.02, 2.75, r"$c^{*}=-12\left(1-\frac{e-1}{2}\right)\approx-1.690$", fontsize=9)
    ax.text(0.02, 2.55, r"$\rho^2\approx0.984$: residual variance $\approx1.6\%$", fontsize=9)
    ax.set_xlabel(r"$u$")
    ax.set_ylabel(r"$f(u)$")


# ---------- Gaussian conditioning ----------

def _cond_panel(ax, vy, cov, xlim, ylim, ycut):
    """Bivariate normal in (Y, X) coordinates with Var Y = vy, Var X = 1, Cov = cov."""
    vx = 1.0
    S = np.array([[vy, cov], [cov, vx]])
    Lc = np.linalg.cholesky(S)
    th = np.linspace(0, 2 * np.pi, 300)
    C = np.vstack([np.cos(th), np.sin(th)])
    for c, ls in [(1.0, "-"), (4.0, ":")]:
        P = Lc @ (math.sqrt(c) * C)
        ax.plot(P[0], P[1], color=GREY, lw=1.1, ls=ls)
    slope = cov / vy
    yy = np.linspace(xlim[0], xlim[1], 50)
    ax.plot(yy, slope * yy, color=BLUE, lw=1.8)
    m = slope * ycut
    sd = math.sqrt(vx - cov ** 2 / vy)
    ax.axvline(ycut, color=ORANGE, ls="--", lw=1.0)
    ax.plot([ycut, ycut], [m - sd, m + sd], color=ORANGE, lw=3.0, solid_capstyle="butt")
    ax.plot(ycut, m, "o", color=ORANGE, ms=6)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_xlabel(r"$Y$")
    ax.set_ylabel(r"$X$")
    return m, sd


@figure("f09_gauss_cond_rho", w=4.4, h=2.9)
def _(ax):
    m, sd = _cond_panel(ax, vy=1.0, cov=0.6, xlim=(-3.5, 3.5), ylim=(-3, 3), ycut=2.0)
    assert abs(m - 1.2) < 1e-12 and abs(sd ** 2 - 0.64) < 1e-12
    ax.text(-3.3, -2.6, r"$E[X\mid Y]=0.6\,Y$", color=BLUE, fontsize=9.5)
    ax.text(2.1, m - 0.45, r"$E[X\mid Y=2]=1.2$", color=ORANGE, fontsize=9.5)
    ax.text(-3.3, 2.5, r"$\mathrm{Var}(X\mid Y)=0.64$ (bar)", color=INK, fontsize=9)
    ax.set_title(r"$\rho=0.6$, standard margins", fontsize=9.5)


@figure("f09_gauss_cond_var4", w=4.4, h=2.9)
def _(ax):
    m, sd = _cond_panel(ax, vy=4.0, cov=1.2, xlim=(-5, 5), ylim=(-3, 3), ycut=2.0)
    assert abs(m - 0.6) < 1e-12 and abs(sd ** 2 - 0.64) < 1e-12
    ax.text(-4.8, -2.6, r"$E[X\mid Y]=0.3\,Y$", color=BLUE, fontsize=9.5)
    ax.text(2.35, m - 0.95, r"$E[X\mid Y=2]=0.6$", color=ORANGE, fontsize=9.5)
    ax.text(-4.8, 2.5, r"$\mathrm{Var}\,Y=4$, $\mathrm{Cov}=1.2$", color=INK, fontsize=9)
    ax.set_title(r"same $\rho=0.6$, $\mathrm{Var}\,Y=4$: slope $\frac{1.2}{4}$", fontsize=9.5)


# ---------- Newton ----------

@figure("f09_newton_tangents", w=4.6, h=2.8)
def _(ax):
    x = np.linspace(0.85, 1.75, 300)
    f = lambda z: z ** 2 - 2
    ax.plot(x, f(x), color=GREY, lw=2.0)
    ax.axhline(0, color=INK, lw=0.7)
    ax.plot([1.0, 1.5], [f(1.0), f(1.5)], "o", color=BLUE, ms=5)
    for x0, c in [(1.0, BLUE), (1.5, ORANGE)]:
        slope = 2 * x0
        x_zero = x0 - f(x0) / slope
        xs = np.linspace(x_zero - 0.05, x0 + 0.25, 50)
        ax.plot(xs, f(x0) + slope * (xs - x0), color=c, lw=1.3, ls="--")
        ax.plot(x_zero, 0, "o", color=c, ms=5)
    x1 = 1.5 - f(1.5) / 3.0  # tangent at 3/2 crosses zero at 17/12
    assert abs(x1 - 17 / 12) < 1e-12
    ax.plot(17 / 12, 0, "o", mfc="white", mec=GREEN, ms=6, mew=1.5)
    ax.plot(SQ2, 0, "x", color=GREEN, ms=8, mew=2)
    ax.text(1.0, -1.3, r"$x_0=1$", color=BLUE, fontsize=9, ha="center")
    ax.text(1.5, 0.42, r"$x_1=\frac{3}{2}$", color=ORANGE, fontsize=9, ha="center")
    ax.text(17 / 12, -0.42, r"$x_2=\frac{17}{12}$", color=GREEN, fontsize=9, ha="center")
    ax.set_xlim(0.85, 1.75)
    ax.set_ylim(-1.6, 1.3)
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$f(x)=x^2-2$")
    ax.set_title(r"tangent at $x_k$ crosses zero at $x_{k+1}$", fontsize=9.5)


# ---------- Taylor ----------

@figure("f09_taylor_error", w=4.4, h=2.6)
def _(ax):
    x = 0.1
    target = math.exp(x)
    n = np.arange(0, 6)
    sums = np.cumsum([x ** k / math.factorial(k) for k in n])
    err = np.abs(sums - target)
    logerr = np.log10(err)
    assert err[3] < 1e-5 and err[2] > 1e-5
    ax.plot(n, logerr, "o-", color=BLUE, lw=1.8, ms=5)
    ax.axhline(-5, color=GREEN, ls="--", lw=1.0)
    ax.text(0.1, -4.75, r"target $10^{-5}$", color=GREEN, fontsize=9)
    ax.plot(3, logerr[3], "o", color=ORANGE, ms=7)
    ax.annotate(r"$n=3$ (through $x^3/3!$): $4\times10^{-6}$", xy=(3, logerr[3]),
                xytext=(1.3, -0.9), fontsize=9, color=ORANGE,
                arrowprops=dict(arrowstyle="-", color=ORANGE, lw=1))
    ax.set_xticks(n)
    ax.set_xlim(-0.2, 5.2)
    ax.set_ylim(-8.8, 0.3)
    ax.set_xlabel(r"degree $n$ of partial sum")
    ax.set_ylabel(r"$\log_{10}\,|\mathrm{error}|$")
    ax.set_title(r"$e^{0.1}$: each term adds about $1.5$ digits", fontsize=9.5)


# ---------- binomial peak ----------

@figure("f09_binom_peak", w=4.6, h=2.6)
def _(ax):
    k = np.arange(35, 66)
    pmf = np.array([math.comb(100, j) / 2 ** 100 for j in k])
    peak = math.comb(100, 50) / 2 ** 100
    assert abs(peak - 0.0796) < 1e-4
    cols = [ORANGE if j == 50 else LIGHT_BLUE for j in k]
    ax.bar(k, pmf, width=0.85, color=cols, edgecolor=BLUE, lw=0.4)
    xx = np.linspace(35, 65, 300)
    normal = np.exp(-(xx - 50) ** 2 / (2 * 25)) / math.sqrt(2 * math.pi * 25)
    ax.plot(xx, normal, color=INK, lw=1.4)
    ax.axhline(1 / math.sqrt(50 * math.pi), color=GREY, ls=":", lw=1.0)
    ax.text(36, 0.0855, r"normal peak $\frac{1}{\sqrt{50\pi}}\approx0.0798$", fontsize=9)
    ax.annotate(r"$\binom{100}{50}2^{-100}\approx0.0796$", xy=(50, peak), xytext=(54.0, 0.066),
                fontsize=9, color=ORANGE, arrowprops=dict(arrowstyle="-", color=ORANGE, lw=1))
    ax.set_xlim(35, 65)
    ax.set_ylim(0, 0.095)
    ax.set_xlabel(r"heads $k$ in 100 fair flips")
    ax.set_ylabel(r"$P(k)$")


# ---------- extremal ----------

@figure("f09_x_to_x", w=4.2, h=2.5)
def _(ax):
    x = np.linspace(0.02, 1.8, 400)
    y = x ** x
    xm = 1 / math.e
    ym = math.exp(-1 / math.e)
    assert abs(ym - 0.6922) < 1e-4
    ax.plot(x, y, color=BLUE, lw=2.0)
    ax.plot(xm, ym, "o", color=ORANGE, ms=6)
    ax.axhline(ym, color=ORANGE, ls=":", lw=0.9)
    ax.annotate(r"min at $x=\frac{1}{e}$" "\n" r"$y=e^{-1/e}\approx0.6922$", xy=(xm, ym),
                xytext=(0.45, 1.75), fontsize=9.5, color=ORANGE,
                arrowprops=dict(arrowstyle="-", color=ORANGE, lw=1))
    ax.plot(1, 1, "o", color=GREY, ms=4)
    ax.text(1.0, 1.12, r"$1^1=1$", color=GREY, fontsize=9, ha="center")
    ax.set_xlim(0, 1.8)
    ax.set_ylim(0.55, 2.6)
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y=x^{x}$")
