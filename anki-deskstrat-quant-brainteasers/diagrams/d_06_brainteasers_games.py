"""Figures for cards/06_brainteasers_games.json."""
import heapq, itertools, math
from fractions import Fraction as Fr
from functools import lru_cache
import numpy as np
from qcfig import *


# ---------- exact helpers (every number a figure states is recomputed here) ----------

def _mex(s):
    m = 0
    while m in s:
        m += 1
    return m


def _grundy(moves, nmax):
    g = []
    for n in range(nmax + 1):
        g.append(_mex({g[n - m] for m in moves if m <= n}))
    return g


def _tileable(free):
    free = frozenset(free)
    if not free:
        return True
    i, j = min(free)
    for nb in [(i, j + 1), (i + 1, j)]:
        if nb in free and _tileable(free - {(i, j), nb}):
            return True
    return False


def _pirates(n, total=100):
    """Backward induction for n pirates; a vote costs the victim's continuation value + 1."""
    if n == 1:
        return (total,)
    prev = _pirates(n - 1, total)
    need = math.ceil(n / 2) - 1
    order = sorted(range(1, n), key=lambda j: prev[j - 1])
    give = [0] * n
    for j in order[:need]:
        give[j] = prev[j - 1] + 1
    give[0] = total - sum(give)
    return tuple(give)


def _bridge_min(times, cap):
    n = len(times)
    full = frozenset(range(n))
    start, goal = (full, 0), (frozenset(), 1)
    dist, pq, cnt = {start: 0}, [(0, 0, start)], 0
    while pq:
        d, _, state = heapq.heappop(pq)
        if state == goal:
            return d
        if d > dist.get(state, math.inf):
            continue
        left, t = state
        here = left if t == 0 else full - left
        for k in range(1, cap + 1):
            for grp in itertools.combinations(sorted(here), k):
                cost = max(times[g] for g in grp)
                nl = (left - set(grp)) if t == 0 else (left | set(grp))
                ns = (frozenset(nl), 1 - t)
                if d + cost < dist.get(ns, math.inf):
                    dist[ns] = d + cost
                    cnt += 1
                    heapq.heappush(pq, (d + cost, cnt, ns))
    return None


def _secretary_p(k, n=100):
    """Success probability when the first k applicants are rejected (threshold r = k + 1)."""
    if k == 0:
        return Fr(1, n)
    return Fr(k, n) * sum(Fr(1, i - 1) for i in range(k + 1, n + 1))


@lru_cache(None)
def _rb_value(r, b):
    if r == 0 or b == 0:
        return Fr(0)
    cont = Fr(r, r + b) * _rb_value(r - 1, b) + Fr(b, r + b) * _rb_value(r, b - 1)
    return max(Fr(r, r + b), cont)


_ACC = {"A": Fr(1, 3), "B": Fr(1, 2), "C": Fr(1)}
_ORDER = ["A", "B", "C"]


def _next_shooter(alive, cur):
    i = _ORDER.index(cur)
    for k in range(1, 4):
        p = _ORDER[(i + k) % 3]
        if p in alive:
            return p


def _solve_exact(M, b):
    n = len(b)
    A = [row[:] + [b[i]] for i, row in enumerate(M)]
    for c in range(n):
        piv = next(r for r in range(c, n) if A[r][c] != 0)
        A[c], A[piv] = A[piv], A[c]
        pv = A[c][c]
        A[c] = [x / pv for x in A[c]]
        for r in range(n):
            if r != c and A[r][c] != 0:
                f = A[r][c]
                A[r] = [x - f * y for x, y in zip(A[r], A[c])]
    return [A[i][n] for i in range(n)]


def _truel_win(targets):
    """targets[(alive, shooter)] = target for the all-alive states. Returns each player's win probability."""
    states = [(frozenset(c), s) for k in (2, 3) for c in itertools.combinations(_ORDER, k) for s in c]
    idx = {s: i for i, s in enumerate(states)}
    out = {}
    for p in _ORDER:
        M = [[Fr(0)] * len(states) for _ in states]
        b = [Fr(0)] * len(states)
        for i, (alive, s) in enumerate(states):
            M[i][i] += 1
            t = targets[(alive, s)] if len(alive) == 3 else next(x for x in alive if x != s)
            hit = _ACC[s]
            na = alive - {t}
            if len(na) == 1:
                if p in na:
                    b[i] += hit
            else:
                M[i][idx[(na, _next_shooter(na, s))]] -= hit
            M[i][idx[(alive, _next_shooter(alive, s))]] -= 1 - hit
        out[p] = _solve_exact(M, b)[idx[(frozenset(_ORDER), "A")]]
    return out


def _u(x):
    """Burn time from the left end to x, as a fraction of the total (non-uniform rope)."""
    return x + 0.15 / (2 * np.pi) * (1 - np.cos(2 * np.pi * x))


def _x_at(target):
    lo, hi = 0.0, 1.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if _u(mid) < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


# ---------- 0. chessboard (card 0) ----------

@figure("f06_chessboard_colour", w=4.2, h=3.2, axis=False)
def _(ax):
    removed = {(0, 0), (7, 7)}  # a1 and h8 as (file, rank), 0-based
    assert sum(1 for f in range(8) for r in range(8) if (f + r) % 2 == 0 and (f, r) not in removed) == 30
    for f in range(8):
        for r in range(8):
            if (f, r) in removed:
                fc = LIGHT_RED
            else:
                fc = LIGHT_BLUE if (f + r) % 2 == 0 else "white"
            ax.add_patch(Rectangle((f, r), 1, 1, fc=fc, ec=INK, lw=0.6, zorder=1))
            if (f, r) in removed:
                ax.text(f + 0.5, r + 0.5, "×", ha="center", va="center", fontsize=14, color=RED, zorder=3)
    for f in range(8):
        ax.text(f + 0.5, -0.4, "abcdefgh"[f], ha="center", va="center", fontsize=9)
    for r in range(8):
        ax.text(-0.4, r + 0.5, str(r + 1), ha="center", va="center", fontsize=9)
    frame(ax, -0.8, 8.2, -1.6, 8.3)
    caption(ax, "blue: i+j even (black in the card)\n"
                "a1 and h8 removed: 30 blue, 32 white, so no tiling", fs=9)


# ---------- 1. balanced but untileable 4x4 (card 3) ----------

@figure("f06_balanced_4x4", w=4.2, h=3.0, axis=False)
def _(ax):
    holes = {(1, 1), (1, 3), (3, 4), (4, 3)}  # (row, column), 1-based, row 1 at the top
    cells = {(r, c) for r in range(1, 5) for c in range(1, 5) if (r, c) not in holes}
    even = sum(1 for r, c in cells if (r + c) % 2 == 0)
    assert even == 6 and len(cells) - even == 6          # balanced colours
    assert not _tileable(cells)                           # yet no domino tiling
    for r in range(1, 5):
        for c in range(1, 5):
            x, y = c - 1, 4 - r
            if (r, c) in holes:
                fc = LIGHT_RED
            else:
                fc = LIGHT_BLUE if (r + c) % 2 == 0 else "white"
            ax.add_patch(Rectangle((x, y), 1, 1, fc=fc, ec=INK, lw=0.6, zorder=1))
            if (r, c) in holes:
                ax.text(x + 0.5, y + 0.5, "×", ha="center", va="center", fontsize=14, color=RED, zorder=3)
    for c in range(1, 5):
        ax.text(c - 0.5, -0.4, str(c), ha="center", va="center", fontsize=9)
    for r in range(1, 5):
        ax.text(-0.4, 4 - r + 0.5, str(r), ha="center", va="center", fontsize=9)
    ax.text(2, -0.95, "column", ha="center", va="center", fontsize=9)
    ax.text(-0.95, 2, "row", ha="center", va="center", fontsize=9, rotation=90)
    frame(ax, -1.2, 4.2, -1.5, 4.2)
    caption(ax, "6 blue and 6 white squares remain, yet no domino tiling exists\n"
                "(checked by exhaustive search: balance is necessary, not sufficient)", fs=9)


# ---------- 2. invariant of three piles (cards 1, 2) ----------

@figure("f06_pile_residues", w=4.6, h=2.6)
def _(ax):
    start, after = [13, 15, 17], [12, 14, 19]    # one meeting of piles A and B: (-1, -1, +2)
    assert [v % 3 for v in start] == [1, 0, 2]
    assert len({v % 3 for v in after}) == 3      # residues stay pairwise distinct
    xs0, xs1 = [0, 1, 2], [4, 5, 6]
    ax.bar(xs0, start, width=0.7, color=LIGHT_BLUE, ec=INK, lw=0.8)
    ax.bar(xs1, after, width=0.7, color=LIGHT_ORANGE, ec=INK, lw=0.8)
    for x, v in zip(xs0 + xs1, start + after):
        ax.text(x, v + 0.4, str(v), ha="center", va="bottom", fontsize=9)
        ax.text(x, 1.2, f"res {v % 3}", ha="center", va="center", fontsize=9, color=INK)
    ax.set_xticks(xs0 + xs1)
    ax.set_xticklabels(["A", "B", "C", "A", "B", "C"], fontsize=9)
    ax.set_ylim(0, 24)
    ax.set_ylabel("pile size", fontsize=9)
    ax.text(1, 22.5, "start", ha="center", va="center", fontsize=9, color=GREY)
    ax.text(5, 22.5, "after A and B meet", ha="center", va="center", fontsize=9, color=GREY)


# ---------- 3. Nim with heaps 3, 4, 5 (cards 33, 34, 37) ----------

@figure("f06_nim_xor_345", w=4.8, h=2.9, axis=False)
def _(ax):
    def binary(v):
        return format(v, "03b")

    heaps = [3, 4, 5]
    x = 0
    for h in heaps:
        x ^= h
    assert x == 2
    after = [1, 4, 5]
    assert after[0] ^ after[1] ^ after[2] == 0 and 1 ^ 3 == 2  # 3 -> 1 removes 2 counters

    def panel(x0, sizes, title, ok, hollow=0):
        ax.text(x0 + 0.05, 5.9, title, ha="left", va="center", fontsize=9, color=INK)
        for i, s_ in enumerate(sizes):
            y = 4.9 - 1.0 * i
            ax.text(x0 + 0.05, y, str(s_), ha="left", va="center", fontsize=10)
            for k in range(s_):
                cx = x0 + 0.55 + 0.42 * k
                if i == 0 and k >= s_ - hollow:
                    ax.add_patch(Circle((cx, y), 0.16, fc="white", ec=ORANGE, lw=1.2, zorder=3))
                else:
                    ax.add_patch(Circle((cx, y), 0.16, fc=GREY, ec=GREY, zorder=3))
            ax.text(x0 + 3.05, y, format(s_, "03b"), ha="left", va="center", fontsize=10,
                    family="DejaVu Sans Mono")
        xor = 0
        for s_ in sizes:
            xor ^= s_
        ax.plot([x0, x0 + 3.7], [2.35, 2.35], color=INK, lw=0.8)
        ax.text(x0 + 0.05, 1.85, "XOR", ha="left", va="center", fontsize=10)
        ax.text(x0 + 3.05, 1.85, format(xor, "03b"), ha="left", va="center", fontsize=10,
                family="DejaVu Sans Mono", color=GREEN if ok else RED)
        ax.text(x0 + 3.05, 1.25, f"= {xor}", ha="left", va="center", fontsize=10,
                color=GREEN if ok else RED)

    frame(ax, -0.2, 10.4, 0.8, 6.3)
    panel(0.0, [3, 4, 5], "start: 3, 4, 5", ok=False, hollow=2)
    panel(5.4, [1, 4, 5], "after 3 to 1: 1, 4, 5", ok=True)
    ax.annotate("", xy=(5.0, 3.9), xytext=(4.3, 3.9),
                arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=1.6))
    ax.text(4.65, 4.35, "remove 2", ha="center", va="center", fontsize=9, color=ORANGE)
    caption(ax, r"$3\oplus4\oplus5=2\neq0$: winning. After $3\to1$ the XOR is $0$.", fs=9)


# ---------- 4. subtraction games and Grundy values (cards 36, 38, 79) ----------

def _subtraction(ax, moves, win_move, nmax=10):
    g = _grundy(moves, nmax)
    frame(ax, -0.7, nmax + 0.7, -1.2, 2.4)
    for m in moves:
        t = nmax - m
        col = ORANGE if m == win_move else GREY
        rad = 0.6
        ax.add_patch(FancyArrowPatch((nmax, 0.32), (t, 0.32), connectionstyle=f"arc3,rad={rad}",
                                     arrowstyle="-|>", mutation_scale=11, color=col, lw=1.3,
                                     shrinkA=0, shrinkB=0, zorder=2))
        ax.text((nmax + t) / 2, 0.32 + rad * m / 2, f"take {m}", ha="center",
                va="center", fontsize=9, color=col, bbox=dict(fc="white", ec="none", pad=0.4), zorder=5)
    for n in range(nmax + 1):
        fc = LIGHT_RED if g[n] == 0 else LIGHT_BLUE
        node(ax, (n, 0), str(n), r=0.3, fc=fc, ec=INK, fs=10)
        ax.text(n, -0.75, f"g={g[n]}", ha="center", va="center", fontsize=9)
    return g


@figure("f06_sub_134_grundy", w=5.0, h=2.4, axis=False)
def _(ax):
    g = _subtraction(ax, (1, 3, 4), win_move=1)
    assert g == [0, 1, 0, 1, 2, 3, 2, 0, 1, 0, 1]
    assert g[10] == 1 and g[9] == 0            # take 1 leaves 9, a losing position
    caption(ax, "red: g = 0, losing for the player to move; g(n) = mex of the values reachable\n"
                "take 3 (to 7) also wins", fs=9)


@figure("f06_sub_124_grundy", w=5.0, h=2.4, axis=False)
def _(ax):
    g = _subtraction(ax, (1, 2, 4), win_move=1)
    assert g == [0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1]
    caption(ax, "red: g = 0, losing for the player to move; g(n) = mex of the values reachable\n"
                "take 4 (to 6) also wins", fs=9)


# ---------- 5. 100 stones, moves 1 to 10 (card 39) ----------

@figure("f06_pile_round_complement", w=5.0, h=1.9, axis=False)
def _(ax):
    N, step = 100, 11
    losing = list(range(0, N, step))
    assert losing == list(range(0, 100, 11)) and N % step == 1
    ax.plot([-3, 106], [0, 0], color=GREY, lw=1.0, zorder=1)
    ax.plot(losing, [0] * len(losing), "o", ms=5, mfc=LIGHT_RED, mec=RED, mew=1.1, zorder=3)
    for v in losing:
        ax.text(v, 3.0, str(v), ha="center", va="center", fontsize=9)
    ax.plot([N], [0], "o", ms=5, mfc=LIGHT_BLUE, mec=BLUE, mew=1.1, zorder=3)
    ax.text(N + 2, 3.0, str(N), ha="left", va="center", fontsize=9, color=BLUE)
    ax.annotate("", xy=(N - 1.8, -2.2), xytext=(N - 0.2, -2.2),
                arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=1.4))
    ax.text(N - 1.0, -4.6, "take 1", ha="center", va="center", fontsize=9, color=ORANGE)
    ax.set_xlim(-4, 112)
    ax.set_ylim(-6.5, 5.0)
    ax.set_axis_off()
    caption(ax, "red: multiples of 11 (losing for the player to move)\n"
                "take 1 from 100, then answer each move x with 11 - x", fs=9)


# ---------- 6. red/black deck, V(r,b) = r/(r+b) (cards 41, 42) ----------

@figure("f06_red_black_dp", w=4.4, h=3.1, axis=False)
def _(ax):
    for r in range(1, 27):
        for b in range(1, 27):
            assert _rb_value(r, b) == Fr(r, r + b)
    assert _rb_value(26, 26) == Fr(1, 2) and _rb_value(30, 20) == Fr(3, 5) and _rb_value(1, 1) == Fr(1, 2)
    for r in range(5):
        for b in range(5):
            if r + b == 0:
                continue
            v = Fr(r, r + b)
            fc = LIGHT_BLUE if v > Fr(1, 2) else (LIGHT_ORANGE if v < Fr(1, 2) else "white")
            ax.add_patch(Rectangle((r, b), 1, 1, fc=fc, ec=INK, lw=0.6, zorder=1))
            ax.text(r + 0.5, b + 0.5, str(v), ha="center", va="center", fontsize=10, zorder=3)
    for (r, b) in [(1, 1), (3, 2)]:
        ax.add_patch(Rectangle((r, b), 1, 1, fc="none", ec=ORANGE, lw=2.0, zorder=4))
    for r in range(5):
        ax.text(r + 0.5, -0.4, str(r), ha="center", va="center", fontsize=9)
    for b in range(5):
        ax.text(-0.4, b + 0.5, str(b), ha="center", va="center", fontsize=9)
    ax.text(2.5, -0.95, "red left, r", ha="center", va="center", fontsize=9)
    ax.text(-0.95, 2.5, "black left, b", ha="center", va="center", fontsize=9, rotation=90)
    frame(ax, -1.3, 5.2, -1.6, 5.2)
    caption(ax, "V(r,b) = r/(r+b) in every cell; no stopping rule beats it\n"
                "V(26,26) = 1/2, V(30,20) = 3/5 (boxed: V(1,1), V(3,2))", fs=9)


# ---------- 7. secretary problem, n = 100 (cards 45, 46, 49) ----------

@figure("f06_secretary_threshold", w=5.0, h=2.6)
def _(ax):
    ks = np.arange(0, 61)
    ps = [float(_secretary_p(int(k))) for k in ks]
    kbest = max(range(0, 100), key=lambda k: _secretary_p(k))
    assert kbest == 37 and round(float(_secretary_p(36)), 5) == 0.37101
    assert round(float(_secretary_p(37)), 5) == 0.37104 and round(float(_secretary_p(38)), 4) == 0.3708
    ax.plot(ks, ps, color=BLUE, lw=1.8)
    ax.plot([36, 37], [ps[36], ps[37]], "o", color=ORANGE, ms=5, zorder=4)
    ax.axhline(1 / np.e, color=GREY, ls="--", lw=1.0)
    ax.text(52, 1 / np.e + 0.008, "1/e", color=GREY, fontsize=9, ha="center")
    ax.annotate("reject 36 or 37: 0.3710", xy=(37, ps[37]), xytext=(43, 0.30), fontsize=9,
                arrowprops=dict(arrowstyle="-", color=INK, lw=0.8))
    ax.set_ylim(0.2, 0.42)
    ax.set_xlabel("applicants rejected first, r - 1  (n = 100)", fontsize=9)
    ax.set_ylabel("P(best hired)", fontsize=9)


# ---------- 8. duel, Alice first (card 50) ----------

@figure("f06_duel_tree", w=4.6, h=2.5, axis=False)
def _(ax):
    a, b = Fr(1, 3), Fr(1, 2)
    P = a / (1 - (1 - a) * (1 - b))
    assert P == Fr(1, 2)
    frame(ax, -1.0, 4.4, -1.3, 2.3)
    box(ax, (0.0, 1.6), "Alice fires", w=1.5, h=0.5, fc=LIGHT_BLUE, fs=9)
    box(ax, (3.2, 1.6), "Bob fires", w=1.5, h=0.5, fc=LIGHT_ORANGE, fs=9)
    arrow(ax, (0.8, 1.6), (2.4, 1.6), r"miss $\frac{2}{3}$", shrink=0, fs=9, label_offset=(0, 0.3))
    arrow(ax, (0.0, 1.33), (0.0, 0.42), r"hit $\frac{1}{3}$", shrink=0, fs=9, color=GREEN, label_offset=(0.5, 0))
    box(ax, (0.0, 0.1), "Alice wins", w=1.5, h=0.5, fc=LIGHT_GREEN, ec=GREEN, fs=9)
    arrow(ax, (3.2, 1.33), (3.2, 0.42), r"hit $\frac{1}{2}$", shrink=0, fs=9, color=RED, label_offset=(0.5, 0))
    box(ax, (3.2, 0.1), "Bob wins", w=1.5, h=0.5, fc=LIGHT_RED, ec=RED, fs=9)
    arrow(ax, (2.4, 1.25), (0.8, 1.25), r"miss $\frac{1}{2}$: back to Alice with $\frac{1}{3}$",
          rad=0.0, shrink=0, fs=9, color=GREY, label_offset=(0.0, -0.32))
    caption(ax, r"$P=\frac{1}{3}+\frac{1}{3}P \Rightarrow P=\frac{1}{2}$  (Alice wins 1/2, Bob 1/2)", fs=9.5)


# ---------- 9. three-person truel (card 52) ----------

@figure("f06_truel_targets", w=4.4, h=2.9, axis=False)
def _(ax):
    full = frozenset(_ORDER)
    base = {(full, "B"): "C", (full, "C"): "B"}
    v_c = _truel_win({**base, (full, "A"): "C"})["A"]     # equilibrium: A aims at C
    v_b = _truel_win({**base, (full, "A"): "B"})["A"]     # aiming at B
    assert v_c == Fr(13, 36) and v_b == Fr(5, 18)
    pos = {"A": (0.0, 0.0), "B": (4.0, 0.0), "C": (2.0, 2.7)}
    frame(ax, -1.0, 5.0, -1.0, 3.6)
    for name, (x, y) in pos.items():
        node(ax, (x, y), name, r=0.3, fc="white", ec=INK, fs=11)
    ax.text(pos["A"][0], -0.65, "hit 1/3", ha="center", va="center", fontsize=9, color=GREY)
    ax.text(pos["B"][0], -0.65, "hit 1/2", ha="center", va="center", fontsize=9, color=GREY)
    ax.text(pos["C"][0], 3.25, "hit 1 (never misses)", ha="center", va="center", fontsize=9, color=GREY)
    ax.add_patch(FancyArrowPatch(pos["A"], pos["C"], connectionstyle="arc3,rad=-0.12", arrowstyle="-|>",
                                 mutation_scale=13, color=ORANGE, lw=2.0, shrinkA=18, shrinkB=18, zorder=2))
    ax.text(0.35, 1.5, f"A aims at C: {v_c}", ha="right", va="center", fontsize=9, color=ORANGE)
    ax.add_patch(FancyArrowPatch(pos["A"], pos["B"], connectionstyle="arc3,rad=0.0", arrowstyle="-|>",
                                 mutation_scale=11, color=GREY, lw=1.2, linestyle="--", shrinkA=18, shrinkB=18))
    ax.text(2.0, -0.45, f"A aims at B: {v_b}", ha="center", va="center", fontsize=9, color=GREY)
    caption(ax, f"A wins {v_c} aiming at C, {v_b} aiming at B\n(equilibrium: B aims at C, C aims at B)", fs=9)


# ---------- 10. guessing game upper bound (cards 54, 57) ----------

@figure("f06_guess_bounds", w=5.0, h=2.5)
def _(ax):
    k = np.arange(0, 15)
    b23 = 100 * (2 / 3) ** k
    b12 = 100 * (1 / 2) ** k
    assert next(i for i in range(60) if 100 * (2 / 3) ** i < 1) == 12
    assert next(i for i in range(60) if 100 * (1 / 2) ** i < 1) == 7
    ax.semilogy(k, b23, "o-", color=BLUE, ms=3.5, lw=1.5, label=r"target $\frac{2}{3}$ of average")
    ax.semilogy(k, b12, "s-", color=ORANGE, ms=3.5, lw=1.5, label=r"target $\frac{1}{2}$ of average")
    ax.axhline(1.0, color=GREEN, ls="--", lw=1.0)
    ax.text(14, 1.25, "only 0 left", color=GREEN, fontsize=9, ha="right", va="bottom")
    ax.annotate("round 12", xy=(12, b23[12]), xytext=(8.6, 0.12), fontsize=9, color=BLUE,
                arrowprops=dict(arrowstyle="-", color=BLUE, lw=0.8))
    ax.annotate("round 7", xy=(7, b12[7]), xytext=(9.4, 3.0), fontsize=9, color=ORANGE,
                arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.8))
    ax.set_xlabel("round k", fontsize=9)
    ax.set_ylabel(r"upper bound $100\,p^k$", fontsize=9)
    ax.set_yticks([0.1, 1, 10, 100])
    ax.set_yticklabels(["0.1", "1", "10", "100"], fontsize=9)
    ax.set_ylim(0.05, 300)
    ax.legend(fontsize=9, frameon=False, loc="lower left")


# ---------- 11. first-price auction bid functions (cards 58, 61) ----------

@figure("f06_first_price_bid", w=4.6, h=2.6)
def _(ax):
    def best_bid(v, n):
        c = (n - 1) / n
        grid = np.linspace(0, v, 4001)
        util = (v - grid) * np.minimum(grid / c, 1.0) ** (n - 1)
        return grid[int(np.argmax(util))]

    for v in (0.2, 0.5, 0.9):
        assert abs(best_bid(v, 3) - 2 * v / 3) < 2e-3 and abs(best_bid(v, 2) - v / 2) < 2e-3
    v = np.linspace(0, 1, 201)
    ax.plot(v, v, color=GREY, ls="--", lw=1.1)
    ax.plot(v, v / 2, color=BLUE, lw=1.8)
    ax.plot(v, 2 * v / 3, color=ORANGE, lw=1.8)
    ax.text(0.97, 0.99, "truthful: b = v", color=GREY, fontsize=9, ha="right", va="bottom")
    ax.text(0.97, 0.30, r"n = 2: $b = \frac{v}{2}$", color=BLUE, fontsize=9, ha="right", va="bottom")
    ax.text(0.97, 0.66, r"n = 3: $b = \frac{2v}{3}$", color=ORANGE, fontsize=9, ha="right", va="bottom")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.05)
    ax.set_xlabel("private value v", fontsize=9)
    ax.set_ylabel("equilibrium bid b(v)", fontsize=9)


# ---------- 12. bridge crossing schedules (cards 62, 63) ----------

@figure("f06_bridge_17", w=5.0, h=2.7)
def _(ax):
    assert _bridge_min([1, 2, 5, 10], 2) == 17
    steps = [("1 and 2 cross", 0, 2, BLUE), ("1 returns torch", 2, 3, GREY),
             ("5 and 10 cross", 3, 13, BLUE), ("2 returns torch", 13, 15, GREY),
             ("1 and 2 cross", 15, 17, BLUE)]
    assert sum(t1 - t0 for _, t0, t1, _ in steps) == 17
    for i, (lab, t0, t1, col) in enumerate(steps):
        y = len(steps) - 1 - i
        ax.barh(y, t1 - t0, left=t0, height=0.55, color=col, alpha=0.85, ec=INK, lw=0.6)
        ax.text(t1 + 0.2, y, f"{t1 - t0} min", va="center", fontsize=9)
    ax.set_yticks(range(len(steps)))
    ax.set_yticklabels([s[0] for s in steps][::-1], fontsize=9)
    ax.set_xlim(0, 19)
    ax.set_xticks([0, 2, 5, 10, 13, 15, 17])
    ax.tick_params(axis="x", labelsize=9)
    ax.set_xlabel("time (min); total 17 = 2 + 1 + 10 + 2 + 2", fontsize=9)


@figure("f06_bridge_13", w=5.0, h=2.2)
def _(ax):
    assert _bridge_min([1, 2, 5, 10], 3) == 13
    steps = [("1 and 2 cross", 0, 2, BLUE), ("1 returns torch", 2, 3, GREY),
             ("1, 5 and 10 cross", 3, 13, BLUE)]
    assert sum(t1 - t0 for _, t0, t1, _ in steps) == 13
    for i, (lab, t0, t1, col) in enumerate(steps):
        y = len(steps) - 1 - i
        ax.barh(y, t1 - t0, left=t0, height=0.55, color=col, alpha=0.85, ec=INK, lw=0.6)
        ax.text(t1 + 0.2, y, f"{t1 - t0} min", va="center", fontsize=9)
    ax.set_yticks(range(len(steps)))
    ax.set_yticklabels([s[0] for s in steps][::-1], fontsize=9)
    ax.set_xlim(0, 15)
    ax.set_xticks([0, 2, 3, 13])
    ax.tick_params(axis="x", labelsize=9)
    ax.set_xlabel("time (min); total 13 with three on the bridge", fontsize=9)


# ---------- 13. burning ropes (cards 25, 26) ----------

@figure("f06_rope_timeline", w=5.2, h=2.5, axis=False)
def _(ax):
    # rope A: lit at both ends at t=0; the fronts meet where u(x) = 1/2, i.e. at t = 30
    assert abs(_u(_x_at(0.5)) - 0.5) < 1e-9
    times = [0, 15, 30, 45]
    L = 1.4
    rows = [("A: both ends", "A"), ("B: one end,\nother at t=30", "B")]
    ax.set_xlim(-0.2, 9.6)
    ax.set_ylim(-0.9, 2.1)
    for c, t in enumerate(times):
        x0 = 2.3 + 1.85 * c
        ax.text(x0 + L / 2, 1.85, f"t = {t}", ha="center", va="center", fontsize=9)
        for rv, (lab, which) in enumerate(rows):
            y = 1.0 - 1.45 * rv
            if which == "A":
                if t >= 30:
                    xl = xr = 1.0
                    burnt = [(0.0, 1.0)]
                else:
                    xl = _x_at(t / 60)
                    xr = _x_at(1 - t / 60)
                    burnt = [(0.0, xl), (xr, 1.0)]
                fire = [0.0, 1.0] if 0 < t < 30 else []
            else:
                if t <= 30:
                    xl = _x_at(t / 60)
                    burnt = [(0.0, xl)]
                    xr = 1.0
                else:
                    xl = _x_at(t / 60)
                    xr = _x_at(1 - (t - 30) / 60)
                    burnt = [(0.0, min(xl, 1.0))]
                    if xr < xl or t >= 45:
                        burnt = [(0.0, 1.0)]
                    else:
                        burnt.append((xr, 1.0))
                fire = [0.0] + ([1.0] if t >= 30 and t < 45 else [])
            ax.add_patch(Rectangle((x0, y - 0.13), L, 0.26, fc=LIGHT_ORANGE, ec=INK, lw=0.6, zorder=1))
            for a, b_ in burnt:
                if b_ > a:
                    ax.add_patch(Rectangle((x0 + a * L, y - 0.13), (b_ - a) * L, 0.26, fc=GREY, ec="none", zorder=2))
            for f in fire:
                ax.add_patch(Circle((x0 + f * L, y), 0.07, fc=ORANGE, ec="none", zorder=4))
            if which == "B" and t <= 30 and 0 < t:
                ax.add_patch(Circle((x0 + xl * L, y), 0.06, fc=RED, ec="none", zorder=4))
            if which == "B" and 30 < t < 45:
                ax.add_patch(Circle((x0 + xl * L, y), 0.06, fc=RED, ec="none", zorder=4))
                ax.add_patch(Circle((x0 + xr * L, y), 0.06, fc=RED, ec="none", zorder=4))
            if which == "A" and 0 < t < 30:
                ax.add_patch(Circle((x0 + xl * L, y), 0.06, fc=RED, ec="none", zorder=4))
                ax.add_patch(Circle((x0 + xr * L, y), 0.06, fc=RED, ec="none", zorder=4))
    for rv, (lab, which) in enumerate(rows):
        ax.text(-0.1, 1.0 - 1.45 * rv, lab, ha="left", va="center", fontsize=9)
    caption(ax, "grey: burnt; red: fire fronts; orange: a lit end\nrope B burns out at 45 = 30 + 15", fs=9)


# ---------- 14. ants as ghosts (cards 67, 68) ----------

@figure("f06_ant_ghosts", w=4.6, h=2.8)
def _(ax):
    # ant 1 starts at 0.3 facing right, ant 2 at 0.6 facing left; they meet at x = 0.45, t = 0.15
    ant1 = [(0.3, 0.0), (0.45, 0.15), (0.0, 0.60)]
    ant2 = [(0.6, 0.0), (0.45, 0.15), (1.0, 0.70)]
    ghost1 = [(0.3, 0.0), (1.0, 0.70)]
    ghost2 = [(0.6, 0.0), (0.0, 0.60)]
    falls = sorted([round(ant1[-1][1], 6), round(ant2[-1][1], 6)])
    ghost_falls = sorted([round(1 - 0.3, 6), round(0.6, 6)])
    assert falls == ghost_falls == [0.6, 0.7] and max(falls) == 0.7
    for g in (ghost1, ghost2):
        xs, ts = zip(*g)
        ax.plot(xs, ts, color=GREY, ls="--", lw=1.1)
    for a, col in ((ant1, BLUE), (ant2, ORANGE)):
        xs, ts = zip(*a)
        ax.plot(xs, ts, color=col, lw=2.0)
    ax.plot([0.45], [0.15], "o", color=INK, ms=4)
    ax.text(0.5, 0.15, "meet", fontsize=9, va="center")
    ax.plot([0.0, 1.0], [0.6, 0.7], "o", color=RED, ms=5, zorder=5)
    ax.text(0.03, 0.62, "falls at 0.6", fontsize=9, color=INK)
    ax.text(0.80, 0.73, "falls at 0.7", fontsize=9, color=INK)
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.02, 0.85)
    ax.set_xlabel("position on the stick (m)", fontsize=9)
    ax.set_ylabel("time (min)", fontsize=9)
    ax.set_title(r"last fall $=\max(0.7,\,0.6)$; expected $\frac{n}{n+1}$ for $n$ ants", fontsize=9)


# ---------- 15. coconut chain (card 69) ----------

@figure("f06_coconut_chain", w=5.0, h=2.6)
def _(ax):
    piles = [3121]
    for _ in range(5):
        assert (piles[-1] - 1) % 5 == 0
        piles.append(4 * (piles[-1] - 1) // 5)
    assert piles == [3121, 2496, 1996, 1596, 1276, 1020] and 1020 % 5 == 0
    labels = ["start", "night 1", "night 2", "night 3", "night 4", "night 5"]
    xs = range(len(piles))
    ax.bar(xs, piles, width=0.62, color=LIGHT_BLUE, ec=INK, lw=0.8)
    for x, v in zip(xs, piles):
        ax.text(x, v + 40, str(v), ha="center", va="bottom", fontsize=9)
    ax.set_xticks(list(xs))
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_ylim(0, 3700)
    ax.set_ylabel("coconuts in the pile", fontsize=9)
    ax.text(5.4, 2350, "morning: 1020 = 5 x 204", ha="right", va="center", fontsize=9, color=ORANGE)
    ax.text(1.4, 3350, r"each night $N \mapsto \frac{4(N-1)}{5}$", ha="left", va="center", fontsize=9)


# ---------- 16. light bulb and three switches (cards 71, 72) ----------

@figure("f06_bulb_switches", w=5.0, h=2.3, axis=False)
def _(ax):
    frame(ax, 0, 10, 0, 5.2)
    heads = [(1.1, "switch"), (4.6, "setting during the visit"), (8.2, "bulb on entry")]
    for x, title in heads:
        ax.text(x, 4.85, title, ha="center", va="center", fontsize=9, color=GREY)
    rows = [
        ("A", "on a few min, then off", "off but warm", LIGHT_RED),
        ("B", "on when you enter", "lit", LIGHT_BLUE),
        ("C", "never touched (off)", "off and cold", LIGHT_GREEN),
    ]
    for i, (sw, setting, seen, fc) in enumerate(rows):
        y = 3.6 - 1.25 * i
        box(ax, (1.1, y), sw, w=0.9, h=0.8, fc="white", fs=11)
        box(ax, (4.6, y), setting, w=3.6, h=0.8, fc="white", fs=9)
        box(ax, (8.2, y), seen, w=2.2, h=0.8, fc=fc, fs=9)
    caption(ax, "A, B, C identified in one visit: lit = B; off and warm = A; off and cold = C", fs=9)


# ---------- 17. blue-eyed islanders and muddy children (cards 73, 75) ----------

@figure("f06_islander_nights", w=4.6, h=2.6, axis=False)
def _(ax):
    ax.set_xlim(-1.0, 5.7)
    ax.set_ylim(-0.9, 5.4)
    ax.set_aspect("auto")
    ax.set_axis_off()
    ax.text(-0.2, 4.6, "k / night", ha="center", va="center", fontsize=9, color=GREY)
    for n in range(1, 6):
        ax.text(n, 4.6, str(n), ha="center", va="center", fontsize=9, color=GREY)
    for k in range(1, 6):
        y = 4 - (k - 1)
        ax.text(-0.2, y, str(k), ha="center", va="center", fontsize=9)
        for n in range(1, 6):
            if n < k:
                box(ax, (n, y), "stay", w=0.9, h=0.6, fc="#ececec", ec=GREY, fs=9)
            elif n == k:
                box(ax, (n, y), "leave", w=0.9, h=0.6, fc=LIGHT_BLUE, ec=BLUE, fs=9)
    caption(ax, "k blue-eyed (or muddy) people all act on night k", fs=9)


# ---------- 18. pirates' allocations (cards 10, 12, 77) ----------

@figure("f06_pirate_allocations", w=4.8, h=2.7, axis=False)
def _(ax):
    expected = {2: (100, 0), 3: (99, 0, 1), 4: (99, 0, 1, 0), 5: (98, 0, 1, 0, 1), 6: (98, 0, 1, 0, 1, 0)}
    frame(ax, -2.2, 6.4, -0.8, 6.6)
    for c in range(6):
        ax.text(c + 0.5, 6.1, f"{c + 1}", ha="center", va="center", fontsize=10)
    for row, n in enumerate(range(2, 7)):
        y = 5 - row
        alloc = _pirates(n)
        assert alloc == expected[n]
        ax.text(-0.15, y + 0.5, f"{n} pirates", ha="right", va="center", fontsize=9)
        for c in range(n):
            v = alloc[c]
            if c == 0:
                fc = LIGHT_ORANGE
            elif v > 0:
                fc = LIGHT_BLUE
            else:
                fc = "white"
            ax.add_patch(Rectangle((c, y), 1, 1, fc=fc, ec=INK, lw=0.6, zorder=1))
            ax.text(c + 0.5, y + 0.5, str(v), ha="center", va="center", fontsize=10, zorder=3)
    ax.text(-0.15, 6.1, "pirate", ha="right", va="center", fontsize=9, color=GREY)
    caption(ax, "orange: the proposer keeps the rest; blue: a vote bought with one coin\n"
                "(the cheapest votes are the ones worth 0 in the smaller game)", fs=9)


# ---------- 19. two-colouring of K5 without a monochrome triangle (card 9) ----------

@figure("f06_ramsey_pentagon", w=4.0, h=3.0, axis=False)
def _(ax):
    verts = range(6)
    tri = list(itertools.combinations(verts, 3))
    mono_free = 0
    for mask in range(2 ** 15):
        col = {e: (mask >> i) & 1 for i, e in enumerate(itertools.combinations(verts, 2))}
        if not any(col[(a, b)] == col[(a, c)] == col[(b, c)] for a, b, c in tri):
            mono_free += 1
    assert mono_free == 0                                   # every colouring of K6 has a triangle
    pts = {i: (np.cos(np.pi / 2 + 2 * np.pi * i / 5), np.sin(np.pi / 2 + 2 * np.pi * i / 5)) for i in range(5)}
    five = list(range(5))
    edge_col = {}
    for a, b in itertools.combinations(five, 2):
        edge_col[(a, b)] = BLUE if (b - a) % 5 in (1, 4) else RED
    for tr in itertools.combinations(five, 3):
        cols = [edge_col[(a, b)] for a, b in itertools.combinations(tr, 2)]
        assert not (cols[0] == cols[1] == cols[2])          # no monochrome triangle
    frame(ax, -1.6, 1.6, -1.45, 1.6)
    for (a, b), col in edge_col.items():
        (x1, y1), (x2, y2) = pts[a], pts[b]
        ax.plot([x1, x2], [y1, y2], color=col, lw=1.8 if col == BLUE else 1.4,
                ls="-" if col == BLUE else "--", zorder=1)
    for i in five:
        x, y = pts[i]
        node(ax, (x, y), str(i + 1), r=0.17, fc="white", ec=INK, fs=10)
    ax.text(0, -1.3, "blue (solid) = acquainted, red (dashed) = strangers", ha="center", va="center",
            fontsize=9, color=INK)
    caption(ax, "no three people all acquainted or all strangers\n"
                "six people always force one (all 2^15 colourings checked)", fs=9)


# ---------- 20. hats: parity call and deduction (cards 14, 15, 17) ----------

@figure("f06_hat_parity", w=5.0, h=2.5, axis=False)
def _(ax):
    hats = [1, 0, 0, 1, 0]          # 1 = red, 0 = blue; prisoner 1 is at the front
    n = len(hats)
    p = sum(hats[:n - 1]) % 2       # the back prisoner calls the parity of the hats in front of him
    calls = [None] * n
    calls[n - 1] = p
    for k in range(n - 2, -1, -1):  # from the back forwards: prisoner k deduces his own hat
        others = sum(hats[i] for i in range(n - 1) if i != k)
        calls[k] = (p - others) % 2
        assert calls[k] == hats[k]
    frame(ax, -1.0, 5.4, -1.3, 3.5)
    name = {1: "R", 0: "B"}
    fill = {1: LIGHT_RED, 0: LIGHT_BLUE}
    ax.text(-0.15, 2.7, "hat", ha="right", va="center", fontsize=9)
    ax.text(-0.15, 1.2, "call", ha="right", va="center", fontsize=9)
    for k in range(n):
        x = k + 0.5
        box(ax, (x, 2.7), name[hats[k]], w=0.8, h=0.7, fc=fill[hats[k]], fs=10)
        box(ax, (x, 1.2), name[calls[k]], w=0.8, h=0.7, fc=fill[calls[k]], ec=INK, fs=10)
        ax.text(x, 0.15, str(k + 1), ha="center", va="center", fontsize=9, color=GREY)
    ax.text(0.5, -0.5, "front", ha="center", va="center", fontsize=9, color=GREY)
    ax.text(n - 0.5, -0.5, "back", ha="center", va="center", fontsize=9, color=GREY)
    ax.text(n - 0.5, 3.45, "back calls p = h1+h2+h3+h4 (mod 2)", ha="right", va="center", fontsize=9,
            color=ORANGE)
    caption(ax, r"$p = 0$ (blue). Prisoner 4 hears $p$, sees $h_1, h_2, h_3$:" "\n"
                r"$h_4 = p - (h_1+h_2+h_3)$ (mod 2) $= 1$ (red), so he calls red", fs=9)


# ---------- 21. two eggs, 100 floors (cards 19, 20, 21) ----------

_EGG_DROPS = [14, 27, 39, 50, 60, 69, 77, 84, 90, 95, 99, 100]


def _eggs_used(t):
    used, prev = 0, 0
    for d in _EGG_DROPS:
        used += 1
        if d >= t:                           # egg 1 breaks at d; egg 2 scans the block below it
            for f in range(prev + 1, d):
                used += 1
                if f >= t:
                    return used
            return used
        prev = d
    return used


@figure("f06_egg_drop_staircase", w=5.2, h=2.3)
def _(ax):
    worst = max(_eggs_used(t) for t in range(1, 102))     # t = 101 means no break
    assert worst == 14
    prev = 0
    for k, d in enumerate(_EGG_DROPS):
        width = d - prev
        ax.add_patch(Rectangle((prev, 0), width, 1.0, fc=LIGHT_BLUE if k % 2 == 0 else "white", ec=INK, lw=0.6))
        ax.text(prev + width / 2, 1.15, str(width), ha="center", va="bottom", fontsize=9)
        prev = d
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 1.6)
    ax.set_yticks([])
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.tick_params(axis="x", labelsize=9)
    ax.set_xlabel("floor (drops at 14, 27, 39, 50, 60, 69, 77, 84, 90, 95, 99, 100)", fontsize=9)
    ax.spines["left"].set_visible(False)


# ---------- 22. wine bottles and rats in binary (cards 31, 32) ----------

@figure("f06_wine_rats_code", w=5.0, h=2.1, axis=False)
def _(ax):
    poisoned = 741
    bits = format(poisoned, "010b")
    assert bits == "1011100101" and int(bits, 2) == poisoned
    frame(ax, -0.6, 10.4, -1.7, 1.8)
    for i in range(10):
        dead = bits[i] == "1"
        fc = LIGHT_RED if dead else "white"
        ec = RED if dead else INK
        node(ax, (i, 0.6), f"R{i + 1}", r=0.36, fc=fc, ec=ec, fs=9)
        ax.text(i, -0.25, bits[i], ha="center", va="center", fontsize=10, family="DejaVu Sans Mono")
    ax.text(-0.9, -0.25, "bit", ha="right", va="center", fontsize=9, color=GREY)
    ax.text(-0.9, 0.6, "rat", ha="right", va="center", fontsize=9, color=GREY)
    ax.text(4.5, -1.1, "dead rats (red) spell 741 = 1011100101 in binary", ha="center", va="center", fontsize=9)
    caption(ax, "rat i drinks every bottle whose i-th bit is 1\n2^10 = 1024 >= 1000, so 10 rats suffice", fs=9)


if __name__ == "__main__":
    import sys
    sys.exit("run via diagrams/render_all.py")
