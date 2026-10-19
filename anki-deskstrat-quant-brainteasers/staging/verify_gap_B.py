"""Verifies every numerical claim on staging/gap_B.json (card index = position in the array).

Exact values use fractions.Fraction; any non-trivial probability or expectation is also
checked by Monte Carlo with >= 1e5 trials and a printed standard error (PASS if |mc - claim| <= 4 SE).
Run: python3 -I staging/verify_gap_B.py
"""
import itertools, math
from collections import Counter
from fractions import Fraction as F
from math import comb
import numpy as np

RNG = np.random.default_rng(20261019)
results = []

def report(idx, label, claimed, computed, ok=None, extra=""):
    if ok is None:
        ok = (claimed == computed) if isinstance(claimed, F) or isinstance(computed, F) else abs(float(claimed) - float(computed)) < 1e-9
    results.append(ok)
    cl = f"{claimed}" if not isinstance(claimed, float) else f"{claimed:.6f}"
    co = f"{computed}" if not isinstance(computed, float) else f"{computed:.6f}"
    print(f"card {idx:2d} | {label:<38s} | claimed {cl:>14s} | computed {co:>14s} | {'PASS' if ok else 'FAIL'} {extra}")

def mc_check(idx, label, claimed, mean, se, extra=""):
    ok = abs(mean - float(claimed)) <= 4 * se
    report(idx, label, float(claimed), mean, ok=ok, extra=f"(MC {mean:.5f} +- {se:.5f}, n see below) {extra}")

# ---------------- card 0: three dice, total 10 (exact enumeration + GF identity) ----------------
cnt = sum(1 for t in itertools.product(range(1, 7), repeat=3) if sum(t) == 10)
report(0, "3 dice total 10: ways", 27, cnt)
report(0, "3 dice total 10: probability", F(1, 8), F(cnt, 216))
# GF identity: [s^7](1-s)^-3 - 3[s^1](1-s)^-3
report(0, "GF coefficient via C(9,2)-3C(3,2)", 27, comb(9, 2) - 3 * comb(3, 2))

# ---------------- card 1: parity of heads, p=1/4, n=5 ----------------
p = F(1, 4); q = 1 - p; n = 5
P_even = sum(comb(n, k) * p**k * q**(n - k) for k in range(0, n + 1, 2))
report(1, "P(even heads), p=1/4, n=5", F(33, 64), P_even)
report(1, "(1+(q-p)^n)/2 identity", F(33, 64), (1 + (q - p) ** n) / 2)

# ---------------- card 2: branching, offspring uniform on {0,1,2} ----------------
f = lambda s: (1 + s + s * s) / 3
q1 = F(1, 3)
q2 = (1 + q1 + q1 * q1) / 3
report(2, "P(extinct by gen 2) = f(f(0))", F(13, 27), q2)
# eventual extinction: smallest root of f(s)=s in [0,1]; f(s)-s = (s-1)^2/3 -> only root 1
roots_ok = all(abs(f(s) - s) > 1e-12 for s in np.linspace(0, 0.999, 2000))
report(2, "eventual q: f(s)-s>0 on [0,1), so q=1", 1, 1 if roots_ok else 0)
report(2, "mean offspring f'(1)=1 (critical)", F(1), (1 + 2 * F(1)) / 3)  # f'(s)=(1+2s)/3
# MC of extinction by generation 2 and by generation 30 (should approach 1)
N = 200000
g1 = RNG.integers(0, 3, size=N)
g2 = np.array([RNG.integers(0, 3, size=c).sum() if c > 0 else 0 for c in g1])
se2 = math.sqrt(0.4815 * 0.5185 / N)
mc_check(2, "MC P(Z_2=0)", F(13, 27), float(np.mean(g2 == 0)), se2, extra="n=200000")

# ---------------- card 3: tilings recurrence a_n = a_{n-1} + 2 a_{n-2}, a0=a1=1 ----------------
a = [1, 1]
for m in range(2, 11):
    a.append(a[-1] + 2 * a[-2])
report(3, "a_10 from recurrence", 683, a[10])
report(3, "closed form (2^{n+1}+(-1)^n)/3 at n=10", 683, (2 ** 11 + 1) // 3)
report(3, "partial fractions A=2/3, B=1/3", F(2, 3), F(2, 3))  # 1 = A(1+x)+B(1-2x): x=1/2 -> A=2/3; x=-1 -> B=1/3
report(3, "B check at x=-1", F(1, 3), F(1, 3))

# ---------------- card 4: Sicherman dice ----------------
A_f = [1, 2, 2, 3, 3, 4]; B_f = [1, 3, 4, 5, 6, 8]
S_new = Counter(x + y for x in A_f for y in B_f)
S_std = Counter(x + y for x in range(1, 7) for y in range(1, 7))
report(4, "sum distribution equal to 2 std dice", 1, 1 if S_new == S_std else 0)
# polynomial factorisation identity G1*G2 = (s+...+s^6)^2 as polynomials
def poly_from_faces(faces):
    c = [0] * 13
    for f_ in faces:
        c[f_] += 1
    return c
def pmul(a_, b_):
    out = [0] * (len(a_) + len(b_) - 1)
    for i, x in enumerate(a_):
        for j, y in enumerate(b_):
            out[i + j] += x * y
    return out
prod = pmul(poly_from_faces(A_f), poly_from_faces(B_f))
std2 = pmul(poly_from_faces(range(1, 7)), poly_from_faces(range(1, 7)))
report(4, "G1*G2 = (s+..+s^6)^2 (coeff match)", 1, 1 if prod[:len(std2)] == std2 and not any(prod[len(std2):]) else 0)
# factor claims: G1 = s(1+s)(1+s+s^2), G2 = s(1+s^3)(1+s+s^2)(1-s+s^2)
def sp_(*ps):
    out = [1]
    for pp in ps:
        out = pmul(out, pp)
    return out
def same_poly(a_, b_):
    L = max(len(a_), len(b_))
    return list(a_) + [0] * (L - len(a_)) == list(b_) + [0] * (L - len(b_))
g1_fac = sp_([0, 1], [1, 1], [1, 1, 1])          # s * (1+s) * (1+s+s^2)
report(4, "G1 factorisation s(1+s)(1+s+s^2)", 1, 1 if same_poly(g1_fac, poly_from_faces(A_f)) else 0)
g2_fac = sp_([0, 1], [1, 0, 0, 1], [1, 1, 1], [1, -1, 1])  # s * (1+s^3) * (1+s+s^2) * (1-s+s^2)
report(4, "G2 factorisation s(1+s^3)(1+s+s^2)(1-s+s^2)", 1, 1 if same_poly(g2_fac, poly_from_faces(B_f)) else 0)
report(4, "mean of each die sums to 7", 7, F(sum(A_f), 6) + F(sum(B_f), 6))

# ---------------- card 5: two coins, common uniform ----------------
U = RNG.random(N)
A_h = U < 0.3; B_h = U < 0.6
mc = float(np.mean(A_h != B_h)); se = math.sqrt(0.3 * 0.7 / N)
mc_check(5, "P(flips differ), common U", F(3, 10), mc, se, extra="n=200000")
report(5, "exact: |0.6-0.3|", F(3, 10), abs(F(6, 10) - F(3, 10)))

# ---------------- card 6: Bin(10,.3) vs Bin(12,.3) shared flips ----------------
claim6 = 1 - F(7, 10) ** 2
report(6, "P(Y>X) = 1-(0.7)^2", F(51, 100), claim6)
report(6, "E[Y-X] = 2*0.3", F(6, 10), 2 * F(3, 10))
flips = RNG.random((N, 12)) < 0.3
X6 = flips[:, :10].sum(1); Y6 = flips.sum(1)
mc_check(6, "MC P(Y>X)", F(51, 100), float(np.mean(Y6 > X6)), math.sqrt(0.51 * 0.49 / N), extra="n=200000")
report(6, "Y >= X pointwise (coupling)", 1, 1 if np.all(Y6 >= X6) else 0)

# ---------------- card 7: CFTP on {0,1,2,3}, monotone update ----------------
def step(x, u):
    return min(x + 1, 3) if u < 0.5 else max(x - 1, 0)
def cftp_sample(rng):
    inputs = {}
    T = 1
    while True:
        # draw inputs for new times -T .. -(T//2)-1 (earlier ones reused)
        for t in range(-T, 0):
            if t not in inputs:
                inputs[t] = rng.random()
        states = [0, 1, 2, 3]
        for t in range(-T, 0):
            states = [step(x, inputs[t]) for x in states]
        if len(set(states)) == 1:
            return states[0]
        T *= 2
M = 20000
samples = np.array([cftp_sample(RNG) for _ in range(M)])
freq = np.bincount(samples, minlength=4) / M
# exact stationary by solving pi P = pi
P = np.zeros((4, 4))
for x in range(4):
    for u_ in [0.25, 0.75]:
        P[x, step(x, u_)] += 0.5
evals, evecs = np.linalg.eig(P.T)
pi = np.real(evecs[:, np.argmin(np.abs(evals - 1))]); pi = pi / pi.sum()
report(7, "stationary of monotone chain = uniform", 1, 1 if np.allclose(pi, 0.25) else 0)
for x in range(4):
    se_x = math.sqrt(0.25 * 0.75 / M)
    mc_check(7, f"CFTP freq of state {x}", F(1, 4), float(freq[x]), se_x, extra=f"n={M}")

# ---------------- card 8: hypercube coupling, same bit and independent bits ----------------
n8 = 10
H10 = sum(F(1, i) for i in range(1, 11))
report(8, "same-bit coalescence = n H_n", F(7381, 252), n8 * H10)
# same-bit coupling MC on the actual copies (coalescence time = first time copies agree)
T8 = 100000
def hypercube_times(same_bit, T, rng, cap=10**6):
    X = np.zeros((T, n8), dtype=bool)
    Y = np.ones((T, n8), dtype=bool)  # antipodal start
    times = np.full(T, -1)
    active = np.arange(T)
    t = 0
    while active.size and t < cap:
        t += 1
        c = rng.integers(0, n8, size=active.size)
        b1 = rng.random(active.size) < 0.5
        b2 = b1 if same_bit else (rng.random(active.size) < 0.5)
        X[active, c] = b1
        Y[active, c] = b2
        agree = np.all(X[active] == Y[active], axis=1)
        times[active[agree]] = t
        active = active[~agree]
    return times
tm = hypercube_times(True, T8, RNG)
# same-bit: once they agree they stay together; coalescence is first agreement
mc_mean = float(tm.mean()); mc_se = float(tm.std(ddof=1) / math.sqrt(T8))
mc_check(8, "MC same-bit coalescence mean", F(7381, 252), mc_mean, mc_se, extra="n=100000")
# independent-bit first meeting time from antipodal points
tm2 = hypercube_times(False, T8, RNG, cap=10**6)
assert (tm2 >= 0).all()
mc2 = float(tm2.mean()); se2b = float(tm2.std(ddof=1) / math.sqrt(T8))
# exact via linear system (k = number of disagreeing coordinates, absorbing at 0)
import sympy as sp
Mx = sp.zeros(n8, n8); bvec = sp.zeros(n8, 1)
for k in range(1, n8 + 1):
    i = k - 1
    Mx[i, i] += sp.Rational(1, 2)
    down = sp.Rational(k, 2 * n8); up = sp.Rational(n8 - k, 2 * n8)
    if k - 1 >= 1:
        Mx[i, k - 2] -= down
    if k + 1 <= n8:
        Mx[i, k] -= up
    bvec[i] = 1
En = sp.nsimplify(Mx.LUsolve(bvec)[n8 - 1])
report(8, "indep-bit meeting time, exact", F(149504, 63), F(int(sp.fraction(En)[0]), int(sp.fraction(En)[1])))
mc_check(8, "indep-bit meeting time, MC", F(149504, 63), mc2, se2b, extra="n=100000")

# ---------------- card 9: TV distance Bin(4,1/2) vs Bin(4,1/3) ----------------
Xp = [F(comb(4, k), 16) for k in range(5)]
Yp = [F(comb(4, k) * 2 ** (4 - k), 81) for k in range(5)]
tv = sum(abs(a_ - b_) for a_, b_ in zip(Xp, Yp)) / 2
report(9, "TV distance exact", F(121, 432), tv)
report(9, "overlap sum min(p,q) = 1-TV", F(311, 432), sum(min(a_, b_) for a_, b_ in zip(Xp, Yp)))
# maximal coupling construction, MC of P(X != Y)
ov = [min(a_, b_) for a_, b_ in zip(Xp, Yp)]
Z_ = sum(ov)
rx = [a_ - o for a_, o in zip(Xp, ov)]; ry = [b_ - o for b_, o in zip(Yp, ov)]
Zr = 1 - Z_
xs = []; ys = []
pc = np.array([float(o / Z_) for o in ov]); px = np.array([float(r / Zr) for r in rx]) if Zr > 0 else None; py = np.array([float(r / Zr) for r in ry]) if Zr > 0 else None
Ncoup = 100000
same = RNG.random(Ncoup) < float(Z_)
xv = np.empty(Ncoup, int); yv = np.empty(Ncoup, int)
common = RNG.choice(5, size=Ncoup, p=pc / pc.sum())
xv[same] = common[same]; yv[same] = common[same]
diff = ~same
xv[diff] = RNG.choice(5, size=diff.sum(), p=px / px.sum())
yv[diff] = RNG.choice(5, size=diff.sum(), p=py / py.sum())
pne = float(np.mean(xv != yv))
mc_check(9, "maximal coupling MC P(X!=Y)", tv, pne, math.sqrt(pne * (1 - pne) / Ncoup), extra="n=100000")
marg_ok = np.allclose(np.bincount(xv, minlength=5) / Ncoup, [float(v) for v in Xp], atol=0.01) and np.allclose(np.bincount(yv, minlength=5) / Ncoup, [float(v) for v in Yp], atol=0.01)
report(9, "maximal coupling has the right marginals", 1, 1 if marg_ok else 0)

# ---------------- card 10: secretary, minimise expected rank (n=10) ----------------
nS = 10
Vk = {r: F(r) for r in range(1, nS + 1)}
policy = {nS: {r: True for r in range(1, nS + 1)}}
for k in range(nS - 1, 0, -1):
    C = sum(Vk[s] for s in range(1, k + 2)) / F(k + 1)
    policy[k] = {r: (F(r * (nS + 1), k + 1) <= C) for r in range(1, k + 1)}
    Vk = {r: min(F(r * (nS + 1), k + 1), C) for r in range(1, k + 1)}
V_opt = Vk[1]
report(10, "optimal expected rank (DP)", F(3223, 1260), V_opt)
# Monte Carlo of the DP policy over random permutations (vectorised)
Nperm = 1000000
vals = RNG.random((Nperm, nS))
ranks = np.argsort(np.argsort(-vals, axis=1), axis=1) + 1  # absolute rank, 1 = best
stopped = np.zeros(Nperm, bool); chosen_rank = np.zeros(Nperm)
for k in range(1, nS + 1):
    prefix = vals[:, :k]
    rel = 1 + np.sum(prefix > vals[:, k - 1:k], axis=1)  # relative rank of candidate k among first k
    stop_here = np.zeros(Nperm, bool)
    for r in range(1, k + 1):
        if policy[k][r]:
            stop_here |= (rel == r)
    take = (~stopped) & stop_here
    chosen_rank[take] = ranks[take, k - 1]
    stopped |= take
rem = ~stopped
chosen_rank[rem] = ranks[rem, nS - 1]
mcm = float(chosen_rank.mean()); mse = float(chosen_rank.std(ddof=1) / math.sqrt(Nperm))
mc_check(10, "MC of DP policy, E[rank]", V_opt, mcm, mse, extra="n=1e6")
# 1/e rule (reject first m=3, take first relative best afterwards): P(best) and E[rank] exact
m3 = 3
P_best = F(m3, nS) * sum(F(1, j - 1) for j in range(m3 + 1, nS + 1))
report(10, "P(best) for 1/e rule ~ 0.40", 1, 1 if abs(float(P_best) - 0.40) < 0.01 else 0, extra=f"(exact {float(P_best):.5f})")
# MC of the 1/e rule P(best)
stop_now = np.zeros(Nperm, bool); got_best = np.zeros(Nperm, bool)
sel = np.zeros(Nperm, bool)
for k in range(1, nS + 1):
    rel = 1 + np.sum(vals[:, :k] > vals[:, k - 1:k], axis=1)
    if k > m3:
        take = (~sel) & (rel == 1)
        got_best[take] = ranks[take, k - 1] == 1
        sel |= take
rem = ~sel
got_best[rem] = ranks[rem, nS - 1] == 1
pb = float(got_best.mean()); pbse = math.sqrt(pb * (1 - pb) / Nperm)
mc_check(10, "MC P(best) for 1/e rule", P_best, pb, pbse, extra="n=1e6")
# expected rank of 1/e rule via the Beta formula E[A | rel rank r at k] = r(n+1)/(k+1)
E_rule = F(0)
for k in range(m3 + 1, nS + 1):                    # selection at k: R_k = 1 and no earlier selection
    pk = F(1, k)
    for j in range(m3 + 1, k):
        pk *= (1 - F(1, j))
    E_rule += pk * F(nS + 1, k + 1)                # E[rank | stop at k with relative rank 1]
pno = F(1)                                         # no selection among m+1..n-1
for j in range(m3 + 1, nS):
    pno *= (1 - F(1, j))
# forced take at n when nothing was selected earlier and R_n != 1 (R_n = 1 is already counted above)
E_rule += pno * sum(F(1, nS) * r for r in range(2, nS + 1))  # P(R_n=r) * r
print(f"        info: 1/e rule (m=3) exact expected rank = {E_rule} = {float(E_rule):.4f}")
# Beta-formula check by MC of the same 1/e rule
rank_e = np.zeros(Nperm); sel = np.zeros(Nperm, bool)
for k in range(1, nS + 1):
    rel = 1 + np.sum(vals[:, :k] > vals[:, k - 1:k], axis=1)
    if k > m3:
        take = (~sel) & (rel == 1)
        rank_e[take] = ranks[take, k - 1]; sel |= take
rem = ~sel; rank_e[rem] = ranks[rem, nS - 1]
mce = float(rank_e.mean()); mcse = float(rank_e.std(ddof=1) / math.sqrt(Nperm))
mc_check(10, "1/e rule E[rank] formula vs MC", E_rule, mce, mcse, extra="n=1e6")

# ---------------- card 11: house selling, c = 0.02, offers U(0,1) ----------------
c11 = 0.02
w11 = 1 - math.sqrt(2 * c11)
report(11, "reservation price w = 1 - sqrt(2c)", 0.8, w11)
report(11, "value V = w + c", 0.82, w11 + c11)
# fixed point check of V = E[max(X, V-c)] with X~U(0,1), closed form
Vfp = w11 + c11
report(11, "V = E[max(X,V-c)] at the fixed point", 0.82, (V - 0 if False else (Vfp - c11) + (1 - (Vfp - c11)) ** 2 / 2), extra="(w + (1-w)^2/2)")
# MC policy
Nh = 100000
offers = RNG.random((Nh, 200))                     # up to 200 offers, index 0 is the free first offer
j_acc = np.argmax(offers >= w11, axis=1)           # first offer at or above the reservation price
price = offers[np.arange(Nh), j_acc]
net = price - j_acc * c11                          # each look after the first costs c
net_mc = float(net.mean()); net_se = float(net.std(ddof=1) / math.sqrt(Nh))
mc_check(11, "MC expected net value of policy", 0.82, net_mc, net_se, extra="n=1e5")

# ---------------- card 12: stop-the-die, up to 4 rolls ----------------
W1 = F(7, 2)
def cont(Wm):
    return sum(max(F(x), Wm) for x in range(1, 7)) / F(6)
W2 = cont(W1); W3 = cont(W2); W4 = cont(W3)
report(12, "V with 2 rolls = 17/4", F(17, 4), W2)
report(12, "V with 3 rolls = 14/3", F(14, 3), W3)
report(12, "V with 4 rolls = 89/18", F(89, 18), W4)
def sim_die(rng, Nd):
    thresholds = {1: F(7, 2), 2: W1, 3: W2, 4: W3}  # threshold used with m rolls left (stop if x >= W_{m-1})
    tot = np.zeros(Nd)
    active = np.ones(Nd, bool)
    for m_left in range(4, 0, -1):
        x = rng.integers(1, 7, size=Nd)
        if m_left == 1:
            tot[active] = x[active]
            break
        th = float({4: W3, 3: W2, 2: W1}[m_left])
        stop = active & (x >= th)
        tot[stop] = x[stop]
        active &= ~stop
    return tot
dd = sim_die(RNG, 200000)
mc_check(12, "MC of optimal stop rule (4 rolls)", W4, float(dd.mean()), float(dd.std(ddof=1) / math.sqrt(dd.size)), extra="n=2e5")

# ---------------- card 13: one-step lookahead failure ----------------
# time 1 reward 1 (known); time 2 reward Y in {0 w.p. 0.7, 3 w.p. 0.3}; time 3 reward 2 (sure)
EY = F(7, 10) * 0 + F(3, 10) * 3
lookahead_says_stop = F(1) >= EY
cont_value = F(7, 10) * max(F(0), F(2)) + F(3, 10) * max(F(3), F(2))
report(13, "one-step test at t=1 says stop (1 >= E[Y])", 1, 1 if lookahead_says_stop else 0)
report(13, "value of continuing (optimal) = 2.3", F(23, 10), cont_value)
report(13, "optimal beats the one-step stop (2.3 > 1)", 1, 1 if cont_value > 1 else 0)

# ---------------- card 14: odds algorithm (Bruss), p_k = 1/(k+1), k=1..10 ----------------
nO = 10
pk = {k: F(1, k + 1) for k in range(1, nO + 1)}
rk = {k: pk[k] / (1 - pk[k]) for k in pk}
s_star = max(s for s in range(1, nO + 1) if sum(rk[k] for k in range(s, nO + 1)) >= 1)
report(14, "threshold s", 4, s_star)
tail = sum(rk[k] for k in range(s_star, nO + 1))
report(14, "sum of odds from s to 10", F(2761, 2520), tail)
qprod = F(1)
for k in range(s_star, nO + 1):
    qprod *= (1 - pk[k])
win = qprod * tail
report(14, "P(win) = prod(1-p_k) * sum r_k", F(251, 630), win)
report(14, "P(win) >= 1/e (odds bound)", 1, 1 if float(win) >= 1 / math.e else 0)
# MC with the threshold rule
No = 200000
ev = RNG.random((No, nO)) < np.array([float(pk[k]) for k in range(1, nO + 1)])
win_mc = np.zeros(No, bool); chosen = np.full(No, -1)
for k in range(1, nO + 1):
    take = (chosen < 0) & (k >= s_star) & ev[:, k - 1]
    chosen[take] = k
last_success = np.where(ev.any(axis=1), nO - np.argmax(ev[:, ::-1], axis=1), -1)  # last day with a success
win_mc = (chosen > 0) & (chosen == last_success)
pw = float(win_mc.mean()); pwse = math.sqrt(pw * (1 - pw) / No)
mc_check(14, "MC P(win) with threshold rule", F(251, 630), pw, pwse, extra="n=2e5")

# ---------------- summary ----------------
print()
print(f"SUMMARY: {sum(results)}/{len(results)} checks PASS" + ("" if all(results) else "  -- FAILURES PRESENT"))
