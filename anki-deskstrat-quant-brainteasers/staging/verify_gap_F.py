"""Verify every numerical claim on staging/gap_F.json (14 cards, file order, index 0-13).

Closed forms use fractions.Fraction or exact float arithmetic. Monte Carlo uses >= 1e5
draws with standard errors (batch or analytic). Optimisation claims (insider best
response, Almgren-Chriss schedule, risk-neutral spread) are checked by direct numerical
optimisation. A claim PASSES when |claimed - computed| <= max(3 SE, half unit in the
last printed digit of the claim, or the stated tolerance).
Run: python3 -I staging/verify_gap_F.py
"""
import math
from fractions import Fraction as F
import numpy as np

rng = np.random.default_rng(20261019)
rows = []


def chk(idx, label, claimed, computed, se=0.0, tol=0.0):
    t = max(3.0 * se, tol)
    ok = abs(claimed - computed) <= t
    rows.append(ok)
    print(f"card {idx:2d} | {label:52s} | claimed {claimed:>11.6g} | computed {computed:>11.6g} "
          f"| se {se:9.2g} | tol {t:9.2g} | {'PASS' if ok else 'FAIL'}")


def batch_se(vals, nb=100):
    """SE of a mean from batch means (vals: per-draw array)."""
    b = np.array_split(vals, nb)
    m = np.array([x.mean() for x in b])
    return float(m.std(ddof=1) / math.sqrt(nb))


def kyle_mc(sv, su, n=10**6):
    """Linear Kyle equilibrium: insider x = (sigma_u/sigma_v) v, price p = lambda*y, y = x + u."""
    lam = sv / (2 * su)
    beta = su / sv
    v = sv * rng.standard_normal(n)
    u = su * rng.standard_normal(n)
    x = beta * v
    y = x + u
    p = lam * y
    # market maker's regression slope of v on y (should equal lambda)
    slope = np.cov(v, y, bias=True)[0, 1] / np.var(y)
    prof = x * (v - p)
    noise_loss = -(u * (v - p))          # noise trader expected loss, sign flipped
    cov_vp_over_var_v = np.cov(v, p, bias=True)[0, 1] / np.var(v)
    return dict(lam=lam, beta=beta, slope=slope, prof=prof, varp=np.var(p), vp=cov_vp_over_var_v,
                noise_loss=noise_loss, v=v, y=y)


# ---------------- Card 0: Kyle solve (sigma_v=2, sigma_u=1) ----------------
sv, su = 2.0, 1.0
K = kyle_mc(sv, su)
chk(0, "lambda = sigma_v/(2 sigma_u) (closed form)", 1.0, sv / (2 * su), tol=1e-12)
chk(0, "beta = sigma_u/sigma_v (closed form)", 0.5, su / sv, tol=1e-12)
chk(0, "MM regression slope of v on y = lambda (MC)", 1.0, K["slope"], se=0.01)
chk(0, "insider profit E[x(v-p)] = sigma_u sigma_v/2 (MC)", 1.0, K["prof"].mean(), se=batch_se(K["prof"]))
chk(0, "Var(p) = sigma_v^2/2 (MC)", 2.0, K["varp"], se=0.02)
chk(0, "Cov(v,p)/Var(v) = 1/2 (MC)", 0.5, K["vp"], se=0.005)
# insider best response: maximise x*v - lambda*x^2 (u has mean zero, independent of x)
grid = np.linspace(-3, 3, 600001)
v0 = 1.3
best = grid[np.argmax(grid * v0 - 1.0 * grid ** 2)]
chk(0, "insider best response x*(v=1.3) = v/(2 lambda) (grid)", 0.65, best, tol=2e-5)

# ---------------- Card 1: Kyle recognise (sigma_u=0.5 gives lambda=2) ----------------
K1b = kyle_mc(2.0, 0.5)
chk(1, "lambda at sigma_u=0.5 (MC slope)", 2.0, K1b["slope"], se=0.02)
chk(1, "beta at sigma_u=0.5", 0.25, K1b["beta"], tol=1e-12)

# ---------------- Card 2: Kyle perturbation, sigma_u doubled to 2 ----------------
K2 = kyle_mc(2.0, 2.0)
chk(2, "new lambda = 1/2 (MC slope)", 0.5, K2["slope"], se=0.005)
chk(2, "new beta = 1", 1.0, K2["beta"], tol=1e-12)
chk(2, "new insider profit = 2 (MC)", 2.0, K2["prof"].mean(), se=batch_se(K2["prof"]))
chk(2, "Var(p) unchanged = 2 (MC)", 2.0, K2["varp"], se=0.02)
chk(2, "Cov(v,p)/Var(v) unchanged = 1/2 (MC)", 0.5, K2["vp"], se=0.005)
chk(2, "noise-trader expected loss = 2 (MC)", 2.0, K2["noise_loss"].mean(), se=batch_se(K2["noise_loss"]))

# ---------------- Card 3: square-root Fermi cost ----------------
sig, frac = 0.02, 0.10
end_imp = sig * math.sqrt(frac)
avg_imp = 2.0 / 3.0 * end_imp
notional = frac * 2e6 * 50.0
chk(3, "end-point impact 63 bp = sigma sqrt(0.1)", 0.0063, end_imp, tol=5e-5)
chk(3, "average impact about 42 bp = (2/3) end-point", 0.0042, avg_imp, tol=5e-5)
xs = rng.uniform(size=10**6)
chk(3, "E[sqrt(U)] = 2/3 used for the average (MC)", 2.0 / 3.0, np.sqrt(xs).mean(),
    se=batch_se(np.sqrt(xs)))
chk(3, "cost about GBP 42k on GBP 10m notional", 42000.0, avg_imp * notional, tol=1000.0)
chk(3, "sanity: 1% ADV average cost 13 bp", 0.0013, 2.0 / 3.0 * 0.02 * math.sqrt(0.01), tol=5e-5)
chk(3, "10% vs 1% cost ratio = sqrt(10) (about 3.2)", math.sqrt(10), avg_imp / (2.0 / 3.0 * 0.02 * math.sqrt(0.01)),
    tol=1e-12)
chk(3, "transfer: 5% ADV, 3% vol, average 45 bp", 0.0045,
    2.0 / 3.0 * 0.03 * math.sqrt(0.05), tol=5e-5)

# ---------------- Card 4: square-root scaling recognise (1% -> 4% ADV) ----------------
imp_ratio = math.sqrt(4 * 0.01) / math.sqrt(0.01)
cost_ratio = 4 * imp_ratio
chk(4, "per-share impact ratio 1% -> 4% ADV = 2", 2.0, imp_ratio, tol=1e-12)
chk(4, "total cost ratio = 8 (= 4^{3/2})", 8.0, cost_ratio, tol=1e-12)
chk(4, "linear-law total cost ratio = 16 (contrast)", 16.0, 4 * 4.0, tol=1e-12)
chk(4, "transfer: 4% -> 1% halves per-share impact", 0.5, math.sqrt(0.01 / 0.04), tol=1e-12)

# ---------------- Card 5: splitting debug ----------------
Qv, Vv, sg = 1.0, 1.0, 1.0


def whole_cost():
    return sg * Qv * math.sqrt(Qv / Vv)


def children_cost(n):
    q = Qv / n
    return n * q * sg * math.sqrt(q / Vv)


chk(5, "four children cost ratio = 1/2 (square-root law)", 0.5, children_cost(4) / whole_cost(), tol=1e-12)
chk(5, "each child cost = C/8", 1 / 8, children_cost(4) / 4 / whole_cost(), tol=1e-12)
chk(5, "linear-law saving for n=4 is 1/4 (flaw claim, 75%)", 0.25,
    4 * (1 / 4) ** 2 / 1.0, tol=1e-12)
chk(5, "general n: ratio = n^{-1/2} at n=9", 1 / 3, children_cost(9) / whole_cost(), tol=1e-12)


# ---------------- Almgren-Chriss: discrete optimum check (eta=1, lambda sigma^2=4, T=1) ----------------
def ac_discrete(N=1000, T=1.0, c=4.0, X=1.0):
    dt = T / N
    # M = rate part (1/dt) * D^T D, D rows: x_{i-1} - x_i for i=1..N, x in R^{N+1}
    D = np.zeros((N, N + 1))
    for i in range(1, N + 1):
        D[i - 1, i - 1] = 1.0
        D[i - 1, i] = -1.0
    Mtot = D.T @ D / dt
    for i in range(1, N):
        Mtot[i, i] += c * dt        # holding term c x_i^2 dt for interior nodes
    I = np.arange(1, N)
    B = np.array([0, N])
    xB = np.array([X, 0.0])
    xI = -np.linalg.solve(Mtot[np.ix_(I, I)], Mtot[np.ix_(I, B)] @ xB)
    x = np.zeros(N + 1)
    x[0], x[N] = X, 0.0
    x[I] = xI
    rate0 = (x[0] - x[1]) / dt
    return x, rate0


xd, r0 = ac_discrete()
kT = 2.0
cont_mid = math.sinh(kT / 2) / math.sinh(kT)
cont_rate = kT * (1 / math.tanh(kT))           # kappa X coth(kappa T), with T=1, X=1
chk(6, "remaining fraction at T/2 = 1/(2 cosh 1) (closed form)", 0.324, cont_mid, tol=5e-4)
chk(6, "remaining fraction at T/2, discrete optimum", 0.324, xd[500], tol=2e-3)
chk(6, "initial selling rate / TWAP (X/T), continuous = 2.075", 2.075, cont_rate, tol=5e-4)
chk(6, "initial selling rate / TWAP, discrete optimum", 2.075, r0, tol=1e-2)

# ---------------- Card 7: AC recognise: schedule is not linear ----------------
chk(7, "optimal midpoint differs from linear 0.5 by > 0.15", 0.176, 0.5 - xd[500], tol=2e-3)

# ---------------- Card 8: taut string twin (same discrete problem, L=1, kappa L=2) ----------------
ut = xd  # identical discrete problem: tension 1, spring stiffness 4 on [0,1]
chk(8, "u(L/4) = sinh(1.5)/sinh(2) = 0.587 (closed form)", 0.587,
    math.sinh(1.5) / math.sinh(2.0), tol=5e-4)
chk(8, "u(L/4) discrete minimiser", 0.587, ut[250], tol=2e-3)
chk(8, "u(L/2) = sinh(1)/sinh(2) = 0.324 (transfer)", 0.324, ut[500], tol=2e-3)
chk(8, "drop over first quarter = 0.413 (convexity)", 0.413, 1 - ut[250], tol=2e-3)
chk(8, "drop over second quarter = 0.263 (convexity)", 0.263, ut[250] - ut[500], tol=2e-3)
chk(8, "drop first quarter > second quarter", 1.0, float(1 - ut[250] > ut[250] - ut[500]), tol=1e-12)

# ---------------- Card 9: Avellaneda-Stoikov solve ----------------
s, q, gam, sig_as, tau_as, k_as = 100.0, 3, 0.1, 0.5, 2.0, 1.5
r_as = s - q * gam * sig_as ** 2 * tau_as
spread_as = gam * sig_as ** 2 * tau_as + (2 / gam) * math.log(1 + gam / k_as)
chk(9, "reservation price r = 99.85", 99.85, r_as, tol=1e-9)
chk(9, "spread = 1.341 (closed form)", 1.341, spread_as, tol=5e-4)
chk(9, "bid = 99.180", 99.180, r_as - spread_as / 2, tol=5e-4)
chk(9, "ask = 100.520", 100.520, r_as + spread_as / 2, tol=5e-4)
chk(9, "transfer: short 3 gives r = 100.15", 100.15, s + 3 * gam * sig_as ** 2 * tau_as, tol=1e-9)
chk(9, "skew 0.05 per unit (sanity: gamma sigma^2 (T-t))", 0.05, gam * sig_as ** 2 * tau_as, tol=1e-12)

# ---------------- Card 10: AS perturbation gamma -> 0 ----------------
g_small = 1e-6
chk(10, "spread at gamma=1e-6 = 1.3333 (limit 2/k)", 1.3333,
    (2 / g_small) * math.log(1 + g_small / k_as), tol=5e-5)
chk(10, "2/k = 1.3333", 1.3333, 2 / k_as, tol=5e-5)
dgrid = np.linspace(1e-4, 5, 500001)
d_opt = dgrid[np.argmax(dgrid * np.exp(-k_as * dgrid))]
chk(10, "risk-neutral optimal offset per side = 1/k (grid)", 0.6667, d_opt, tol=2e-4)
nq = 10**5
lam_side = math.exp(-1.0) * 2.0                   # A=1, delta=1/k: e^{-k/k}=e^{-1}, times T-t=2
bu = rng.poisson(lam_side, nq)
bs = rng.poisson(lam_side, nq)
inv = (bu - bs).astype(float)
var_inv = inv.var()
se_var = float(np.std((inv - inv.mean()) ** 2) / math.sqrt(nq))
chk(10, "inventory variance after T-t=2 = 4/e (MC)", 1.47, var_inv, se=max(se_var, 0.005))
chk(10, "closed form 4/e = 1.4715", 1.4715, 4 / math.e, tol=5e-5)

# ---------------- Card 11: AS skew toolkit ----------------
chk(11, "long 3 units: quotes move down by 0.15", 0.15, 3 * 0.05, tol=1e-12)

# ---------------- Card 12: Glosten-Milgrom solve ----------------
VH, VL, mu = F(110), F(90), F(1, 4)
PbuyH = mu + (1 - mu) * F(1, 2)
PbuyL = (1 - mu) * F(1, 2)
Pbuy = (PbuyH + PbuyL) / 2
ask_exact = (F(1, 2) * VH * PbuyH + F(1, 2) * VL * PbuyL) / Pbuy
Psell_H, Psell_L = 1 - PbuyH, 1 - PbuyL
Psell = (Psell_H + Psell_L) / 2
bid_exact = (F(1, 2) * VH * Psell_H + F(1, 2) * VL * Psell_L) / Psell
chk(12, "ask = 102.5 exact", 102.5, float(ask_exact), tol=1e-12)
chk(12, "bid = 97.5 exact", 97.5, float(bid_exact), tol=1e-12)
chk(12, "spread = mu (V_H - V_L) = 5 exact", 5.0, float(ask_exact - bid_exact), tol=1e-12)
chk(12, "P(buy|V_H) = 5/8 exact", 0.625, float(PbuyH), tol=1e-12)
N = 10**6
Vs = np.where(rng.uniform(size=N) < 0.5, 110.0, 90.0)
inf = rng.uniform(size=N) < 0.25
uninf_buy = rng.uniform(size=N) < 0.5
buy = np.where(inf, Vs == 110.0, uninf_buy)
ask_mc = Vs[buy]
bid_mc = Vs[~buy]
chk(12, "MC E[V | buy] = 102.5", 102.5, ask_mc.mean(), se=float(ask_mc.std() / math.sqrt(len(ask_mc))))
chk(12, "MC E[V | sell] = 97.5", 97.5, bid_mc.mean(), se=float(bid_mc.std() / math.sqrt(len(bid_mc))))
mu0_ph, mu0_pl = F(1, 2), F(1, 2)
mu0_ask = (F(1, 2) * VH * mu0_ph + F(1, 2) * VL * mu0_pl) / ((mu0_ph + mu0_pl) / 2)
chk(12, "mu=0 gives ask = 100 (exact)", 100.0, float(mu0_ask), tol=1e-12)
mu1_ph, mu1_pl = F(1), F(0)
mu1_ask = (F(1, 2) * VH * mu1_ph + F(1, 2) * VL * mu1_pl) / ((mu1_ph + mu1_pl) / 2)
chk(12, "mu=1 gives ask 110 (full revelation, exact)", 110.0, float(mu1_ask), tol=1e-12)
chk(12, "transfer V_H=120, V_L=80, mu=1/2: ask 110", 110.0, 100 + 0.5 * 20, tol=1e-12)
chk(12, "transfer V_H=120, V_L=80, mu=1/2: bid 90", 90.0, 100 - 0.5 * 20, tol=1e-12)

# ---------------- Card 13: Glosten-Milgrom rebuild (exact, several mu) ----------------
ok_all = True
for mm in [F(0), F(1, 4), F(1, 2), F(3, 4), F(1)]:
    ph = mm + (1 - mm) / 2
    pl = (1 - mm) / 2
    pb = (ph + pl) / 2
    direct = (F(1, 2) * VH * ph + F(1, 2) * VL * pl) / pb
    formula = (VH + VL) / 2 + mm * (VH - VL) / 2
    ok_all = ok_all and (direct == formula)
chk(13, "ask = mid + mu (V_H - V_L)/2 for five mu values (exact)", 1.0, float(ok_all), tol=1e-12)

n_pass = sum(rows)
print(f"SUMMARY: {n_pass}/{len(rows)} checks PASS")
