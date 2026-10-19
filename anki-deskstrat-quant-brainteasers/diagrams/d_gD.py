"""Figures for the gap-fill cards in staging/gap_D.json (Bachelier, Dupire, convexity, quanto, Vasicek, copulas).

Every plotted number is computed here from the same formulas the cards use; staging/verify_gap_D.py checks them.
"""
import math
import numpy as np
from scipy.stats import norm, t as tdist, chi2
from scipy.special import owens_t
from scipy.integrate import quad
from qcfig import *


def _bach_atm_sigma(sig_ln, F, T):
    # normal vol with the same ATM Bachelier price as the Black vol sig_ln at forward F
    black_atm = F * (2 * norm.cdf(sig_ln * math.sqrt(T) / 2) - 1)
    return black_atm * math.sqrt(2 * math.pi) / math.sqrt(T)


def _phi2_eq(h, rho):
    # bivariate normal CDF Phi2(h,h;rho) by Owen (1956); accurate in the tail
    a = math.sqrt((1 - rho) / (1 + rho))
    return norm.cdf(h) - 2 * owens_t(h, a)


def _t4_cond(q, rho, nu=4):
    # P(U2<q | U1<q) for a t_nu copula via the chi-square mixture representation
    a = tdist.ppf(q, nu)
    f = lambda w: _phi2_eq(a * math.sqrt(w / nu), rho) * chi2.pdf(w, nu)
    return quad(f, 0, 400, points=[nu / a ** 2], limit=1000, epsabs=1e-16, epsrel=1e-11)[0] / q


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
    # short-dated smile linear in log-strike y = ln(K/F): implied vol = 0.20 - y (1 vol point per 1% log-strike)
    y = np.linspace(-0.06, 0.06, 241)
    imp = 0.20 - y
    loc = (0.20 - y) ** 2 / 0.20                # exact T -> 0 local vol: sigma^2 / (sigma - y sigma_y)
    ax.plot(y * 100, imp * 100, color=BLUE, lw=1.8, label="implied vol")
    ax.plot(y * 100, loc * 100, color=ORANGE, lw=1.8, label="local vol")
    ax.plot([2.0], [((0.20 - 0.02) ** 2 / 0.20) * 100], "o", color=ORANGE, ms=5)
    ax.set_xlabel("log-strike $\\ln(K/F)$, %")
    ax.set_ylabel("vol (%)")
    ax.legend(frameon=False, fontsize=9, loc="upper right")
    h = 1e-4
    sl_imp = ((0.20 - h) - (0.20 + h)) / (2 * h)
    sl_loc = ((0.20 - h) ** 2 / 0.20 - (0.20 + h) ** 2 / 0.20) / (2 * h)
    ax.set_title(rf"ATM slopes: local ${sl_loc:.0f}$ vs implied ${sl_imp:.0f}$ (per unit $\ln K$)", fontsize=10)


@figure("fgD_forward_vol", w=4.6, h=2.7)
def _(ax):
    T = np.linspace(0.02, 2.0, 199)              # step 0.01, so T=1 is a grid point
    sig = 0.20 + 0.05 * T                        # implied vol, flat in strike
    loc = np.sqrt((0.20 + 0.05 * T) ** 2 + 0.10 * T * (0.20 + 0.05 * T))   # sqrt(d(sigma^2 T)/dT), exact
    i1 = np.argmin(abs(T - 1.0))
    ax.plot(T, sig * 100, color=BLUE, lw=1.8,
            label=rf"implied $\sigma(1y)={sig[i1]*100:.0f}\%$")
    ax.plot(T, loc * 100, color=ORANGE, lw=1.8,
            label=rf"local (T=1) $=\sqrt{{\partial_T(\sigma^2T)}}={loc[i1]*100:.1f}\%$")
    ax.plot([T[i1]], [sig[i1] * 100], "o", color=BLUE, ms=5)
    ax.plot([T[i1]], [loc[i1] * 100], "o", color=ORANGE, ms=5)
    ax.set_xlabel("maturity T (years)")
    ax.set_ylabel("vol (%)")
    ax.set_ylim(18, 36)
    ax.legend(frameon=False, fontsize=8.5, loc="upper left")
    ax.set_title("flat smile, rising term structure: local vol is the forward vol", fontsize=9.5)


@figure("fgD_convexity_kappa", w=4.8, h=2.7)
def _(ax):
    sg, k = 0.01, 0.10
    T = np.linspace(0.1, 10, 300)
    hl = 0.5 * sg * sg * T ** 2 * 1e4                       # Ho-Lee, bp
    vs = sg * sg / (2 * k * k) * (1 - np.exp(-k * T)) ** 2 * 1e4   # Vasicek kappa=0.1, bp
    ax.plot(T, hl, color=RED, ls="--", lw=1.3, label=r"Ho-Lee $\frac{1}{2}\sigma^2T^2$")
    ax.plot(T, vs, color=BLUE, lw=1.8, label=r"Vasicek $\kappa=0.1$")
    i5 = np.argmin(abs(T - 5.0))
    ax.plot([T[i5]], [hl[i5]], "o", color=RED, ms=5)
    ax.plot([T[i5]], [vs[i5]], "o", color=BLUE, ms=5)
    ax.text(5.25, hl[i5] + 0.4, rf"${hl[i5]:.1f}$ bp", color=RED, fontsize=9)
    ax.text(5.25, vs[i5] - 1.4, rf"${vs[i5]:.2f}$ bp", color=BLUE, fontsize=9)
    ax.set_xlabel("futures expiry $T$ (years)")
    ax.set_ylabel("convexity (bp)")
    ax.legend(frameon=False, fontsize=8.5, loc="upper left")
    ax.set_title(r"growth stops: $\frac{\sigma^2}{2\kappa^2}(1-e^{-\kappa T})^2$ is bounded", fontsize=9.5)


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
    sd = math.sqrt(1 - rho * rho)
    # bivariate normal density with correlation rho
    dens = np.exp(-(X ** 2 - 2 * rho * X * Y + Y ** 2) / (2 * (1 - rho * rho))) / (2 * math.pi * sd)
    joint = _phi2_eq(c, rho)
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
    gq = np.array([_phi2_eq(norm.ppf(q), rho) / q for q in qs])
    tq = np.array([_t4_cond(q, rho, nu) for q in qs])
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
