"""Figures for cards/14_coding_numerics.json.

Only cards whose numerical behaviour a picture clarifies get a figure: MC error vs N,
QMC vs MC, sample paths with reflection, barrier-monitoring bias, Euler bias and
strong order, finite-difference V-shapes, Newton vs bisection, binomial-tree
oscillation, quadrature order, explicit-scheme stability, geometric probability,
a small Markov chain, a stopping rule and reservoir-sampling frequencies.
Every figure recomputes the numbers it shows and prints a line per check against
the value quoted on the card (the card is never edited).
"""
from fractions import Fraction
from math import comb
import numpy as np
from scipy.stats import norm, qmc
from qcfig import *


def _check(label, got, want, tol):
    flag = "ok" if abs(got - want) <= tol else "MISMATCH"
    print(f"  [{flag}] {label}: computed {got:.6g}, card {want:.6g}")


def _sci(x):
    return f"$10^{{{int(round(np.log10(x)))}}}$"


def _bs_call(S, K, T, r, sig):
    d1 = (np.log(S / K) + (r + 0.5 * sig**2) * T) / (sig * np.sqrt(T))
    d2 = d1 - sig * np.sqrt(T)
    return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)


def _bs_vega(S, K, T, r, sig):
    d1 = (np.log(S / K) + (r + 0.5 * sig**2) * T) / (sig * np.sqrt(T))
    return S * norm.pdf(d1) * np.sqrt(T)


def _crr_put(S, K, T, r, sig, n):
    """European put on a CRR tree (card 31 code, American branch not needed here)."""
    dt = T / n; u = np.exp(sig * np.sqrt(dt)); d = 1 / u
    p = (np.exp(r * dt) - d) / (u - d); disc = np.exp(-r * dt)
    j = np.arange(n + 1)
    V = np.maximum(K - S * u**(n - j) * d**j, 0)
    for _ in range(n):
        V = disc * (p * V[:-1] + (1 - p) * V[1:])
    return V[0]


# ---------------------------------------------------------------- card 0: MC error vs N
@figure("f14_mc_error_loglog", w=5.0, h=2.6)
def _(ax):
    p = 1 / 6                                    # P(U1+U2+U3 < 1)
    rng = np.random.default_rng(0)
    Ns = np.logspace(2, 6, 9).astype(int)
    rms = []
    for N in Ns:
        err = np.array([(rng.random((N, 3)).sum(axis=1) < 1).mean() - p for _ in range(20)])
        rms.append(np.sqrt(np.mean(err**2)))
    rms = np.array(rms)
    theo = np.sqrt(p * (1 - p) / Ns)
    _check("se at N=1e6 (card rounds to 2 s.f.)", theo[-1], 0.00037, 1e-5)
    ax.loglog(Ns, theo, color=GREY, ls="--", lw=1.4, label=r"$\sqrt{p(1-p)/N}$")
    ax.loglog(Ns, rms, "o", color=BLUE, ms=5, label="observed RMS error, 20 runs")
    ax.set_xlabel("number of draws $N$"); ax.set_ylabel("standard error of $\\hat p$")
    ax.set_title(r"$P(U_1+U_2+U_3<1)=\frac{1}{6}$: error falls as $1/\sqrt{N}$", fontsize=10)
    ax.legend(frameon=False, fontsize=9, loc="lower left")


# ---------------------------------------------------------------- card 63: QMC vs MC
@figure("f14_qmc_vs_mc", w=5.0, h=2.6)
def _(ax):
    d = 5
    exact = (np.e - 1)**d
    f = lambda x: np.exp(x.sum(axis=1))
    ms = np.arange(6, 15)
    mc, qm = [], []
    for m in ms:
        e1, e2 = [], []
        for s in range(20):
            rng = np.random.default_rng(s)
            e1.append(abs(f(rng.random((2**m, d))).mean() - exact))
            q = qmc.Sobol(d=d, scramble=True, seed=s).random_base2(m)
            e2.append(abs(f(q).mean() - exact))
        mc.append(np.mean(e1)); qm.append(np.mean(e2))
    mc, qm = np.array(mc), np.array(qm)
    _check("MC mean abs error at 2^14", mc[-1], 5.84e-2, 6e-4)
    _check("Sobol mean abs error at 2^14", qm[-1], 9.19e-5, 1e-6)
    N = 2.0**ms
    ax.loglog(N, mc, "o-", color=BLUE, ms=4, label="plain Monte Carlo")
    ax.loglog(N, qm, "s-", color=ORANGE, ms=4, label="scrambled Sobol")
    ax.loglog(N, mc[0] * np.sqrt(N[0] / N), color=GREY, ls="--", lw=1.2, label=r"slope $-\frac{1}{2}$")
    ax.set_xlabel("points $N=2^m$"); ax.set_ylabel("mean abs error, 20 seeds")
    ax.set_title(r"$\int_{[0,1]^5} e^{x_1+\dots+x_5}dx=(e-1)^5$", fontsize=10)
    ax.legend(frameon=False, fontsize=9, loc="lower left")


# ---------------------------------------------------------------- card 1: walk, reflection
@figure("f14_walk_reflection", w=5.0, h=2.6)
def _(ax):
    rng = np.random.default_rng(0)
    s = np.concatenate([[0], rng.choice([-1, 1], size=10).cumsum()])
    t = np.arange(len(s))
    tau = int(np.argmax(s >= 3))                 # first visit to +3
    refl = s.copy(); refl[tau:] = 6 - s[tau:]    # reflect the rest of the path about 3
    # exact P(M_10 >= 3) = P(S_10 >= 3) + P(S_10 > 3)
    p_ge = sum(comb(10, k) for k in range(11) if 2 * k - 10 >= 3) / 1024
    p_gt = sum(comb(10, k) for k in range(11) if 2 * k - 10 > 3) / 1024
    _check("P(max_10 >= 3)", p_ge + p_gt, 0.34375, 1e-9)
    ax.axhline(3, color=GREEN, ls=":", lw=1.3)
    ax.plot(t, s, "o-", color=BLUE, ms=4, label="sample path")
    ax.plot(t[tau:], refl[tau:], "o--", color=ORANGE, ms=3.5, lw=1.3, label="reflected after first hit")
    ax.plot(t[tau], 3, "o", color=GREEN, ms=8, zorder=5)
    ax.text(10.25, s[-1], f"$S_{{10}}={s[-1]}$", color=BLUE, va="center", fontsize=9)
    ax.text(10.25, refl[-1], f"${refl[-1]}$", color=ORANGE, va="center", fontsize=9)
    ax.text(6.2, 2.2, r"barrier $a=3$", color=GREEN, fontsize=9)
    ax.set_xlim(-0.4, 12.2); ax.set_ylim(-4.5, 10)
    ax.set_xticks(range(0, 11, 2)); ax.set_xlabel("step $n$"); ax.set_ylabel("$S_n$")
    ax.set_title(r"$P(M_{10}\geq 3)=P(S_{10}\geq 3)+P(S_{10}>3)=\frac{352}{1024}$", fontsize=10)
    ax.legend(frameon=False, fontsize=9, loc="lower left")


# ---------------------------------------------------------------- card 21: barrier monitoring
def _uoc_pair(m, n=200_000, seed=0):
    S0, K, B, T, r, sig = 100.0, 100.0, 120.0, 1.0, 0.05, 0.2
    rng = np.random.default_rng(seed)
    dt = T / m
    Z = rng.standard_normal((n, m))
    S = S0 * np.exp(np.cumsum((r - 0.5 * sig**2) * dt + sig * np.sqrt(dt) * Z, axis=1))
    pay = np.exp(-r * T) * np.maximum(S[:, -1] - K, 0)
    out = []
    for Bk in (B, B * np.exp(-0.5826 * sig * np.sqrt(dt))):
        x = np.where(S.max(axis=1) < Bk, pay, 0.0)
        out.append((x.mean(), x.std(ddof=1) / np.sqrt(n)))
    return out


@figure("f14_barrier_monitor", w=5.0, h=2.6)
def _(ax):
    ms = [4, 8, 13, 26, 52]
    plain, shift = [], []
    for m in ms:
        (a, sa), (b, sb) = _uoc_pair(m)
        plain.append((a, sa)); shift.append((b, sb))
    _check("up-and-out, m=52, no shift", plain[-1][0], 1.4958, 1.5e-4)
    _check("up-and-out, m=52, BGK shift", shift[-1][0], 1.1508, 1.5e-4)
    ms = np.array(ms)
    ax.errorbar(ms, [p[0] for p in plain], yerr=[p[1] for p in plain], fmt="o-", color=RED, ms=4,
                capsize=2, lw=1.2, label="discrete monitor, no shift")
    ax.errorbar(ms + 1.0, [p[0] for p in shift], yerr=[p[1] for p in shift], fmt="s-", color=BLUE, ms=4,
                capsize=2, lw=1.2, label=r"discrete monitor, barrier $B e^{-0.5826\sigma\sqrt{\Delta t}}$")
    ax.set_xlabel("monitoring dates $m$ (weekly at $m=52$)"); ax.set_ylabel("price")
    ax.set_xticks(ms)
    ax.set_title(r"up-and-out call, $B=120$, $S_0=K=100$: monitoring bias", fontsize=10)
    ax.legend(frameon=False, fontsize=9, loc="upper right")


# ---------------------------------------------------------------- card 19: Euler weak bias
@figure("f14_euler_weak_bias", w=5.0, h=2.5)
def _(ax):
    S0, mu, sig, T, n = 100.0, 0.5, 0.3, 1.0, 200_000
    rng = np.random.default_rng(9)

    def run(m):                                  # card 19 code, same stream order
        dW = np.sqrt(T / m) * rng.standard_normal((n, m))
        S = np.full(n, S0)
        for j in range(m):
            S = S * (1 + mu * (T / m) + sig * dW[:, j])
        exact = S0 * np.exp((mu - 0.5 * sig**2) * T + sig * dW.sum(axis=1))
        return (S - exact).mean()

    d5, d50 = run(5), run(50)
    _check("paired Euler-exact bias, m=5", d5, -3.82, 0.02)
    _check("paired Euler-exact bias, m=50", d50, -0.405, 0.02)
    ms = np.logspace(0, 2.3, 120)
    pred = lambda m: S0 * (1 + mu / m)**m        # E[S_T] under Euler is exact in expectation
    ax.semilogx(ms, pred(ms), color=BLUE, lw=1.6, label=r"Euler $S_0(1+\mu/m)^m$")
    ax.axhline(S0 * np.exp(mu), color=GREEN, ls="--", lw=1.2, label=r"exact $S_0e^{\mu T}=164.87$")
    ax.plot([5, 50], [pred(5), pred(50)], "o", color=ORANGE, ms=6, zorder=5)
    ax.annotate(f"m=5: bias {d5:+.2f}", (5, pred(5)), xytext=(7, 161.0), fontsize=9, color=ORANGE)
    ax.annotate(f"m=50: bias {d50:+.3f}", (50, pred(50)), xytext=(11, 165.6), fontsize=9, color=ORANGE)
    ax.set_ylim(156, 167); ax.set_yticks([158, 160, 162, 164, 166]); ax.set_xlabel("steps $m$"); ax.set_ylabel(r"$E[S_T]$")
    ax.set_title(r"Euler mean is biased at order $\Delta t$ ($\mu=0.5$, $T=1$)", fontsize=10)
    ax.legend(frameon=False, fontsize=9, loc="lower right")


# ---------------------------------------------------------------- card 20: strong order
@figure("f14_gbm_strong_order", w=5.0, h=2.7)
def _(ax):
    S0, mu, sig, T, n = 1.0, 0.1, 0.5, 1.0, 100_000
    rng = np.random.default_rng(10)
    res = {}
    for m in (10, 100, 20, 50, 200):             # card runs m=10 then m=100 on one stream
        dt = T / m
        dW = np.sqrt(dt) * rng.standard_normal((n, m))
        Se = np.full(n, S0); Sm = np.full(n, S0)
        for j in range(m):
            dw = dW[:, j]
            Se = Se + mu * Se * dt + sig * Se * dw
            Sm = Sm + mu * Sm * dt + sig * Sm * dw + 0.5 * sig**2 * Sm * (dw**2 - dt)
        exact = S0 * np.exp((mu - 0.5 * sig**2) * T + sig * dW.sum(axis=1))
        res[m] = (np.mean(np.abs(Se - exact)), np.mean(np.abs(Sm - exact)))
    _check("Euler err m=10", res[10][0], 0.0484, 5e-5)
    _check("Euler err m=100", res[100][0], 0.0155, 5e-5)
    _check("Milstein err m=10", res[10][1], 0.0053, 5e-5)
    _check("Milstein err m=100", res[100][1], 0.0006, 5e-5)
    ms = np.array(sorted(res))
    eu = np.array([res[m][0] for m in ms]); mi = np.array([res[m][1] for m in ms])
    ax.loglog(ms, eu, "o-", color=BLUE, ms=4, label="Euler")
    ax.loglog(ms, mi, "s-", color=ORANGE, ms=4, label="Milstein")
    ax.loglog(ms, eu[0] * np.sqrt(ms[0] / ms), color=BLUE, ls=":", lw=1.2, label=r"slope $-\frac{1}{2}$")
    ax.loglog(ms, mi[0] * (ms[0] / ms), color=ORANGE, ls=":", lw=1.2, label="slope $-1$")
    ax.set_xlabel("steps $m$"); ax.set_ylabel(r"mean $|S_T-\hat S_T|$")
    ax.set_title("GBM strong error on the same Brownian path", fontsize=10)
    ax.legend(frameon=False, fontsize=9, loc="lower left")


# ---------------------------------------------------------------- card 25 and 27: delta V-shape
@figure("f14_fd_delta", w=5.0, h=2.7)
def _(ax):
    S, K, T, r, sig = 100.0, 100.0, 1.0, 0.05, 0.2
    d1 = (np.log(S / K) + (r + 0.5 * sig**2) * T) / (sig * np.sqrt(T))
    exact = norm.cdf(d1)
    C0 = _bs_call(S, K, T, r, sig)
    hs = np.logspace(-12, -1, 45)
    cen = np.array([(_bs_call(S + h, K, T, r, sig) - _bs_call(S - h, K, T, r, sig)) / (2 * h) - exact for h in hs])
    fwd = np.array([(_bs_call(S + h, K, T, r, sig) - C0) / h - exact for h in hs])
    _check("central delta err h=1e-4", cen[np.argmin(abs(hs - 1e-4))], 6.1e-12, 1e-12)
    _check("forward delta err h=1e-6", fwd[np.argmin(abs(hs - 1e-6))], 1.2e-8, 1e-9)
    ac, af = np.maximum(np.abs(cen), 1e-17), np.maximum(np.abs(fwd), 1e-17)
    ic, iff = np.argmin(ac), np.argmin(af)
    ax.loglog(hs, ac, "o-", color=BLUE, ms=3, label="central difference")
    ax.loglog(hs, af, "s-", color=ORANGE, ms=3, label="forward difference")
    ax.loglog(hs, ac[np.argmin(abs(hs - 1e-3))] * (hs / 1e-3)**2, color=GREY, ls="--", lw=1.0,
              label=r"truncation $\propto h^2$ (central), $\propto h$ (forward)")
    ax.loglog(hs, af[np.argmin(abs(hs - 1e-2))] * (hs / 1e-2), color=GREY, ls="--", lw=1.0)
    ax.loglog(hs, 2.2e-16 * C0 / hs, color=GREY, ls=":", lw=1.2, label=r"round-off $\varepsilon C/h$")
    ax.set_xlabel("step $h$"); ax.set_ylabel(r"$|\hat\Delta-N(d_1)|$")
    ax.set_ylim(1e-13, 3e-1)
    ax.set_title(f"smallest grid error: {_sci(hs[ic])} central, {_sci(hs[iff])} forward", fontsize=10)
    ax.legend(frameon=False, fontsize=9, loc="upper right")


# ---------------------------------------------------------------- card 26: gamma V-shape
@figure("f14_fd_gamma", w=5.0, h=2.6)
def _(ax):
    S, K, T, r, sig = 100.0, 100.0, 1.0, 0.05, 0.2
    d1 = (np.log(S / K) + (r + 0.5 * sig**2) * T) / (sig * np.sqrt(T))
    exact = norm.pdf(d1) / (S * sig * np.sqrt(T))
    C0 = _bs_call(S, K, T, r, sig)
    hs = np.logspace(-7, -1, 37)
    err = np.array([(_bs_call(S + h, K, T, r, sig) - 2 * C0 + _bs_call(S - h, K, T, r, sig)) / h**2 - exact
                    for h in hs])
    for h, want in ((1e-4, -1.4e-7), (1e-5, -3.7e-6), (1e-6, 9.7e-3)):
        _check(f"gamma err h={h:.0e}", err[np.argmin(abs(hs - h))], want, 0.1 * abs(want))
    a = np.abs(err)
    ok = a > 0
    ia = np.argmin(np.where(ok, a, np.inf))
    ax.loglog(hs[ok], a[ok], "o-", color=GREEN, ms=3, label="second central difference")
    ax.loglog(hs, 4 * 2.2e-16 * C0 / hs**2, color=GREY, ls=":", lw=1.2,
              label=r"round-off $\approx 4\varepsilon C/h^2$")
    ax.loglog(hs, a[np.argmin(abs(hs - 1e-4))] * (hs / 1e-4)**2, color=GREY, ls="--", lw=1.0,
              label=r"truncation $\propto h^2$")
    ax.set_xlabel("step $h$"); ax.set_ylabel(r"$|\hat\Gamma-\Gamma|$")
    ax.set_ylim(1e-12, 10)
    ax.set_title(f"gamma: smallest grid error at {_sci(hs[ia])}, {a[ia]:.1e}", fontsize=10)
    ax.legend(frameon=False, fontsize=8.5, loc="upper right")


# ---------------------------------------------------------------- card 28 and 29: Newton vs bisection
@figure("f14_iv_newton_bisect", w=5.0, h=2.6)
def _(ax):
    S, K, T, r, sig_true = 100.0, 110.0, 0.5, 0.01, 0.25
    price = _bs_call(S, K, T, r, sig_true)
    _check("market price", price, 3.589239, 1e-6)
    sig, newt, k = 0.2, [abs(0.2 - sig_true)], 0
    while k < 50:
        diff = _bs_call(S, K, T, r, sig) - price
        if abs(diff) < 1e-10:
            break
        sig -= diff / _bs_vega(S, K, T, r, sig); k += 1
        newt.append(abs(sig - sig_true))
    _check("Newton iterations", k, 3, 0)
    lo, hi, kb, bis = 1e-6, 5.0, 0, [abs(2.5 - sig_true)]
    while hi - lo > 1e-10:
        mid = 0.5 * (lo + hi); kb += 1
        if _bs_call(S, K, T, r, mid) - price > 0:
            hi = mid
        else:
            lo = mid
        bis.append(abs(0.5 * (lo + hi) - sig_true))
    _check("bisection iterations", kb, 36, 0)
    ax.semilogy(range(len(newt)), np.maximum(newt, 1e-17), "o-", color=BLUE, ms=5, label=f"Newton, {k} steps")
    ax.semilogy(range(len(bis)), np.maximum(bis, 1e-17), "s-", color=ORANGE, ms=3, label=f"bisection, {kb} steps")
    kk = np.arange(kb + 1)
    ax.semilogy(kk, (5.0 - 1e-6) / 2.0**kk, color=GREY, ls="--", lw=1.1, label=r"bracket width $\propto 2^{-k}$")
    ax.set_ylim(1e-13, 10)
    ax.set_xlabel("iteration $k$"); ax.set_ylabel(r"$|\sigma_k-0.25|$")
    ax.set_title("implied vol from price 3.589239: Newton vs bisection", fontsize=10)
    ax.legend(frameon=False, fontsize=9, loc="upper right")


# ---------------------------------------------------------------- card 31: CRR oscillation
@figure("f14_crr_convergence", w=5.0, h=2.6)
def _(ax):
    S, K, T, r, sig = 100.0, 100.0, 1.0, 0.05, 0.2
    bs_put = _bs_call(S, K, T, r, sig) - S + K * np.exp(-r * T)
    _check("Black-Scholes put", bs_put, 5.5735, 5e-5)
    ns = np.arange(20, 501)
    pr = np.array([_crr_put(S, K, T, r, sig, n) for n in ns])
    _check("CRR European put n=500", pr[-1], 5.5695, 5e-5)
    ax.plot(ns, pr, "-", color=BLUE, lw=0.9, label="CRR European put")
    ax.axhline(bs_put, color=GREEN, ls="--", lw=1.2, label=f"Black-Scholes {bs_put:.4f}")
    ax.set_ylim(bs_put - 0.06, bs_put + 0.06)
    ax.set_xlabel("tree steps $n$"); ax.set_ylabel("put price")
    ax.set_title("CRR price oscillates about Black-Scholes as $n$ grows", fontsize=10)
    ax.legend(frameon=False, fontsize=9, loc="upper right")


# ---------------------------------------------------------------- card 46: quadrature order
@figure("f14_trap_simpson", w=5.0, h=2.6)
def _(ax):
    exact = np.e - 1
    def trap(n):
        x = np.linspace(0, 1, n + 1); y = np.exp(x); h = 1 / n
        return h * (y.sum() - 0.5 * (y[0] + y[-1]))
    def simp(n):
        x = np.linspace(0, 1, n + 1); y = np.exp(x); h = 1 / n
        return h / 3 * (y[0] + y[-1] + 4 * y[1:-1:2].sum() + 2 * y[2:-1:2].sum())
    ns = np.array([4, 8, 16, 32, 64, 128])
    et = np.array([abs(trap(n) - exact) for n in ns])
    es = np.array([abs(simp(n) - exact) for n in ns])
    _check("trapezoid err n=8", et[1], 2.24e-3, 5e-6)
    _check("Simpson err n=8", es[1], 2.33e-6, 1e-8)
    _check("Simpson ratio n=8->16 (card: 15.98 to 16.00)", es[1] / es[2], 15.99, 0.02)
    ax.loglog(ns, et, "o-", color=BLUE, ms=4, label="trapezoid")
    ax.loglog(ns, es, "s-", color=ORANGE, ms=4, label="Simpson")
    ax.loglog(ns, et[0] * (ns[0] / ns)**2, color=BLUE, ls=":", lw=1.2, label=r"slope $-2$")
    ax.loglog(ns, es[0] * (ns[0] / ns)**4, color=ORANGE, ls=":", lw=1.2, label=r"slope $-4$")
    ax.set_xlabel("intervals $n$"); ax.set_ylabel("abs error")
    ax.set_title(r"$\int_0^1 e^x\,dx$: error order $h^2$ vs $h^4$", fontsize=10)
    ax.legend(frameon=False, fontsize=9, loc="lower left")


# ---------------------------------------------------------------- card 44 and 45: stability
@figure("f14_ftcs_stability", w=5.0, h=2.5)
def _(ax):
    nx = 50; x = np.linspace(0, 1, nx + 1)
    final = {}
    for r, c, lab in ((0.4, BLUE, r"$r=0.4$ (stable)"), (0.6, RED, r"$r=0.6$ (unstable)")):
        u = np.sin(np.pi * x); amp = [np.abs(u).max()]
        for _ in range(200):
            u[1:-1] = u[1:-1] + r * (u[2:] - 2 * u[1:-1] + u[:-2])
            amp.append(np.abs(u).max())
        final[r] = amp[-1]
        ax.semilogy(range(len(amp)), amp, color=c, lw=1.4, label=lab)
    _check("r=0.6 max|u| after 200 steps", final[0.6], 1.7e12, 0.05e12)
    ax.set_xlabel("step $n$"); ax.set_ylabel(r"$\max_i |u_i^n|$")
    ax.set_title(r"explicit heat scheme, $u_t=u_{xx}$, $n_x=50$: stability needs $r\leq\frac{1}{2}$",
                 fontsize=9.5)
    ax.legend(frameon=False, fontsize=9, loc="upper left")


# ---------------------------------------------------------------- card 65: pi in the unit square
@figure("f14_pi_disc", w=4.2, h=3.1)
def _(ax):
    N = 10**6
    rng = np.random.default_rng(29)
    xy = rng.random((N, 2))
    inside = (xy**2).sum(axis=1) <= 1
    p = inside.mean()
    se = 4 * np.sqrt(p * (1 - p) / N)
    _check("pi estimate", 4 * p, 3.14098, 1e-5)
    _check("pi standard error", se, 0.00164, 1e-5)
    pts = xy[:2000]                              # the same stream: first 2000 of the 10^6 points
    ins = inside[:2000]
    ax.scatter(pts[ins, 0], pts[ins, 1], s=2.5, color=BLUE, lw=0)
    ax.scatter(pts[~ins, 0], pts[~ins, 1], s=2.5, color=GREY, lw=0)
    th = np.linspace(0, np.pi / 2, 200)
    ax.plot(np.cos(th), np.sin(th), color=ORANGE, lw=1.6)
    frame(ax, -0.02, 1.02, -0.02, 1.02)
    ax.set_xlabel("$x$"); ax.set_ylabel("$y$")
    ax.set_title(rf"$\hat\pi={4 * p:.5f}$, se $={se:.5f}$ ($N=10^6$)", fontsize=9.5)


# ---------------------------------------------------------------- card 9: HTH Markov chain
@figure("f14_hth_chain", w=5.0, h=2.5, axis=False)
def _(ax):
    Q = np.array([[0.5, 0.5, 0.0], [0.0, 0.5, 0.5], [0.5, 0.0, 0.0]])   # states '', H, HT
    E = np.linalg.solve(np.eye(3) - Q, np.ones(3))
    _check("E from empty", E[0], 10.0, 1e-9)
    _check("E from H", E[1], 8.0, 1e-9)
    _check("E from HT", E[2], 6.0, 1e-9)
    P = {"0": (0, 0), "H": (2.4, 0), "HT": (4.8, 0), "HTH": (4.8, -1.7)}
    node(ax, P["0"], r"$\emptyset$"); node(ax, P["H"], "H"); node(ax, P["HT"], "HT")
    node(ax, P["HTH"], "HTH", r=0.42, fc=LIGHT_GREEN, ec=GREEN)
    arrow(ax, P["0"], P["H"], "H  ½", color=BLUE, label_offset=(0, 0.32))
    arrow(ax, P["H"], P["HT"], "T  ½", color=RED, label_offset=(0, 0.32))
    arrow(ax, P["HT"], P["HTH"], "H  ½", color=BLUE, label_offset=(0.5, 0))
    arrow(ax, P["HT"], P["0"], "T  ½", color=RED, rad=-0.45, label_offset=(0, -0.05))
    self_loop(ax, P["0"], "T  ½", color=RED)
    self_loop(ax, P["H"], "H  ½", color=BLUE)
    frame(ax, -0.9, 6.0, -2.6, 1.2)
    caption(ax, r"$E_\emptyset=10,\; E_H=8,\; E_{HT}=6$ from $(I-Q)E=\mathbf{1}$, so $E[T_{\mathrm{HTH}}]=10$")


# ---------------------------------------------------------------- card 10: stopping rule
@figure("f14_die_threshold", w=5.0, h=2.4)
def _(ax):
    # V(0,x)=x; V(r,x)=max(x, E[V(r-1,Y)]) with Y uniform on 1..6 (exact fractions)
    V0 = {x: Fraction(x) for x in range(1, 7)}
    cont1 = sum(V0.values()) / 6                              # one reroll left
    V1 = {x: max(Fraction(x), cont1) for x in range(1, 7)}
    cont2 = sum(V1.values()) / 6                              # two rerolls left
    V2 = {x: max(Fraction(x), cont2) for x in range(1, 7)}
    start3 = sum(V2.values()) / 6
    _check("continuation, 2 left = 17/4", float(cont2), 4.25, 1e-12)
    _check("start value, 3 rolls = 14/3", float(start3), 14 / 3, 1e-12)
    xs = np.arange(1, 7)
    stop = [float(V2[x]) == x for x in xs]
    ax.bar(xs, xs, width=0.6, color=[BLUE if s else GREY for s in stop])
    ax.axhline(float(cont2), color=INK, ls="--", lw=1.2)
    ax.text(0.6, float(cont2) + 0.3, r"continue value $\frac{17}{4}$ (2 rerolls left)", fontsize=9)
    ax.set_xticks(xs); ax.set_xlabel("face $x$ on the roll"); ax.set_ylabel("payoff if stop")
    ax.set_ylim(0, 7)
    ax.set_title(r"stop iff $x\geq\frac{17}{4}$, so $x\in\{5,6\}$ (blue); $14/3$ overall", fontsize=10)


# ---------------------------------------------------------------- cards 51 and 52: reservoir
@figure("f14_reservoir_freq", w=5.0, h=2.4)
def _(ax):
    N = 100_000
    rng = np.random.default_rng(20)
    good = np.zeros(N, dtype=int)                 # card 51: 1-indexed, prob 1/i
    for i in range(1, 11):
        good[rng.integers(1, i + 1, size=N) == 1] = i - 1
    rng2 = np.random.default_rng(20)
    bad = np.zeros(N, dtype=int)                  # card 52: 0-indexed with prob 1/i
    for i in range(1, 10):
        bad[rng2.integers(0, i, size=N) == 0] = i
    fg = np.bincount(good, minlength=10) / N
    fb = np.bincount(bad, minlength=10) / N
    _check("buggy item 0 frequency", fb[0], 0.0, 0.0)
    print(f"  [info] correct freq range {fg.min():.4f}-{fg.max():.4f}; buggy items 1-9 "
          f"{fb[1:].min():.4f}-{fb[1:].max():.4f}")
    xs = np.arange(10)
    ax.bar(xs - 0.2, fg, width=0.4, color=BLUE, label="correct (card 51)")
    ax.bar(xs + 0.2, fb, width=0.4, color=RED, label="buggy (card 52)")
    ax.axhline(0.1, color=GREY, ls="--", lw=1.1)
    ax.set_xticks(xs); ax.set_xlabel("item"); ax.set_ylabel("frequency")
    ax.set_ylim(0, 0.16)
    ax.set_title("reservoir sampling of range(10), 100 000 runs: target 0.1", fontsize=10)
    ax.legend(frameon=False, fontsize=9, loc="upper right", ncol=2)
