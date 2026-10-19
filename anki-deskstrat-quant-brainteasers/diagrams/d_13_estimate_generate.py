"""Figures for cards/13_estimate_generate.json (estimate-first and invent-a-problem cards).

Figures show the bounds or limiting cases that bracket the exact answer on each estimate card.
Every number drawn is computed here and matches the card's stated result.
"""
import math
from math import comb
import numpy as np
from qcfig import *

EULER_GAMMA = 0.5772156649015329


def _phi(x):
    """Standard normal pdf, vectorised."""
    return np.exp(-0.5 * np.asarray(x, dtype=float) ** 2) / math.sqrt(2 * math.pi)


def _Phi(x):
    """Standard normal cdf, vectorised (math.erf per element; grids are small)."""
    x = np.asarray(x, dtype=float)
    return 0.5 * (1.0 + np.array([math.erf(v / math.sqrt(2.0)) for v in x.ravel()]).reshape(x.shape))


# ---------- 0, 27: birthday problem, bracketing bounds ----------

def _birthday_exact(n):
    p = 1.0
    for k in range(n):
        p *= (365 - k) / 365
    return 1 - p


@figure("f13_birthday_bounds", w=5.0, h=2.6)
def _(ax):
    n = np.arange(1, 61)
    pairs = n * (n - 1) / 2
    exact = np.array([_birthday_exact(m) for m in n])
    lower = 1 - np.exp(-pairs / 365)
    union = np.minimum(1.0, pairs / 365)
    ax.fill_between(n, lower, union, color=LIGHT_BLUE, lw=0, alpha=0.7)
    ax.plot(n, union, color=GREY, ls="--", lw=1.2, label=r"union bound $\frac{n(n-1)}{730}$")
    ax.plot(n, lower, color=GREEN, ls=":", lw=1.8, label="Poisson lower bound")
    ax.plot(n, exact, color=BLUE, lw=2.0, label="exact")
    for m, xy_text in ((23, (27, 0.22)), (50, (33, 0.66))):
        v = _birthday_exact(m)
        ax.plot(m, v, "o", color=ORANGE, ms=5, zorder=5)
        ax.annotate(f"n={m}: {v:.4f}", (m, v), xytext=xy_text, fontsize=9, color=ORANGE,
                    arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.8))
    ax.set_xlim(0, 60)
    ax.set_ylim(0, 1.05)
    ax.set_xlabel("people n")
    ax.set_ylabel("P(shared birthday)")
    ax.legend(loc="lower right", fontsize=9, frameon=False)


# ---------- 1, 37: harmonic numbers H_n with ln bounds ----------

@figure("f13_harmonic_bounds", w=5.0, h=2.5)
def _(ax):
    n = np.arange(1, 101)
    H = np.cumsum(1.0 / n)
    lo = np.log(n + 1)
    hi = 1 + np.log(n)
    ax.fill_between(n, lo, hi, color=LIGHT_BLUE, lw=0, alpha=0.7)
    ax.plot(n, hi, color=GREY, ls="--", lw=1.1, label=r"upper $1+\ln n$")
    ax.plot(n, lo, color=GREEN, ls=":", lw=1.6, label=r"lower $\ln(n+1)$")
    ax.plot(n, H, color=BLUE, lw=2.0, label=r"exact $H_n$")
    for m, xy_text in ((10, (14, 1.0)), (100, (68, 2.6))):
        v = H[m - 1]
        ax.plot(m, v, "o", color=ORANGE, ms=5, zorder=5)
        ax.annotate(f"$H_{{{m}}}={v:.3f}$", (m, v), xytext=xy_text, fontsize=9, color=ORANGE,
                    arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.8))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 5.9)
    ax.set_xlabel("n")
    ax.set_ylabel("harmonic sum")
    ax.legend(loc="upper left", fontsize=9, frameon=False)


# ---------- 5, 45: coupon collector n H_n with bounds ----------

@figure("f13_coupon_bounds", w=5.0, h=2.6)
def _(ax):
    n = np.arange(1, 13)
    H = np.cumsum(1.0 / np.arange(1, 13))
    exact = n * H
    lo = n * np.log(n + 1)
    hi = n * (1 + np.log(n))
    asym = n * np.log(n) + EULER_GAMMA * n
    ax.fill_between(n, lo, hi, color=LIGHT_BLUE, lw=0, alpha=0.7)
    ax.plot(n, hi, color=GREY, ls="--", lw=1.1, label=r"upper $n(1+\ln n)$")
    ax.plot(n, lo, color=GREEN, ls=":", lw=1.6, label=r"lower $n\ln(n+1)$")
    ax.plot(n, asym, color=GREY, ls="-.", lw=1.0, label=r"$n\ln n+\gamma n$")
    ax.plot(n, exact, color=BLUE, lw=2.0, label=r"exact $nH_n$")
    for m, xy_text in ((6, (7.0, 3.0)), (10, (7.3, 40.0))):
        v = exact[m - 1]
        ax.plot(m, v, "o", color=ORANGE, ms=5, zorder=5)
        ax.annotate(f"$n={m}$: {v:.2f}", (m, v), xytext=xy_text, fontsize=9, color=ORANGE,
                    arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.8))
    ax.set_xlim(0.5, 12.5)
    ax.set_ylim(0, 46)
    ax.set_xticks(range(1, 13))
    ax.set_xlabel("number of coupons n")
    ax.set_ylabel("expected draws")
    ax.legend(loc="upper left", fontsize=9, frameon=False)


# ---------- 2: expected maximum of n standard normals ----------

_Z = np.linspace(-9.0, 9.0, 6001)
_PHI_Z = _phi(_Z)
_CDF_Z = _Phi(_Z)


def _normal_max_mean(n):
    """E[max of n iid N(0,1)] = integral of x n phi(x) Phi(x)^(n-1) dx."""
    integrand = _Z * n * _PHI_Z * np.power(_CDF_Z, n - 1)
    return float(np.trapezoid(integrand, _Z))


@figure("f13_normal_max", w=5.0, h=2.6)
def _(ax):
    n = np.arange(2, 201)
    exact = np.array([_normal_max_mean(m) for m in n])
    upper = np.sqrt(2 * np.log(n))
    ballpark = upper - (np.log(np.log(n)) + np.log(4 * np.pi)) / (2 * upper)
    ax.plot(n, upper, color=GREY, ls="--", lw=1.2, label=r"Jensen upper bound $\sqrt{2\ln n}$")
    ax.plot(n, ballpark, color=GREEN, ls=":", lw=1.6, label="leading term minus correction")
    ax.plot(n, exact, color=BLUE, lw=2.0, label="exact")
    v = _normal_max_mean(100)
    ax.plot(100, v, "o", color=ORANGE, ms=5, zorder=5)
    ax.annotate(f"n=100: {v:.4f}", (100, v), xytext=(108, 3.3), fontsize=9, color=ORANGE,
                arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.8))
    ax.set_xlim(0, 200)
    ax.set_ylim(0, 3.6)
    ax.set_xlabel("number of variables n")
    ax.set_ylabel("E[max]")
    ax.legend(loc="lower right", fontsize=9, frameon=False)


# ---------- 4: ATM straddle as expected absolute move ----------

@figure("f13_straddle_bachelier", w=5.0, h=2.6)
def _(ax):
    # r=0, S=K=100, sigma*sqrt(T)=0.1 -> terminal sd 10. Straddle = E|S_T-100|.
    sd = 10.0
    s = np.linspace(60, 140, 4001)
    dens = _phi((s - 100) / sd) / sd
    g = np.abs(s - 100) * dens
    price = float(np.trapezoid(g, s))
    ax.fill_between(s, 0, g, color=LIGHT_ORANGE, lw=0)
    ax.plot(s, g, color=ORANGE, lw=1.8, label=r"$|S_T-100|\times$ density")
    ax.axvline(100, color=INK, lw=0.9, ls="--")
    be = price
    for x in (100 - be, 100 + be):
        ax.axvline(x, color=GREY, lw=0.9, ls=":")
    ax.text(100.8, 0.295, "strike 100", fontsize=9, color=INK, ha="left")
    ax.text(139, 0.17, f"breakeven\n100 +/- {be:.2f}", fontsize=9, color=GREY, ha="right")
    ax.text(62, 0.09, f"area = {price:.2f}", fontsize=9, color=ORANGE)
    ax.set_xlim(60, 140)
    ax.set_ylim(0, 0.33)
    ax.set_xlabel(r"terminal price $S_T$")
    ax.set_ylabel("payoff times density")
    ax.legend(loc="upper left", fontsize=9, frameon=False)


# ---------- 11: derangements, alternating partial sums ----------

@figure("f13_derange_partial", w=5.0, h=2.4)
def _(ax):
    terms = [(-1) ** j / math.factorial(j) for j in range(11)]
    S = np.cumsum(terms)
    k = np.arange(11)
    odd = k % 2 == 1
    exact = S[-1]
    ax.axhline(1 / math.e, color=GREEN, ls="--", lw=1.1)
    ax.plot(k[odd], S[odd], "o", color=BLUE, ms=6, label="odd k: lower bound")
    ax.plot(k[~odd], S[~odd], "o", color=ORANGE, ms=6, label="even k: upper bound")
    ax.plot(k, S, color=GREY, lw=0.8, zorder=1)
    ax.annotate(f"k=3: {S[3]:.4f} (lower)", (3, S[3]), xytext=(4.3, 0.12), fontsize=9, color=BLUE,
                arrowprops=dict(arrowstyle="-", color=BLUE, lw=0.8))
    ax.annotate(f"k=2: {S[2]:.4f} (upper)", (2, S[2]), xytext=(2.3, 0.92), fontsize=9, color=ORANGE,
                arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.8))
    ax.text(5.6, 0.27, f"limit 1/e = 0.36788", fontsize=9, color=GREEN)
    ax.set_xlim(-0.4, 10.4)
    ax.set_ylim(-0.05, 1.12)
    ax.set_xticks(range(11))
    ax.set_xlabel("terms kept: k (sum of j=0..k)")
    ax.set_ylabel("partial sum")
    ax.legend(loc="center right", fontsize=9, frameon=False)


# ---------- 13: maximum of 10 uniforms ----------

@figure("f13_uniform_max_cdf", w=4.6, h=2.6)
def _(ax):
    x = np.linspace(0, 1, 400)
    F = x ** 10
    mean = 10 / 11
    median = 0.5 ** (1 / 10)
    ax.fill_between(x, F, 1.0, color=LIGHT_BLUE, lw=0, alpha=0.8)
    ax.plot(x, F, color=BLUE, lw=2.0)
    ax.text(0.30, 0.22, r"$P(\max\leq x)=x^{10}$", fontsize=9, color=BLUE)
    ax.plot([0, median], [0.5, 0.5], color=ORANGE, ls="--", lw=1.0)
    ax.plot([median, median], [0, 0.5], color=ORANGE, ls="--", lw=1.0)
    ax.plot(median, 0.5, "o", color=ORANGE, ms=5, zorder=5)
    ax.text(median - 0.03, 0.07, f"median {median:.3f}", fontsize=9, color=ORANGE, ha="right")
    ax.text(0.30, 0.80, f"area above the curve\n= E[max] = 10/11 = {mean:.3f}", fontsize=9, color=INK)
    ax.set_xlim(0, 1.0)
    ax.set_ylim(0, 1.05)
    ax.set_xlabel("x")
    ax.set_ylabel("CDF of the maximum")


# ---------- 15: stick, piece containing the second point ----------

@figure("f13_stick_inspection", w=5.0, h=2.5)
def _(ax):
    L = np.linspace(0, 1, 401)
    h = L ** 2 + (1 - L) ** 2
    avg = float(np.trapezoid(h, L))
    ax.fill_between(L, 0, h, color=LIGHT_BLUE, lw=0, alpha=0.8)
    ax.plot(L, h, color=BLUE, lw=2.0, label=r"expected piece given L: $L^2+(1-L)^2$")
    ax.axhline(0.5, color=GREY, ls=":", lw=1.2, label="naive mean piece 1/2")
    ax.axhline(avg, color=ORANGE, ls="--", lw=1.2, label=f"average over L = {avg:.4f}")
    ax.annotate("L=0 or 1: 1", (0.01, 0.99), xytext=(0.08, 0.30), fontsize=9, color=BLUE,
                arrowprops=dict(arrowstyle="-", color=BLUE, lw=0.8))
    ax.annotate("L=1/2: 1/2", (0.5, 0.5), xytext=(0.58, 0.28), fontsize=9, color=BLUE,
                arrowprops=dict(arrowstyle="-", color=BLUE, lw=0.8))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.25)
    ax.set_xlabel("first cut L (uniform on [0,1])")
    ax.set_ylabel("expected piece length")
    ax.legend(loc="upper center", fontsize=9, frameon=False, ncol=1)


# ---------- 22: Brownian reflection principle ----------

BM_SEED = 134  # first-hit near t=0.44, endpoint W_1 near 0.09: a visible reflection


@figure("f13_bm_reflection", w=5.0, h=2.7)
def _(ax):
    N = 1000
    rng = np.random.default_rng(BM_SEED)
    W = np.concatenate([[0.0], np.cumsum(rng.normal(0.0, math.sqrt(1.0 / N), N))])
    t = np.linspace(0, 1, N + 1)
    tau = int(np.argmax(W >= 1.0))
    Wr = W.copy()
    Wr[tau:] = 2.0 - W[tau:]
    p_end = 1 - float(_Phi(np.array([1.0]))[0])
    ax.plot(t[: tau + 1], W[: tau + 1], color=BLUE, lw=1.6)
    ax.plot(t[tau:], W[tau:], color=BLUE, lw=1.6, label=r"path $W$")
    ax.plot(t[tau:], Wr[tau:], color=GREY, lw=1.3, ls="--", label=r"reflected after $\tau$: $2-W_t$")
    ax.axhline(1.0, color=GREEN, ls=":", lw=1.4)
    ax.plot(t[tau], 1.0, "o", color=ORANGE, ms=5, zorder=5)
    ax.annotate(r"first hit $\tau$", (t[tau], 1.0), xytext=(0.25, 1.6), fontsize=9, color=ORANGE,
                arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.8))
    ax.plot(1.0, W[-1], "o", color=BLUE, ms=5, zorder=5)
    ax.plot(1.0, Wr[-1], "o", mfc="white", mec=GREY, ms=5, zorder=5)
    ax.text(0.02, 2.45, r"$P(\max_{t\leq 1}W_t\geq 1)=2P(W_1\geq 1)=2(1-\Phi(1))=0.3173$", fontsize=9,
            ha="left", color=INK)
    ax.text(0.02, 1.04, "b = 1", fontsize=9, color=GREEN)
    ax.set_xlim(-0.02, 1.04)
    ax.set_ylim(-1.35, 2.7)
    ax.set_xlabel("time t")
    ax.set_ylabel("position")
    ax.legend(loc="lower left", fontsize=9, frameon=False)


# ---------- 10, 14: half-normal law of |W_1| = law of max; Jensen bound 1 ----------

@figure("f13_halfnormal_bounds", w=5.0, h=2.5)
def _(ax):
    xw = np.linspace(0, 8, 4001)
    dw = 2 * _phi(xw)
    mean = float(np.trapezoid(xw * dw, xw))
    rms = math.sqrt(float(np.trapezoid(xw ** 2 * dw, xw)))
    x = np.linspace(0, 3.2, 500)
    dens = 2 * _phi(x)
    ax.fill_between(x, 0, dens, color=LIGHT_BLUE, lw=0, alpha=0.8)
    ax.plot(x, dens, color=BLUE, lw=2.0, label=r"density of $|Z|$ (= law of $\max_{t\leq 1}W_t$)")
    ax.axvline(mean, color=ORANGE, lw=1.4, ls="--")
    ax.axvline(rms, color=GREY, lw=1.2, ls=":")
    ax.text(mean + 0.06, 0.62, f"E|Z| = {mean:.4f}", fontsize=9, color=ORANGE)
    ax.text(rms + 0.12, 0.40, f"$\\sqrt{{E[Z^2]}}={rms:.0f}$ (Jensen)", fontsize=9, color=GREY)
    ax.set_xlim(0, 3.2)
    ax.set_ylim(0, 0.9)
    ax.set_xlabel("x")
    ax.set_ylabel("density")
    ax.legend(loc="upper right", fontsize=9, frameon=False)


# ---------- 44: gambler's ruin with a small edge ----------

def _ruin(p, k=3, N=10):
    if abs(p - 0.5) < 1e-12:
        return k / N
    r = (1 - p) / p
    return (1 - r ** k) / (1 - r ** N)


@figure("f13_ruin_drift", w=5.0, h=2.5)
def _(ax):
    p = np.linspace(0.40, 0.60, 401)
    P = np.array([_ruin(v) for v in p])
    fair, tilt = _ruin(0.5), _ruin(0.52)
    ax.axhline(fair, color=GREY, ls=":", lw=1.2, label="fair answer k/N = 0.30 (lower bound for p at least 1/2)")
    ax.plot(p, P, color=BLUE, lw=2.0, label="P(hit 10 before 0), start 3")
    ax.plot(0.5, fair, "o", color=GREEN, ms=5, zorder=5)
    ax.plot(0.52, tilt, "o", color=ORANGE, ms=5, zorder=5)
    ax.annotate(f"p=0.52: {tilt:.4f}", (0.52, tilt), xytext=(0.535, 0.12), fontsize=9, color=ORANGE,
                arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.8))
    ax.annotate(f"p=1/2: {fair:.2f}", (0.5, fair), xytext=(0.43, 0.46), fontsize=9, color=GREEN,
                arrowprops=dict(arrowstyle="-", color=GREEN, lw=0.8))
    ax.set_xlim(0.40, 0.60)
    ax.set_ylim(0, 1.0)
    ax.set_xlabel("win probability p per round")
    ax.set_ylabel("P(hit 10 first)")
    ax.legend(loc="upper left", fontsize=9, frameon=False)


# ---------- 24: Kelly even-money bet, Jensen chord ----------

@figure("f13_kelly_jensen", w=5.0, h=2.6)
def _(ax):
    f, p = 0.10, 0.55
    x = np.linspace(-1.25, 1.25, 300)
    curve = np.log(1 + f * x)
    up, dn = math.log(1 + f), math.log(1 - f)
    mean_x = p - (1 - p)
    chord_at_mean = p * up + (1 - p) * dn
    jensen_at_mean = math.log(1 + f * mean_x)
    ax.plot(x, curve, color=GREY, lw=1.3, label=r"$\ln(1+fx)$, $f=0.1$")
    ax.plot([-1, 1], [dn, up], color=BLUE, lw=1.6, label="chord between the two outcomes")
    ax.plot([1], [up], "o", color=BLUE, ms=5, zorder=5)
    ax.plot([-1], [dn], "o", color=RED, ms=5, zorder=5)
    ax.annotate("win X=+1", (1, up), xytext=(0.62, -0.035), fontsize=9, color=BLUE,
                arrowprops=dict(arrowstyle="-", color=BLUE, lw=0.8))
    ax.annotate("loss X=-1", (-1, dn), xytext=(-1.2, -0.075), fontsize=9, color=RED,
                arrowprops=dict(arrowstyle="-", color=RED, lw=0.8))
    ax.plot([mean_x, mean_x], [chord_at_mean, jensen_at_mean], color=INK, lw=0.8, ls=":")
    ax.plot(mean_x, chord_at_mean, "o", color=ORANGE, ms=6, zorder=6)
    ax.plot(mean_x, jensen_at_mean, "o", color=GREY, ms=5, zorder=6)
    ax.annotate(f"E log = {chord_at_mean:.5f}", (mean_x, chord_at_mean), xytext=(0.25, -0.085), fontsize=9,
                color=ORANGE, arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.8))
    ax.annotate(f"log(1+f E X) = {jensen_at_mean:.5f}", (mean_x, jensen_at_mean), xytext=(0.15, 0.115),
                fontsize=9, color=GREY, arrowprops=dict(arrowstyle="-", color=GREY, lw=0.8))
    ax.axhline(0, color=GREY, lw=0.6)
    ax.set_xlim(-1.25, 1.25)
    ax.set_ylim(-0.13, 0.13)
    ax.set_xlabel("outcome x of the bet (X = +1 or -1)")
    ax.set_ylabel("log growth per round")
    ax.legend(loc="upper left", fontsize=9, frameon=False)


# ---------- 34: bond price, duration tangent versus exact price ----------

def _bond_price(y):
    t = np.arange(1, 11)
    return float(np.sum(5 / (1 + y) ** t) + 100 / (1 + y) ** 10)


@figure("f13_bond_convexity", w=5.0, h=2.5)
def _(ax):
    y0 = 0.05
    P0 = _bond_price(y0)
    t = np.arange(1, 11)
    moddur = float(np.sum(t * 5 / (1 + y0) ** (t + 1)) + 10 * 100 / (1 + y0) ** 11) / P0
    y = np.linspace(0.02, 0.09, 300)
    px = np.array([_bond_price(v) for v in y])
    lin = P0 - moddur * P0 * (y - y0)
    gap = px - lin
    gap6 = _bond_price(0.06) - (P0 - moddur * P0 * 0.01)
    ax.axhline(0, color=GREY, lw=0.8)
    ax.fill_between(100 * y, 0, gap, color=LIGHT_ORANGE, lw=0, alpha=0.8)
    ax.plot(100 * y, gap, color=ORANGE, lw=2.0)
    ax.plot(6, gap6, "o", color=ORANGE, ms=5, zorder=5)
    ax.annotate(f"at 6%: exact - linear = {gap6:.2f}",
                (6, gap6), xytext=(2.2, 4.6), fontsize=9, color=ORANGE,
                arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.8))
    ax.set_xlim(2, 9)
    ax.set_ylim(0, 6.5)
    ax.set_xlabel("yield (%)")
    ax.set_ylabel("exact minus duration\nestimate (price points)")


# ---------- 8: expected maximum of a simple walk, exact vs sqrt(2n/pi) ----------

def _walk_max_mean(n):
    k = np.arange(n + 1)
    w = np.array([comb(n, int(j)) for j in k], dtype=float) / 2.0 ** n
    e_abs = float(np.sum(np.abs(2 * k - n) * w))
    p_pos = float(np.sum(w[2 * k - n >= 1]))
    return e_abs - p_pos


@figure("f13_walk_max", w=5.0, h=2.5)
def _(ax):
    n = np.arange(1, 101)
    exact = np.array([_walk_max_mean(int(m)) for m in n])
    cont = np.sqrt(2 * n / math.pi)
    ax.plot(n, cont, color=GREY, ls="--", lw=1.2, label=r"continuous $\sqrt{2n/\pi}$")
    ax.plot(n, exact, color=BLUE, lw=2.0, label=r"exact $E|S_n|-P(S_n\geq 1)$")
    ax.plot(100, exact[-1], "o", color=ORANGE, ms=5, zorder=5)
    ax.plot(100, cont[-1], "o", color=GREY, ms=5, zorder=5)
    ax.annotate(f"exact {exact[-1]:.3f}", (100, exact[-1]), xytext=(60, 2.0), fontsize=9, color=ORANGE,
                arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.8))
    ax.annotate(f"continuous {cont[-1]:.3f}", (100, cont[-1]), xytext=(55, 8.8), fontsize=9, color=GREY,
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.8))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 10.5)
    ax.set_xlabel("steps n")
    ax.set_ylabel("E[max of walk]")
    ax.legend(loc="upper left", fontsize=9, frameon=False)


# ---------- 26: base rate, natural frequencies ----------

@figure("f13_base_rate_grid", w=5.0, h=2.2)
def _(ax):
    pop, prev, sens, fpr = 10000, 0.01, 0.99, 0.05
    sick = pop * prev
    tp = sick * sens
    fp = (pop - sick) * fpr
    pos = tp + fp
    ratio = tp / pos
    ax.barh(0, tp, height=0.9, color=LIGHT_BLUE, ec=BLUE, lw=1.2)
    ax.barh(0, fp, left=tp, height=0.9, color=LIGHT_RED, ec=RED, lw=1.2)
    ax.text(tp / 2, 0, f"{tp:.0f} true", ha="center", va="center", fontsize=9, color=INK)
    ax.text(tp + fp / 2, 0, f"{fp:.0f} false", ha="center", va="center", fontsize=9, color=INK)
    ax.text(0, 0.62, f"{pos:.0f} positive tests out of {pop:,} people", fontsize=9, color=INK)
    ax.text(0, -0.72, f"only {sick:.0f} of {pop:,} people are sick (1%), and {tp:.0f} of them test positive",
            fontsize=9, color=GREY)
    ax.set_xlim(-10, pos + 40)
    ax.set_ylim(-1.0, 1.0)
    ax.set_yticks([])
    ax.set_xticks([0, 100, 200, 300, 400, 500, 594])
    ax.set_xlabel(rf"P(sick $\mid$ +) $=\frac{{{tp:.0f}}}{{{pos:.0f}}}={ratio:.4f}\approx\frac{{1}}{{6}}$")
    ax.spines["left"].set_visible(False)


# ---------- 18: binomial tail, continuity correction ----------

@figure("f13_binomial_tail", w=5.0, h=2.6)
def _(ax):
    n = 100
    k = np.arange(25, 76)
    pmf = np.array([comb(n, int(j)) for j in k], dtype=float) / 2.0 ** n
    tail = (k <= 40) | (k >= 60)
    ax.bar(k[~tail], pmf[~tail], width=0.9, color=LIGHT_BLUE, ec="none")
    ax.bar(k[tail], pmf[tail], width=0.9, color=ORANGE, ec="none")
    x = np.linspace(25, 75, 500)
    ax.plot(x, _phi((x - 50) / 5) / 5, color=GREY, lw=1.4, label="normal, mean 50, sd 5")
    exact = float(pmf[tail].sum())
    cc = 2 * float(_Phi(np.array([-9.5 / 5]))[0])
    for c in (40.5, 59.5):
        ax.axvline(c, color=INK, ls=":", lw=0.9)
    ax.text(36.5, 0.03, f"P(H<=40)\n= {exact / 2:.4f}", fontsize=9, color=ORANGE, ha="center")
    ax.text(63.5, 0.03, f"P(H>=60)\n= {exact / 2:.4f}", fontsize=9, color=ORANGE, ha="center")
    ax.set_title(f"P(|H-50| >= 10): exact {exact:.4f}, normal + continuity {cc:.4f}",
                 fontsize=9, color=INK)
    ax.set_xlim(25, 75)
    ax.set_ylim(0, 0.105)
    ax.set_xlabel("heads H in 100 tosses")
    ax.set_ylabel("probability")
    ax.legend(loc="upper left", fontsize=9, frameon=False)


# ---------- 33: three random points on a circle, arcs on the simplex ----------

@figure("f13_acute_simplex", w=4.6, h=3.0, axis=False)
def _(ax):
    Va, Vb, Vc = np.array([0.5, math.sqrt(3) / 2]), np.array([0.0, 0.0]), np.array([1.0, 0.0])
    mab, mac, mbc = (Va + Vb) / 2, (Va + Vc) / 2, (Vb + Vc) / 2
    corner_a = [Va, mab, mac]
    corner_b = [Vb, mab, mbc]
    corner_c = [Vc, mac, mbc]
    centre = [mab, mbc, mac]
    for poly in (corner_a, corner_b, corner_c):
        ax.add_patch(Polygon(poly, closed=True, fc=LIGHT_RED, ec=RED, lw=1.0))
    ax.add_patch(Polygon(centre, closed=True, fc=LIGHT_BLUE, ec=BLUE, lw=1.2))
    ax.text(*(Va + np.array([0.0, -0.09])), "arc a > 1/2", ha="center", va="center", fontsize=9, color=INK)
    ax.text(*(Vb + np.array([0.27, 0.11])), "arc b > 1/2", ha="center", va="center", fontsize=9, color=INK)
    ax.text(*(Vc + np.array([-0.27, 0.11])), "arc c > 1/2", ha="center", va="center", fontsize=9, color=INK)
    cen = (mab + mbc + mac) / 3
    ax.text(*cen, "acute\n(area 1/4)", ha="center", va="center", fontsize=9, color=BLUE)
    ax.text(0.5, -0.2, "obtuse corners: total area 3/4 of the simplex", ha="center", fontsize=9, color=RED)
    ax.set_xlim(-0.12, 1.12)
    ax.set_ylim(-0.27, 0.98)
    ax.set_aspect("equal")
