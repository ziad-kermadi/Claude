"""Verifies every numerical claim on staging/gap_C.json (card indices as in gap_C.json).

Exact values use fractions.Fraction or closed forms; non-trivial probabilities and expectations are
checked by Monte Carlo with >= 1e5 trials and a printed standard error. A check passes when the
claimed value lies within max(4 SE, stated slack) of the computed value.
Run: python3 staging/verify_gap_C.py   (exit status 1 if any line FAILs)
"""
import math
import sys
from fractions import Fraction as F
from math import comb, exp, log, sqrt, pi

import numpy as np
from scipy.optimize import minimize_scalar
from scipy.stats import norm, binom

RNG = np.random.default_rng(20261019)
rows = []


def line(idx, label, claimed, computed, ok, extra=""):
    status = "PASS" if ok else "FAIL"
    rows.append(ok)
    print(f"card {idx:2d} | {label:<42s} | claimed {claimed:<14} | computed {computed:<22} | {status} {extra}")


def exact_check(idx, label, claimed_str, claimed, computed, tol=5e-5):
    ok = abs(float(claimed) - float(computed)) <= tol
    line(idx, label, claimed_str, f"{float(computed):.6f}", ok)


def mc_check(idx, label, claimed_str, claimed, est, se, k=4.0, slack=0.0):
    ok = abs(est - claimed) <= max(k * se, slack)
    line(idx, label, claimed_str, f"{est:.5f} +- {se:.5f}", ok, f"(n_se={abs(est - claimed) / se:.2f})" if se > 0 else "")


# ---------------- card 0: thinning of Poisson(12/h), large with p = 1/4 ----------------
lam, p = 12.0, 0.25
exact0 = F(177147, 80)                        # (9/2)(9^5/5!) = 531441/240 = 177147/80
val0 = float(exact0) * exp(-12)
# Route 1: independent Poisson(3) and Poisson(9) counts
route1 = exp(-3) * 3**2 / 2 * exp(-9) * 9**5 / 120
# Route 2: total count Poisson(12), then binomial split (cross-check of the sanity line)
route2 = exp(-12) * 12**7 / math.factorial(7) * comb(7, 2) * p**2 * (1 - p)**5
line(0, "thinning: P(2 large, 5 small) = 177147/80 e^-12", "0.013605", f"{val0:.6f}",
     abs(val0 - 0.013605) < 5e-7 and abs(route1 - val0) < 1e-12 and abs(route2 - val0) < 1e-12)
# Monte Carlo from the arrival process itself: exponential gaps, independent fair marks at p=1/4
T, chunk = 400_000, 100_000
hits, n_tot = 0, 0
for _ in range(T // chunk):
    gaps = RNG.exponential(1 / lam, size=(chunk, 90))          # 90 gaps: mean count 12/h is ~12
    arr = np.cumsum(gaps, axis=1)
    inside = arr <= 1.0
    marks = RNG.random((chunk, 90)) < p
    large = (inside & marks).sum(axis=1)
    small = (inside & ~marks).sum(axis=1)
    hits += int(np.sum((large == 2) & (small == 5)))
    n_tot += chunk
est0 = hits / n_tot
se0 = sqrt(est0 * (1 - est0) / n_tot)
mc_check(0, "thinning MC (arrival process)", "0.013605", val0, est0, se0)

# ---------------- card 1: time until all of three Poisson processes (rates 1,2,3) have fired -------
rates = [F(1), F(2), F(3)]
from itertools import combinations
emax = F(0)
for r in range(1, 4):
    for S in combinations(rates, r):
        emax += (-1) ** (r + 1) / sum(S)
exact_check(1, "E[max of Exp(1),Exp(2),Exp(3)] = 73/60", "73/60", F(73, 60), emax)
print("        note: sum of means 11/6 is NOT the answer; inclusion-exclusion gives 73/60")
n1 = 200_000
X = np.column_stack([RNG.exponential(1.0 / float(r), n1) for r in rates])
mx = X.max(axis=1)
mc_check(1, "E[max] MC", "1.216667", 73 / 60, mx.mean(), mx.std(ddof=1) / sqrt(n1))
line(1, "sum of means 11/6 exceeds the answer", "11/6 > 73/60", f"{float(F(11, 6)):.4f}", float(F(11, 6)) > 73 / 60)

# ---------------- card 2: middle of three Poisson arrivals on [0,10], given N(10)=3 ----------------
F_mid = lambda x: 3 * x**2 - 2 * x**3          # P(second order statistic <= x) for 3 uniforms
p2 = F_mid(F(3, 5)) - F_mid(F(2, 5))
exact_check(2, "P(4 <= middle arrival <= 6 | N(10)=3)", "37/125", F(37, 125), p2)
# Monte Carlo from the process (lambda = 0.3 chosen only so that N(10)=3 is not too rare)
lam2 = 0.3
hits2 = tot2 = 0
for _ in range(10):
    g = RNG.exponential(1 / lam2, size=(200_000, 30))
    arr = np.cumsum(g, axis=1)
    cnt = (arr <= 10.0).sum(axis=1)
    sel = cnt == 3
    mid = arr[np.arange(arr.shape[0]), 1]       # second arrival (index 1)
    hits2 += int(np.sum(sel & (mid >= 4) & (mid <= 6)))
    tot2 += int(sel.sum())
est2 = hits2 / tot2
se2 = sqrt(est2 * (1 - est2) / tot2)
mc_check(2, "conditional MC (given N(10)=3)", "0.296", 37 / 125, est2, se2)
print(f"        conditioning sample size: {tot2} paths with N(10)=3")

# ---------------- card 3: compound Poisson, claim sizes {1,2,5} w.p. {1/2,1/3,1/6} ----------------
xs = [F(1), F(2), F(5)]
ps = [F(1, 2), F(1, 3), F(1, 6)]
EX = sum(x * q for x, q in zip(xs, ps))
EX2 = sum(x * x * q for x, q in zip(xs, ps))
VX = EX2 - EX**2
var_pois = 4 * VX + 4 * EX**2           # Var(N)=4 for Poisson(4): E[N]VX + Var(N)(EX)^2
var_binom = 4 * VX + 2 * EX**2          # Var(N)=8*(1/2)*(1/2)=2 for Binomial(8,1/2)
line(3, "compound Poisson Var(S) = 24 (known)", "24", str(var_pois), var_pois == 24 and EX == 2 and EX2 == 6)
line(3, "Binomial(8,1/2) count: Var(S) = 16", "16", str(var_binom), var_binom == 16)
n3 = 200_000
maxN = 40
Npois = RNG.poisson(4.0, n3)
assert Npois.max() < maxN
Xs = RNG.choice([1, 2, 5], size=(n3, maxN), p=[0.5, 1 / 3, 1 / 6])
mask = np.arange(maxN)[None, :] < Npois[:, None]
Sp = (Xs * mask).sum(axis=1)
mc_check(3, "Poisson(4) compound: Var(S) MC", "24", 24.0, Sp.var(ddof=1), Sp.var(ddof=1) * sqrt(2 / n3), k=4)
Nb = RNG.binomial(8, 0.5, n3)
Xb = RNG.choice([1, 2, 5], size=(n3, 8), p=[0.5, 1 / 3, 1 / 6])
Sb = (Xb * (np.arange(8)[None, :] < Nb[:, None])).sum(axis=1)
mc_check(3, "Binomial(8,1/2) compound: Var(S) MC", "16", 16.0, Sb.var(ddof=1), Sb.var(ddof=1) * sqrt(2 / n3), k=4)
mc_check(3, "Binomial compound: E[S] = 8 (unchanged mean)", "8", 8.0, Sb.mean(), Sb.std(ddof=1) / sqrt(n3))

# ---------------- card 4: expected length of the gap containing t, Poisson(0.1/min) started at 0 ------
lam4, t4 = 0.1, 5.0
L_formula = (2 - exp(-lam4 * t4)) / lam4
claimed4 = 10 * (2 - exp(-0.5))
line(4, "E[L] = (2 - e^{-lam t})/lam at t=5", "13.93", f"{L_formula:.4f}", abs(L_formula - claimed4) < 1e-9
     and abs(L_formula - 13.93) < 0.005)
n4 = 200_000
g4 = RNG.exponential(1 / lam4, size=(n4, 25))
arr4 = np.cumsum(g4, axis=1)
prev = np.where(arr4 <= t4, arr4, 0.0).max(axis=1)          # last arrival at or before t (0 = start)
nxt = np.where(arr4 > t4, arr4, np.inf).min(axis=1)
Lmc = nxt - prev
mc_check(4, "gap containing t, MC", "13.93", claimed4, Lmc.mean(), Lmc.std(ddof=1) / sqrt(n4))
mc_check(4, "E[age] = (1-e^{-lam t})/lam", f"{(1 - exp(-0.5)) / lam4:.4f}", (1 - exp(-0.5)) / lam4,
         (t4 - prev).mean(), (t4 - prev).std(ddof=1) / sqrt(n4))
line(4, "stationary limit 2/lam = 20 min", "20", f"{2 / lam4:.1f}", abs(2 / lam4 - 20) < 1e-12)

# ---------------- card 5: Wald, stop at the first 6 (6 included) ----------------
ET = sum(F(5, 6) ** (i - 1) for i in range(1, 400))   # truncated tail is < (5/6)^399, negligible
ET_closed = F(6)
EXd = F(7, 2)
ES_exact = EXd * ET_closed
exact_check(5, "E[S_T] = E[T] E[X] = 6 * 7/2", "21", F(21), ES_exact)
line(5, "E[T] = 6 (series truncation check)", "6", f"{float(ET):.12f}", abs(float(ET) - 6) < 1e-12)
n5, L5 = 200_000, 120
rolls = RNG.integers(1, 7, size=(n5, L5))
is6 = rolls == 6
assert is6.any(axis=1).all()
T5 = np.argmax(is6, axis=1) + 1                              # index of the first 6 (1-based)
cs = np.cumsum(rolls, axis=1)
S5 = cs[np.arange(n5), T5 - 1]
mc_check(5, "Wald MC: E[S_T]", "21", 21.0, S5.mean(), S5.std(ddof=1) / sqrt(n5))

# ---------------- card 6: debug card, N = number of rolls before the first 6 ----------------
EN = F(5)                                    # E[T - 1] with E[T] = 6
wrong = EN * EXd
line(6, "flawed Wald line gives 35/2", "17.5", str(wrong), wrong == F(35, 2))
# correct value: E[S_N] = sum_i E[X_i 1{X_1..X_i != 6}] = (15/6) * sum (5/6)^(i-1) = 15
correct = (F(15, 6)) * (1 / (1 - F(5, 6)))
exact_check(6, "correct E[S_N] = 15", "15", F(15), correct)
# Monte Carlo: sum of rolls strictly before the first 6
n6 = 200_000
r6 = RNG.integers(1, 7, size=(n6, 120))
is6b = r6 == 6
T6 = np.argmax(is6b, axis=1)                  # 0-based index of first 6 = number of rolls before it
cs6 = np.concatenate([np.zeros((n6, 1), dtype=np.int64), np.cumsum(r6, axis=1)], axis=1)
S6 = cs6[np.arange(n6), T6]
mc_check(6, "MC: sum of rolls before first 6", "15", 15.0, S6.mean(), S6.std(ddof=1) / sqrt(n6))
mc_check(6, "MC: E[N] = 5", "5", 5.0, T6.mean(), T6.std(ddof=1) / sqrt(n6))

# ---------------- card 7: Doob L2 bound on E[max] for SRW, n = 100 ----------------
n7 = 100
def P_max_ge(a, n):
    tot = F(0)
    for k in range(n + 1):
        s = 2 * k - n
        if s > a:
            tot += F(2 * comb(n, k), 2**n)
        elif s == a:
            tot += F(comb(n, k), 2**n)
    return tot
EM = sum(P_max_ge(a, n7) for a in range(1, n7 + 1))
line(7, "exact E[max_{k<=100} S_k] (lattice)", "7.499", f"{float(EM):.6f}", abs(float(EM) - 7.4987) < 5e-5)
doob_bound = 4 * n7                           # E[max S_k^2] <= 4 E[S_n^2] = 4 n
bound_mean = 2 * sqrt(n7)                     # E[M^+] <= sqrt(E[max (S_k^+)^2]) <= 2 sqrt(n)
line(7, "Doob: E[max S_k^2] <= 400", "400", str(doob_bound), doob_bound == 400)
line(7, "Doob: E[M] <= 2 sqrt(n) = 20", "20", f"{bound_mean:.1f}", abs(bound_mean - 20) < 1e-12 and float(EM) <= bound_mean)
line(7, "BM scaling sqrt(2n/pi) = 7.98", "7.98", f"{sqrt(2 * n7 / pi):.4f}", abs(sqrt(2 * n7 / pi) - 7.98) < 0.005)
n7m = 100_000
Wsteps = RNG.choice([-1, 1], size=(n7m, n7)).astype(np.int32)
Sp7 = np.cumsum(Wsteps, axis=1)
M7 = np.maximum(Sp7.max(axis=1), 0)
mc_check(7, "MC E[M] (k=0..n, M>=0)", "7.499", float(EM), M7.mean(), M7.std(ddof=1) / sqrt(n7m))
mx2 = np.maximum((np.concatenate([np.zeros((n7m, 1), dtype=np.int32), Sp7], axis=1) ** 2).max(axis=1), 0)
line(7, "MC E[max S_k^2] value", "<= 400", f"{mx2.mean():.2f} +- {mx2.std(ddof=1) / sqrt(n7m):.2f}", mx2.mean() <= 400)

# ---------------- card 8: Brownian bridge covariance, Cov(B_{1/4}, B_{3/4}) = 1/16 ----------------
s8, t8 = F(1, 4), F(3, 4)
cov8 = min(s8, t8) - s8 * t8
exact_check(8, "Cov(B_{1/4},B_{3/4}) = s(1-t)", "1/16", F(1, 16), cov8)
line(8, "correlation = 1/3", "1/3", str(cov8 / (F(3, 16))), cov8 / F(3, 16) == F(1, 3))
N8, n8 = 400, 200_000
dt8 = 1.0 / N8
dW = RNG.standard_normal((n8, N8)) * sqrt(dt8)
W8 = np.cumsum(dW, axis=1)
grid = lambda k: W8[:, k - 1]                       # W at time k/N8
B_q = grid(100) - 0.25 * grid(400)                  # bridge at 1/4
B_t = grid(300) - 0.75 * grid(400)                  # bridge at 3/4
prod = B_q * B_t
mc_check(8, "MC Cov(B_{1/4},B_{3/4})", "0.0625", 1 / 16, prod.mean(), prod.std(ddof=1) / sqrt(n8))
mc_check(8, "MC Var(B_{1/4}) = 3/16", "0.1875", 3 / 16, (B_q ** 2).mean(), (B_q ** 2).std(ddof=1) / sqrt(n8))

# ---------------- card 9: bridge from 0 to 1, P(max >= 2) = exp(-2a(a-c)) = e^-4 ----------------
a9, c9 = 2.0, 1.0
p9 = exp(-2 * a9 * (a9 - c9))
line(9, "closed form exp(-2a(a-c)) = e^-4", "0.018316", f"{p9:.6f}", abs(p9 - exp(-4)) < 1e-15 and abs(p9 - 0.018316) < 1e-6)
N9, n9, chunks9 = 1000, 100_000, 10
dt9 = 1.0 / N9
beta9 = 0.5826 * sqrt(dt9)                           # Broadie-Glasserman continuity correction
hits9 = 0
for _ in range(chunks9):
    m = n9 // chunks9
    dW9 = RNG.standard_normal((m, N9)) * sqrt(dt9)
    Wp = np.cumsum(dW9, axis=1)
    tt = np.arange(1, N9 + 1) * dt9
    B9 = Wp + tt[None, :] * (c9 - Wp[:, -1:])        # bridge from 0 to c9 on the grid
    hits9 += int(np.sum(B9.max(axis=1) >= a9 - beta9))   # discrete max under-reads the continuous max
est9 = hits9 / n9
se9 = sqrt(est9 * (1 - est9) / n9)
mc_check(9, "bridge 0->1 MC (grid + continuity corr.)", "0.018316", p9, est9, se9, k=4, slack=0.03 * p9)

# ---------------- card 10: arcsine law for time spent positive, P(A >= 3/4) = 1/3 ----------------
p10 = 1 - 2 / pi * math.asin(sqrt(0.75))
exact_check(10, "P(A >= 3/4) = 1 - (2/pi) arcsin sqrt(3/4)", "1/3", F(1, 3), p10, tol=1e-12)
N10, n10, chunks10 = 2000, 100_000, 10
hit10 = 0
for _ in range(chunks10):
    m = n10 // chunks10
    Wp = np.cumsum(RNG.standard_normal((m, N10)) / sqrt(N10), axis=1)
    A10 = (Wp > 0).mean(axis=1)
    hit10 += int(np.sum(A10 >= 0.75))
est10 = hit10 / n10
se10 = sqrt(est10 * (1 - est10) / n10)
mc_check(10, "MC P(occupation >= 3/4), grid N=2000", "0.333333", 1 / 3, est10, se10, k=4, slack=0.01)
# density integrates to one over the tails: P(A <= 1/4) = P(A >= 3/4) by symmetry
line(10, "density 1/(pi sqrt(a(1-a))): P(A<=1/4) = 1/3", "1/3", f"{2 / pi * math.asin(sqrt(0.25)):.6f}",
     abs(2 / pi * math.asin(sqrt(0.25)) - 1 / 3) < 1e-12)

# ---------------- card 11: median of M_1 for standard BM on [0,1] ----------------
m11 = norm.ppf(0.75)
line(11, "median of M_1 = Phi^-1(3/4) = 0.6745", "0.6745", f"{m11:.6f}", abs(m11 - 0.6745) < 5e-5)
line(11, "P(M_1 <= m) = 2 Phi(m) - 1 at median", "1/2", f"{2 * norm.cdf(m11) - 1:.6f}", abs(2 * norm.cdf(m11) - 1 - 0.5) < 1e-12)
line(11, "E[M_1] = sqrt(2/pi) = 0.7979 > median", "0.7979", f"{sqrt(2 / pi):.4f}", sqrt(2 / pi) > m11)
N11, n11, chunks11 = 2000, 100_000, 10
below = 0
beta11 = 0.5826 * sqrt(1.0 / N11)
for _ in range(chunks11):
    m = n11 // chunks11
    Wp = np.cumsum(RNG.standard_normal((m, N11)) / sqrt(N11), axis=1)
    M11 = np.maximum(Wp.max(axis=1), 0) + beta11
    below += int(np.sum(M11 <= m11))
est11 = below / n11
se11 = sqrt(est11 * (1 - est11) / n11)
mc_check(11, "MC P(M_1 <= 0.6745), grid + correction", "0.5", 0.5, est11, se11, k=4, slack=0.01)

# ---------------- card 12: four tail bounds for X ~ Bin(100, 1/2), P(X >= 60) ----------------
n12 = 100
exact12 = F(sum(comb(n12, k) for k in range(60, n12 + 1)), 2**n12)
exact_check(12, "exact P(X>=60)", "0.0284", F(284, 10000), exact12, tol=5e-5)
line(12, "exact tail to 4 places", "0.0284", f"{float(exact12):.6f}", round(float(exact12), 4) == 0.0284)
markov = F(50, 60)
line(12, "Markov: E X / 60 = 5/6", "0.8333", f"{float(markov):.6f}", markov == F(5, 6))
cheb = F(25, 100)
line(12, "Chebyshev: Var/10^2 = 1/4", "0.25", str(cheb), cheb == F(1, 4))
D12 = 0.6 * log(1.2) + 0.4 * log(0.8)
mgf_bound = lambda lam: exp(-60 * lam) * ((1 + exp(lam)) / 2) ** 100
res = minimize_scalar(mgf_bound, bounds=(0, 5), method="bounded", options={"xatol": 1e-10})
chern_num = res.fun
chern_closed = exp(-100 * D12)
line(12, "Chernoff: optimised mgf bound = exp(-n D), D = KL", "0.1335", f"{chern_closed:.6f}",
     abs(chern_num - chern_closed) < 1e-9 and abs(chern_closed - 0.1335) < 5e-5)
line(12, "Chernoff KL value D(0.6||0.5) = 0.02014", "0.02014", f"{D12:.5f}", abs(D12 - 0.02014) < 5e-6)
hoeff = exp(-2 * 10**2 / 100)
line(12, "Hoeffding: exp(-2 t^2 / n), t = 10", "0.1353", f"{hoeff:.6f}", abs(hoeff - exp(-2)) < 1e-15)
line(12, "ordering: exact < Chernoff < Hoeffding < Chebyshev < Markov", "true",
     "true", float(exact12) < chern_closed < hoeff < 0.25 < 5 / 6)
n12m = 1_000_000
bs = RNG.binomial(100, 0.5, n12m)
e12 = np.mean(bs >= 60)
s12 = sqrt(e12 * (1 - e12) / n12m)
mc_check(12, "MC P(X>=60)", "0.0284", float(exact12), e12, s12)

# ---------------- card 13: Hoeffding sample size, eps = 0.02, delta = 0.05 ----------------
eps, delta = 0.02, 0.05
n_real = log(2 / delta) / (2 * eps**2)
n_ceil = math.ceil(n_real)
line(13, "n >= ln(2/delta)/(2 eps^2) = 4611.1", "4611.1", f"{n_real:.2f}", abs(n_real - 4611.0993) < 0.001)
ok13 = (2 * exp(-2 * n_ceil * eps**2) <= delta) and (2 * exp(-2 * (n_ceil - 1) * eps**2) > delta)
line(13, "minimal integer n = 4612", "4612", str(n_ceil), n_ceil == 4612 and ok13)
clt_n = (norm.ppf(0.975) / eps) ** 2 * 0.25
n_one = math.ceil(log(1 / delta) / (2 * eps**2))
line(13, "one-sided: n >= ln(1/delta)/(2 eps^2) = 3744.7, so 3745", "3745", str(n_one),
     abs(log(1 / delta) / (2 * eps**2) - 3744.67) < 0.01 and n_one == 3745
     and 2 * exp(-2 * n_one * eps**2) > 0 and exp(-2 * n_one * eps**2) <= delta)
line(13, "CLT contrast (p=1/2): (1.96/eps)^2/4 = 2401", "2401", f"{clt_n:.2f}", abs(clt_n - 2401) < 1)
n13m = 100_000
phat = RNG.binomial(n_ceil, 0.5, n13m) / n_ceil
fail = np.mean(np.abs(phat - 0.5) >= eps)
s13 = sqrt(fail * (1 - fail) / n13m)
line(13, "MC P(|phat - p| >= 0.02) at n=4612 <= 0.05", "<= 0.05", f"{fail:.5f} +- {s13:.5f}",
     fail <= 0.05)

# ---------------- card 14: Chebyshev equality case, Y in {-2,0,2} ----------------
pY = {F(-2): F(1, 8), F(0): F(3, 4), F(2): F(1, 8)}
EY = sum(v * q for v, q in pY.items())
VY = sum(v * v * q for v, q in pY.items())
tailY = sum(q for v, q in pY.items() if abs(v) >= 2)
line(14, "mean 0, variance 1, P(|Y|>=2) = 1/4", "1/4", str(tailY),
     EY == 0 and VY == 1 and tailY == F(1, 4))
line(14, "Chebyshev bound Var/2^2 = 1/4 attained", "1/4", str(F(1, 4)), F(VY, 4) == tailY)

# ---------------- card 15: toolkit card quotes the binomial example ----------------
line(15, "toolkit example: Hoeffding e^-2 = 0.135", "0.135", f"{exp(-2):.4f}", abs(exp(-2) - 0.1353) < 5e-5)

# ---------------- summary ----------------
n_pass = sum(rows)
print(f"SUMMARY: {len(rows)} checks, {n_pass} PASS, {len(rows) - n_pass} FAIL")
sys.exit(0 if n_pass == len(rows) else 1)
