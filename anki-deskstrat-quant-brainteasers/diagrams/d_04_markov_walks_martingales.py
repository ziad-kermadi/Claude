"""Figures for cards/04_markov_walks_martingales.json."""
import itertools
from fractions import Fraction as Fr
from math import comb
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from qcfig import *


def fr(x):
    """Exact fraction as mathtext \\frac{a}{b} (braces kept)."""
    x = Fr(x)
    if x.denominator == 1:
        return str(x.numerator)
    return rf"\frac{{{x.numerator}}}{{{x.denominator}}}"


def _solve(A, b):
    return np.linalg.solve(np.array(A, float), np.array(b, float))


def _ftext(ax, x, y, s, color=INK, fs=9):
    ax.text(x, y, s, color=color, fontsize=fs, ha="center", va="center")


def _edge(ax, A, B, rA=0.3, rB=0.3, label=None, color=INK, rad=0.0, off=(0, 0), fs=9):
    """Arrow from A to B, starting rA and ending rB short of the centres (data units)."""
    A = np.array(A, float); B = np.array(B, float)
    d = B - A
    u = d / np.hypot(*d)
    arrow(ax, tuple(A + u * rA), tuple(B - u * rB), label, rad=rad, color=color,
          shrink=0, fs=fs, label_offset=off)


# ---------- 1. HH waiting time: run-length chain (exemplar, notation fixed) ----------

@figure("f04_hh_run_chain", w=4.6, h=2.0, axis=False)
def _(ax):
    # State = current run of heads. E0 = 1 + E0/2 + E1/2, E1 = 1 + E0/2  ->  E0 = 6, E1 = 4
    E0, E1 = _solve([[0.5, -0.5], [-0.5, 1.0]], [1, 1])
    assert abs(E0 - 6) < 1e-9 and abs(E1 - 4) < 1e-9
    P = {"E0": (0, 0), "E1": (2.2, 0), "HH": (4.4, 0)}
    node(ax, P["E0"], r"$E_0$")
    node(ax, P["E1"], r"$E_1$")
    node(ax, P["HH"], "HH", fc=LIGHT_GREEN, ec=GREEN)
    arrow(ax, P["E0"], P["E1"], "H  ½", rad=-0.35, color=BLUE)
    arrow(ax, P["E1"], P["E0"], "T  ½", rad=-0.35, color=RED)
    arrow(ax, P["E1"], P["HH"], "H  ½", color=BLUE)
    self_loop(ax, P["E0"], "T  ½", color=RED)
    _ftext(ax, 0, -0.62, "no head", color=GREY)
    _ftext(ax, 2.2, -0.62, "one head", color=GREY)
    frame(ax, -0.6, 5.0, -1.0, 1.15)
    caption(ax, r"$E_0 = 1+\frac{1}{2}E_0+\frac{1}{2}E_1,\quad E_1 = 1+\frac{1}{2}E_0 \;\Rightarrow\; E_0 = 6$")


# ---------- 2. Gambler's ruin paths (exemplar, kept) ----------

@figure("f04_gamblers_ruin_paths", w=5.0, h=2.8)
def _(ax):
    rng = np.random.default_rng(7)
    for k, c in zip(range(4), [BLUE, ORANGE, GREEN, GREY]):
        s = [3]
        while 0 < s[-1] < 10:
            s.append(s[-1] + rng.choice([-1, 1]))
        ax.step(range(len(s)), s, where="post", color=c, lw=1.4, alpha=0.9)
        ax.plot(len(s) - 1, s[-1], "o", color=c, ms=5)
    ax.axhline(10, color=GREEN, ls="--", lw=1.1); ax.axhline(0, color=RED, ls="--", lw=1.1)
    ax.text(0.3, 10.4, "win: absorb at 10", color=GREEN, fontsize=9)
    ax.text(0.3, 0.4, "ruin: absorb at 0", color=RED, fontsize=9)
    ax.set_xlabel("toss n"); ax.set_ylabel(r"$S_n$"); ax.set_ylim(-0.8, 11.5); ax.set_yticks([0, 3, 10])
    ax.set_title(r"$S_n$ martingale, bounded $\Rightarrow$ $E[S_T]=3 \Rightarrow P(10)=3/10$", fontsize=10)


# ---------- 3. Biased HH waiting time (card 47) ----------

@figure("f04_hh_run_biased", w=4.6, h=2.0, axis=False)
def _(ax):
    p, q = 0.6, 0.4
    # E0 = 1 + q E0 + p E1 ; E1 = 1 + q E0  ->  E0 = 1/p + 1/p^2 = 40/9
    E0, E1 = _solve([[p, -p], [-q, 1.0]], [1, 1])
    assert abs(E0 - 40 / 9) < 1e-9
    P = {"E0": (0, 0), "E1": (2.2, 0), "HH": (4.4, 0)}
    node(ax, P["E0"], r"$E_0$")
    node(ax, P["E1"], r"$E_1$")
    node(ax, P["HH"], "HH", fc=LIGHT_GREEN, ec=GREEN)
    arrow(ax, P["E0"], P["E1"], "H 3/5", rad=-0.35, color=BLUE)
    arrow(ax, P["E1"], P["E0"], "T 2/5", rad=-0.35, color=RED)
    arrow(ax, P["E1"], P["HH"], "H 3/5", color=BLUE)
    self_loop(ax, P["E0"], "T 2/5", color=RED)
    _ftext(ax, 0, -0.62, "no head", color=GREY)
    _ftext(ax, 2.2, -0.62, "one head", color=GREY)
    frame(ax, -0.6, 5.0, -1.0, 1.15)
    caption(ax, r"$E_0=\frac{1}{p}+\frac{1}{p^2}=\frac{1}{0.6}+\frac{1}{0.36}=\frac{40}{9}\approx4.444$")


# ---------- 4. Absorbing ruin chain, N=7 from 2 (card 20) ----------

@figure("f04_ruin_chain", w=5.2, h=2.2, axis=False)
def _(ax):
    N, s = 7, 2
    E = {i: i * (N - i) for i in range(N + 1)}          # expected steps to absorption
    assert E[s] == 10
    for i in range(N + 1):
        if i == 0:
            node(ax, (i, 0), "0", r=0.26, fc=LIGHT_RED, ec=RED, fs=10)
        elif i == N:
            node(ax, (i, 0), str(N), r=0.26, fc=LIGHT_GREEN, ec=GREEN, fs=10)
        elif i == s:
            node(ax, (i, 0), str(i), r=0.26, fc=LIGHT_ORANGE, ec=ORANGE, fs=10)
        else:
            node(ax, (i, 0), str(i), r=0.26, fs=10)
        if 0 < i < N:
            _ftext(ax, i, -0.6, str(E[i]), color=ORANGE if i == s else GREY)
    for i in range(N):
        arrow(ax, (i, 0), (i + 1, 0), "½", rad=-0.5, color=BLUE, shrink=9, fs=9)
        arrow(ax, (i + 1, 0), (i, 0), "½", rad=-0.5, color=RED, shrink=9, fs=9)
    frame(ax, -0.6, N + 0.6, -0.95, 0.65)
    caption(ax, r"$E_i=i(N-i)$ steps to absorb, $N=7$: $E_2=2\cdot5=10$; $P(\mathrm{reach}\ 7)=\frac{2}{7}$")


# ---------- 5. Biased ruin probability curve (cards 74, 76) ----------

@figure("f04_ruin_curve", w=4.8, h=2.7)
def _(ax):
    N, r = 12, Fr(2, 3)                  # r = q/p with p = 0.6
    i = np.arange(N + 1)
    rf = 2 / 3
    Pb = (1 - rf ** i) / (1 - rf ** N)
    assert abs(Pb[4] - 6561 / 8113) < 1e-12
    ax.plot(i, i / N, ls="--", color=GREY, lw=1.3, label=r"fair: $i/12$")
    ax.plot(i, Pb, "o-", color=BLUE, ms=3.5, label=r"$P(H)=0.6$")
    ax.plot(4, Pb[4], "o", color=ORANGE, ms=6, zorder=5)
    ax.plot(4, 4 / N, "o", color=GREY, ms=5, zorder=5)
    ax.annotate(r"$i=4$: $\frac{6561}{8113}\approx0.809$", (4, Pb[4]), xytext=(5.4, 0.28),
                fontsize=9, color=ORANGE, arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.8))
    ax.annotate(r"fair: $\frac{1}{3}$", (4, 4 / N), xytext=(5.6, 0.12),
                fontsize=9, color=GREY, arrowprops=dict(arrowstyle="-", color=GREY, lw=0.8))
    ax.set_xlim(-0.3, N + 0.3); ax.set_ylim(-0.05, 1.08)
    ax.set_xticks(range(0, N + 1, 2)); ax.set_yticks([0, 0.5, 1])
    ax.set_xlabel("start $i$"); ax.set_ylabel(r"$P(\mathrm{reach}\ 12)$")
    ax.legend(frameon=False, fontsize=9, loc="upper left")
    ax.set_title(r"$P_i=\frac{1-r^{i}}{1-r^{12}}$, $r=q/p=\frac{2}{3}$", fontsize=10)


# ---------- 6. Ring hitting time, unwrapped (card 2) ----------

@figure("f04_ring_hit", w=5.2, h=2.3, axis=False)
def _(ax):
    n, start, R = 10, 3, 1.0
    E = {i: i * (n - i) for i in range(n + 1)}
    assert E[start] == 21
    th = np.linspace(0, 2 * np.pi, 200)
    ax.plot(R * np.cos(th), R * np.sin(th), color=GREY, lw=1)
    for k in range(n):
        a = 2 * np.pi * k / n
        xy = (R * np.sin(a), R * np.cos(a))
        if k == 0:
            node(ax, xy, "0", r=0.17, fc=LIGHT_GREEN, ec=GREEN, fs=9)
        elif k == start:
            node(ax, xy, str(k), r=0.17, fc=LIGHT_ORANGE, ec=ORANGE, fs=9)
        else:
            node(ax, xy, str(k), r=0.17, fs=9)
    ax.text(0, 1.42, "ring of 10", ha="center", fontsize=9, color=GREY)
    # unwrapped segment 0..10, both ends are vertex 0
    x0, dx = 2.9, 0.42
    ax.plot([x0, x0 + n * dx], [0, 0], color=GREY, lw=1, zorder=1)
    for i in range(n + 1):
        xy = (x0 + i * dx, 0)
        if i in (0, n):
            node(ax, xy, str(i), r=0.16, fc=LIGHT_GREEN, ec=GREEN, fs=9)
        elif i == start:
            node(ax, xy, str(i), r=0.16, fc=LIGHT_ORANGE, ec=ORANGE, fs=9)
        else:
            node(ax, xy, str(i), r=0.16, fs=9)
        if 0 < i < n:
            _ftext(ax, x0 + i * dx, -0.6, str(E[i]), color=ORANGE if i == start else GREY)
    ax.text(x0 + n * dx / 2, 1.0, "unwrap at vertex 0", ha="center", fontsize=9, color=GREY)
    frame(ax, -1.3, x0 + n * dx + 0.4, -1.6, 1.5)
    caption(ax, r"$E_i=i(10-i)$ on $\{0,\dots,10\}$: $E_3=3\cdot7=21$")


# ---------- 7 & 8. Reflection principle for the running maximum (cards 3, 65, 35) ----------

def _reflect(ax, n, a):
    for seed in range(1, 5000):
        rng = np.random.default_rng(seed)
        s = np.concatenate([[0], np.cumsum(rng.choice([-1, 1], size=n))])
        hit = np.where(s >= a)[0]
        if len(hit) and 3 <= hit[0] <= n - 3 and s[-1] <= a - 2:
            break
    tau = int(hit[0])
    k = np.arange(n + 1)
    refl = np.where(k >= tau, 2 * a - s, np.nan)
    ax.plot(k, refl, "--", color=ORANGE, lw=1.4, zorder=2)
    ax.plot(k, s, "o-", color=BLUE, ms=3, lw=1.6, zorder=3)
    ax.axhline(a, color=GREEN, ls=":", lw=1.2)
    ax.plot(tau, a, "o", color=GREEN, ms=5, zorder=4)
    ax.plot(n, s[-1], "o", color=BLUE, ms=5, zorder=4)
    ax.plot(n, 2 * a - s[-1], "o", mfc="white", mec=ORANGE, ms=5, zorder=4)
    ax.text(tau, a + 0.45, r"$\tau$", color=GREEN, fontsize=9, ha="center")
    ax.text(n + 0.25, 2 * a - s[-1], "reflected\npath", color=ORANGE, fontsize=9, va="center")
    # exact probabilities from the reflection identity
    Pge = Fr(sum(comb(n, j) for j in range(n + 1) if 2 * j - n >= a), 2 ** n)
    Pgt = Fr(sum(comb(n, j) for j in range(n + 1) if 2 * j - n > a), 2 ** n)
    ax.set_xlim(-0.4, n + 2.6)
    ax.set_ylim(min(s.min(), 2 * a - s[-1]) - 1, max(a, 2 * a - s[-1]) + 1.2)
    ax.set_xticks(range(0, n + 1, 2))
    ax.set_xlabel("step $n$"); ax.set_ylabel(r"$S_n$")
    ax.set_title(f"reflect after $\\tau$, the first hit of ${a}$\n"
                 + rf"$P(M_{{{n}}}\geq{a})=P(S_{{{n}}}\geq{a})+P(S_{{{n}}}>{a})={fr(Pge + Pgt)}$",
                 fontsize=9)
    return Pge + Pgt, seed, s


@figure("f04_reflection_max10", w=5.0, h=2.7)
def _(ax):
    PM, seed, s = _reflect(ax, 10, 4)
    assert PM == Fr(29, 128)


@figure("f04_reflection_max8", w=5.0, h=2.7)
def _(ax):
    PM, seed, s = _reflect(ax, 8, 3)
    assert PM == Fr(37, 128)


# ---------- 9 & 10. First passage: lattice paths (cards 16, 36) ----------

def _first_visit(ax, a, n):
    valid_count = 0
    for steps in itertools.product([-1, 1], repeat=n):
        s = np.concatenate([[0], np.cumsum(steps)])
        if s[-1] != a:
            continue
        valid = bool(s[:-1].max() < a)
        valid_count += valid
        ax.plot(range(n + 1), s, color=BLUE if valid else GREY,
                lw=2.0 if valid else 1.0, alpha=1.0 if valid else 0.4, zorder=3 if valid else 2)
    p = Fr(valid_count, 2 ** n)
    assert p == Fr(a, n) * Fr(comb(n, (n + a) // 2), 2 ** n)
    ax.axhline(a, color=ORANGE, ls="--", lw=1)
    ax.plot(n, a, "o", color=GREEN, ms=6, zorder=5)
    ax.set_xticks(range(0, n + 1)); ax.set_yticks(range(-(n - 1), n))
    ax.set_ylim(-(n - 1) - 0.6, n + 0.6)
    ax.set_xlabel("step $n$"); ax.set_ylabel(r"$S_n$")
    ax.set_title(rf"first visit to ${a:+d}$ at step ${n}$: {valid_count} of {2 ** n} paths, "
                 rf"$\frac{{{Fr(a, n).numerator}}}{{{Fr(a, n).denominator}}}\cdot P(S_{{{n}}}={a})={fr(p)}$",
                 fontsize=9)


@figure("f04_first_visit_1_5", w=4.8, h=2.7)
def _(ax):
    _first_visit(ax, 1, 5)


@figure("f04_first_visit_2_4", w=4.8, h=2.7)
def _(ax):
    _first_visit(ax, 2, 4)


# ---------- 11. Ballot: paths ending at +4 that stay positive (cards 37, 61) ----------

@figure("f04_ballot", w=5.0, h=2.7)
def _(ax):
    n = 10
    good = []
    total_end = 0
    for steps in itertools.product([-1, 1], repeat=n):
        s = np.concatenate([[0], np.cumsum(steps)])
        if s[-1] == 4:
            total_end += 1
            if (s[1:] > 0).all():
                good.append(s)
    assert len(good) == 48 and total_end == 120
    for s in good:
        ax.plot(range(n + 1), s, color=BLUE, lw=0.8, alpha=0.2)
    ax.axhline(0, color=RED, ls="--", lw=1.1)
    ax.plot(n, 4, "o", color=GREEN, ms=5, zorder=5)
    ax.set_xticks(range(0, n + 1, 2)); ax.set_yticks(range(-2, 6, 2))
    ax.set_ylim(-2.5, 6.6)
    ax.set_xlabel("step $n$"); ax.set_ylabel(r"$S_n$")
    ax.set_title(r"48 of the 120 paths ending at $+4$ stay above $0$: $\frac{48}{1024}=\frac{3}{64}$",
                 fontsize=9.5)


# ---------- 12 & 13. Penney race HT vs HH (cards 12, 57) ----------

def _ht_hh(ax, pl, ql):
    pos = {"S": (0, 0), "H": (2.0, 0), "HH": (4.0, 0.95), "HT": (4.0, -0.95)}
    node(ax, pos["S"], "∅")
    node(ax, pos["H"], "H")
    box(ax, pos["HH"], "HH: Bob", w=1.45, h=0.5, fc=LIGHT_RED, ec=RED, fs=10)
    box(ax, pos["HT"], "HT: Alice", w=1.45, h=0.5, fc=LIGHT_GREEN, ec=GREEN, fs=10)
    arrow(ax, pos["S"], pos["H"], f"H {pl}", color=BLUE, shrink=14)
    self_loop(ax, pos["S"], f"T {ql}", color=RED)
    arrow(ax, (2.25, 0.12), (3.2, 0.8), f"H {pl}", color=BLUE, shrink=0)
    arrow(ax, (2.25, -0.12), (3.2, -0.8), f"T {ql}", color=RED, shrink=0)
    frame(ax, -0.8, 6.3, -1.5, 1.5)


@figure("f04_ht_hh_race", w=5.0, h=2.6, axis=False)
def _(ax):
    _ht_hh(ax, "½", "½")
    caption(ax, r"after the first $H$: $P(\mathrm{Alice\ wins})=\frac{1}{2}$")


@figure("f04_ht_hh_biased", w=5.0, h=2.6, axis=False)
def _(ax):
    _ht_hh(ax, "3/5", "2/5")
    assert abs((1 - 0.6) - 0.4) < 1e-12
    caption(ax, r"after the first $H$: $P(\mathrm{Alice})=\frac{2}{5}$, $P(\mathrm{Bob})=\frac{3}{5}$")


# ---------- 14. Penney best-reply cycle (cards 68, 78, 79) ----------

@figure("f04_penney_cycle", w=4.4, h=3.0, axis=False)
def _(ax):
    # verified exactly: THH beats HHT 3/4, TTH beats THH 2/3, HTT beats TTH 3/4, HHT beats HTT 2/3
    P = {"HHT": (0, 1), "THH": (2, 1), "TTH": (2, -1), "HTT": (0, -1)}
    for name, xy in P.items():
        box(ax, xy, name, w=0.9, h=0.5, fs=10)
    _edge(ax, P["THH"], P["HHT"], rA=0.5, rB=0.5, label="3:1", color=BLUE, off=(0, 0.3))
    _edge(ax, P["TTH"], P["THH"], rA=0.3, rB=0.3, label="2:1", color=BLUE, off=(0.4, 0))
    _edge(ax, P["HTT"], P["TTH"], rA=0.5, rB=0.5, label="3:1", color=BLUE, off=(0, -0.3))
    _edge(ax, P["HHT"], P["HTT"], rA=0.3, rB=0.3, label="2:1", color=BLUE, off=(-0.4, 0))
    ax.text(1, 0, "no best\nreply", ha="center", va="center", fontsize=9.5, color=GREY)
    frame(ax, -1.0, 3.0, -1.8, 1.8)
    caption(ax, "arrow = beats; label = odds of the winner", fs=9)


# ---------- 15. Penney chain with p = 3/5 (card 48) ----------

@figure("f04_penney_biased_chain", w=5.4, h=2.9, axis=False)
def _(ax):
    p, q = 0.6, 0.4
    # states = longest suffix that is a prefix of THH or HHT; x = P(THH first)
    x = {"": 0.0, "H": 0.0, "T": 0.0, "TH": 0.0, "HH": 0.0}
    # solve the first-step equations exactly
    names = ["", "H", "T", "TH", "HH"]
    A = np.eye(5); b = np.zeros(5)
    idx = {s: i for i, s in enumerate(names)}
    trans = {"": {"H": "H", "T": "T"}, "H": {"H": "HH", "T": "T"}, "T": {"H": "TH", "T": "T"},
             "TH": {"H": "THH", "T": "T"}, "HH": {"H": "HH", "T": "HHT"}}
    for s in names:
        for c in "HT":
            pr = p if c == "H" else q
            t = trans[s][c]
            if t == "THH":
                b[idx[s]] += pr
            elif t == "HHT":
                pass
            else:
                A[idx[s], idx[t]] -= pr
    sol = np.linalg.solve(A, b)
    assert abs(sol[idx[""]] - 16 / 25) < 1e-12
    pos = {"": (0, 0), "H": (1.7, 0.9), "T": (0, -1.1), "HH": (3.4, 0.9), "TH": (1.7, -1.1)}
    for s, xy in pos.items():
        node(ax, xy, "∅" if s == "" else s, r=0.28, fs=10)
    box(ax, (3.4, -1.1), "THH", w=0.9, h=0.42, fc=LIGHT_GREEN, ec=GREEN, fs=9.5)
    box(ax, (5.0, 0.9), "HHT", w=0.9, h=0.42, fc=LIGHT_RED, ec=RED, fs=9.5)
    _edge(ax, pos[""], pos["H"], rA=0.3, rB=0.3, label="3/5", color=BLUE, off=(-0.2, 0.2))
    _edge(ax, pos[""], pos["T"], rA=0.3, rB=0.3, label="2/5", color=RED, off=(-0.3, 0))
    _edge(ax, pos["H"], pos["HH"], rA=0.3, rB=0.3, label="3/5", color=BLUE, off=(0, 0.2))
    _edge(ax, pos["H"], pos["T"], rA=0.3, rB=0.3, label="2/5", color=RED, rad=0.25, off=(0.25, 0.1))
    _edge(ax, pos["T"], pos["TH"], rA=0.3, rB=0.3, label="3/5", color=BLUE, rad=-0.25, off=(0, -0.3))
    _edge(ax, pos["TH"], pos["T"], rA=0.3, rB=0.3, label="2/5", color=RED, rad=-0.25, off=(0, 0.3))
    _edge(ax, pos["TH"], (3.4, -1.1), rA=0.3, rB=0.45, label="3/5", color=BLUE, off=(0, -0.22))
    _edge(ax, pos["HH"], (5.0, 0.9), rA=0.3, rB=0.45, label="2/5", color=RED, off=(0, 0.2))
    self_loop(ax, pos["T"], "2/5", color=RED, up=False)
    self_loop(ax, pos["HH"], "3/5", color=BLUE)
    frame(ax, -0.7, 5.8, -2.0, 1.9)
    caption(ax, r"$P(\mathrm{THH\ first})=\frac{16}{25}$, state = longest suffix that prefixes THH or HHT")


# ---------- 16 & 17. Generating function, extinction (cards 42, 64, 50) ----------

def _gw(ax, p0, p1, p2):
    s = np.linspace(0, 1.05, 300)
    G = p0 + p1 * s + p2 * s ** 2
    ax.plot(s, G, color=BLUE, lw=1.8, label=r"$G(s)$")
    ax.plot([0, 1.05], [0, 1.05], color=GREY, ls="--", lw=1)
    roots = sorted(r.real for r in np.roots([p2, p1 - 1, p0])
                   if abs(r.imag) < 1e-9 and -1e-9 <= r.real <= 1 + 1e-9)
    q = roots[0]
    ax.plot(q, q, "o", color=GREEN, ms=6, zorder=5)
    ax.annotate(rf"$q={fr(Fr(q).limit_denominator(100))}$" if abs(q - 1) > 1e-9 else r"$q=1$",
                (q, q), xytext=(q + 0.12, q - 0.3), fontsize=9, color=GREEN,
                arrowprops=dict(arrowstyle="-", color=GREEN, lw=0.8))
    ax.set_xlim(0, 1.05); ax.set_ylim(0, 1.05)
    ax.set_xlabel("$s$"); ax.set_ylabel("$G(s)$")
    ax.set_xticks([0, 0.5, 1]); ax.set_yticks([0, 0.5, 1])
    return q


@figure("f04_gw_fixed", w=4.6, h=2.8)
def _(ax):
    q = _gw(ax, Fr(1, 4), 0, Fr(3, 4))
    assert abs(q - 1 / 3) < 1e-9
    ax.set_title(r"$G(s)=\frac{1}{4}+\frac{3}{4}s^2$; smallest root of $G(s)=s$ is $q=\frac{1}{3}$",
                 fontsize=9.5)


@figure("f04_gw_critical", w=4.6, h=2.8)
def _(ax):
    q = _gw(ax, Fr(1, 2), 0, Fr(1, 2))
    assert abs(q - 1) < 1e-6
    ax.set_title(r"$G(s)=\frac{1}{2}+\frac{1}{2}s^2$ touches $s$ only at $s=1$: $q=1$",
                 fontsize=9.5)


# ---------- 18. Polya urn tree, first three draws (cards 8, 60) ----------

@figure("f04_polya_tree", w=5.2, h=3.1, axis=False)
def _(ax):
    seqs = ["".join(t) for t in itertools.product("RB", repeat=3)]
    ypos = {s: 7 - i for i, s in enumerate(seqs)}

    def state(prefix):
        r, b = 1, 1
        for c in prefix:
            if c == "R":
                r += 1
            else:
                b += 1
        return r, b

    def prob(seq):
        pr = Fr(1)
        for k, c in enumerate(seq):
            r, b = state(seq[:k])
            pr *= Fr(r, r + b) if c == "R" else Fr(b, r + b)
        return pr

    probs = {s: prob(s) for s in seqs}
    assert sum(probs.values()) == 1 and probs["RRR"] == Fr(1, 4)

    def ynode(prefix):
        ls = [ypos[s] for s in seqs if s.startswith(prefix)]
        return sum(ls) / len(ls)

    def xy(prefix):
        return (len(prefix), ynode(prefix))

    for k in range(3):
        for pre in itertools.product("RB", repeat=k):
            pre = "".join(pre)
            r, b = state(pre)
            for c in "RB":
                child = pre + c
                pe = Fr(r, r + b) if c == "R" else Fr(b, r + b)
                on = "RRR".startswith(child)
                col = BLUE if on else GREY
                (x0, y0), (x1, y1) = xy(pre), xy(child)
                ax.plot([x0, x1], [y0, y1], color=col, lw=2.0 if on else 0.9, zorder=1)
                ax.text((x0 + x1) / 2, (y0 + y1) / 2 + (0.2 if y1 > y0 else -0.2), "$" + fr(pe) + "$",
                        fontsize=9, color=col, ha="center", va="center",
                        bbox=dict(fc="white", ec="none", pad=0.4), zorder=3)
    for s in seqs:
        pass
    for pre in [""] + ["".join(t) for k in (1, 2) for t in itertools.product("RB", repeat=k)]:
        ax.plot(*xy(pre), "o", color=INK, ms=2.5, zorder=4)
    for s in seqs:
        ax.plot(3, ypos[s], "o", color=GREEN if s == "RRR" else INK, ms=3, zorder=4)
        ax.text(3.2, ypos[s], s + ":  $" + fr(probs[s]) + "$", fontsize=9,
                color=GREEN if s == "RRR" else INK, va="center")
    ax.set_xlim(-0.3, 4.6); ax.set_ylim(-1.2, 7.7)
    ax.text(-0.25, -0.9, r"$P(RRR)=\frac{1}{2}\cdot\frac{2}{3}\cdot\frac{3}{4}=\frac{1}{4}$ (start 1 R, 1 B)",
            fontsize=9, color=INK)


# ---------- 19 & 20. Doubling strategy, optional stopping (cards 11, 54) ----------

def _doubling(ax, p):
    q = 1 - p
    pwin, plose = 1 - q ** 5, q ** 5
    E = pwin - 31 * plose
    ax.plot([1], [0], "o", color=BLUE, ms=4 + 14 * float(pwin), zorder=3)
    ax.plot([-31], [0], "o", color=RED, ms=4 + 14 * float(plose), zorder=3)
    ax.axvline(float(E), color=ORANGE, ls="--", lw=1.2)
    ax.axhline(0, color=GREY, lw=0.8)
    ax.text(1, 0.22, "+1 (win by round 5)", ha="center", fontsize=9, color=BLUE)
    ax.text(-31, 0.22, "-31 (lose all 5)", ha="center", fontsize=9, color=RED)
    ax.text(1.0, -0.3, "$P=" + fr(pwin) + "$", ha="center", fontsize=9, color=BLUE)
    ax.text(-31, -0.3, "$P=" + fr(plose) + "$", ha="center", fontsize=9, color=RED)
    ax.text(float(E) + 0.6, 0.62, "$E=" + fr(E) + "$", fontsize=9, color=ORANGE)
    ax.set_xlim(-34, 4); ax.set_ylim(-0.6, 0.85)
    ax.set_yticks([])
    ax.set_xticks([-31, -20, -10, 0]); ax.set_xlabel("profit when the strategy stops")
    return E


@figure("f04_doubling_cap", w=5.0, h=2.4)
def _(ax):
    E = _doubling(ax, Fr(1, 2))
    assert E == 0
    ax.set_title(r"$E=\frac{31}{32}\cdot1+\frac{1}{32}\cdot(-31)=0$: stopped wealth is bounded",
                 fontsize=9.5)


@figure("f04_doubling_biased", w=5.0, h=2.4)
def _(ax):
    E = _doubling(ax, Fr(3, 5))
    assert E == 1 - 32 * Fr(2, 5) ** 5 and abs(float(E) - 0.67232) < 1e-9
    ax.set_title(r"$E=1-32q^5=1-32(0.4)^5=0.67232$ with $P(H)=\frac{3}{5}$", fontsize=9.5)


# ---------- 21. Two barriers, E[T] = ab (card 45) ----------

@figure("f04_two_barrier", w=5.0, h=2.7)
def _(ax):
    lo, hi = -2, 5
    for seed in range(1, 5000):
        rng = np.random.default_rng(seed)
        s = [0]
        while lo < s[-1] < hi:
            s.append(s[-1] + rng.choice([-1, 1]))
        if s[-1] == hi and 10 <= len(s) - 1 <= 14:
            break
    T = len(s) - 1
    assert Fr(4 * 5, 7) + Fr(25 * 2, 7) == 10
    ax.step(range(T + 1), s, where="post", color=BLUE, lw=1.6)
    ax.plot(T, s[-1], "o", color=GREEN, ms=5, zorder=5)
    ax.axhline(hi, color=GREEN, ls="--", lw=1.1)
    ax.axhline(lo, color=RED, ls="--", lw=1.1)
    ax.text(0.2, hi + 0.35, "absorb at 5", color=GREEN, fontsize=9)
    ax.text(0.2, lo - 0.75, "absorb at -2", color=RED, fontsize=9)
    ax.set_ylim(lo - 1.1, hi + 1.0)
    ax.set_yticks([-2, 0, 5]); ax.set_xticks(range(0, T + 1, 2))
    ax.set_xlabel("step $n$"); ax.set_ylabel(r"$S_n$")
    ax.set_title(r"$E[T]=E[S_T^2]=4\cdot\frac{5}{7}+25\cdot\frac{2}{7}=10$  (since $S_n^2-n$ is a martingale)",
                 fontsize=9)


# ---------- 22. Knight walk: stationary law proportional to degree (cards 9, 32) ----------

@figure("f04_knight_degree", w=5.5, h=3.1, axis=False)
def _(ax):
    mv = [(1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1)]
    deg = np.zeros((8, 8), int)
    for r in range(8):
        for c in range(8):
            deg[r, c] = sum(1 for dr, dc in mv if 0 <= r + dr < 8 and 0 <= c + dc < 8)
    assert deg.sum() == 336 and deg[3, 3] == 8 and deg[0, 0] == 2
    cmap = LinearSegmentedColormap.from_list("lb", [LIGHT_BLUE, BLUE])
    for r in range(8):
        for c in range(8):
            d = deg[r, c]
            v = (d - 2) / 6
            ax.add_patch(Rectangle((c, 7 - r), 1, 1, fc=cmap(v), ec="white", lw=1.2))
            ax.text(c + 0.5, 7 - r + 0.5, str(d), ha="center", va="center", fontsize=9,
                    color="white" if v > 0.55 else INK)
    ax.add_patch(Rectangle((3, 4), 1, 1, fill=False, ec=ORANGE, lw=2.4, zorder=5))
    ax.add_patch(Rectangle((0, 7), 1, 1, fill=False, ec=GREEN, lw=2.4, zorder=5))
    tx = 8.6
    lines = [(r"$\pi(v)=\frac{\mathrm{deg}\,v}{336}$", INK),
             ("", INK),
             ("centre (3,3), orange", ORANGE),
             (r"$\mathrm{deg}=8$", ORANGE),
             (r"return $=\frac{336}{8}=42$", ORANGE),
             ("", INK),
             ("corner (0,0), green", GREEN),
             (r"$\mathrm{deg}=2$", GREEN),
             (r"return $=\frac{336}{2}=168$", GREEN)]
    for i, (s, col) in enumerate(lines):
        ax.text(tx, 7.6 - 0.62 * i, s, fontsize=9, color=col, va="center")
    ax.set_xlim(-0.2, 12.2); ax.set_ylim(-0.2, 8.3)
    ax.set_aspect("equal")


# ---------- 23. Birth-death chain, detailed balance (cards 10, 33) ----------

@figure("f04_birth_death", w=5.2, h=2.5, axis=False)
def _(ax):
    # detailed balance: pi0 * 1 = pi1 * 1/3 ; pi_k * 2/3 = pi_{k+1} * 1/3 (k=1,2,3) ; pi3 * 2/3 = pi4 * 1
    pi = [Fr(1)]
    pi.append(pi[0] * 1 / Fr(1, 3))
    pi.append(pi[1] * Fr(2, 3) / Fr(1, 3))
    pi.append(pi[2] * Fr(2, 3) / Fr(1, 3))
    pi.append(pi[3] * Fr(2, 3) / 1)
    tot = sum(pi)
    pi = [x / tot for x in pi]
    assert pi[0] == Fr(1, 30) and pi[4] == Fr(4, 15)
    xs = [k * 1.25 for k in range(5)]
    for k, x in enumerate(xs):
        node(ax, (x, 0), str(k), r=0.3, fs=10, fc=LIGHT_ORANGE if k == 0 else "white",
             ec=ORANGE if k == 0 else INK)
        ax.text(x, -0.75, "$" + fr(pi[k]) + "$", ha="center", va="center", fontsize=9, color=GREY)
    up = ["1", "2/3", "2/3", "2/3"]
    dn = ["1/3", "1/3", "1/3", "1"]
    for k in range(4):
        arrow(ax, (xs[k], 0), (xs[k + 1], 0), up[k], rad=-0.4, color=BLUE, shrink=9, fs=9)
        arrow(ax, (xs[k + 1], 0), (xs[k], 0), dn[k], rad=-0.4, color=RED, shrink=9, fs=9)
    frame(ax, -0.6, xs[-1] + 0.6, -1.2, 1.1)
    caption(ax, r"$\pi_k\cdot p_{k,k+1}=\pi_{k+1}\cdot p_{k+1,k}$, so $\pi\propto(1,3,6,12,8)$ and $\pi_0=\frac{1}{30}$")


# ---------- 24 & 25. Reflect at 0, absorb at N: E_i = N^2 - i^2 (cards 46, 59) ----------

def _reflect_hit(ax, N):
    M = np.zeros((N, N)); rhs = np.ones(N)
    M[0, 0] = 1; M[0, 1] = -1                     # reflecting end: E0 = 1 + E1
    for i in range(1, N):
        M[i, i] = 1
        M[i, i - 1] = -0.5
        if i + 1 < N:
            M[i, i + 1] = -0.5                    # E_N = 0 (absorbing)
    E = np.linalg.solve(M, rhs)
    assert abs(E[0] - N * N) < 1e-9
    xs = list(range(N + 1))
    for i in xs:
        if i == N:
            node(ax, (i, 0), str(i), r=0.22, fc=LIGHT_GREEN, ec=GREEN, fs=9)
        elif i == 0:
            node(ax, (i, 0), "0", r=0.22, fc=LIGHT_ORANGE, ec=ORANGE, fs=9)
        else:
            node(ax, (i, 0), str(i), r=0.22, fs=9)
        if i < N:
            _ftext(ax, i, -0.62, str(N * N - i * i), color=ORANGE if i == 0 else GREY)
    arrow(ax, (0, 0), (1, 0), "1", rad=-0.6, color=BLUE, shrink=8, fs=9)
    for i in range(1, N):
        arrow(ax, (i, 0), (i + 1, 0), "½", rad=-0.6, color=BLUE, shrink=8, fs=9)
        arrow(ax, (i + 1, 0), (i, 0), "½", rad=-0.6, color=RED, shrink=8, fs=9)
    frame(ax, -0.6, N + 0.6, -1.0, 0.8)
    return E


@figure("f04_reflect_hit5", w=5.0, h=2.3, axis=False)
def _(ax):
    _reflect_hit(ax, 5)
    caption(ax, r"$E_i=25-i^2$ on $\{0,\dots,5\}$, state $0$ reflecting: $E_0=25$")


@figure("f04_corridor9", w=5.4, h=2.3, axis=False)
def _(ax):
    _reflect_hit(ax, 9)
    caption(ax, r"$E_i=81-i^2$ from the end shelf: $E_0=N^2=81$ with $N=9$ steps inward")


# ---------- 26. Coupon phases (card 18) ----------

@figure("f04_coupon_phases", w=5.0, h=2.7)
def _(ax):
    n = 6
    waits = [Fr(n, n - k) for k in range(n)]          # phase k: k faces seen, wait n/(n-k)
    tot = sum(waits)
    assert tot == Fr(147, 10)
    vals = [float(w) for w in waits]
    ax.bar(range(n), vals, color=BLUE, width=0.6)
    for k, (v, w) in enumerate(zip(vals, waits)):
        lab = str(w.numerator) if w.denominator == 1 else f"{w.numerator}/{w.denominator}"
        ax.text(k, v + 0.12, lab, ha="center", fontsize=9)
    ax.set_xticks(range(n)); ax.set_ylim(0, 7.4)
    ax.set_xlabel("faces already seen $k$"); ax.set_ylabel("expected wait")
    ax.set_title(rf"$\sum_{{k=0}}^{{5}}\frac{{6}}{{6-k}}=6H_6={fr(tot)}\approx14.7$", fontsize=9.5)


# ---------- 27. Tail-sum bars, die total passes 6 (card 5) ----------

@figure("f04_tail_bars", w=5.0, h=2.7)
def _(ax):
    L = 6
    dist = {0: Fr(1)}
    tails = []
    for k in range(L + 1):
        tails.append(sum(v for s, v in dist.items() if s <= L))   # P(N > k) = P(S_k <= 6)
        new = {}
        for s, v in dist.items():
            for f in range(1, 7):
                new[s + f] = new.get(s + f, Fr(0)) + v / 6
        dist = new
    E = sum(tails)
    assert E == Fr(7 ** 6, 6 ** 6)
    ax.bar(range(L + 1), [float(t) for t in tails], color=BLUE, width=0.6)
    for k, t in enumerate(tails):
        ax.text(k, float(t) + 0.03, f"{float(t):.3f}", ha="center", fontsize=9)
    ax.set_xticks(range(L + 1)); ax.set_ylim(0, 1.2)
    ax.set_xlabel("$k$"); ax.set_ylabel(r"$P(N>k)$")
    ax.set_title(rf"$E[N]=\sum_{{k\geq0}}P(N>k)=\frac{{7^6}}{{6^6}}\approx{float(E):.3f}$", fontsize=9.5)


# ---------- 28. Overlaps for leading numbers (card 24) ----------

@figure("f04_overlap_htx", w=5.2, h=3.0, axis=False)
def _(ax):
    def word(y, letters, x0, hl=None, fill=LIGHT_ORANGE):
        for j, ch in enumerate(letters):
            fc = fill if (hl is not None and j in hl) else "white"
            ax.add_patch(Rectangle((x0 + j * 0.8, y - 0.3), 0.7, 0.6, fc=fc, ec=INK, lw=1))
            ax.text(x0 + j * 0.8 + 0.35, y, ch, ha="center", va="center", fontsize=10)

    def name(y, s):
        ax.text(-0.3, y, s, ha="right", va="center", fontsize=10, weight="bold")

    # HTH: k=1 overlap (last H = first H of the shifted copy), then the whole word (k=3)
    assert "HTH"[:1] == "HTH"[-1:] and "HTH"[:3] == "HTH"
    name(1.0, "HTH")
    word(1.0, "HTH", 0, hl={2})
    word(0.1, "HTH", 1.6, hl={0})                 # shifted by 2 letters
    ax.text(4.3, 1.0, r"$k=1$: $2^1=2$", fontsize=9, va="center", color=ORANGE)
    name(-0.9, "HTH")
    word(-0.9, "HTH", 0, hl={0, 1, 2}, fill=LIGHT_GREEN)
    ax.text(4.3, -0.9, r"$k=3$: $2^3=8$", fontsize=9, va="center", color=GREEN)
    ax.text(4.3, -1.6, r"total $2+8=10$", fontsize=9, va="center")
    # HHT: only the whole word overlaps
    name(-2.2, "HHT")
    word(-2.2, "HHT", 0, hl={0, 1, 2}, fill=LIGHT_GREEN)
    ax.text(4.3, -2.2, r"$k=3$ only: $8$", fontsize=9, va="center", color=GREEN)
    ax.set_xlim(-1.3, 6.2); ax.set_ylim(-3.0, 1.6)
    ax.set_aspect("equal")
    ax.text(-1.2, -2.85, r"$E[\mathrm{wait}]=\sum_{k\in O}2^k$, $O$ = lengths where prefix equals suffix",
            fontsize=9, color=GREY, va="center")
