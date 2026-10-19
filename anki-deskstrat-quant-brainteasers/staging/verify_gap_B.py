"""Verifies every numerical claim on staging/gap_B.json (card index = position in the array).

Exact values use fractions.Fraction or sympy. Every non-trivial probability or expectation is also
checked by Monte Carlo with >= 1e5 trials and a printed standard error (PASS if |mc - claim| <= 4 SE).
Run: python3 -I staging/verify_gap_B.py
"""
import itertools, math
from collections import Counter
from fractions import Fraction as F
from math import comb
import numpy as np
import sympy as sp

RNG = np.random.default_rng(20261019)
results = []


def report(idx, label, claimed, computed, ok=None, extra=""):
    if ok is None:
        if isinstance(claimed, F) or isinstance(computed, F):
            ok = (F(claimed) == F(computed))
        else:
            ok = abs(float(claimed) - float(computed)) < 1e-9
    results.append(ok)
    cl = f"{claimed}" if not isinstance(claimed, float) else f"{claimed:.6f}"
    co = f"{computed}" if not isinstance(computed, float) else f"{computed:.6f}"
    print(f"card {idx:2d} | {label:<44s} | claimed {cl:>14s} | computed {co:>14s} | {'PASS' if ok else 'FAIL'} {extra}")


def mc_check(idx, label, claimed, mean, se, n):
    ok = abs(mean - float(claimed)) <= 4 * se
    report(idx, label, float(claimed), mean, ok=ok, extra=f"(MC {mean:.5f} +- {se:.5f}, n={n})")


x = sp.symbols("x")
s = sp.symbols("s")

# ---------------- card 0: four fair dice, P(sum = 10), GF [s^10](s+...+s^6)^4 ----------------
cnt4 = sum(1 for t in itertools.product(range(1, 7), repeat=4) if sum(t) == 10)
report(0, "4 dice: number of outcomes with sum 10", 80, cnt4)
report(0, "4 dice: P(sum=10) = 5/81", F(5, 81), F(cnt4, 1296))
# GF: (s+..+s^6)^4 = s^4 (1-s^6)^4 (1-s)^{-4}; [s^10] = [s^6](1-s^6)^4(1-s)^{-4} = C(9,3) - 4*C(3,3)
report(0, "GF coefficient C(9,3)-4C(3,3)", 80, comb(9, 3) - 4 * comb(3, 3))
# symbolic check of the GF identity
poly = sp.expand((s + s**2 + s**3 + s**4 + s**5 + s**6) ** 4)
report(0, "sympy [s^10](s+..+s^6)^4 = 80", 80, int(poly.coeff(s, 10)))

# ---------------- card 1: branching, offspring uniform on {0,1,2} (critical) ----------------
fexpr = (1 + s + s**2) / 3
roots = sp.solve(sp.Eq(fexpr, s), s)
report(1, "fixed points of f(s)=s: only s=1", 1, 1 if set(roots) == {sp.Integer(1)} else 0)
report(1, "f'(1) = mean offspring = 1", 1, int(sp.diff(fexpr, s).subs(s, 1)))
report(1, "f(s)-s = (s-1)^2/3 (double root)", 1, 1 if sp.simplify(fexpr - s - (s - 1) ** 2 / 3) == 0 else 0)
# iterate f_n(0): extinction by generation n tends to 1 (slowly, critical case)
q = F(0)
for _ in range(1000):
    q = (1 + q + q * q) / 3
report(1, "f_1000(0) > 0.99 (extinction certain)", 1, 1 if float(q) > 0.99 else 0, extra=f"(f_1000(0)={float(q):.5f})")
q2 = (1 + F(1, 3) + F(1, 9)) / 3  # f(f(0)), f(0)=1/3
report(1, "P(Z_2 = 0) = f(f(0)) = 13/27", F(13, 27), q2)
N = 100000
g1 = RNG.integers(0, 3, size=N)
g2 = np.array([RNG.integers(0, 3, size=c).sum() if c > 0 else 0 for c in g1])
pz2 = float(np.mean(g2 == 0)); se = math.sqrt(pz2 * (1 - pz2) / N)
mc_check(1, "MC P(Z_2 = 0)", F(13, 27), pz2, se, N)

# ---------------- card 2: tilings of a 1 x n strip, a_n = a_{n-1} + 2 a_{n-2}, a_0 = a_1 = 1 ----------------
a = [1, 1]
for _ in range(2, 11):
    a.append(a[-1] + 2 * a[-2])
report(2, "a_10 from the recurrence", 683, a[10])
report(2, "closed form (2^{n+1}+(-1)^n)/3 at n=10", 683, (2 ** 11 + 1) // 3)
# GF A(x) = 1/(1-x-2x^2): partial fractions 2/3 * 1/(1-2x) + 1/3 * 1/(1+x)
gf = 1 / (1 - x - 2 * x**2)
pf = sp.Rational(2, 3) / (1 - 2 * x) + sp.Rational(1, 3) / (1 + x)
report(2, "partial fractions equal the GF (symbolic)", 1, 1 if sp.simplify(pf - gf) == 0 else 0)
ser = sp.series(gf, x, 0, 11).removeO()
report(2, "series coefficients match recurrence (n<=10)", 1,
       1 if all(int(ser.coeff(x, k)) == a[k] for k in range(11)) else 0)

# ---------------- card 3: parity of heads, n = 5 flips, P(H) = 1/4 ----------------
p = F(1, 4); q_ = 1 - p; n = 5
P_even = sum(comb(n, k) * p**k * q_**(n - k) for k in range(0, n + 1, 2))
report(3, "P(even heads) = 33/64 (binomial sum)", F(33, 64), P_even)
report(3, "(1+(q-p)^n)/2 identity", F(33, 64), (1 + (q_ - p) ** n) / 2)
report(3, "G(-1) = (q-p)^5 = 1/32", F(1, 32), (q_ - p) ** n)
heads = (RNG.random((N, n)) < 0.25).sum(axis=1)
pe = float(np.mean(heads % 2 == 0)); se = math.sqrt(pe * (1 - pe) / N)
mc_check(3, "MC P(even heads)", F(33, 64), pe, se, N)

# ---------------- card 4: Sicherman dice (twin) ----------------
A_f = [1, 2, 2, 3, 3, 4]; B_f = [1, 3, 4, 5, 6, 8]
S_new = Counter(u + v for u in A_f for v in B_f)
S_std = Counter(u + v for u in range(1, 7) for v in range(1, 7))
report(4, "sum distribution of Sicherman pair = standard", 1, 1 if S_new == S_std else 0)


def gf_of(faces):
    c = [0] * (max(faces) + 1)
    for f_ in faces:
        c[f_] += 1
    return c


def pmul(u, v):
    out = [0] * (len(u) + len(v) - 1)
    for i, a_ in enumerate(u):
        for j, b_ in enumerate(v):
            out[i + j] += a_ * b_
    return out


def trim(u):
    u = list(u)
    while len(u) > 1 and u[-1] == 0:
        u.pop()
    return u


T = trim(pmul(gf_of(range(1, 7)), gf_of(range(1, 7))))
report(4, "G_A G_B = (s+..+s^6)^2 as polynomials", 1,
       1 if trim(pmul(gf_of(A_f), gf_of(B_f))) == T else 0)
# factorisation check in sympy
GA = sp.expand(sum(s**f_ for f_ in A_f)); GB = sp.expand(sum(s**f_ for f_ in B_f))
fa = s * (1 + s) * (1 + s + s**2)
fb = s * (1 + s**3) * (1 + s + s**2) * (1 - s + s**2)
report(4, "G_A = s(1+s)(1+s+s^2)", 1, 1 if sp.expand(fa - GA) == 0 else 0)
report(4, "G_B = s(1+s^3)(1+s+s^2)(1-s+s^2)", 1, 1 if sp.expand(fb - GB) == 0 else 0)
# uniqueness: all multisets of 6 positive faces in 1..11 whose GF divides T with a face-multiset quotient
pols_T = sp.Poly(sum(s**f_ for f_ in range(1, 7)) ** 2, s)
sols = set()
for A in itertools.combinations_with_replacement(range(1, 12), 6):
    GAp = sp.Poly(sum(s**f_ for f_ in A), s)
    qq, rr = sp.div(pols_T, GAp)
    if rr.is_zero and all(c.is_integer and c >= 0 for c in qq.all_coeffs()):
        coeffs = qq.all_coeffs()[::-1]  # coefficient of s^k
        if coeffs[0] == 0 and sum(coeffs) == 6:
            B = tuple(sorted(k for k, c in enumerate(coeffs) for _ in range(int(c))))
            sols.add(tuple(sorted([tuple(sorted(A)), B])))
expected = {tuple(sorted([(1, 2, 3, 4, 5, 6), (1, 2, 3, 4, 5, 6)])),
            tuple(sorted([(1, 2, 2, 3, 3, 4), (1, 3, 4, 5, 6, 8)]))}
report(4, "only two face-pairs (standard, Sicherman)", 1, 1 if sols == expected else 0,
       extra=f"(found {len(sols)} unordered pairs)")
report(4, "E[sum] = 7 for the Sicherman pair (mean of each die)", 7, F(sum(A_f), 6) + F(sum(B_f), 6))

# ---------------- card 5: stochastic dominance, X = heads in 10 flips, Y = X + 2 more flips ----------------
p5 = F(3, 10)
P_gt = 1 - (1 - p5) ** 2  # Y > X iff at least one of the two extra flips is heads
report(5, "P(Y > X) = 1 - (7/10)^2 = 51/100", F(51, 100), P_gt)
report(5, "E[Y - X] = 2 * 3/10", F(3, 5), 2 * p5)
ok_tail = True
for t in range(-1, 13):
    tailX = sum(comb(10, k) * p5**k * (1 - p5) ** (10 - k) for k in range(10 + 1) if k > t)
    tailY = sum(comb(12, k) * p5**k * (1 - p5) ** (12 - k) for k in range(12 + 1) if k > t)
    ok_tail &= tailY >= tailX
report(5, "P(Y>t) >= P(X>t) for all t (dominance)", 1, 1 if ok_tail else 0)
flips = RNG.random((N, 12)) < 0.3
X5 = flips[:, :10].sum(1); Y5 = flips.sum(1)
report(5, "coupling gives Y >= X pointwise", 1, 1 if np.all(Y5 >= X5) else 0)
pg = float(np.mean(Y5 > X5)); se = math.sqrt(pg * (1 - pg) / N)
mc_check(5, "MC P(Y > X) under the coupling", P_gt, pg, se, N)

# ---------------- card 6: hypercube {0,1}^10, same-bit coupling (coupon collector) ----------------
n6 = 10
H10 = sum(F(1, i) for i in range(1, n6 + 1))
report(6, "same-bit coalescence: n H_n = 7381/252", F(7381, 252), n6 * H10)


def same_bit_times(T_, rng, n_):
    Xa = np.zeros((T_, n_), dtype=bool)
    Ya = np.ones((T_, n_), dtype=bool)  # antipodal start
    times = np.full(T_, -1)
    active = np.arange(T_)
    t = 0
    while active.size:
        t += 1
        c = rng.integers(0, n_, size=active.size)
        b = rng.random(active.size) < 0.5
        Xa[active, c] = b
        Ya[active, c] = b
        agree = np.all(Xa[active] == Ya[active], axis=1)
        times[active[agree]] = t
        active = active[~agree]
    return times


TM = 100000
tm = same_bit_times(TM, RNG, n6)
mc_check(6, "MC same-bit coalescence time mean", F(7381, 252), float(tm.mean()),
         float(tm.std(ddof=1) / math.sqrt(TM)), TM)
# what breaks: independent bits. Exact via k = # disagreeing coordinates (absorbing at 0)
Mx = sp.zeros(n6, n6); bvec = sp.zeros(n6, 1)
for k in range(1, n6 + 1):
    i = k - 1
    Mx[i, i] += sp.Rational(1, 2)
    down = sp.Rational(k, 2 * n6); up = sp.Rational(n6 - k, 2 * n6)
    if k - 1 >= 1:
        Mx[i, k - 2] -= down
    if k + 1 <= n6:
        Mx[i, k] -= up
    bvec[i] = 1
En = sp.Rational(Mx.LUsolve(bvec)[n6 - 1])
report(6, "independent bits: exact first-meeting time 149504/63", F(149504, 63), F(int(En.p), int(En.q)))
TI = 100000


def indep_bit_times(T_, rng, n_, cap=10**6):
    Xa = np.zeros((T_, n_), dtype=bool)
    Ya = np.ones((T_, n_), dtype=bool)
    times = np.full(T_, -1)
    active = np.arange(T_)
    t = 0
    while active.size and t < cap:
        t += 1
        c = rng.integers(0, n_, size=active.size)
        Xa[active, c] = rng.random(active.size) < 0.5
        Ya[active, c] = rng.random(active.size) < 0.5
        agree = np.all(Xa[active] == Ya[active], axis=1)
        times[active[agree]] = t
        active = active[~agree]
    return times


ti = indep_bit_times(TI, RNG, n6)
assert (ti >= 0).all()
mc_check(6, "MC independent-bit first meeting (mean)", F(149504, 63), float(ti.mean()),
         float(ti.std(ddof=1) / math.sqrt(TI)), TI)

# ---------------- card 7: CFTP on {0,1,2,3}, monotone reflecting walk ----------------
def step(xv, u):
    return min(xv + 1, 3) if u < 0.5 else max(xv - 1, 0)


Pm = [[F(0)] * 4 for _ in range(4)]
for xv in range(4):
    Pm[xv][min(xv + 1, 3)] += F(1, 2)
    Pm[xv][max(xv - 1, 0)] += F(1, 2)
unif = [F(1, 4)] * 4
piP = [sum(unif[i] * Pm[i][j] for i in range(4)) for j in range(4)]
report(7, "uniform is stationary (exact piP = pi)", 1, 1 if piP == unif else 0)


def cftp_sample(rng):
    inputs = {}
    T_ = 1
    while True:
        for t in range(-T_, 0):
            if t not in inputs:
                inputs[t] = rng.random()  # reuse old uniforms; never redraw
        states = [0, 1, 2, 3]
        for t in range(-T_, 0):
            states = [step(xv, inputs[t]) for xv in states]
        if len(set(states)) == 1:
            return states[0]
        T_ *= 2


M7 = 100000
samp = np.array([cftp_sample(RNG) for _ in range(M7)])
freq = np.bincount(samp, minlength=4) / M7
for xv in range(4):
    mc_check(7, f"CFTP frequency of state {xv}", F(1, 4), float(freq[xv]),
             math.sqrt(0.25 * 0.75 / M7), M7)

# ---------------- card 8: two biased coins, one uniform U ----------------
U = RNG.random(N)
A8 = U < 0.3; B8 = U < 0.6
pd = float(np.mean(A8 != B8)); se = math.sqrt(pd * (1 - pd) / N)
report(8, "exact P(differ) = |0.6 - 0.3| = 3/10", F(3, 10), abs(F(6, 10) - F(3, 10)))
mc_check(8, "MC P(flips differ), common U", F(3, 10), pd, se, N)

# ---------------- card 9: coupling inequality, Bin(4,1/2) vs Bin(4,1/3) ----------------
Xp = [F(comb(4, k), 16) for k in range(5)]
Yp = [F(comb(4, k) * 2 ** (4 - k), 81) for k in range(5)]
tv = sum(abs(u - v) for u, v in zip(Xp, Yp)) / 2
report(9, "TV distance = 121/432", F(121, 432), tv)
report(9, "overlap sum min(p,q) = 1 - TV", F(311, 432), sum(min(u, v) for u, v in zip(Xp, Yp)))
ov = [min(u, v) for u, v in zip(Xp, Yp)]
Z_ = sum(ov)
rx = [u - o for u, o in zip(Xp, ov)]; ry = [v - o for v, o in zip(Yp, ov)]
Zr = 1 - Z_
pc = np.array([float(o / Z_) for o in ov])
px = np.array([float(r / Zr) for r in rx]); py = np.array([float(r / Zr) for r in ry])
Nc = 100000
same = RNG.random(Nc) < float(Z_)
xv9 = np.empty(Nc, int); yv9 = np.empty(Nc, int)
common = RNG.choice(5, size=Nc, p=pc / pc.sum())
xv9[same] = common[same]; yv9[same] = common[same]
dif = ~same
xv9[dif] = RNG.choice(5, size=dif.sum(), p=px / px.sum())
yv9[dif] = RNG.choice(5, size=dif.sum(), p=py / py.sum())
pne = float(np.mean(xv9 != yv9))
mc_check(9, "maximal coupling: MC P(X != Y) = TV", tv, pne, math.sqrt(pne * (1 - pne) / Nc), Nc)
marg = np.allclose(np.bincount(xv9, minlength=5) / Nc, [float(v) for v in Xp], atol=0.01) and \
    np.allclose(np.bincount(yv9, minlength=5) / Nc, [float(v) for v in Yp], atol=0.01)
report(9, "maximal coupling has the right marginals", 1, 1 if marg else 0)

# ---------------- card 10: secretary, n = 10, objective = expected rank ----------------
nS = 10
Vk = {r: F(r) for r in range(1, nS + 1)}          # V_n(r) = r: hire the last candidate
policy = {nS: {r: True for r in range(1, nS + 1)}}
for k in range(nS - 1, 0, -1):
    C = sum(Vk[r] for r in range(1, k + 2)) / F(k + 1)  # continue: E[V_{k+1}(R_{k+1})]
    policy[k] = {r: (F(r * (nS + 1), k + 1) <= C) for r in range(1, k + 1)}
    Vk = {r: min(F(r * (nS + 1), k + 1), C) for r in range(1, k + 1)}
V_opt = Vk[1]
report(10, "optimal expected rank (DP) = 3223/1260", F(3223, 1260), V_opt)
Np = 1000000
vals = RNG.random((Np, nS))
ranks = np.argsort(np.argsort(-vals, axis=1), axis=1) + 1
stopped = np.zeros(Np, bool); chosen = np.zeros(Np)
for k in range(1, nS + 1):
    rel = 1 + np.sum(vals[:, :k] > vals[:, k - 1:k], axis=1)
    stop_here = np.zeros(Np, bool)
    for r in range(1, k + 1):
        if policy[k][r]:
            stop_here |= (rel == r)
    take = (~stopped) & stop_here
    chosen[take] = ranks[take, k - 1]
    stopped |= take
rem = ~stopped
chosen[rem] = ranks[rem, nS - 1]
mc_check(10, "MC of optimal DP policy, E[rank]", V_opt, float(chosen.mean()),
         float(chosen.std(ddof=1) / math.sqrt(Np)), Np)


def p_best_threshold(m, n_=nS):
    if m == 0:
        return F(1, n_)
    return F(m, n_) * sum(F(1, j - 1) for j in range(m + 1, n_ + 1))


best_m = max(range(0, nS), key=lambda m: p_best_threshold(m))
report(10, "1/e-type threshold m=3 maximises P(best) for n=10", 3, best_m)
P_best3 = p_best_threshold(3)
report(10, "P(best) with threshold 3 = 0.3987 (2 d.p. 0.40)", 1,
       1 if abs(float(P_best3) - 0.40) < 0.005 else 0, extra=f"(exact {float(P_best3):.5f})")
# expected rank of the classic 1/e rule (m=3), via E[rank | rel. rank 1 at k] = (n+1)/(k+1)
m3 = 3
E_rule = F(0)
pno = F(1)  # P(no selection among m+1..k-1)
for k in range(m3 + 1, nS + 1):
    pk = pno / k
    E_rule += pk * F(nS + 1, k + 1)
    pno *= (1 - F(1, k))
# nothing selected: last candidate forced, its absolute rank has mean r given relative rank r
E_rule += pno * sum(F(1, nS) * r for r in range(2, nS + 1))
rule_e = np.zeros(Np); sel = np.zeros(Np, bool)
for k in range(1, nS + 1):
    rel = 1 + np.sum(vals[:, :k] > vals[:, k - 1:k], axis=1)
    if k > m3:
        take = (~sel) & (rel == 1)
        rule_e[take] = ranks[take, k - 1]; sel |= take
rem = ~sel; rule_e[rem] = ranks[rem, nS - 1]
mc_check(10, "1/e rule (m=3) E[rank]: formula vs MC", E_rule, float(rule_e.mean()),
         float(rule_e.std(ddof=1) / math.sqrt(Np)), Np)
report(10, "1/e rule is NOT optimal for E[rank]: E_rule > optimum", 1, 1 if E_rule > V_opt else 0,
       extra=f"(E_rule={float(E_rule):.4f})")

# ---------------- card 11: house selling, c = 0.02, offers U(0,1), first offer free ----------------
c11 = 0.02
w11 = 1 - math.sqrt(2 * c11)
report(11, "reservation price w = 1 - sqrt(2c) = 0.8", 0.8, w11)
report(11, "value V = w + c = 0.82", 0.82, w11 + c11)
wsym = sp.symbols("w")
quad = sp.Eq(wsym ** 2 - 2 * wsym + 1 - 2 * sp.Rational(2, 100), 0)  # from (1+w^2)/2 = w + c
report(11, "w solves w^2 - 2w + 1 - 2c = 0", 1, 1 if sp.simplify(quad.lhs.subs(wsym, sp.Rational(4, 5))) == 0 else 0)
Vfp = w11 + c11
rhs = (Vfp - c11) + (1 - (Vfp - c11)) ** 2 / 2   # E[max(X, w)] = w + (1-w)^2/2
report(11, "fixed point V = E[max(X, V-c)]", 0.82, rhs)
Nh = 100000
offers = RNG.random((Nh, 200))
j_acc = np.argmax(offers >= w11, axis=1)
price = offers[np.arange(Nh), j_acc]
net = price - j_acc * c11
mc_check(11, "MC expected net value of the policy", 0.82, float(net.mean()),
         float(net.std(ddof=1) / math.sqrt(Nh)), Nh)

# ---------------- card 12: stop-the-die with up to 4 rolls ----------------
def cont(Wm):
    return sum(max(F(v), Wm) for v in range(1, 7)) / F(6)


W1 = F(7, 2); W2 = cont(W1); W3 = cont(W2); W4 = cont(W3)
report(12, "V with 2 rolls = 17/4", F(17, 4), W2)
report(12, "V with 3 rolls = 14/3", F(14, 3), W3)
report(12, "V with 4 rolls = 89/18", F(89, 18), W4)
Nd = 200000
tot = np.zeros(Nd); active = np.ones(Nd, bool)
th = {4: float(W3), 3: float(W2), 2: float(W1)}
for m_left in range(4, 0, -1):
    xr = RNG.integers(1, 7, size=Nd)
    if m_left == 1:
        tot[active] = xr[active]
        break
    stop = active & (xr >= th[m_left])
    tot[stop] = xr[stop]
    active &= ~stop
mc_check(12, "MC of optimal stop rule, 4 rolls", W4, float(tot.mean()),
         float(tot.std(ddof=1) / math.sqrt(Nd)), Nd)

# ---------------- card 13: one-step lookahead failure ----------------
R1 = F(1)
EY = F(7, 10) * 0 + F(3, 10) * 3          # next reward R2 has mean 0.9
report(13, "one-step rule: stop because 1 >= E[R2] = 0.9", 1, 1 if R1 >= EY else 0)
report(13, "E[R2] = 9/10", F(9, 10), EY)
cont13 = F(7, 10) * max(F(0), F(2)) + F(3, 10) * max(F(3), F(2))  # at t=2 stop iff R2 >= 2
report(13, "optimal value of continuing = 23/10", F(23, 10), cont13)
report(13, "optimal beats the one-step stop", 1, 1 if cont13 > R1 else 0)

# ---------------- card 14: odds algorithm, p_k = 1/(k+1), k = 1..10 ----------------
nO = 10
pk = {k: F(1, k + 1) for k in range(1, nO + 1)}
rk = {k: pk[k] / (1 - pk[k]) for k in pk}
s_star = max(t for t in range(1, nO + 1) if sum(rk[k] for k in range(t, nO + 1)) >= 1)
report(14, "odds threshold s = 4", 4, s_star)
tail = sum(rk[k] for k in range(s_star, nO + 1))
report(14, "sum of odds from s to 10 = 2761/2520", F(2761, 2520), tail)
qprod = F(1)
for k in range(s_star, nO + 1):
    qprod *= (1 - pk[k])
win = qprod * tail
report(14, "P(win) = prod(1-p_k) * sum r_k = 251/630", F(251, 630), win)
report(14, "P(win) >= 1/e", 1, 1 if float(win) >= 1 / math.e else 0)
No = 200000
ev = RNG.random((No, nO)) < np.array([float(pk[k]) for k in range(1, nO + 1)])
chosen14 = np.full(No, -1)
for k in range(1, nO + 1):
    take = (chosen14 < 0) & (k >= s_star) & ev[:, k - 1]
    chosen14[take] = k
last = np.where(ev.any(axis=1), nO - np.argmax(ev[:, ::-1], axis=1), -1)
pw = float(np.mean((chosen14 > 0) & (chosen14 == last))); se = math.sqrt(pw * (1 - pw) / No)
mc_check(14, "MC P(win) with the threshold rule", F(251, 630), pw, se, No)

# ---------------- summary ----------------
print()
print(f"SUMMARY: {sum(results)}/{len(results)} checks PASS" + ("" if all(results) else "  -- FAILURES PRESENT"))
