"""Figures for cards/11_rebuild_connect.json (rebuild / derive cards)."""
import itertools, math
from fractions import Fraction
import numpy as np
from matplotlib.patches import Wedge
from qcfig import *


def Phi(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def bs_call(S, K, r, T, sig):
    d1 = (math.log(S / K) + (r + 0.5 * sig * sig) * T) / (sig * math.sqrt(T))
    d2 = d1 - sig * math.sqrt(T)
    return S * Phi(d1) - K * math.exp(-r * T) * Phi(d2)


# ---------- 1. derangement limit (card 1) ----------
@figure("f11_derangement_limit", w=4.6, h=2.5)
def _(ax):
    D = [1]
    for n in range(1, 11):
        D.append(n * D[-1] + (-1) ** n)          # D_n = n D_{n-1} + (-1)^n
    assert D[2] * 2 == 2 * 1 and abs(D[2] / 2 - 1 / 2) < 1e-12 and abs(D[3] / 6 - 1 / 3) < 1e-12
    ns = np.arange(1, 11)
    ratio = np.array([D[n] / math.factorial(n) for n in ns])
    ax.plot(ns, ratio, "o-", color=BLUE, ms=4.5, lw=1.2)
    ax.axhline(1 / math.e, color=ORANGE, ls="--", lw=1.2)
    ax.text(10, 1 / math.e + 0.03, r"$1/e$", color=ORANGE, ha="right", fontsize=10)
    ax.annotate(r"$n=2$: $\frac{1}{2}$", xy=(2, 0.5), xytext=(3.2, 0.5), fontsize=9,
                arrowprops=dict(arrowstyle="-", color=INK, lw=0.7))
    ax.set_xticks(range(1, 11)); ax.set_xlabel("$n$"); ax.set_ylabel(r"$D_n/n!$")
    ax.set_ylim(-0.05, 0.62)
    ax.set_title(r"$D_n/n!=\sum_{k=0}^{n}(-1)^k/k!\to 1/e$", fontsize=10)


# ---------- 2. birthday bound (card 4) ----------
@figure("f11_birthday_bound", w=5.0, h=2.8)
def _(ax):
    N = 365
    n = np.arange(1, 61)
    exact = np.array([1 - np.prod([1 - i / N for i in range(k)]) for k in n])
    bound = 1 - np.exp(-n * (n - 1) / (2 * N))
    assert np.all(bound <= exact + 1e-12)
    assert abs(exact[22] - 0.5073) < 1e-3 and abs(bound[22] - 0.5000) < 1e-3
    ax.plot(n, exact, color=BLUE, lw=1.8, label="exact")
    ax.plot(n, bound, color=ORANGE, lw=1.5, ls="--", label=r"bound $1-e^{-n(n-1)/(2N)}$")
    ax.axhline(0.5, color=GREY, lw=0.9, ls=":")
    ax.axvline(math.sqrt(2 * N * math.log(2)), color=GREY, lw=0.9, ls=":")
    ax.plot([23], [exact[22]], "o", color=BLUE, ms=5)
    ax.annotate(f"n=23, N=365: exact {exact[22]:.3f}, bound {bound[22]:.3f}", xy=(23, exact[22]),
                xytext=(30, 0.2), fontsize=9, arrowprops=dict(arrowstyle="-", color=INK, lw=0.7))
    ax.text(23.6, 0.03, r"$\sqrt{2N\ln 2}\approx 22.5$", fontsize=9, color=GREY)
    ax.set_xlabel("people $n$"); ax.set_ylabel("P(shared birthday)")
    ax.set_ylim(0, 1.02)
    ax.legend(loc="upper left", fontsize=9, frameon=False)


# ---------- 3. Monty Hall equally likely cases (cards 6, 113) ----------
@figure("f11_monty_cases", w=4.8, h=3.0, axis=False)
def _(ax):
    total = Fraction(0); switch = Fraction(0)
    ax.set_xlim(-1.15, 3.05); ax.set_ylim(-1.35, 3.45); ax.set_aspect("equal")
    for c in (1, 2, 3):
        for p in (1, 2, 3):
            x, y = p - 1, 3 - c
            if c != p:                                   # host is forced to the third door
                h = ({1, 2, 3} - {c, p}).pop()
                pr = Fraction(1, 9)
                total += pr; switch += pr                # switching wins exactly here
                ax.add_patch(Rectangle((x + 0.04, y + 0.04), 0.92, 0.92, fc=LIGHT_BLUE, ec=BLUE, lw=1.2, zorder=2))
                ax.text(x + 0.5, y + 0.5, r"$\frac{1}{9}$", ha="center", va="center", fontsize=10, zorder=3)
            else:                                        # host picks one of two doors, each 1/18
                for k, h in enumerate(sorted({1, 2, 3} - {c})):
                    pr = Fraction(1, 18)
                    total += pr
                    yy = y + 0.04 + 0.46 * (1 - k)
                    ax.add_patch(Rectangle((x + 0.04, yy), 0.92, 0.44, fc=LIGHT_RED, ec=RED, lw=1.0, zorder=2))
                    ax.text(x + 0.5, yy + 0.22, f"H={h}: " + r"$\frac{1}{18}$", ha="center", va="center",
                            fontsize=9, zorder=3)
    assert total == 1 and switch == Fraction(2, 3)
    for p in (1, 2, 3):
        ax.text(p - 0.5, 3.18, f"pick {p}", ha="center", fontsize=9)
    for c in (1, 2, 3):
        ax.text(-0.1, 3 - c + 0.5, f"prize {c}", ha="right", va="center", fontsize=9)
    ax.text(1.0, -0.42, r"blue: switch wins, $6\times\frac{1}{9}=\frac{2}{3}$", ha="center", fontsize=9, color=BLUE)
    ax.text(1.0, -0.95, r"red: stay wins, $3\times 2\times\frac{1}{18}=\frac{1}{3}$", ha="center", fontsize=9, color=RED)


# ---------- 4. ballot theorem lattice with reflection (cards 28, 93) ----------
@figure("f11_ballot_lattice", w=4.8, h=3.2)
def _(ax):
    a, b = 5, 3

    def paths():
        for pos in itertools.combinations(range(a + b), b):
            s = ["A"] * (a + b)
            for q in pos:
                s[q] = "B"
            yield s

    def pts(s):
        x = y = 0; out = [(0, 0)]
        for t in s:
            x, y = (x + 1, y) if t == "A" else (x, y + 1)
            out.append((x, y))
        return out

    allp = list(paths())
    good = [s for s in allp if all(x > y for x, y in pts(s)[1:])]
    assert len(allp) == 56 and len(good) == 14                       # (a-b)/(a+b) * C(8,3)
    bad = [s for s in allp if s[0] == "A" and any(x == y for x, y in pts(s)[2:])]
    rng = np.random.default_rng(3)
    g = good[rng.integers(len(good))]
    bd = bad[rng.integers(len(bad))]
    P = pts(bd)
    tau = next(t for t in range(2, len(P)) if P[t][0] == P[t][1])
    refl = [(0, 0)] + [(y, x) for x, y in P[1:tau + 1]] + P[tau + 1:]
    # paths starting with A: C(7,4)=35 of them, 14 good, so 21 = C(7,5) bad (reflect to paths from (0,1))
    assert len(bad) == 21
    for x in range(a + 1):
        ax.plot([x, x], [0, b], color=GREY, lw=0.4, alpha=0.6, zorder=0)
    for y in range(b + 1):
        ax.plot([0, a], [y, y], color=GREY, lw=0.4, alpha=0.6, zorder=0)
    ax.plot([0, b + 0.3], [0, b + 0.3], color=GREY, ls="--", lw=1.0, zorder=1)
    ax.text(3.35, 3.25, "tie line", color=GREY, fontsize=9)
    xs, ys = zip(*P)
    ax.plot(xs, ys, color=GREY, lw=1.4, zorder=2)
    rx, ry = zip(*refl[:tau + 1])
    ax.plot(rx, ry, color=ORANGE, lw=1.8, ls="--", zorder=3)
    ax.plot(*zip(*P[tau:tau + 1]), "o", color=RED, ms=5, zorder=4)
    gx, gy = zip(*pts(g))
    ax.plot(gx, gy, color=BLUE, lw=2.2, zorder=3)
    ax.plot(gx, gy, "o", color=BLUE, ms=3, zorder=4)
    ax.set_xlim(-0.3, 5.4); ax.set_ylim(-0.3, 3.6); ax.set_aspect("equal")
    ax.set_xticks(range(a + 1)); ax.set_yticks(range(b + 1))
    ax.set_xlabel("A votes"); ax.set_ylabel("B votes")
    ax.set_title(r"blue: A ahead throughout; orange: reflect after first tie", fontsize=9.5)


# ---------- 5. Dyck reflection (card 3) ----------
@figure("f11_dyck_reflect", w=5.0, h=2.7)
def _(ax):
    p = [0, -1, 0, 1, 2, 1, 0, 1, 0]                 # bad walk 0 -> 0 (n=4) touching -1
    tau = next(t for t, v in enumerate(p) if v == -1)
    q = [(-2 - v) if t <= tau else v for t, v in enumerate(p)]   # reflect initial segment about -1
    assert q[0] == -2 and q[-1] == 0 and sum(1 for i in range(8) if q[i + 1] - q[i] == 1) == 5
    t = np.arange(len(p))
    ax.axhline(-1, color=RED, ls="--", lw=1.0)
    ax.text(6.0, -1.45, "forbidden level", color=RED, fontsize=9, va="center")
    ax.plot(t, p, "o-", color=GREY, lw=1.4, ms=4, label="original walk")
    ax.plot(t[:tau + 1], q[:tau + 1], "o--", color=ORANGE, lw=1.6, ms=4, label="reflected start")
    ax.plot(t[tau:], q[tau:], color=ORANGE, lw=1.6, ls="--")
    ax.plot([tau], [-1], "o", color=RED, ms=6, zorder=5)
    ax.text(tau + 0.2, -0.6, r"$\tau$", fontsize=10, color=RED)
    ax.set_xlim(-0.4, 8.9); ax.set_ylim(-2.6, 2.4)
    ax.set_xticks(range(0, 9)); ax.set_yticks([-2, -1, 0, 1, 2])
    ax.set_xlabel("step $t$"); ax.set_ylabel("walk")
    ax.legend(loc="upper right", fontsize=9, frameon=False)
    ax.set_title(r"$C_4=14$: walks $0\to 0$ touching $-1$ (56 of them) map to walks $-2\to 0$", fontsize=9.5)


# ---------- 6. Brownian reflection (cards 27, 89) ----------
@figure("f11_bm_reflection", w=5.0, h=2.8)
def _(ax):
    M = 1000; dt = 1.0 / M; a = 0.5
    for k in range(1000):
        rng = np.random.default_rng(k)
        W = np.concatenate([[0.0], np.cumsum(rng.normal(0, np.sqrt(dt), M))])
        hit = np.where(W >= a)[0]
        if len(hit) and W[-1] < 0.0:
            break
    tau = hit[0]
    t = np.linspace(0, 1, M + 1)
    Wr = W.copy(); Wr[tau:] = 2 * a - W[tau:]
    ax.axhline(a, color=GREY, ls=":", lw=1.0)
    ax.text(0.02, a + 0.05, f"$a={a}$", color=GREY, fontsize=9)
    ax.plot(t, W, color=BLUE, lw=1.3, label=r"$W$")
    ax.plot(t[tau:], Wr[tau:], color=ORANGE, lw=1.4, ls="--", label=r"reflected after $\tau_a$")
    ax.plot([t[tau]], [a], "o", color=INK, ms=4, zorder=5)
    ax.text(t[tau] + 0.01, a + 0.07, r"$\tau_a$", fontsize=10)
    ax.plot([1, 1], [W[-1], Wr[-1]], "o", color=BLUE, ms=4)
    ax.set_xlabel("time $s$"); ax.set_ylabel("$W_s$")
    ax.legend(loc="upper left", fontsize=9, frameon=False)
    ax.set_title(r"reflection: $2P(W_1\geq a)=2(1-\Phi(a))=0.617$ at $a=\frac{1}{2}$",
                 fontsize=9.5)
    assert abs(2 * (1 - Phi(0.5)) - 0.6171) < 1e-3


# ---------- 7. quadratic variation (card 42) ----------
@figure("f11_qv_convergence", w=4.6, h=2.6)
def _(ax):
    rng = np.random.default_rng(5)
    K = 14; M = 2 ** K
    W = np.concatenate([[0.0], np.cumsum(rng.normal(0, np.sqrt(1.0 / M), M))])
    ns = 2 ** np.arange(0, K + 1)
    S = np.array([np.sum(np.diff(W[np.arange(0, M + 1, M // n)]) ** 2) for n in ns])
    ax.semilogx(ns, S, "o-", color=BLUE, ms=3.5, lw=1.1)
    ax.axhline(1.0, color=ORANGE, ls="--", lw=1.2)
    ax.text(ns[0] * 1.2, 1.05, r"$t=1$", color=ORANGE, fontsize=9)
    ax.set_xlabel("number of steps $n$ on $[0,1]$")
    ax.set_ylabel(r"$\sum(\Delta W_i)^2$")
    ax.set_title(r"quadratic variation: $\operatorname{Var}\sum=2\sum(\Delta t_i)^2\to 0$", fontsize=9.5)


# ---------- 8. put-call parity payoffs (cards 51, 112) ----------
@figure("f11_put_call_parity", w=5.0, h=2.6)
def _(ax):
    K = 100.0
    S = np.linspace(60, 140, 401)
    call = np.maximum(S - K, 0); put = np.maximum(K - S, 0)
    A = call + K                       # long call + cash K e^{-rT}, grown to K at T
    B = put + S                        # long put + one share
    assert np.allclose(A, B)
    ax.plot(S, call, color=GREY, lw=1.0, ls=":")
    ax.plot(S, put, color=GREY, lw=1.0, ls=":")
    ax.plot(S, B, color=ORANGE, lw=1.8, ls="--", label="long put + share", zorder=3)
    ax.plot(S, A, color=BLUE, lw=3.4, alpha=0.75, label="long call + cash $K$", zorder=2)
    ax.text(72, 33, "put", color=GREY, fontsize=9); ax.text(122, 24, "call", color=GREY, fontsize=9)
    ax.axvline(K, color=GREY, lw=0.8, ls=":")
    ax.text(K + 1.5, 12, "$K$", fontsize=9, color=GREY)
    ax.set_xlabel("$S_T$"); ax.set_ylabel("payoff at $T$")
    ax.legend(loc="upper left", fontsize=9, frameon=False)
    ax.set_title(r"both pay $\max(S_T,K)$ at $T$, so $C+Ke^{-rT}=P+S$", fontsize=9.5)


# ---------- 9. Breeden-Litzenberger: convexity and second difference (card 56) ----------
@figure("f11_bl_convex", w=5.0, h=2.8)
def _(ax):
    S0, r, T, sig = 100.0, 0.05, 1.0, 0.2
    Ks = np.linspace(70, 130, 241)
    C = np.array([bs_call(S0, K, r, T, sig) for K in Ks])
    assert np.all(np.diff(C, 2) > 0)                       # convex in K
    h, K0 = 15.0, 100.0
    cm, c0, cp = (bs_call(S0, K, r, T, sig) for K in (K0 - h, K0, K0 + h))
    d2 = cm - 2 * c0 + cp
    f_est = math.exp(r * T) * d2 / h ** 2
    dk = 1e-3
    f_exact = math.exp(r * T) * (bs_call(S0, K0 + dk, r, T, sig) - 2 * c0 + bs_call(S0, K0 - dk, r, T, sig)) / dk ** 2
    ax.plot(Ks, C, color=BLUE, lw=1.8)
    ax.plot([K0 - h, K0 + h], [cm, cp], color=GREY, ls="--", lw=1.0)
    ax.plot([K0 - h, K0, K0 + h], [cm, c0, cp], "o", color=BLUE, ms=4.5)
    ax.plot([K0], [(cm + cp) / 2], "o", color=GREY, ms=4)
    ax.annotate("", xy=(K0, (cm + cp) / 2), xytext=(K0, c0),
                arrowprops=dict(arrowstyle="<->", color=ORANGE, lw=1.3))
    ax.text(K0 + 3.0, (cm + 3 * c0 + cp) / 5, r"$\frac{1}{2}\Delta^2C$", color=ORANGE, fontsize=10, va="center")
    ax.text(K0 - h, cm + 2.5, f"$K-h$", fontsize=9, ha="center")
    ax.text(K0 + h, cp + 2.5, f"$K+h$", fontsize=9, ha="center")
    ax.set_xlabel("strike $K$"); ax.set_ylabel("call price $C(K)$")
    assert abs(f_est / f_exact - 1) < 0.05
    ax.set_title(r"$C(K-h)-2C(K)+C(K+h)\approx e^{-rT}h^2 f(K)$, the chord gap", fontsize=9.5)


# ---------- 10. butterfly payoff = tent of area h^2 (card 84) ----------
@figure("f11_butterfly_density", w=4.6, h=2.5)
def _(ax):
    K, h = 100.0, 10.0
    S = np.linspace(80, 120, 801)
    tent = np.maximum(S - K + h, 0) - 2 * np.maximum(S - K, 0) + np.maximum(S - K - h, 0)
    area = np.trapezoid(tent, S)
    assert abs(area - h * h) < 1e-6 and abs(tent.max() - h) < 1e-9
    ax.fill_between(S, tent, color=LIGHT_ORANGE, zorder=1)
    ax.plot(S, tent, color=ORANGE, lw=1.8)
    for x, lab in [(K - h, "$K-h$"), (K, "$K$"), (K + h, "$K+h$")]:
        ax.plot([x, x], [0, 0.1], color=INK, lw=0.8); ax.text(x, -0.9, lab, ha="center", fontsize=9)
    ax.annotate("height $h$", xy=(K, h), xytext=(K + 5, h - 1.5), fontsize=9,
                arrowprops=dict(arrowstyle="-", color=INK, lw=0.7))
    ax.text(K, 2.0, r"area $=h^2$", fontsize=9.5, color=ORANGE, ha="center")
    ax.set_ylim(-1.6, 11.5); ax.set_xlim(80, 120)
    ax.set_xticks([]); ax.set_xlabel("$S_T$"); ax.set_ylabel("butterfly payoff")
    ax.set_title(r"$E^Q[\mathrm{tent}]\approx h^2 f(K)$ as $h\to 0$", fontsize=9.5)


# ---------- 11. ruin duration from S_n^2-n (cards 19, 81) ----------
@figure("f11_ruin_martingale", w=5.0, h=2.9)
def _(ax):
    i0, N = 3, 10
    for k in range(10000):
        rng = np.random.default_rng(k)
        s = [i0]
        while 0 < s[-1] < N:
            s.append(s[-1] + (1 if rng.random() < 0.5 else -1))
        tau = len(s) - 1
        if s[-1] == N and 15 <= tau <= 35:
            break
    S = np.array(s); n = np.arange(len(S)); M = S ** 2 - n
    assert abs(i0 * (N - i0) - 21) < 1e-9
    ax.plot(n, M, color=ORANGE, lw=1.5, drawstyle="steps-post")
    ax.axhline(i0 ** 2, color=GREY, ls=":", lw=1.0)
    ax.text(7.5, i0 ** 2 + 1.5, r"dotted: $M_0=i^2=9$", fontsize=9, color=GREY)
    ax.plot([tau], [M[-1]], "o", color=INK, ms=4.5, zorder=5)
    ax.annotate(rf"win: $M_\tau=100-\tau={N * N - tau}$", xy=(tau, M[-1]),
                xytext=(0.5, 70), fontsize=9,
                arrowprops=dict(arrowstyle="-", color=INK, lw=0.7))
    ax.set_xlabel("step $n$"); ax.set_ylabel(r"$S_n^2-n$")
    ax.set_title(r"$E[M_\tau]=M_0$: $\frac{3}{10}\cdot 100-E[\tau]=9$, so $E[\tau]=21=i(N-i)$",
                 fontsize=9.5)


# ---------- 12. stick breaks into a triangle (card 34) ----------
@figure("f11_stick_triangle", w=4.0, h=3.1)
def _(ax):
    ax.add_patch(Polygon([(0, 0.5), (0.5, 0.5), (0.5, 1.0)], closed=True, fc=LIGHT_BLUE, ec=BLUE, lw=1.0, zorder=2))
    ax.add_patch(Polygon([(0.5, 0), (0.5, 0.5), (1.0, 0.5)], closed=True, fc=LIGHT_BLUE, ec=BLUE, lw=1.0, zorder=2))
    ax.plot([0, 1], [0, 1], color=GREY, ls="--", lw=0.9)
    ax.plot([0.5, 0.5], [0, 1], color=GREY, ls=":", lw=0.9)
    ax.plot([0, 1], [0.5, 0.5], color=GREY, ls=":", lw=0.9)
    ax.text(0.27, 0.8, "$U<\\frac{1}{2}$", fontsize=9, ha="right")
    ax.text(0.97, 0.12, "$V<\\frac{1}{2}$", fontsize=9, ha="right")
    ax.set_xlim(-0.05, 1.05); ax.set_ylim(-0.05, 1.05); ax.set_aspect("equal")
    ax.set_xticks([0, 0.5, 1]); ax.set_yticks([0, 0.5, 1])
    ax.set_xlabel("first break $U$"); ax.set_ylabel("second break $V$")
    ax.set_title(r"two blue triangles of area $\frac{1}{8}$ each: $P=\frac{1}{4}$", fontsize=9.5)


# ---------- 13. Poisson thinning (card 37) ----------
@figure("f11_poisson_thin", w=5.2, h=2.6)
def _(ax):
    lam, p, T = 3.0, 1 / 3, 4.0
    rng = np.random.default_rng(8)
    ts, t = [], 0.0
    while True:
        t += rng.exponential(1 / lam)
        if t >= T:
            break
        ts.append(t)
    kept = [rng.random() < p for _ in ts]
    ts = np.array(ts); kept = np.array(kept)
    ax.scatter(ts, np.full(len(ts), 2.0), s=26, facecolor=[BLUE if k else "white" for k in kept],
               edgecolor=[BLUE if k else GREY for k in kept], zorder=3)
    ax.scatter(ts[kept], np.full(kept.sum(), 1.0), s=26, color=BLUE, zorder=3)
    ax.scatter(ts[~kept], np.full((~kept).sum(), 0.0), s=26, color="white", edgecolor=GREY, zorder=3)
    ax.axhline(2, color=GREY, lw=0.5); ax.axhline(1, color=GREY, lw=0.5); ax.axhline(0, color=GREY, lw=0.5)
    ax.set_yticks([2, 1, 0])
    ax.set_yticklabels([r"all, rate $\lambda$", r"kept, rate $\lambda p$", r"discarded, $\lambda(1-p)$"], fontsize=9)
    ax.set_ylim(-0.5, 2.5); ax.set_xlim(-0.1, T + 0.1)
    ax.set_xlabel("time $t$")
    ax.set_title(r"kept w.p. $p$: two independent Poisson streams", fontsize=9.5)


# ---------- 14. Poisson superposition and the exponential race (cards 36, 97) ----------
@figure("f11_poisson_merge", w=5.2, h=2.6)
def _(ax):
    l1, l2, T = 2.0, 1.0, 3.0

    def stream(lam):
        out, t = [], 0.0
        while True:
            t += rng.exponential(1 / lam)
            if t >= T:
                return np.array(out)
            out.append(t)

    for seed in range(1000):
        rng = np.random.default_rng(seed)
        s1, s2 = stream(l1), stream(l2)
        merged = sorted([(t, 1) for t in s1] + [(t, 2) for t in s2])
        if len(s1) >= 3 and len(s2) >= 1 and merged[0][1] == 1:
            break
    first = merged[0]
    ax.scatter(s1, np.full(len(s1), 2.0), s=26, color=BLUE, zorder=3)
    ax.scatter(s2, np.full(len(s2), 1.0), s=26, color=ORANGE, zorder=3)
    ax.scatter([t for t, _ in merged], np.zeros(len(merged)), s=26,
               color=[BLUE if src == 1 else ORANGE for _, src in merged], zorder=3)
    ax.plot([first[0]], [0], "o", mfc="none", mec=INK, ms=10, zorder=4)
    ax.axhline(2, color=GREY, lw=0.5); ax.axhline(1, color=GREY, lw=0.5); ax.axhline(0, color=GREY, lw=0.5)
    ax.set_yticks([2, 1, 0])
    ax.set_yticklabels([r"source 1, $\lambda_1$", r"source 2, $\lambda_2$", "merged"], fontsize=9)
    ax.set_ylim(-0.5, 2.5); ax.set_xlim(-0.1, T + 0.1)
    ax.set_xlabel("time $t$")
    ax.set_title(r"circled: first merged arrival, from source 1 w.p. $\frac{\lambda_1}{\lambda_1+\lambda_2}=\frac{2}{3}$",
                 fontsize=9)


# ---------- 15. inspection paradox timeline (cards 38, 98) ----------
@figure("f11_inspection", w=5.0, h=2.0, axis=False)
def _(ax):
    L = [3, 1, 1, 3, 1, 3, 3, 1]              # two lengths, each half the intervals: E[L]=2, E[L^2]=5
    x = 0
    ax.set_xlim(-0.3, sum(L) + 0.3); ax.set_ylim(-1.3, 1.1)
    for l in L:
        col = LIGHT_ORANGE if l == 3 else LIGHT_BLUE
        ec = ORANGE if l == 3 else BLUE
        ax.add_patch(Rectangle((x + 0.03, 0), l - 0.06, 0.8, fc=col, ec=ec, lw=1.0))
        ax.text(x + l / 2, 0.4, f"{l}", ha="center", va="center", fontsize=10)
        x += l
    long_time = sum(l for l in L if l == 3); total = sum(L)
    assert Fraction(long_time, total) == Fraction(3, 4)
    ax.annotate("", xy=(0, -0.2), xytext=(total, -0.2), arrowprops=dict(arrowstyle="<->", color=GREY, lw=0.8))
    ax.text(total / 2, -0.55, "time $t$ (length 16 in this sample)", ha="center", fontsize=9, color=GREY)
    ax.text(total / 2, -1.05, r"time in length-3 intervals: $\frac{3}{4}$; mean length seen $=1\cdot\frac{1}{4}+3\cdot\frac{3}{4}=\frac{5}{2}$",
            ha="center", fontsize=9)


# ---------- 16. Kelly growth curve (card 59) ----------
@figure("f11_kelly_growth", w=5.0, h=2.6)
def _(ax):
    p, q = 0.6, 0.4
    f = np.linspace(-0.3, 0.8, 500)
    g = p * np.log(1 + f) + q * np.log(1 - f)
    fs = p - q
    gs = p * np.log(1 + fs) + q * np.log(1 - fs)
    assert np.all(g[np.argmax(g)] >= g - 1e-12) and abs(f[np.argmax(g)] - fs) < 2e-3
    ax.plot(f, g, color=BLUE, lw=1.8)
    ax.axvline(fs, color=ORANGE, ls="--", lw=1.1)
    ax.plot([fs], [gs], "o", color=ORANGE, ms=5)
    ax.axhline(0, color=GREY, lw=0.8, ls=":")
    ax.text(fs + 0.02, gs - 0.035, f"$f^*=p-q={fs:.1f}$", color=ORANGE, fontsize=9)
    ax.set_ylim(-0.2, 0.05); ax.set_xlim(-0.3, 0.8)
    ax.set_xlabel("bet fraction $f$"); ax.set_ylabel(r"growth $g(f)$")
    ax.set_title(r"$g(f)=p\ln(1+f)+q\ln(1-f)$, $p=0.6$: maximum at $f^*=0.2$", fontsize=9.5)


# ---------- 17. OLS slope and residuals (cards 61, 90, 103) ----------
@figure("f11_ols_residuals", w=4.8, h=2.8)
def _(ax):
    rng = np.random.default_rng(2)
    n = 12
    x = rng.normal(0, 1, n)
    y = 1.0 + 2.0 * x + rng.normal(0, 0.8, n)
    xb, yb = x.mean(), y.mean()
    Sxy = np.sum((x - xb) * (y - yb)); Sxx = np.sum((x - xb) ** 2); Syy = np.sum((y - yb) ** 2)
    b = Sxy / Sxx; a = yb - b * xb
    res = y - a - b * x
    SSR = np.sum(res ** 2)
    assert abs(SSR - (Syy - b * Sxy)) < 1e-9
    R2 = 1 - SSR / Syy
    xs = np.linspace(x.min() - 0.3, x.max() + 0.3, 50)
    for xi, yi, ri in zip(x, y, res):
        ax.plot([xi, xi], [yi - ri, yi], color=GREY, lw=0.9, ls=":")
    ax.plot(xs, a + b * xs, color=BLUE, lw=1.6)
    ax.plot(x, y, "o", color=INK, ms=4, zorder=3)
    ax.plot([xb], [yb], "o", color=ORANGE, ms=6, zorder=4)
    ax.text(xb + 0.1, yb - 1.0, r"$(\bar x,\bar y)$", color=ORANGE, fontsize=9)
    ax.set_xlabel("$x$"); ax.set_ylabel("$y$")
    ax.set_title(rf"$b=S_{{xy}}/S_{{xx}}={b:.3f}$, $R^2=1-\mathrm{{SSR}}/\mathrm{{SST}}={R2:.3f}$",
                 fontsize=9.5)
    ax.set_xlim(xs[0], xs[-1])


# ---------- 18. uniform MLE (card 63) ----------
@figure("f11_uniform_mle", w=4.8, h=2.5)
def _(ax):
    n, theta = 5, 1.0
    rng = np.random.default_rng(11)
    X = rng.uniform(0, theta, n)
    Mx = X.max()
    th = np.linspace(0.4, 1.6, 600)
    L = np.where(th >= Mx, th ** (-n), 0.0)
    ax.plot(th[th < Mx], np.zeros(np.sum(th < Mx)), color=GREY, lw=1.6)
    ax.plot(th[th >= Mx], L[th >= Mx], color=BLUE, lw=1.8)
    ax.plot([Mx], [Mx ** (-n)], "o", color=ORANGE, ms=5, zorder=4)
    ax.annotate(rf"$\hat\theta=\max X_i={Mx:.3f}$", xy=(Mx, Mx ** (-n)), xytext=(Mx + 0.2, Mx ** (-n) * 0.7),
                fontsize=9, arrowprops=dict(arrowstyle="-", color=INK, lw=0.7))
    ax.axvline(theta, color=GREY, ls=":", lw=1.0)
    ax.text(theta + 0.03, 4.0, r"true $\theta=1$", fontsize=9, color=GREY)
    ax.set_xlabel(r"$\theta$"); ax.set_ylabel(r"$L(\theta)$")
    ax.set_title(r"$L(\theta)=\theta^{-n}\mathbf{1}\{\theta\geq\max X_i\}$, $n=5$; $E\hat\theta=\frac{5}{6}\theta$",
                 fontsize=9.5)


# ---------- 19. FTCS amplification factor (card 70) ----------
@figure("f11_ftcs_stability", w=5.0, h=2.6)
def _(ax):
    th = np.linspace(0, np.pi, 300)
    ax.axhspan(-1, 1, color=LIGHT_GREEN, zorder=0)
    for r, col in [(0.25, BLUE), (0.5, GREEN), (0.6, RED)]:
        g = 1 - 4 * r * np.sin(th / 2) ** 2
        ax.plot(th, g, color=col, lw=1.7)
        ax.plot([], [], color=col, lw=1.7, label=f"$r={r}$")
    ax.legend(loc="lower left", fontsize=9, frameon=True, facecolor="white", edgecolor="none", framealpha=1)
    ax.axhline(-1, color=GREY, ls=":", lw=0.9); ax.axhline(1, color=GREY, ls=":", lw=0.9)
    ax.set_xticks([0, np.pi / 2, np.pi]); ax.set_xticklabels(["0", r"$\pi/2$", r"$\pi$"])
    ax.set_xlabel(r"$k\Delta x$"); ax.set_ylabel(r"$g$")
    ax.set_ylim(-1.6, 1.25); ax.set_xlim(0, np.pi)
    ax.set_title(r"$g=1-4r\sin^2(k\Delta x/2)$: stable iff $1-4r\geq -1$, i.e. $r\leq\frac{1}{2}$",
                 fontsize=9.5)


# ---------- 20. Monte Carlo error vs N (card 71) ----------
@figure("f11_mc_error_loglog", w=5.0, h=2.8)
def _(ax):
    sig = np.sqrt(1 / 12)                              # Y ~ Uniform(0,1), target mean 1/2
    Ns = np.unique(np.round(np.logspace(1, 4, 13)).astype(int))
    rng = np.random.default_rng(4)
    R = 300
    rms = np.array([np.sqrt(np.mean((rng.random((R, N)).mean(axis=1) - 0.5) ** 2)) for N in Ns])
    ax.loglog(Ns, rms, "o", color=BLUE, ms=4.5, label=f"simulated RMS error, {R} runs")
    ax.loglog(Ns, sig / np.sqrt(Ns), color=ORANGE, lw=1.6, ls="--", label=r"$\sigma/\sqrt{N}$, $\sigma^2=\frac{1}{12}$")
    ax.set_xlabel("sample size $N$"); ax.set_ylabel("standard error")
    ax.legend(loc="lower left", fontsize=9, frameon=False)
    ax.set_title(r"Monte Carlo: error $\propto N^{-1/2}$ (slope $-\frac{1}{2}$ on log-log)", fontsize=9.5)
    assert abs(np.log(rms[-1] / rms[0]) / np.log(Ns[-1] / Ns[0]) + 0.5) < 0.1


# ---------- 21. secretary cut-off curve (cards 32, 118) ----------
@figure("f11_secretary_curve", w=5.0, h=2.6)
def _(ax):
    n = 100
    rs = np.arange(1, n)
    P = np.array([(r / n) * sum(1 / j for j in range(r, n)) for r in rs])
    rstar = rs[np.argmax(P)]
    assert rstar == 37 and abs(P.max() - 0.371) < 1e-3
    ax.plot(rs, P, color=BLUE, lw=1.8)
    ax.plot([rstar], [P.max()], "o", color=ORANGE, ms=5)
    ax.annotate(f"$r={rstar}$: $P={P.max():.3f}$", xy=(rstar, P.max()), xytext=(46, 0.12), fontsize=9,
                arrowprops=dict(arrowstyle="-", color=INK, lw=0.7))
    ax.axhline(1 / math.e, color=GREY, ls="--", lw=1.0)
    ax.text(88, 1 / math.e + 0.012, r"$1/e$", color=GREY, fontsize=9)
    ax.axvline(n / math.e, color=GREY, ls=":", lw=0.9)
    ax.set_xlabel("cut-off $r$ (reject first $r$), $n=100$"); ax.set_ylabel("$P(r)$")
    ax.set_ylim(0, 0.42)
    ax.set_title(r"success probability $P(r)$ peaks near $r\approx n/e$, value near $1/e$", fontsize=9.5)


# ---------- 22. order statistics and spacings (cards 33, 111) ----------
@figure("f11_order_spacings", w=5.0, h=1.9, axis=False)
def _(ax):
    n = 4
    rng = np.random.default_rng(21)
    U = np.sort(rng.uniform(0, 1, n))
    ax.set_xlim(-0.05, 1.05); ax.set_ylim(-0.9, 0.9)
    ax.plot([0, 1], [0, 0], color=INK, lw=1.0)
    for k in range(1, n + 1):
        ax.plot([k / (n + 1)], [0], "o", mfc="white", mec=GREY, ms=7, zorder=3)
        ax.text(k / (n + 1), -0.38, f"$\\frac{{{k}}}{{{n + 1}}}$", ha="center", fontsize=9, color=GREY)
    ax.plot(U, np.zeros(n), "o", color=BLUE, ms=5, zorder=4)
    for k, u in enumerate(U, start=1):
        ax.text(u, 0.18, f"$U_{{({k})}}$", ha="center", fontsize=9, color=BLUE)
    ax.text(0.5, 0.62, r"each of the $n+1=5$ spacings has mean $\frac{1}{5}$; hollow dots are $\frac{k}{n+1}$",
            ha="center", fontsize=9)


# ---------- 23. bivariate normal sign regions (card 41) ----------
@figure("f11_bivariate_quadrants", w=4.0, h=3.2, axis=False)
def _(ax):
    rho = 0.5
    th_n = math.degrees(math.acos(rho))                     # 60 deg: normal to the line Y=0
    lo = th_n - 90                                          # -30 deg
    hi = lo + 180                                           # 150 deg
    sector_w = 90 - lo                                      # 120 deg: [-30, 90]
    assert abs(sector_w - (90 + math.degrees(math.asin(rho)))) < 1e-9
    for a0, a1 in [(lo, 90), (hi, 270)]:                    # XY > 0 sectors
        ax.add_patch(Wedge((0, 0), 1, a0, a1, fc=LIGHT_BLUE, ec="none", zorder=1))
    for a0, a1 in [(90, hi), (270, lo + 360)]:              # XY < 0 sectors
        ax.add_patch(Wedge((0, 0), 1, a0, a1, fc="white", ec="none", zorder=1))
    ax.add_patch(Circle((0, 0), 1, fc="none", ec=INK, lw=1.0, zorder=2))
    ax.plot([0, 0], [-1.05, 1.05], color=GREY, ls="--", lw=0.9)                       # X = 0
    for ang in (lo, hi):
        c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        ax.plot([-1.05 * c, 1.05 * c], [-1.05 * s, 1.05 * s], color=GREY, ls="--", lw=0.9)  # Y = 0
    ax.text(0.5, 0.3, "$XY>0$", ha="center", va="center", color=BLUE, fontsize=10)
    ax.text(-0.5, -0.3, "$XY>0$", ha="center", va="center", color=BLUE, fontsize=10)
    ax.text(-0.3, 0.5, r"$XY<0$", ha="center", va="center", fontsize=9)
    ax.text(0.3, -0.5, r"$XY<0$", ha="center", va="center", fontsize=9)
    ax.text(0.9, 1.12, r"$\frac{2\cdot 120^\circ}{360^\circ}=\frac{2}{3}$", fontsize=9, ha="center")
    ax.text(0.0, -1.32, r"$\rho=\frac{1}{2}$: $P(XY>0)=\frac{1}{2}+\frac{\arcsin\rho}{\pi}=\frac{2}{3}$",
            ha="center", fontsize=9)
    ax.set_xlim(-1.3, 1.3); ax.set_ylim(-1.5, 1.3); ax.set_aspect("equal")


# ---------- 24. Polya urn martingale (card 30) ----------
@figure("f11_urn_martingale", w=5.0, h=2.6)
def _(ax):
    n_steps = 200
    cols = [BLUE, ORANGE, GREEN, RED, GREY]
    finals = []
    for k, col in enumerate(cols):
        rng = np.random.default_rng(100 + k)
        R, B = 1, 1
        X = [0.5]
        for _ in range(n_steps):
            if rng.random() < R / (R + B):
                R += 1
            else:
                B += 1
            X.append(R / (R + B))
        ax.plot(np.arange(n_steps + 1), X, color=col, lw=1.2)
        finals.append(X[-1])
    ax.axhline(0.5, color=GREY, ls=":", lw=0.9)
    ax.set_xlabel("draw $n$"); ax.set_ylabel("$X_n$")
    ax.set_ylim(0, 1); ax.set_xlim(0, n_steps)
    ax.set_title(r"$X_n=\frac{R_n}{R_n+B_n}$ is a martingale; limit is Uniform$[0,1]$", fontsize=9.5)


# ---------- 25. random walk on a graph, stationary law (cards 26, 94) ----------
@figure("f11_graph_walk_pi", w=4.4, h=2.8, axis=False)
def _(ax):
    pos = {1: (0.0, 0.0), 2: (1.0, 1.2), 3: (2.0, 0.0), 4: (3.0, 1.2), 5: (4.0, 0.0)}
    edges = [(1, 2), (2, 3), (1, 3), (3, 4), (4, 5), (2, 4)]
    deg = {v: sum(v in e for e in edges) for v in pos}
    twoE = 2 * len(edges)
    assert sum(deg.values()) == twoE and deg == {1: 2, 2: 3, 3: 3, 4: 3, 5: 1}
    for u, v in edges:
        ax.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]], color=INK, lw=1.2, zorder=1)
    for v, (x, y) in pos.items():
        node(ax, (x, y), str(v), r=0.3, fs=10, fc=LIGHT_BLUE if deg[v] == 3 else "white")
        pi = Fraction(deg[v], twoE)
        dy = 0.6 if v in (1, 3, 5) else 0.6
        ty = y - dy if v in (1, 3, 5) else y + dy
        ax.text(x, ty, rf"$\pi=\frac{{{deg[v]}}}{{{twoE}}}$, return ${int(twoE / deg[v])}$", ha="center",
                fontsize=9, color=INK)
    ax.set_xlim(-0.6, 4.6); ax.set_ylim(-1.1, 2.5); ax.set_aspect("equal")
    ax.text(2.0, 2.3, r"$\pi_v=\frac{\deg v}{2|E|}$, $|E|=6$", ha="center", fontsize=9)


# ---------- 26. two-state flow balance (card 24) ----------
@figure("f11_two_state_flow", w=4.4, h=2.5, axis=False)
def _(ax):
    a, b = 0.3, 0.6
    pi1, pi2 = b / (a + b), a / (a + b)
    assert abs(pi1 * a - pi2 * b) < 1e-12 and abs(pi1 - 2 / 3) < 1e-12
    ax.set_xlim(-0.9, 4.0); ax.set_ylim(-1.3, 1.9); ax.set_aspect("equal")
    node(ax, (0, 0), "1", r=0.36, fs=11)
    node(ax, (3.0, 0), "2", r=0.36, fs=11)
    ax.add_patch(FancyArrowPatch((0.4, 0.2), (2.6, 0.2), arrowstyle="-|>", mutation_scale=12, color=BLUE, lw=1.5))
    ax.text(1.5, 0.55, f"$a={a}$", ha="center", fontsize=9.5, color=BLUE)
    ax.add_patch(FancyArrowPatch((2.6, -0.2), (0.4, -0.2), arrowstyle="-|>", mutation_scale=12, color=RED, lw=1.5))
    ax.text(1.5, -0.6, f"$b={b}$", ha="center", fontsize=9.5, color=RED)
    ax.text(0, -1.1, rf"$\pi_1=\frac{{2}}{{3}}$", ha="center", fontsize=9.5)
    ax.text(3.0, -1.1, rf"$\pi_2=\frac{{1}}{{3}}$", ha="center", fontsize=9.5)
    ax.text(1.5, 1.45, r"cut flow: $\pi_1 a=\pi_2 b=0.2$", ha="center", fontsize=9.5)
    self_loop(ax, (0, 0), r"$1-a$", color=GREY, r=0.36)
    self_loop(ax, (3.0, 0), r"$1-b$", color=GREY, r=0.36)


# ---------- 27. HTH pattern chain (card 21) ----------
@figure("f11_htH_chain", w=5.2, h=2.3, axis=False)
def _(ax):
    P = np.array([[0.5, 0.5, 0, 0], [0, 0.5, 0.5, 0], [0.5, 0, 0, 0.5], [0, 0, 0, 1]], float)  # S0,S1,S2,HTH
    # states: 0 = no progress, 1 = H, 2 = HT, 3 = HTH (absorbing); first-step equations E = 1 + P E on transient states
    Q = P[:3, :3]
    E = np.linalg.solve(np.eye(3) - Q, np.ones(3))
    assert abs(E[0] - 10) < 1e-9
    ax.set_xlim(-0.6, 8.8); ax.set_ylim(-1.5, 1.6); ax.set_aspect("equal")
    xy = {0: (0, 0), 1: (2.7, 0), 2: (5.4, 0), 3: (8.1, 0)}
    node(ax, xy[0], "∅", r=0.36, fs=11)
    node(ax, xy[1], "H", r=0.36, fs=11)
    node(ax, xy[2], "HT", r=0.36, fs=10)
    node(ax, xy[3], "HTH", r=0.36, fs=10, fc=LIGHT_GREEN, ec=GREEN)
    for i in range(3):
        ax.text(xy[i][0], -0.85, rf"$E={E[i]:.0f}$", ha="center", fontsize=9.5)
    arrow(ax, xy[0], xy[1], r"H  $\frac{1}{2}$", color=BLUE, shrink=20, fs=9, label_offset=(0, 0.35))
    arrow(ax, xy[1], xy[2], r"T  $\frac{1}{2}$", color=RED, shrink=20, fs=9, label_offset=(0, 0.35))
    arrow(ax, xy[2], xy[3], r"H  $\frac{1}{2}$", color=BLUE, shrink=20, fs=9, label_offset=(0, 0.35))
    arrow(ax, xy[2], xy[0], r"T  $\frac{1}{2}$", color=RED, rad=-0.45, shrink=20, fs=9)
    self_loop(ax, xy[0], r"T  $\frac{1}{2}$", color=RED, r=0.36, fs=9)
    self_loop(ax, xy[1], r"H  $\frac{1}{2}$", color=BLUE, r=0.36, fs=9)


# ---------- 28. dependency map around card 102 ----------
@figure("f11_dependency_map", w=5.4, h=3.0, axis=False)
def _(ax):
    ax.set_xlim(-1.2, 6.8); ax.set_ylim(-0.6, 3.1); ax.set_aspect("equal")
    nodes = {
        "ito": ((0.0, 2.3), "Itô's lemma", LIGHT_BLUE),
        "mart": ((0.0, 0.2), r"$Q$-martingale $e^{-rt}C$", LIGHT_BLUE),
        "pde": ((2.9, 1.25), "Black-Scholes PDE", LIGHT_ORANGE),
        "heat": ((5.6, 2.3), "heat equation", "white"),
        "theta": ((5.6, 0.2), r"$\Theta$ identity", "white"),
    }
    bw, bh = 2.0, 0.62
    for key, (xy, lab, fc) in nodes.items():
        box(ax, xy, lab, w=bw, h=bh, fc=fc, fs=9)
    x_ito, y_ito = nodes["ito"][0]; x_m, y_m = nodes["mart"][0]
    x_p, y_p = nodes["pde"][0]; x_h, y_h = nodes["heat"][0]; x_t, y_t = nodes["theta"][0]
    ax.add_patch(FancyArrowPatch((x_ito + bw / 2, y_ito), (x_p - 0.55, y_p + bh / 2), arrowstyle="-|>",
                                 mutation_scale=12, color=ORANGE, lw=1.8))
    ax.add_patch(FancyArrowPatch((x_m + bw / 2, y_m), (x_p - 0.55, y_p - bh / 2), arrowstyle="-|>",
                                 mutation_scale=12, color=ORANGE, lw=1.8))
    ax.add_patch(FancyArrowPatch((x_p + bw / 2 - 0.5, y_p + 0.1), (x_h - bw / 2, y_h - 0.2), arrowstyle="-|>",
                                 mutation_scale=12, color=INK, lw=1.3))
    ax.add_patch(FancyArrowPatch((x_p + bw / 2 - 0.5, y_p - 0.1), (x_t - bw / 2, y_t + 0.2), arrowstyle="-|>",
                                 mutation_scale=12, color=INK, lw=1.3))
    ax.text(1.55, 2.5, "Itô on $C$", fontsize=9, color=ORANGE, ha="center")
    ax.text(1.75, 0.2, "zero drift", fontsize=9, color=ORANGE, ha="center")
    ax.text(3.9, 2.2, "change of\nvariables", fontsize=9, ha="center", va="center")
    ax.text(3.95, 0.3, "rearrange", fontsize=9, ha="center", va="center")
    ax.text(2.9, -0.45, "orange: this card (the PDE step); arrows: result used to derive result",
            ha="center", fontsize=9, color=GREY)
