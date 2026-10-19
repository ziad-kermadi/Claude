#!/usr/bin/env python3
"""Verify every numerical claim in staging/gap_D.json (gap batch D).

Card index = position in gap_D.json:
  0 B1 Bachelier ATM      1 B2 normal-vol toolkit   2 B3 negative-forward caplet
  3 D1 Dupire connect     4 D2 local skew 2x        5 D3 forward-vol perturbation
  6 C1 Ho-Lee convexity   7 C2 Vasicek convexity   8 C3 payment-timing identity
  9 Q1 quanto forward    10 Q2 quanto as Black      11 V1 Vasicek moments
 12 V2 Vasicek B(tau)    13 V3 rate sensitivity     14 G1 default correlation
 15 G2 tail dependence   16 G3 large-pool loss CDF
Exact values use closed forms / sympy / mpmath; probabilities and expectations
are also checked by Monte Carlo (>= 1e5 paths) with a printed standard error.
Run: python3 staging/verify_gap_D.py
"""
import math

import mpmath as mp
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.stats import multivariate_normal as mvn
from scipy.stats import multivariate_t as mvt
from scipy.stats import norm
from scipy.stats import t as tdist

RESULTS = []
RNG = np.random.default_rng(20260519)
mp.mp.dps = 60


def check(idx, label, claimed, computed, tol):
    ok = abs(float(claimed) - float(computed)) <= tol
    RESULTS.append(ok)
    print(f"card {idx:2d} [{label}] claimed={float(claimed):.6g} computed={float(computed):.6g} "
          f"tol={tol:g} {'PASS' if ok else 'FAIL'}")


def mc_line(idx, label, samples, claimed, n_sigmas=4.0):
    m = float(np.mean(samples))
    se = float(np.std(samples, ddof=1) / math.sqrt(len(samples)))
    ok = abs(m - claimed) <= n_sigmas * se
    RESULTS.append(ok)
    print(f"card {idx:2d} [{label}] MC mean={m:.6g} SE={se:.2g} n={len(samples)} "
          f"claimed={claimed:.6g} {'PASS' if ok else 'FAIL'}")


def N(x):
    return norm.cdf(x)


def dif(f, x, n=1):
    """Central-difference derivative in 60-digit arithmetic (explicit step, no sign flips)."""
    h = mp.mpf("1e-20") if n == 1 else mp.mpf("1e-12")
    return mp.diff(f, x, n, h=h)


def bs_black_call(F, K, sig, T, df=1.0):
    d1 = (math.log(F / K) + 0.5 * sig * sig * T) / (sig * math.sqrt(T))
    return df * (F * N(d1) - K * N(d1 - sig * math.sqrt(T)))


def bach_call(F, K, s, T):
    d = (F - K) / s
    return (F - K) * N(d) + s * norm.pdf(d)


# ---------- card 0: Bachelier ATM, F=2%, sigma_N=0.8%, T=1 ----------
def card0():
    F, sN, T = 0.02, 0.008, 1.0
    s = sN * math.sqrt(T)
    price = bach_call(F, F, s, T)
    check(0, "ATM Bachelier = sN*sqrt(T)/sqrt(2pi), in %", 0.31915, price * 100, 1e-4)
    # Monte Carlo of E[(F_T-K)^+] with F_T ~ N(F, s^2)
    x = RNG.normal(F, s, 200_000)
    mc_line(0, "ATM payoff E[(F_T-F)^+]", np.maximum(x - F, 0.0), price, 4.0)
    # Black lognormal vol with identical ATM price (exact root)
    target = price
    sL = brentq(lambda v: F * (2 * N(v * math.sqrt(T) / 2) - 1) - target, 1e-6, 3.0)
    check(0, "equivalent Black vol (%)", 40.27, sL * 100, 0.01)
    check(0, "first-order sN/F (%)", 40.0, sN / F * 100, 1e-9)
    # ATM Bachelier price as a fraction of one standard deviation
    check(0, "price / (sN sqrt T) = phi(0)", 0.398942, price / s, 1e-5)


# ---------- card 1: toolkit, sigma_N/F rule at F=0.5% ----------
def card1():
    check(1, "lognormal equivalent of sN=0.8% at F=0.5% (first order, %)", 160.0,
          0.008 / 0.005 * 100, 1e-9)


# ---------- card 2: Bachelier caplet at strike 0, F=-0.2%, sigma_N from 25% Black at 1% ----------
def card2():
    T = 1.0
    sN = 0.01 * (2 * N(0.25 * math.sqrt(T) / 2) - 1) * math.sqrt(2 * math.pi) / math.sqrt(T)
    check(2, "sigma_N equivalent to 25% Black at 1% (%)", 0.2494, sN * 100, 1e-4)
    s = sN * math.sqrt(T)
    Fn, K = -0.002, 0.0
    price = bach_call(Fn, K, s, T)
    check(2, "Bachelier caplet value (bp)", 2.99, price * 1e4, 0.01)
    check(2, "d = (F-K)/s", -0.802, (Fn - K) / s, 5e-4)
    check(2, "P(F_T>0) = N(F/s)", 0.2113, N(Fn / s), 5e-4)
    x = RNG.normal(Fn, s, 200_000)
    mc_line(2, "caplet payoff at 0 strike", np.maximum(x - K, 0.0), price, 4.0)


# ---------- card 3: Dupire forward equation from Fokker-Planck (sympy check on BS call) ----------
def card3():
    K, T, r, sg = sp.symbols("K T r sigma", positive=True)
    S0 = sp.Symbol("S0", positive=True)
    d1 = (sp.log(S0 / K) + (r + sg**2 / 2) * T) / (sg * sp.sqrt(T))
    d2 = d1 - sg * sp.sqrt(T)
    Nc = lambda z: (1 + sp.erf(z / sp.sqrt(2))) / 2
    C = S0 * Nc(d1) - K * sp.exp(-r * T) * Nc(d2)
    # Dupire forward equation: dC/dT = 1/2 sigma^2 K^2 C_KK - r K C_K
    residual = sp.diff(C, T) - (sg**2 * K**2 / 2 * sp.diff(C, K, 2) - r * K * sp.diff(C, K))
    vals = {S0: 100, K: 113, T: sp.Rational(7, 3), r: sp.Rational(3, 100), sg: sp.Rational(23, 100)}
    res = float(sp.N(residual.subs(vals), 30))
    check(3, "Dupire forward eq residual on BS call (sympy)", 0.0, res, 1e-15)


# ---------- card 4: local vol skew for sigma_imp(m)=0.20-m at K=102 (T -> 0) ----------
def card4():
    # smile linear in LOG-strike: sigma(y) = 0.20 - y, y = ln(K/F), F = 100, zero rates
    def C(K, T):
        sig = mp.mpf("0.20") - mp.log(K / 100)
        d1 = (mp.log(mp.mpf(100) / K) + sig * sig * T / 2) / (sig * mp.sqrt(T))
        d2 = d1 - sig * mp.sqrt(T)
        Nm = lambda z: mp.erfc(-z / mp.sqrt(2)) / 2      # erfc keeps the far tail exact
        return 100 * Nm(d1) - K * Nm(d2)

    T0 = mp.mpf("1e-6")

    def sloc_at_y(y):
        K = 100 * mp.exp(y)
        CT = dif(lambda t: C(K, t), T0)
        CKK = dif(lambda k: C(k, T0), K, 2)
        return mp.sqrt(2 * CT / (K * K * CKK))

    y_pt = mp.mpf("0.02")
    sloc = sloc_at_y(y_pt)
    check(4, "local vol at y=ln(K/F)=0.02 (T->0), exact Dupire", 0.162, sloc, 2e-5)
    check(4, "closed form (0.20-y)^2/0.20 at y=0.02", 0.162, 0.18**2 / 0.20, 1e-12)
    check(4, "linear approximation 0.20-2y (not exact)", 0.160, 0.20 - 2 * 0.02, 1e-12)
    h = mp.mpf("1e-4")
    skew_loc = (sloc_at_y(h) - sloc_at_y(-h)) / (2 * h)
    check(4, "local-vol skew d sigma_loc / dy at ATM", -2.0, skew_loc, 2e-3)


# ---------- card 5: forward vol, flat smile, sigma(T)=0.20+0.05T ----------
def card5():
    def w(t):
        return (0.20 + 0.05 * t) ** 2 * t
    h = 1e-6
    dw = (w(1 + h) - w(1 - h)) / (2 * h)
    check(5, "d(w)/dT at T=1", 0.0875, dw, 1e-7)
    check(5, "local vol at T=1 (%)", 29.58, math.sqrt(dw) * 100, 0.005)

    # Dupire with the full price surface, two strikes: must agree (flat in K => K-independent)
    def C(K, T):
        sig = mp.mpf("0.20") + mp.mpf("0.05") * T
        d1 = (mp.log(mp.mpf(100) / K) + sig * sig * T / 2) / (sig * mp.sqrt(T))
        d2 = d1 - sig * mp.sqrt(T)
        Nm = lambda z: (1 + mp.erf(z / mp.sqrt(2))) / 2
        return 100 * Nm(d1) - K * Nm(d2)
    for K in (100, 120):
        Km = mp.mpf(K)
        loc = mp.sqrt(2 * dif(lambda t: C(Km, t), mp.mpf(1)) / (Km * Km * dif(lambda k: C(k, mp.mpf(1)), Km, 2)))
        check(5, f"Dupire local vol at T=1, K={K}", 0.295804, loc, 1e-5)


# ---------- card 6: Ho-Lee futures convexity, sigma=1%, T=5 ----------
def card6():
    sg, f, T = 0.01, 0.04, 5.0
    check(6, "0.5 sigma^2 T^2 (bp)", 12.5, 0.5 * sg * sg * T * T * 1e4, 1e-9)
    check(6, "1y gap (bp)", 0.5, 0.5 * sg * sg * 1 * 1 * 1e4, 1e-9)
    check(6, "10y gap (bp)", 50.0, 0.5 * sg * sg * 100 * 1e4, 1e-9)
    # Monte Carlo under Ho-Lee: r_t = f + sigma^2 t^2/2 + sigma W_t
    n, steps = 100_000, 500
    dt = T / steps
    t_grid = np.linspace(0, T, steps + 1)
    drift = f + 0.5 * sg * sg * t_grid ** 2
    intW, rT, disc_int = [], [], []
    chunk = 20_000
    for _ in range(n // chunk):
        dW = RNG.normal(0, math.sqrt(dt), (chunk, steps))
        W = np.concatenate([np.zeros((chunk, 1)), np.cumsum(dW, axis=1)], axis=1)
        r = drift + sg * W
        rT.append(r[:, -1])
        disc_int.append(np.trapezoid(r, t_grid, axis=1))
        intW.append(np.trapezoid(W, t_grid, axis=1))
    rT = np.concatenate(rT)
    disc_int = np.concatenate(disc_int)
    # bond fit: E[exp(-int r)] must equal exp(-f T)
    disc = np.exp(-disc_int)
    mc_line(6, "Ho-Lee bond fit E[exp(-int r)] = exp(-fT)", disc, math.exp(-f * T), 4.0)
    cov = np.cov(rT, disc_int)[0, 1]
    se_cov = float(np.std(rT * disc_int) / math.sqrt(n))
    check(6, "Cov(r_T, int r) = sigma^2 T^2/2 (bp, MC)", 12.5, cov * 1e4, 3 * se_cov * 1e4 + 0.2)
    # forward recovered from futures-minus-convexity
    fwd_mc = rT.mean() - cov
    check(6, "E[r_T] - Cov = f(0,T) (MC, %)", f * 100, fwd_mc * 100, 3 * se_cov * 100 + 0.01)


# ---------- card 7: Vasicek futures convexity, kappa=0.1, sigma=1%, T=5 ----------
def card7():
    sg, f, T, k = 0.01, 0.04, 5.0, 0.10
    conv = sg * sg / (2 * k * k) * (1 - math.exp(-k * T)) ** 2
    check(7, "Vasicek convexity (bp)", 7.74, conv * 1e4, 0.01)
    check(7, "ratio to Ho-Lee", 0.62, conv / (0.5 * sg * sg * T * T), 0.005)
    # MC of x (OU, exact transitions), r = x + phi(t), phi(t) = f + sigma^2/(2k^2)(1-e^{-kt})^2
    n, steps = 100_000, 500
    dt = T / steps
    t_grid = np.linspace(0, T, steps + 1)
    phi = f + sg * sg / (2 * k * k) * (1 - np.exp(-k * t_grid)) ** 2
    e = math.exp(-k * dt)
    sd_step = sg * math.sqrt((1 - math.exp(-2 * k * dt)) / (2 * k))
    xT, intx = [], []
    chunk = 20_000
    for _ in range(n // chunk):
        x = np.zeros((chunk, steps + 1))
        z = RNG.normal(size=(chunk, steps))
        for j in range(steps):
            x[:, j + 1] = x[:, j] * e + sd_step * z[:, j]
        r = x + phi
        xT.append(x[:, -1])
        intx.append(np.trapezoid(x, t_grid, axis=1))
    xT = np.concatenate(xT)
    intx = np.concatenate(intx)
    rT = xT + phi[-1]
    cov = np.cov(xT, intx)[0, 1]
    se_cov = float(np.std(xT * intx) / math.sqrt(n))
    check(7, "Cov(x_T, int x) = sigma^2(1-e^{-kT})^2/(2k^2) (MC bp)", conv * 1e4,
          cov * 1e4, 3 * se_cov * 1e4 + 0.2)
    check(7, "E[r_T]-f(0,T) = phi(T)-f (bp)", conv * 1e4, (rT.mean() - f) * 1e4, 3 * float(np.std(rT) / math.sqrt(n)) * 1e4 + 0.2)
    # bond fit: E[exp(-int r)] with r = x + phi
    intr = intx + np.trapezoid(phi, t_grid)
    mc_line(7, "Vasicek bond fit E[exp(-int r)] = exp(-fT)", np.exp(-intr), math.exp(-f * T), 4.0)
    # the rate fitted to the curve: E[exp(-int r)] is e^{-fT} only with this phi(t)


# ---------- card 8: payment-timing identity under Ho-Lee (value of L(T1) paid at T2) ----------
def card8():
    sg, f = 0.01, 0.04
    T1, T2 = 2.0, 2.5
    tau = T2 - T1

    def P(t, T):
        return math.exp(-f * (T - t) - sg * sg * (T**3 - t**3) / 6
                        + sg * sg * (T - t) ** 3 / 6)

    # identity (exact): E[D(0,T2) * (1/P(T1,T2) - 1)] = P(0,T1) - P(0,T2)
    rhs = P(0, T1) - P(0, T2)
    n, steps = 100_000, 400
    dt = T2 / steps
    t_grid = np.linspace(0, T2, steps + 1)
    drift = f + 0.5 * sg * sg * t_grid ** 2
    vals = []
    chunk = 20_000
    for _ in range(n // chunk):
        dW = RNG.normal(0, math.sqrt(dt), (chunk, steps))
        W = np.concatenate([np.zeros((chunk, 1)), np.cumsum(dW, axis=1)], axis=1)
        r = drift + sg * W
        disc = np.exp(-np.trapezoid(r, t_grid, axis=1))
        WT1 = W[:, int(round(T1 / dt))]
        PT1T2 = np.exp(-f * tau - sg * sg * (T2**3 - T1**3) / 6 - sg * tau * WT1 + sg * sg * tau**3 / 6)
        vals.append(disc * (1 / PT1T2 - 1))
    vals = np.concatenate(vals)
    mc_line(8, "E[D(0,T2)(1/P(T1,T2)-1)] = P(0,T1)-P(0,T2)", vals, rhs, 4.0)


# ---------- card 9: quanto forward, S0=100, sS=25%, sX=10%, rho=0.5, rf=2%, T=2 ----------
def card9():
    S0, rf, rd, rho, sS, sX, T = 100.0, 0.02, 0.05, 0.5, 0.25, 0.10, 2.0
    mu = rf - rho * sS * sX
    FQ = S0 * math.exp(mu * T)
    check(9, "quanto forward 100 exp((rf-rho sS sX) T)", 101.51, FQ, 0.005)
    check(9, "drift under Q_d (per year)", 0.0075, mu, 1e-12)
    check(9, "no-correlation forward S0 e^{rf T}", 104.08, S0 * math.exp(rf * T), 0.005)
    # Monte Carlo: simulate (ln S, ln X) under Q_d
    n = 200_000
    cov = np.array([[sS * sS, rho * sS * sX], [rho * sS * sX, sX * sX]]) * T
    Z = RNG.multivariate_normal([0, 0], cov, n)
    ST = S0 * np.exp((rf - rho * sS * sX - 0.5 * sS * sS) * T + Z[:, 0])
    # the domestic value X*S must drift at rd: check E[X_T S_T]/(X0 S0) = e^{rd T}
    XT = 1.0 * np.exp((rd - rf - 0.5 * sX * sX) * T + Z[:, 1])
    mc_line(9, "E[S_T] under Q_d", ST, FQ, 4.0)
    mc_line(9, "E[X_T S_T]/(X0 S0) = e^{rd T}", XT * ST / S0, math.exp(rd * T), 4.0)


# ---------- card 10: quanto call as Black-76 with forward FQ, discount at rd ----------
def card10():
    S0, K, rf, rd, rho, sS, sX, T = 100.0, 100.0, 0.02, 0.05, 0.5, 0.25, 0.10, 1.0
    FQ = S0 * math.exp((rf - rho * sS * sX) * T)
    price = bs_black_call(FQ, K, sS, T, df=math.exp(-rd * T))
    check(10, "quanto call price per unit of X0 (T=1)", 9.86, price, 0.005)
    naive = bs_black_call(S0 * math.exp(rf * T), K, sS, T, df=math.exp(-rd * T))
    check(10, "same call with rho=0 (naive forward), per unit", 10.55, naive, 0.005)
    n = 200_000
    cov = np.array([[sS * sS, rho * sS * sX], [rho * sS * sX, sX * sX]]) * T
    Z = RNG.multivariate_normal([0, 0], cov, n)
    ST = S0 * np.exp((rf - rho * sS * sX - 0.5 * sS * sS) * T + Z[:, 0])
    payoff = np.exp(-rd * T) * np.maximum(ST - K, 0.0)
    mc_line(10, "quanto call MC (domestic discount)", payoff, price, 4.0)


# ---------- card 11: Vasicek moments, kappa=0.5, theta=3%, sigma=1%, r0=5%, T=2 ----------
def card11():
    k, th, sg, r0, T = 0.5, 0.03, 0.01, 0.05, 2.0
    mean = th + (r0 - th) * math.exp(-k * T)
    var = sg * sg * (1 - math.exp(-2 * k * T)) / (2 * k)
    check(11, "E[r_2] (%)", 3.736, mean * 100, 0.0005)
    check(11, "sd(r_2) (%)", 0.930, math.sqrt(var) * 100, 0.0005)
    check(11, "stationary sd sigma/sqrt(2k) (%)", 1.0, sg / math.sqrt(2 * k) * 100, 1e-12)
    check(11, "half-life ln2/k (years)", 1.386, math.log(2) / k, 0.001)
    # exact MC of the OU transition
    n, steps = 200_000, 200
    dt = T / steps
    x = np.full(n, r0 - th)
    e = math.exp(-k * dt)
    sd_step = sg * math.sqrt((1 - math.exp(-2 * k * dt)) / (2 * k))
    for _ in range(steps):
        x = x * e + sd_step * RNG.normal(size=n)
    rT = x + th
    mc_line(11, "MC E[r_2] (%)", rT * 100, mean * 100, 4.0)
    check(11, "MC sd(r_2) (%) vs closed form", math.sqrt(var) * 100, float(np.std(rT) * 100), 0.01)


# ---------- card 12: Vasicek B(tau) from the Riccati ODE B' + kB = 1 (sympy) ----------
def card12():
    k, tau, sg = sp.symbols("kappa tau sigma", positive=True)
    B = (1 - sp.exp(-k * tau)) / k
    ode = sp.simplify(sp.diff(B, tau) + k * B - 1)
    check(12, "B'+kB-1 = 0 (sympy)", 0.0, float(ode.subs({k: 0.3, tau: 1.7})), 1e-15)
    check(12, "B(0)=0 (sympy)", 0.0, float(B.subs(tau, 0)), 1e-15)
    # numerical check of the same ODE system (B, A) with the variance term
    kv, sv, th = 0.5, 0.01, 0.03

    def rhs(tau_, y):
        Bv, Av = y
        return [1 - kv * Bv, -kv * th * Bv + 0.5 * sv * sv * Bv * Bv]
    sol = solve_ivp(rhs, [0, 5.0], [0.0, 0.0], rtol=1e-11, atol=1e-13)
    check(12, "B(5) from ODE vs closed form (kappa=0.5)", (1 - math.exp(-2.5)) / 0.5,
          sol.y[0, -1], 1e-9)


# ---------- card 13: rate sensitivity B(5) at kappa=0.5, and B(30) at kappa=0.1 ----------
def card13():
    check(13, "B(5), kappa=0.5", 1.836, (1 - math.exp(-2.5)) / 0.5, 5e-4)
    check(13, "B(30), kappa=0.1 (years)", 9.502, (1 - math.exp(-3.0)) / 0.1, 5e-4)
    check(13, "saturation 1/kappa = 2", 2.0, 1 / 0.5, 1e-12)


# ---------- card 14: one-factor default correlation, p=2%, rho=0.3 ----------
def card14():
    p, rho = 0.02, 0.3
    c = norm.ppf(p)
    check(14, "c = Phi^{-1}(0.02)", -2.0537, c, 5e-5)
    joint = mvn(mean=[0, 0], cov=[[1, rho], [rho, 1]]).cdf([c, c])
    check(14, "P(D1 and D2) (%)", 0.1664, joint * 100, 5e-5)
    dcorr = (joint - p * p) / (p * (1 - p))
    check(14, "default correlation (%)", 6.45, dcorr * 100, 0.005)
    # Monte Carlo of the joint default probability
    n = 1_000_000
    M = RNG.normal(size=n)
    Z1 = RNG.normal(size=n)
    Z2 = RNG.normal(size=n)
    V1 = math.sqrt(rho) * M + math.sqrt(1 - rho) * Z1
    V2 = math.sqrt(rho) * M + math.sqrt(1 - rho) * Z2
    both = ((V1 < c) & (V2 < c)).astype(float)
    mc_line(14, "MC P(D1 and D2), n=1e6", both, joint, 4.0)


# ---------- card 15: tail dependence, Gaussian vs t4 (rho=0.3) ----------
def phi2_eq(h, rho):
    """Phi2(h,h;rho) by Owen (1956): Phi(h) - 2 T(h,a), a = sqrt((1-rho)/(1+rho)), h != 0."""
    from scipy.special import owens_t
    a = math.sqrt((1 - rho) / (1 + rho))
    return norm.cdf(h) - 2 * owens_t(h, a)


def card15():
    from scipy.integrate import quad
    from scipy.stats import chi2
    rho, nu = 0.3, 4
    lam = 2 * tdist.cdf(-math.sqrt((nu + 1) * (1 - rho) / (1 + rho)), nu + 1)
    check(15, "t4 copula tail dependence lambda", 0.162, lam, 5e-4)

    def gauss_cond(q):
        return phi2_eq(norm.ppf(q), rho) / q

    def t_cond(q):
        # X = Z / sqrt(W/nu), W ~ chi2_nu:  P(U1<q,U2<q) = E_W[Phi2(a sqrt(W/nu))], a = t_nu^{-1}(q)
        a = tdist.ppf(q, nu)
        f = lambda w: phi2_eq(a * math.sqrt(w / nu), rho) * chi2.pdf(w, nu)
        return quad(f, 0, 400, points=[nu / a ** 2], limit=1000, epsabs=1e-16, epsrel=1e-11)[0] / q

    check(15, "Gaussian conditional at q=0.1% (%)", 1.49, gauss_cond(1e-3) * 100, 0.005)
    check(15, "t4 conditional at q=1% (%)", 19.11, t_cond(1e-2) * 100, 0.01)
    check(15, "t4 conditional at q=0.1% (%)", 17.04, t_cond(1e-3) * 100, 0.01)
    check(15, "t4 conditional at q=0.01% (%) is close to lambda (tol 0.5pt)", lam * 100, t_cond(1e-4) * 100, 0.5)


# ---------- card 16: large-pool loss CDF, p=2%, rho=0.2 (correct vs candidate) ----------
def card16():
    p, rho = 0.02, 0.2
    c = norm.ppf(p)
    correct = norm.cdf((math.sqrt(1 - rho) * norm.ppf(0.02) - c) / math.sqrt(rho))
    candidate = norm.cdf((norm.ppf(0.02) - c) / math.sqrt(rho))
    check(16, "correct P(L<=2%) at rho=0.2", 0.686, correct, 5e-4)
    check(16, "candidate P(L<=2%) = 1/2 (wrong)", 0.5, candidate, 1e-12)
    # Monte Carlo: large pool loss = conditional PD given the factor M
    n = 400_000
    M = RNG.normal(size=n)
    L = norm.cdf((c - math.sqrt(rho) * M) / math.sqrt(1 - rho))
    mc_line(16, "E[L] = p (large pool)", L, p, 4.0)
    mc_line(16, "P(L<=2%) MC indicator", (L <= 0.02).astype(float), correct, 4.0)


def main():
    card0(); card1(); card2(); card3(); card4(); card5(); card6(); card7(); card8()
    card9(); card10(); card11(); card12(); card13(); card14(); card15(); card16()
    print(f"SUMMARY: {sum(RESULTS)}/{len(RESULTS)} PASS")


if __name__ == "__main__":
    main()
