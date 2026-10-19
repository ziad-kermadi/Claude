"""Figures for staging/gap_E.json (cointegration, GARCH, Kalman, AR(1)/OU)."""
import math
import numpy as np
from qcfig import *

@figure("fgE_spurious_paths", w=5.0, h=2.6)
def _(ax):
    rng = np.random.default_rng(11)
    T = 200
    t = np.arange(T)
    ax.plot(t, np.cumsum(rng.standard_normal(T)), color=BLUE, lw=1.4, label=r"$X_t$")
    ax.plot(t, np.cumsum(rng.standard_normal(T)), color=ORANGE, lw=1.4, label=r"$Y_t$")
    ax.axhline(0, color=GREY, lw=0.8)
    ax.set_xlabel("t"); ax.set_ylabel("level")
    ax.legend(frameon=False, fontsize=9, loc="upper left")
    ax.set_title("independent by construction, yet both wander", fontsize=10)

@figure("fgE_eg_cv", w=5.0, h=2.8)
def _(ax):
    rng = np.random.default_rng(12)
    R, T = 20000, 500
    x = np.cumsum(rng.standard_normal((R, T)), 1)
    y = np.cumsum(rng.standard_normal((R, T)), 1)
    xm = x.mean(1, keepdims=True); ym = y.mean(1, keepdims=True)
    b = ((x - xm) * (y - ym)).sum(1) / ((x - xm) ** 2).sum(1)
    a = ym[:, 0] - b * xm[:, 0]
    u = y - a[:, None] - b[:, None] * x                 # estimated residuals
    du = np.diff(u, axis=1); ul = u[:, :-1]
    g = (du * ul).sum(1) / (ul ** 2).sum(1)
    res = du - g[:, None] * ul
    tau = g / np.sqrt((res ** 2).sum(1) / (T - 3) / (ul ** 2).sum(1))
    edges = np.linspace(-6, 1.5, 76)
    counts, _ = np.histogram(tau, bins=edges, density=True)
    left = edges[:-1]
    w = np.diff(edges)
    ax.bar(left, counts, width=w, align="edge", color=np.where(left < -2.86, LIGHT_RED, LIGHT_BLUE),
           edgecolor="none")
    ax.axvline(-2.86, color=ORANGE, ls="--", lw=1.2)
    ax.axvline(-3.34, color=GREEN, ls="--", lw=1.2)
    frac = float(np.mean(tau < -2.86))
    ax.plot([], [], color=ORANGE, ls="--", lw=1.2, label=f"table $-2.86$: rejects {frac:.0%}")
    ax.plot([], [], color=GREEN, ls="--", lw=1.2, label="EG 5% cutoff $-3.34$")
    ax.legend(frameon=False, fontsize=8.5, loc="upper left")
    ax.set_xlabel(r"$\tau$ on estimated residuals ($T=500$, independent walks)")
    ax.set_ylabel("density")
    ax.set_title("residuals look stationary, so the test needs a further-left cutoff", fontsize=9.5)

@figure("fgE_ou_spread", w=5.0, h=2.7)
def _(ax):
    rng = np.random.default_rng(13)
    phi, sd_e = 0.98, 0.004
    sd_stat = sd_e / math.sqrt(1 - phi * phi)
    n = 300
    s = np.zeros(n)
    for t in range(1, n):
        s[t] = phi * s[t - 1] + sd_e * rng.standard_normal()
    t = np.arange(n)
    ax.plot(t, 100 * s, color=GREY, lw=1.1, label="simulated spread")
    ax.axhline(0, color=INK, lw=0.7)
    ax.axhline(2 * 100 * sd_stat, color=ORANGE, ls="--", lw=1.1, label=r"$\pm 2$ stationary sd")
    ax.axhline(-2 * 100 * sd_stat, color=ORANGE, ls="--", lw=1.1)
    k = np.arange(0, n)
    decay = 2 * 100 * sd_stat * phi ** k
    ax.plot(k, decay, color=BLUE, lw=1.8, label=r"expected decay from $+2$ sd")
    half = math.log(0.5) / math.log(phi)
    ax.axvline(half, color=BLUE, ls=":", lw=1.0)
    ax.text(half + 4, -2.6, f"half-life {half:.0f} d", fontsize=8.5, color=BLUE)
    ax.set_xlabel("trading days"); ax.set_ylabel("spread (%)")
    ax.legend(frameon=False, fontsize=8, loc="lower center", ncol=2)

@figure("fgE_garch_h_step", w=5.0, h=2.7)
def _(ax):
    om, al, be = 2e-6, 0.08, 0.90
    V = om / (1 - al - be)
    s0 = 4e-4
    k = np.arange(1, 61)
    garch = np.sqrt(V + (al + be) ** (k - 1) * (s0 - V))
    igarch = np.sqrt(s0 + (k - 1) * om)
    ax.plot(k, 100 * garch, color=BLUE, lw=1.8, label=r"GARCH: reverts to $\sqrt{V}$")
    ax.plot(k, 100 * igarch, color=RED, lw=1.5, ls="--", label=r"IGARCH: $\alpha+\beta=1$")
    ax.axhline(100 * math.sqrt(V), color=GREY, lw=1.0, ls=":")
    for kk in (1, 10, 30):
        ax.plot(kk, 100 * math.sqrt(V + (al + be) ** (kk - 1) * (s0 - V)), "o", color=BLUE, ms=4)
    ax.set_xlabel("horizon $k$ (days)"); ax.set_ylabel("forecast daily vol (%)")
    ax.set_ylim(0.9, 2.5)
    ax.legend(frameon=False, fontsize=8.5, loc="lower right")
    ax.set_title(r"$E_t[\sigma^2_{t+k}]$ from $\sigma^2_{t+1}=4\times10^{-4}$", fontsize=9.5)

@figure("fgE_normal_update", w=5.0, h=2.6)
def _(ax):
    x = np.linspace(-4, 6, 600)
    def pdf(z, m, v):
        return np.exp(-(z - m) ** 2 / (2 * v)) / math.sqrt(2 * math.pi * v)
    prior = pdf(x, 0.0, 4.0)
    like = pdf(x, 2.0, 1.0)          # N(y; x, R) as a function of x, with y = 2, R = 1
    post = pdf(x, 1.6, 0.8)
    ax.plot(x, prior, color=GREY, lw=1.4, label="prior $N(0,4)$")
    ax.plot(x, like, color=BLUE, lw=1.2, ls="--", label="likelihood $N(y;x,1)$, $y=2$")
    ax.plot(x, post, color=ORANGE, lw=1.9, label="posterior $N(1.6,\\,0.8)$")
    for m, c in [(0.0, GREY), (2.0, BLUE), (1.6, ORANGE)]:
        ax.axvline(m, color=c, lw=0.8, ls=":")
    ax.set_xlabel("x"); ax.set_ylabel("density")
    ax.legend(frameon=False, fontsize=8.5, loc="upper left")
    ax.set_title("posterior sits at the precision-weighted mean", fontsize=9.5)

@figure("fgE_gain_converge", w=5.0, h=2.6)
def _(ax):
    Q, R = 1.0, 4.0
    P = 10.0
    ks, gains = [], []
    for t in range(1, 31):
        p = P + Q
        K = p / (p + R)
        gains.append(K); ks.append(t)
        P = (1 - K) * p
    p_ss = (Q + math.sqrt(Q * Q + 4 * Q * R)) / 2
    K_ss = p_ss / (p_ss + R)
    ax.plot(ks, gains, "o-", color=BLUE, ms=3.5, lw=1.2, label=r"$K_t$ from $P_0=10$")
    ax.axhline(K_ss, color=GREEN, ls="--", lw=1.2, label=r"steady state $K\approx0.390$")
    for t, lab in [(1, r"$\frac{11}{15}$"), (2, r"$\frac{59}{119}$"), (3, r"$\frac{355}{831}$")]:
        ax.annotate(lab, (t, gains[t - 1]), textcoords="offset points", xytext=(6, 4), fontsize=8.5)
    ax.set_xlabel("update $t$"); ax.set_ylabel("gain $K_t$")
    ax.set_ylim(0.3, 0.85)
    ax.legend(frameon=False, fontsize=8.5, loc="upper right")

@figure("fgE_ewma_weights", w=5.0, h=2.6)
def _(ax):
    lags = np.arange(0, 21)
    for K, c, lab in [(0.06, ORANGE, r"$K=0.06$ ($\lambda=0.94$)"), (0.39, BLUE, r"$K=0.39$ ($\lambda=0.61$)")]:
        w = K * (1 - K) ** lags
        ax.bar(lags + (0.2 if K < 0.1 else -0.2), w, width=0.4, color=c, label=lab)
    ax.set_xlabel("lag $k$ (observations back)"); ax.set_ylabel(r"weight $K(1-K)^k$")
    ax.legend(frameon=False, fontsize=8.5, loc="upper right")
    ax.set_title("Kalman weights decay geometrically: an EWMA", fontsize=9.5)

@figure("fgE_hedge_path", w=5.0, h=2.8)
def _(ax):
    rng = np.random.default_rng(17)
    T = 250
    Q, Rn = 4e-4, 0.01
    beta = np.empty(T); beta[0] = 1.2
    for t in range(1, T):
        beta[t] = beta[t - 1] + math.sqrt(Q) * rng.standard_normal()
    x = 2.0 + 0.5 * rng.standard_normal(T)
    y = beta * x + math.sqrt(Rn) * rng.standard_normal(T)
    m, P = 1.2, 0.01
    est = np.empty(T); sd = np.empty(T)
    for t in range(T):
        Pm = P + Q
        K = Pm * x[t] / (x[t] ** 2 * Pm + Rn)
        m = m + K * (y[t] - x[t] * m)
        P = (1 - K * x[t]) * Pm
        est[t] = m; sd[t] = math.sqrt(P)
    beta_ols = float(np.sum(x * y) / np.sum(x * x))
    t = np.arange(T)
    ax.fill_between(t, est - 2 * sd, est + 2 * sd, color=LIGHT_BLUE, lw=0, label=r"Kalman $\pm 2$ sd")
    ax.plot(t, beta, color=GREY, lw=1.2, label=r"true $\beta_t$")
    ax.plot(t, est, color=BLUE, lw=1.6, label=r"Kalman $\hat\beta_t$")
    ax.axhline(beta_ols, color=ORANGE, ls="--", lw=1.2, label="static OLS")
    ax.set_xlabel("day"); ax.set_ylabel(r"hedge ratio $\beta$")
    ax.set_ylim(0.7, 1.45)
    ax.legend(frameon=False, fontsize=8, loc="upper left", ncol=2)
