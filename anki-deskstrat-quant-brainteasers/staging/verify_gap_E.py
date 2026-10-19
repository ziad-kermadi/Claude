"""Verify every numerical claim on staging/gap_E.json (cards 1-14, in file order).

Exact values use fractions/closed forms; probabilities, medians and quantiles of
simulated statistics use Monte Carlo with >= 1e5 replications (or >= 2e4 paths for
long-run moments), with standard errors printed. A claim PASSES when the claimed
(rounded) value lies within max(3 SE, half a unit in the last printed digit) of the
recomputed value; where a finite-sample effect is known the allowance is stated.
Run: python3 -I staging/verify_gap_E.py
"""
import math
from fractions import Fraction as F
import numpy as np

rng = np.random.default_rng(20261019)
rows = []

def chk(card, label, claimed, computed, se=0.0, half_unit=0.0, allow=0.0):
    tol = max(3.0 * se, half_unit) + allow
    ok = abs(claimed - computed) <= tol
    rows.append(ok)
    print(f"card {card:2d} | {label:44s} | claimed {claimed:>10.5g} | computed {computed:>10.5g} "
          f"| se {se:8.2g} | tol {tol:8.2g} | {'PASS' if ok else 'FAIL'}")

def ols_slope_t_r2_dw(y, x):
    """Per-row OLS of y on [1, x] with usual SE, R^2 and Durbin-Watson of residuals."""
    T = y.shape[1]
    xm = x.mean(1, keepdims=True); ym = y.mean(1, keepdims=True)
    sxx = ((x - xm) ** 2).sum(1)
    b = ((x - xm) * (y - ym)).sum(1) / sxx
    a = ym[:, 0] - b * xm[:, 0]
    res = y - a[:, None] - b[:, None] * x
    s2 = (res ** 2).sum(1) / (T - 2)
    t = b / np.sqrt(s2 / sxx)
    r2 = 1 - (res ** 2).sum(1) / ((y - ym) ** 2).sum(1)
    dw = (np.diff(res, axis=1) ** 2).sum(1) / (res ** 2).sum(1)
    return t, r2, dw

def eg_tau(y, x):
    """Engle-Granger residual test: OLS of y on [1,x], then no-constant ADF on residuals."""
    T = y.shape[1]
    xm = x.mean(1, keepdims=True); ym = y.mean(1, keepdims=True)
    b = ((x - xm) * (y - ym)).sum(1) / ((x - xm) ** 2).sum(1)
    a = ym[:, 0] - b * xm[:, 0]
    u = y - a[:, None] - b[:, None] * x
    du = np.diff(u, axis=1); ul = u[:, :-1]
    g = (du * ul).sum(1) / (ul ** 2).sum(1)
    res = du - g[:, None] * ul
    se = np.sqrt((res ** 2).sum(1) / (T - 3) / (ul ** 2).sum(1))
    return g / se

def df_const_tau(y):
    """ADF(0) with constant: t-stat on lagged level."""
    T = y.shape[1]
    dy = np.diff(y, axis=1); yl = y[:, :-1]
    X = np.stack([np.ones_like(yl), yl], 2)
    XtX = np.einsum('rti,rtj->rij', X, X); Xty = np.einsum('rti,rt->ri', X, dy)
    inv = np.linalg.inv(XtX); b = np.einsum('rij,rj->ri', inv, Xty)
    res = dy - np.einsum('rti,ri->rt', X, b)
    s2 = (res ** 2).sum(1) / (T - 1 - 2)
    return b[:, 1] / np.sqrt(inv[:, 1, 1] * s2)

def boot_quantile_se(v, q, B=200):
    n = len(v); qs = [np.quantile(v[rng.integers(0, n, n)], q) for _ in range(B)]
    return float(np.std(qs))

def ar1_paths(phi, R, n, burn=300, sig=1.0):
    x = np.zeros(R); out = np.empty((R, n))
    for t in range(burn + n):
        x = phi * x + sig * rng.standard_normal(R)
        if t >= burn:
            out[:, t - burn] = x
    return out

print("=== Card 1: spurious regression of independent random walks, T=200 ===")
ts, r2s, dws = [], [], []
for _ in range(10):
    x = np.cumsum(rng.standard_normal((10000, 200)), 1)
    y = np.cumsum(rng.standard_normal((10000, 200)), 1)
    t, r2, dw = ols_slope_t_r2_dw(y, x)
    ts.append(t); r2s.append(r2); dws.append(dw)
t = np.concatenate(ts); r2 = np.concatenate(r2s); dw = np.concatenate(dws)
N = len(t); p = np.mean(np.abs(t) > 1.96)
chk(1, "P(|t|>1.96), T=200, N=1e5", 0.83, p, se=math.sqrt(p * (1 - p) / N), half_unit=0.005)
chk(1, "median R^2, T=200", 0.17, float(np.median(r2)), se=0.001, half_unit=0.005)
chk(1, "median Durbin-Watson, T=200", 0.08, float(np.median(dw)), se=0.001, half_unit=0.005)

print("=== Card 2: Engle-Granger residual test vs table values ===")
e = []
for _ in range(20):
    x = np.cumsum(rng.standard_normal((5000, 500)), 1)
    y = np.cumsum(rng.standard_normal((5000, 500)), 1)
    e.append(eg_tau(y, x))
e = np.concatenate(e)
q5 = float(np.quantile(e, 0.05))
chk(2, "EG residual 5% quantile (T=500, N=1e5)", -3.34, q5,
    se=boot_quantile_se(e, 0.05), half_unit=0.005, allow=0.01)
pe = float(np.mean(e < -2.86))
chk(2, "P(EG tau < -2.86) = rejection rate at table", 0.15, pe,
    se=math.sqrt(pe * (1 - pe) / len(e)), half_unit=0.005)
d = []
for _ in range(20):
    y = np.cumsum(rng.standard_normal((5000, 1000)), 1)
    d.append(df_const_tau(y))
d = np.concatenate(d)
chk(2, "ADF with constant 5% quantile (T=1000)", -2.86, float(np.quantile(d, 0.05)),
    se=boot_quantile_se(d, 0.05), half_unit=0.005, allow=0.02)

print("=== Card 3: pairs spread as AR(1)/OU, phi=0.98, sd(eps)=0.4% ===")
phi, sde = 0.98, 0.004
sd_stat = sde / math.sqrt(1 - phi * phi)
chk(3, "half-life ln0.5/ln phi (days)", 34.3, math.log(0.5) / math.log(phi), half_unit=0.05)
chk(3, "stationary sd in percent", 2.01, 100 * sd_stat, half_unit=0.005)
chk(3, "implied kappa per day (-ln phi)", 0.0202, -math.log(phi), half_unit=0.00005)
X = ar1_paths(phi, 2000, 5000, sig=sde)
ex = (np.abs(X) > 2 * sd_stat).mean(1)           # per-path exceedance; paths independent
chk(3, "P(|s - mu| > 2 sd_stat), path-level SE", 0.0455, float(ex.mean()),
    se=float(ex.std()) / math.sqrt(len(ex)), half_unit=0.0005)
from math import erf
chk(3, "exact Gaussian value 2(1-Phi(2))", 0.0455, 2 * (1 - 0.5 * (1 + erf(2 / math.sqrt(2)))), half_unit=0.00005)

print("=== Card 4: R^2 = 0.8 debug, independent random walks T=750 ===")
r2b = []
for _ in range(5):
    x = np.cumsum(rng.standard_normal((10000, 750)), 1)
    y = np.cumsum(rng.standard_normal((10000, 750)), 1)
    _, r2, _ = ols_slope_t_r2_dw(y, x)
    r2b.append(r2)
r2b = np.concatenate(r2b)
pr = float(np.mean(r2b > 0.8))
chk(4, "P(R^2 > 0.8) for independent RWs, T=750", 0.015, pr,
    se=math.sqrt(pr * (1 - pr) / len(r2b)), half_unit=0.0005)

print("=== Card 5: GARCH(1,1) omega=2e-6, alpha=0.08, beta=0.90 ===")
om, al, be = 2e-6, 0.08, 0.90
V = om / (1 - al - be)
chk(5, "unconditional daily variance (x1e4)", 1.0, V * 1e4, half_unit=1e-9)
chk(5, "daily vol in percent", 1.00, 100 * math.sqrt(V), half_unit=0.005)
chk(5, "annualised vol in percent (x sqrt252)", 15.87, 100 * math.sqrt(252 * V), half_unit=0.005)
chk(5, "persistence alpha+beta", 0.98, al + be, half_unit=1e-9)
chk(5, "vol half-life in days", 34.3, math.log(0.5) / math.log(al + be), half_unit=0.05)
R = 20000; T = 1500; burn = 500
s2 = np.full(R, V); A = np.zeros(R)
for t_ in range(T + burn):
    r = np.sqrt(s2) * rng.standard_normal(R)
    if t_ >= burn:
        A += r * r
    s2 = om + al * r * r + be * s2
A /= T
chk(5, "MC long-run variance (x1e4), path SE", 1.0, A.mean() * 1e4,
    se=A.std() / math.sqrt(R) * 1e4, half_unit=0.005)

print("=== Card 6: GARCH h-step forecast and IGARCH ===")
s_next = 4e-4
for k, claim in [(1, 2.00), (10, 1.87), (30, 1.63)]:
    f = V + (al + be) ** (k - 1) * (s_next - V)
    chk(6, f"vol forecast k={k} (percent)", claim, 100 * math.sqrt(f), half_unit=0.005)
for k, claim in [(10, 2.04), (30, 2.14)]:
    f = s_next + (k - 1) * om            # IGARCH: alpha+beta = 1
    chk(6, f"IGARCH vol forecast k={k} (percent)", claim, 100 * math.sqrt(f), half_unit=0.005)
R = 200000; s2 = np.full(R, s_next); fc = {}
for j in range(1, 30):                   # step j -> state at t+j+1
    r = np.sqrt(s2) * rng.standard_normal(R)
    s2 = om + al * r * r + be * s2
    if j + 1 == 10:
        fc[10] = (s2.mean(), s2.std() / math.sqrt(R))
    if j + 1 == 30:
        fc[30] = (s2.mean(), s2.std() / math.sqrt(R))
chk(6, "MC E[sigma^2_{t+10}] (x1e4)", 3.50, fc[10][0] * 1e4, se=fc[10][1] * 1e4, half_unit=0.005)
chk(6, "MC E[sigma^2_{t+30}] (x1e4)", 2.67, fc[30][0] * 1e4, se=fc[30][1] * 1e4, half_unit=0.005)

print("=== Card 7: GARCH(1,1) fat tails, alpha=0.10, beta=0.85, normal innovations ===")
al7, be7 = 0.10, 0.85
kf = 3 * (1 - (al7 + be7) ** 2) / (1 - (al7 + be7) ** 2 - 2 * al7 ** 2)
chk(7, "closed-form kurtosis", 3.77, kf, half_unit=0.005)
R = 20000; T = 1500; burn = 500; om7 = 2e-6
s2 = np.full(R, om7 / (1 - al7 - be7)); A4 = np.zeros(R); B2 = np.zeros(R)
for t_ in range(T + burn):
    r = np.sqrt(s2) * rng.standard_normal(R)
    if t_ >= burn:
        A4 += r ** 4; B2 += r * r
    s2 = om7 + al7 * r * r + be7 * s2
A4 /= T; B2 /= T
K_mc = A4.mean() / B2.mean() ** 2
boots = []
for _ in range(300):
    j = rng.integers(0, R, R)
    boots.append(A4[j].mean() / B2[j].mean() ** 2)
chk(7, "MC kurtosis E[r^4]/E[r^2]^2", 3.77, K_mc, se=float(np.std(boots)), half_unit=0.005)

print("=== Card 8: normal-normal update, prior N(0,4), R=1, y=2 ===")
P0 = F(4); Rn = F(1); m0 = F(0); y = F(2)
K = P0 / (P0 + Rn)
post_m = m0 + K * (y - m0)
post_v = (1 - K) * P0
chk(8, "Kalman gain K = 4/5", 0.8, float(K), half_unit=1e-9)
chk(8, "posterior mean 8/5", 1.6, float(post_m), half_unit=1e-9)
chk(8, "posterior variance 4/5", 0.8, float(post_v), half_unit=1e-9)
chk(8, "posterior variance = PR/(P+R)", 0.8, float(P0 * Rn / (P0 + Rn)), half_unit=1e-9)

print("=== Card 9: local-level steady state, Q=1, R=4, P0=10 ===")
Q, Rl = 1.0, 4.0
p_ss = (Q + math.sqrt(Q * Q + 4 * Q * Rl)) / 2
K_ss = p_ss / (p_ss + Rl)
chk(9, "steady predicted variance p", 2.5616, p_ss, half_unit=0.00005)
chk(9, "steady gain K", 0.3904, K_ss, half_unit=0.00005)
chk(9, "steady posterior variance pR/(p+R)", 1.5616, p_ss * Rl / (p_ss + Rl), half_unit=0.00005)
P = F(10); gains = []
for _ in range(3):
    pp = P + F(1); Kt = pp / (pp + F(4)); gains.append(Kt); P = (1 - Kt) * pp
chk(9, "gain after first update from P0=10 (11/15)", 0.7333, float(gains[0]), half_unit=0.00005)
chk(9, "gain after second update (59/119)", 0.4958, float(gains[1]), half_unit=0.00005)
chk(9, "gain after third update (355/831)", 0.4272, float(gains[2]), half_unit=0.00005)
Pn = 10.0
for _ in range(400):
    pp = Pn + Q; Kt = pp / (pp + Rl); Pn = (1 - Kt) * pp
chk(9, "Riccati iteration limit equals steady K", K_ss, Kt, half_unit=1e-9)
chk(9, "limit as Q/R->0 is sqrt(Q/R) (Q/R=1e-6)", 1e-3,
    ((1e-6 + math.sqrt(1e-12 + 4e-6)) / 2) / (((1e-6 + math.sqrt(1e-12 + 4e-6)) / 2) + 1), half_unit=1e-5)

print("=== Card 10: EWMA as steady-state Kalman, lambda = 1-K = 0.94, R=1 ===")
Kw = F(6, 100); Rw = F(1)
pw = Kw / (1 - Kw)                       # p/(p+R)=K with R=1
Qw = pw * pw / (pw + Rw)                 # from p^2 - Q p - Q R = 0
chk(10, "steady predicted variance p = 3/47", 0.0638, float(pw), half_unit=0.00005)
chk(10, "Q/R = 423/110450", 0.00383, float(Qw), half_unit=0.000005)
chk(10, "quadratic residual p^2 - Qp - QR = 0", 0.0, float(pw * pw - Qw * pw - Qw * Rw), half_unit=1e-12)
chk(10, "1/(Q/R) about 261", 261, float(1 / Qw), half_unit=0.5)

print("=== Card 11: dynamic hedge ratio, beta_prior=1.2, P=0.01, Q=4e-4, R=0.01, x=2, y=2.5 ===")
bp = F(12, 10); Pb = F(1, 100); Qb = F(4, 10000); Rb = F(1, 100); xb = F(2); yb = F(5, 2)
Ppred = Pb + Qb
Sinn = xb * xb * Ppred + Rb
Kb = Ppred * xb / Sinn
innov = yb - xb * bp
bpost = bp + Kb * innov
Ppost = (1 - Kb * xb) * Ppred
chk(11, "predicted variance 0.0104", 0.0104, float(Ppred), half_unit=1e-9)
chk(11, "innovation variance 0.0516", 0.0516, float(Sinn), half_unit=1e-9)
chk(11, "gain K = 52/129", 0.4031, float(Kb), half_unit=0.00005)
chk(11, "posterior beta 1.2403", 1.2403, float(bpost), half_unit=0.00005)
chk(11, "posterior variance 0.00202", 0.00202, float(Ppost), half_unit=0.000005)

print("=== Card 12: AR(1) x_t = 0.9 x_{t-1} + e_t, Var(e)=1 ===")
ph = 0.9
chk(12, "stationary variance 100/19", 5.263, 1 / (1 - ph * ph), half_unit=0.0005)
chk(12, "stationary sd", 2.294, math.sqrt(1 / (1 - ph * ph)), half_unit=0.0005)
chk(12, "half-life ln0.5/ln0.9 (seconds)", 6.58, math.log(0.5) / math.log(ph), half_unit=0.005)
Xp = ar1_paths(ph, 200000, 600)              # cross-section at t=600 is stationary
v_cs = Xp[:, -1].var()
chk(12, "MC stationary variance, cross-section, N=2e5", 5.263, float(v_cs),
    se=float(v_cs) * math.sqrt(2 / Xp.shape[0]), half_unit=0.0005)

print("=== Card 13: OLS bias of phi, T=50 observations ===")
kend = -(1 + 3 * 0.9) / 50
chk(13, "Kendall approximation at phi=0.9, T=50", -0.074, kend, half_unit=0.0005)
Xa = ar1_paths(0.9, 100000, 51)
xx = Xa[:, :-1]; yy = Xa[:, 1:]
xm = xx.mean(1, keepdims=True); ym = yy.mean(1, keepdims=True)
bh = ((xx - xm) * (yy - ym)).sum(1) / ((xx - xm) ** 2).sum(1)
chk(13, "simulated bias at phi=0.9, T=50", -0.081, float(bh.mean() - 0.9),
    se=float(bh.std()) / math.sqrt(len(bh)), half_unit=0.0005)
means = {}
for phi_t in [0.97, 0.99, 1.0]:
    Xs = ar1_paths(phi_t, 100000, 51)
    xx = Xs[:, :-1]; yy = Xs[:, 1:]
    xm = xx.mean(1, keepdims=True); ym = yy.mean(1, keepdims=True)
    bs_ = ((xx - xm) * (yy - ym)).sum(1) / ((xx - xm) ** 2).sum(1)
    means[phi_t] = (float(bs_.mean()), float(bs_.std()) / math.sqrt(len(bs_)))
    print(f"   phi={phi_t}: E[phihat] = {means[phi_t][0]:.4f} (se {means[phi_t][1]:.4f})")
chk(13, "simulated E[phihat] at true phi=1.0 is about 0.90", 0.90, means[1.0][0],
    se=means[1.0][1], half_unit=0.005)
chk(13, "E[phihat] at phi=0.97 is about 0.88", 0.88, means[0.97][0], se=means[0.97][1], half_unit=0.005)
chk(13, "first-order Kendall inversion gives phi about 0.979", 0.979,
    (0.90 + 1 / 50) / (1 - 3 / 50), half_unit=0.0005)

print("=== Card 14: monthly OU/AR(1) mapping, phi=0.9, residual sd 0.02, Delta=1/12 yr ===")
Dl = 1 / 12
kap = -math.log(0.9) / Dl
chk(14, "kappa per year = -ln(phi)/Delta", 1.26, kap, half_unit=0.005)
chk(14, "half-life in years ln2/kappa", 0.548, math.log(2) / kap, half_unit=0.0005)
chk(14, "half-life in months", 6.58, math.log(0.5) / math.log(0.9), half_unit=0.005)
resid_var = 0.02 ** 2
stat_sd = math.sqrt(resid_var / (1 - 0.81))
chk(14, "stationary sd of X in percent", 4.59, 100 * stat_sd, half_unit=0.005)
sig_ou = math.sqrt(2 * kap * resid_var / (1 - 0.81))
chk(14, "OU sigma per sqrt(year)", 0.073, sig_ou, half_unit=0.0005)
# transition variance from the OU solution, by numerical integration of the noise kernel
ss = np.linspace(0, Dl, 200001)
w = np.exp(-kap * (Dl - ss)) ** 2
vt = sig_ou ** 2 * np.trapezoid(w, ss)
chk(14, "OU transition variance = residual variance", 0.0004, vt, half_unit=1e-7)
chk(14, "naive Euler reading (1-phi)/Delta", 1.2, (1 - 0.9) / Dl, half_unit=1e-9)

n_ok = sum(rows)
print(f"SUMMARY: {len(rows)} checks, {n_ok} PASS, {len(rows) - n_ok} FAIL")
