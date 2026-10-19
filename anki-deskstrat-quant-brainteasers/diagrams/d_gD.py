"""Figures for the gap-fill cards in staging/gap_D.json (topics: Bachelier, Dupire, convexity, quanto, OU/Vasicek, copulas)."""
import math
import numpy as np
from scipy.stats import norm, t as tdist, multivariate_normal as mvn
from scipy.optimize import brentq
from scipy.integrate import quad
from qcfig import *


def _bach_atm_sigma(sig_ln, F, T):
    # normal vol with the same ATM Bachelier price as the Black vol sig_ln at forward F
    black_atm = F * (2 * norm.cdf(sig_ln * math.sqrt(T) / 2) - 1)
    return black_atm * math.sqrt(2 * math.pi) / math.sqrt(T)


@figure("fgD_bachelier_negative_forward", w=4.8, h=2.6)
def _(ax):
    F0, T = -0.002, 1.0
    sN = _bach_atm_sigma(0.25, 0.01, T)        # normal vol equal to a 25% Black vol at 1%
    s = sN * math.sqrt(T)
    x = np.linspace(-0.0075, 0.0055, 600)
    y = norm.pdf(x, F0, s)
    ax.fill_between(x * 100, 0, y, where=x < 0, color=LIGHT_RED, lw=0)
    ax.fill_between(x * 100, 0, y, where=x >= 0, color=LIGHT_BLUE, lw=0)
    ax.plot(x * 100, y, color=INK, lw=1.4)
    ax.axvline(0, color=RED, ls="--", lw=1.1)
    p_neg = norm.cdf(0, F0, s)
    ax.text(0.05, max(y) * 0.92, "F < 0: Black undefined", color=RED, fontsize=9)
    ax.text(0.08, max(y) * 0.72, "Bachelier: fine", color=BLUE, fontsize=9)
    ax.set_xlabel("forward rate at T (%)")
    ax.set_yticks([])
    ax.set_title(rf"$P(F_T<0)={p_neg:.2f}$ with $\sigma_N\sqrt{{T}}={s*100:.3f}\%$", fontsize=10)


@figure("fgD_skew_rule_two", w=4.8, h=2.8)
def _(ax):
    F, s0, b, T = 100.0, 0.20, -1.0, 1.0 / 12.0   # implied vol falls 1 vol point per 1% strike rise

    def smile(K):
        return s0 + b * (K - F) / F

    def Cfun(K, TT):
        sig = s0 + b * (K - F) / F
        d1 = (np.log(F / K) + 0.5 * sig * sig * TT) / (sig * math.sqrt(TT))
        return F * norm.cdf(d1) - K * norm.cdf(d1 - sig * math.sqrt(TT))

    def local_vol(K, hT=1e-5, hK=0.05):
        dT = (Cfun(K, T + hT) - Cfun(K, T - hT)) / (2 * hT)       # Dupire: dC/dT
        dKK = (Cfun(K + hK, T) - 2 * Cfun(K, T) + Cfun(K - hK, T)) / hK ** 2
        return math.sqrt(2 * dT / (K * K * dKK))

    Ks = np.linspace(93, 107, 57)
    imp = np.array([smile(K) for K in Ks]) * 100
    loc = np.array([local_vol(K) for K in Ks]) * 100
    ax.plot((Ks / F - 1) * 100, imp, color=BLUE, lw=1.8, label="implied vol")
    ax.plot((Ks / F - 1) * 100, loc, color=ORANGE, lw=1.8, label="local vol")
    ax.set_xlabel("strike, % from ATM")
    ax.set_ylabel("vol (%)")
    ax.legend(frameon=False, fontsize=9, loc="upper right")
    slope_imp = (smile(F + 0.5) - smile(F - 0.5)) / 1.0
    slope_loc = (local_vol(F + 0.5) - local_vol(F - 0.5)) / 1.0
    ax.set_title(rf"ATM skews: local ${slope_loc/slope_imp:.2f}\times$ implied (1 month)", fontsize=10)


@figure("fgD_jensen_chord", w=4.4, h=2.8)
def _(ax):
    xa, xb = 0.95, 1.10                     # two equally likely values of a bond-like P
    xs = np.linspace(0.90, 1.16, 200)
    ax.plot(xs, 1 / xs, color=INK, lw=1.6)
    ax.plot([xa, xb], [1 / xa, 1 / xb], color=ORANGE, lw=1.6)
    m = 0.5 * (xa + xb)
    Ej = 0.5 * (1 / xa + 1 / xb)
    ax.plot([xa, xb], [1 / xa, 1 / xb], "o", color=ORANGE, ms=4)
    ax.plot([m], [1 / m], "o", color=BLUE, ms=5)
    ax.plot([m], [Ej], "o", color=ORANGE, ms=5)
    ax.plot([m, m], [1 / m, Ej], color=GREY, ls=":", lw=1.1)
    ax.text(m - 0.03, 1 / m - 0.045, r"$1/E[P]$", color=BLUE, fontsize=10, ha="right")
    ax.text(m + 0.02, Ej + 0.035, r"$E[1/P]$ (on chord)", color=ORANGE, fontsize=10)
    ax.set_xlabel("P"); ax.set_ylabel("1/P")
    ax.set_title(r"$x\mapsto 1/x$ is convex: $E[1/P]\geq 1/E[P]$", fontsize=10)


@figure("fgD_ou_fan", w=4.8, h=2.7)
def _(ax):
    kap, th, sig, r0 = 0.5, 0.03, 0.01, 0.05
    t = np.linspace(0, 6, 300)
    m = th + (r0 - th) * np.exp(-kap * t)
    sd = sig * np.sqrt((1 - np.exp(-2 * kap * t)) / (2 * kap))
    ax.fill_between(t, (m - 2 * sd) * 100, (m + 2 * sd) * 100, color=LIGHT_BLUE, lw=0)
    ax.plot(t, m * 100, color=BLUE, lw=1.8)
    ax.axhline(th * 100, color=GREY, ls="--", lw=1)
    thalf = math.log(2) / kap
    ax.axvline(thalf, color=ORANGE, ls=":", lw=1.2)
    ax.text(thalf + 0.1, 5.4, rf"half-life $\ln 2/\kappa={thalf:.2f}$y", color=ORANGE, fontsize=9)
    ax.plot([0], [r0 * 100], "o", color=INK, ms=4)
    ax.text(0.1, 5.5 - 0.0, r"$r_0=5\%$", fontsize=9)
    ax.text(4.2, th * 100 + 0.25, r"$\theta=3\%$", fontsize=9, color=GREY)
    ax.set_xlabel("years"); ax.set_ylabel("rate (%)")
    ax.set_ylim(0, 6.5)
    ax.set_title(r"mean $\pm 2$ sd: band closes to $\pm 2\sigma/\sqrt{2\kappa}=\pm 2\%$", fontsize=10)


@figure("fgD_duration_saturation", w=4.6, h=2.7)
def _(ax):
    tau = np.linspace(0.01, 10, 400)
    B = lambda k: (1 - np.exp(-k * tau)) / k
    ax.plot(tau, B(0.5), color=BLUE, lw=1.8, label=r"Vasicek, $\kappa=0.5$")
    ax.plot(tau, B(0.1), color=GREY, lw=1.4, label=r"Vasicek, $\kappa=0.1$")
    ax.plot(tau, tau, color=RED, ls="--", lw=1.3, label=r"$\kappa\to 0$: $B=\tau$")
    ax.axhline(1 / 0.5, color=BLUE, ls=":", lw=1)
    ax.plot([5], [B(0.5)[np.argmin(abs(tau - 5))]], "o", color=BLUE, ms=5)
    ax.plot([5], [5], "o", color=RED, ms=5)
    ax.text(5.3, 1.05, rf"$B(5)={(1-math.exp(-2.5))/0.5:.3f}$", color=BLUE, fontsize=9)
    ax.text(3.6, 5.25, r"$B(5)=5$", color=RED, fontsize=9)
    ax.text(7.2, 2.15, r"$1/\kappa=2$", color=BLUE, fontsize=9)
    ax.set_xlabel(r"maturity $\tau$ (years)"); ax.set_ylabel(r"$B(\tau)$ (duration)")
    ax.legend(frameon=False, fontsize=8, loc="upper left")


@figure("fgD_default_region", w=4.4, h=3.5)
def _(ax):
    rho, p = 0.3, 0.02
    c = norm.ppf(p)
    g = np.linspace(-4, 4, 300)
    X, Y = np.meshgrid(g, g)
    pos = np.dstack([X, Y])
    dens = mvn(mean=[0, 0], cov=[[1, rho], [rho, 1]]).pdf(pos)
    joint = mvn(mean=[0, 0], cov=[[1, rho], [rho, 1]]).cdf([c, c])
    ax.add_patch(plt.Rectangle((-4, -4), c + 4, c + 4, color=LIGHT_RED, lw=0, zorder=0))
    ax.contour(X, Y, dens, levels=6, colors=GREY, linewidths=0.8)
    ax.axvline(c, color=RED, ls="--", lw=1)
    ax.axhline(c, color=RED, ls="--", lw=1)
    ax.text(-3.9, -3.7, f"both default\n{joint*100:.3f}%", color=RED, fontsize=8.5)
    ax.set_xlim(-4, 4); ax.set_ylim(-4, 4); ax.set_aspect("equal")
    ax.set_xlabel(r"$V_1$"); ax.set_ylabel(r"$V_2$")
    ax.set_title(rf"default if $V<c$, $c=\Phi^{{-1}}(0.02)={c:.3f}$, $\rho=0.3$", fontsize=9.5)


@figure("fgD_gauss_t_tail", w=4.8, h=2.8)
def _(ax):
    rho, nu = 0.3, 4
    qs = np.logspace(-4, math.log10(0.05), 40)

    def gauss_joint(a):
        f = lambda x: norm.pdf(x) * norm.cdf((a - rho * x) / math.sqrt(1 - rho * rho))
        return quad(f, -40, a, limit=500, epsabs=0, epsrel=1e-12)[0]

    def t_joint(a):
        def f(x):
            s = math.sqrt((nu + x * x) * (1 - rho * rho) / (nu + 1))
            return tdist.pdf(x, nu) * tdist.cdf((a - rho * x) / s, nu + 1)
        return quad(f, -200, a, limit=500, epsabs=0, epsrel=1e-12)[0]

    gq = np.array([gauss_joint(norm.ppf(q)) / q for q in qs])
    tq = np.array([t_joint(tdist.ppf(q, nu)) / q for q in qs])
    lam = 2 * tdist.cdf(-math.sqrt((nu + 1) * (1 - rho) / (1 + rho)), nu + 1)
    ax.semilogx(qs, gq, color=BLUE, lw=1.8, label="Gaussian copula")
    ax.semilogx(qs, tq, color=ORANGE, lw=1.8, label=r"$t_4$ copula")
    ax.axhline(lam, color=ORANGE, ls=":", lw=1)
    ax.text(1.2e-4, lam + 0.012, rf"$\lambda={lam:.3f}$", color=ORANGE, fontsize=9)
    ax.text(1.2e-4, 0.012, r"$\to 0$", color=BLUE, fontsize=9)
    ax.set_xlabel(r"$q$"); ax.set_ylabel(r"$P(U_2<q\mid U_1<q)$")
    ax.set_ylim(0, 0.27)
    ax.legend(frameon=False, fontsize=8.5, loc="upper left")


@figure("fgD_vasicek_loss_cdf", w=4.8, h=2.8)
def _(ax):
    p = 0.02
    c = norm.ppf(p)
    x = np.linspace(0.0005, 0.25, 400)
    for rho, col in [(0.05, GREY), (0.2, BLUE), (0.4, ORANGE)]:
        F = norm.cdf((math.sqrt(1 - rho) * norm.ppf(x) - c) / math.sqrt(rho))
        ax.plot(x * 100, F, color=col, lw=1.6, label=rf"$\rho={rho}$")
    ax.axvline(p * 100, color=RED, ls="--", lw=1)
    ax.text(p * 100 + 0.4, 0.2, r"$E[L]=p=2\%$", color=RED, fontsize=9)
    ax.set_xlabel("pool loss fraction $x$ (%)"); ax.set_ylabel(r"$P(L\leq x)$")
    ax.set_xlim(0, 25)
    ax.legend(frameon=False, fontsize=9, loc="lower right")
