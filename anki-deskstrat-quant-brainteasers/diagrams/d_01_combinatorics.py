"""Figures for cards/01_combinatorics.json."""
import numpy as np
from math import comb, factorial, exp, log, pi, cos, sin
from fractions import Fraction as Fr
from qcfig import *

def _grid(ax, nx, ny):
    for x in range(nx + 1):
        ax.plot([x, x], [0, ny], color=GREY, lw=0.6, alpha=0.5, zorder=1)
    for y in range(ny + 1):
        ax.plot([0, nx], [y, y], color=GREY, lw=0.6, alpha=0.5, zorder=1)
    X = [x for x in range(nx + 1) for _ in range(ny + 1)]
    Y = [y for _ in range(nx + 1) for y in range(ny + 1)]
    ax.plot(X, Y, "o", ms=2.2, color=GREY, zorder=1)

def _path(ax, pts, color, lw=2.2, ls="-", zorder=3):
    xs, ys = zip(*pts)
    ax.plot(xs, ys, ls, color=color, lw=lw, zorder=zorder, solid_capstyle="round")

def _dyck_pts(steps):
    h, out = 0, [(0, 0)]
    for i, c in enumerate(steps):
        h += 1 if c == "U" else -1
        out.append((i + 1, h))
    return out

def _steps_to_pts(steps, start=(0, 0)):
    pts = [start]
    for s in steps:
        x, y = pts[-1]
        pts.append((x + (s == "R"), y + (s == "U")))
    return pts

# ---------------------------------------------------------------- stars and bars
@figure("f01_stars_bars_row", w=5.2, h=1.7, axis=False)
def _(ax):
    # one solution of x1+...+x5 = 20 written as 20 stars and 4 bars
    x = [3, 0, 7, 6, 4]
    pos, groups = 0, []
    for i, v in enumerate(x):
        start = pos
        for _ in range(v):
            ax.plot(pos, 0, "o", color=INK, ms=6.5, zorder=3); pos += 1
        groups.append((start, pos - 1, v))
        if i < len(x) - 1:
            ax.plot([pos, pos], [-0.32, 0.32], color=ORANGE, lw=2.4, zorder=3); pos += 1
    for i, (s, e, v) in enumerate(groups):
        cx = (s + e) / 2 if v else s - 0.5
        ax.text(cx, 0.6, rf"$x_{i+1}={v}$", ha="center", va="center", fontsize=10, color=BLUE)
    frame(ax, -1, 24, -1.0, 1.0)
    ax.text(11.5, -0.75, "24 slots, 4 of them bars: C(24,4) = 10626 solutions",
            ha="center", va="center", fontsize=9.5, color=GREY)

# ---------------------------------------------------------------- bounded compositions
@figure("f01_bounded_waterfall", w=5.0, h=2.8)
def _(ax):
    deltas = [10626, -15300, 4950, -150]
    names = ["no cap\nC(24,4)", "one $x_i\\geq 6$\n5 x C(18,4)", "two capped\n10 x C(12,4)", "three capped\n10 x C(6,4)", "answer"]
    run, labels = 0, []
    for i, d in enumerate(deltas):
        new = run + d
        ax.bar(i, abs(d), bottom=min(run, new), color=BLUE if d > 0 else RED, ec=INK, lw=0.8, width=0.6, zorder=3)
        ax.plot([i + 0.3, i + 0.7], [new, new], color=GREY, lw=0.8, zorder=2)
        ax.text(i, max(run, new) + 450, f"{d:+d}", ha="center", va="bottom", fontsize=9.5)
        run = new
    ax.bar(4, run, color=GREEN, ec=INK, lw=0.8, width=0.6, zorder=3)
    ax.text(4, run + 450, f"{run}", ha="center", va="bottom", fontsize=9.5, color=GREEN)
    ax.axhline(0, color=INK, lw=0.8)
    ax.set_xticks(range(5)); ax.set_xticklabels(names, fontsize=8.5)
    ax.set_ylabel("running count"); ax.set_ylim(-6200, 13200)
    ax.set_title(r"$x_1+\cdots+x_5=20,\ 0\leq x_i\leq 5$: alternating running total", fontsize=10)

# ---------------------------------------------------------------- seats with a gap
@figure("f01_seats_gap", w=5.0, h=1.9, axis=False)
def _(ax):
    people = [2, 5, 11, 17]
    for s in range(1, 21):
        if s in people:
            ax.plot(s, 0, "o", color=BLUE, ms=10, zorder=3)
        else:
            ax.plot(s, 0, "s", mfc="white", mec=GREY, ms=8, zorder=2)
    bounds = [(1, 1), (3, 4), (6, 10), (12, 16), (18, 20)]
    for i, (a, b) in enumerate(bounds):
        ax.text((a + b) / 2, -0.85, rf"$g_{i}={b - a + 1}$", ha="center", va="center", fontsize=9.5, color=ORANGE)
    ax.text(10.5, 1.0, "seats 1..20; blue = chosen seats, no two adjacent",
            ha="center", va="center", fontsize=9.5, color=GREY)
    frame(ax, 0, 21, -2.1, 1.5)
    ax.text(10.5, -1.6, r"$g_1,g_2,g_3\geq 1$: shrink each by 1, leaving 13 units in 5 gaps: C(17,4)=2380",
            ha="center", va="center", fontsize=9, color=GREY)

# ---------------------------------------------------------------- binary strings / Fibonacci
@figure("f01_fib_tiling", w=5.0, h=2.3, axis=False)
def _(ax):
    a = [1, 2]
    for _ in range(10):
        a.append(a[-1] + a[-2])
    a9, a8 = a[9], a[8]
    assert a[10] == 144 and a9 == 89 and a8 == 55
    u = 0.5
    ax.add_patch(Rectangle((0, 1.1), 9 * u, 0.7, fc=LIGHT_BLUE, ec=INK, lw=1, zorder=2))
    ax.text(4.5 * u, 1.45, f"length 9: {a9} strings", ha="center", va="center", fontsize=9.5)
    ax.add_patch(Rectangle((9 * u, 1.1), 1 * u, 0.7, fc="white", ec=INK, lw=1, zorder=2))
    ax.text(9.5 * u, 1.45, "0", ha="center", va="center", fontsize=10)
    ax.add_patch(Rectangle((0, -0.1), 8 * u, 0.7, fc=LIGHT_ORANGE, ec=INK, lw=1, zorder=2))
    ax.text(4 * u, 0.25, f"length 8: {a8} strings", ha="center", va="center", fontsize=9.5)
    ax.add_patch(Rectangle((8 * u, -0.1), 2 * u, 0.7, fc="white", ec=INK, lw=1, zorder=2))
    ax.text(9 * u, 0.25, "01", ha="center", va="center", fontsize=10)
    ax.text(-0.15, 1.45, "ends in 0", ha="right", va="center", fontsize=9, color=GREY)
    ax.text(-0.15, 0.25, "ends in 01", ha="right", va="center", fontsize=9, color=GREY)
    ax.set_xlim(-1.9, 5.4); ax.set_ylim(-0.7, 2.0)
    ax.text(-1.9, -0.5, r"$a_{10}=a_9+a_8=89+55=144=F_{12}$ (no two consecutive integers in {1..10})",
            ha="left", va="center", fontsize=9, color=BLUE)

# ---------------------------------------------------------------- derangements / hats
def _derangements(nmax):
    D = [1, 0]
    for n in range(2, nmax + 1):
        D.append((n - 1) * (D[-1] + D[-2]))
    return D

@figure("f01_hat_fixed_points", w=5.0, h=2.7)
def _(ax):
    D = _derangements(10)
    assert D[10] == 1334961 and D[9] == 133496
    P = [Fr(comb(10, k) * D[10 - k], factorial(10)) for k in range(11)]
    vals = [float(p) for p in P]
    cols = [GREEN, ORANGE] + [GREY] * 9
    ax.bar(range(11), vals, color=cols, ec=INK, lw=0.7, width=0.7, zorder=3)
    ax.text(0, vals[0] + 0.012, f"{vals[0]:.3f}", ha="center", fontsize=9, color=GREEN)
    ax.text(1, vals[1] + 0.012, f"{vals[1]:.3f}", ha="center", fontsize=9, color=ORANGE)
    ax.text(2, vals[2] + 0.012, f"{vals[2]:.3f}", ha="center", fontsize=9)
    ax.text(3, vals[3] + 0.012, f"{vals[3]:.3f}", ha="center", fontsize=9)
    ax.set_xticks(range(11)); ax.set_xlabel("number of people who get their own hat, k")
    ax.set_ylabel("probability"); ax.set_ylim(0, 0.46)
    ax.text(10, 0.36, f"at most one: {float(P[0] + P[1]):.5f}", ha="right", va="center", fontsize=9.5, color=INK)
    ax.text(10, 0.31, "(orange + green)", ha="right", va="center", fontsize=9.5, color=GREY)

# ---------------------------------------------------------------- surjections Venn
@figure("f01_venn_surjection", w=4.6, h=3.0, axis=False)
def _(ax):
    R = 1.0
    C = {1: (-0.65, 0.4), 2: (0.65, 0.4), 3: (0.0, -0.75)}
    for j, c in C.items():
        ax.add_patch(Circle(c, R, fc=LIGHT_RED, ec=RED, lw=1.3, alpha=0.55, zorder=2))
    ax.text(-1.22, 0.6, "30", ha="center", va="center", fontsize=11)
    ax.text(1.22, 0.6, "30", ha="center", va="center", fontsize=11)
    ax.text(0.0, -1.62, "30", ha="center", va="center", fontsize=11)
    ax.text(0.0, 0.82, "1", ha="center", va="center", fontsize=11)
    ax.text(-0.72, -0.4, "1", ha="center", va="center", fontsize=11)
    ax.text(0.72, -0.4, "1", ha="center", va="center", fontsize=11)
    ax.text(0.0, -0.05, "0", ha="center", va="center", fontsize=11)
    ax.text(-1.9, 1.35, "box 1 empty", ha="center", va="center", fontsize=9.5, color=RED)
    ax.text(1.9, 1.35, "box 2 empty", ha="center", va="center", fontsize=9.5, color=RED)
    ax.text(-1.6, -1.85, "box 3 empty", ha="center", va="center", fontsize=9.5, color=RED)
    ax.add_patch(Rectangle((0.7, -2.45), 1.9, 0.6, fc=LIGHT_GREEN, ec=GREEN, lw=1.2, zorder=3))
    ax.text(1.65, -2.15, "150 surjections", ha="center", va="center", fontsize=9.5, color=GREEN, zorder=4)
    frame(ax, -2.6, 2.7, -2.7, 1.8)

# ---------------------------------------------------------------- permutation cycles of S4
@figure("f01_s4_cycles", w=4.6, h=2.3)
def _(ax):
    ks = [1, 2, 3, 4]; cnt = [6, 11, 6, 1]
    cols = [BLUE, ORANGE, BLUE, BLUE]
    ax.bar(ks, cnt, color=cols, ec=INK, lw=0.7, width=0.6, zorder=3)
    for k, c in zip(ks, cnt):
        ax.text(k, c + 0.25, str(c), ha="center", fontsize=10)
    ax.set_xticks(ks); ax.set_xlabel("number of cycles k"); ax.set_ylabel("permutations of 4")
    ax.set_ylim(0, 13.2)
    ax.text(3.9, 10.8, "k=2: 11/24 = 0.458", ha="right", va="center", fontsize=9.5, color=ORANGE)
    assert sum(cnt) == 24

# ---------------------------------------------------------------- Stirling recursion triangle
@figure("f01_stirling_recursion", w=5.2, h=3.0, axis=False)
def _(ax):
    S = {1: [1], 2: [1, 1], 3: [1, 3, 1], 4: [1, 7, 6, 1], 5: [1, 15, 25, 10, 1], 6: [1, 31, 90, 65, 15, 1]}
    assert S[6][2] == 3 * S[5][2] + S[5][1] == 90
    dy = 1.2
    cell = lambda n, k: (k, -dy * n)
    for n in range(1, 7):
        for k in range(1, n + 1):
            x, y = cell(n, k)
            fc, ec = "white", INK
            if (n, k) == (6, 3):
                fc, ec = LIGHT_GREEN, GREEN
            elif (n, k) in [(5, 3), (5, 2)]:
                fc, ec = LIGHT_BLUE, BLUE
            ax.add_patch(Rectangle((x - 0.36, y - 0.42), 0.72, 0.84, fc=fc, ec=ec, lw=1.2, zorder=2))
            ax.text(x, y, str(S[n][k - 1]), ha="center", va="center", fontsize=10, zorder=3)
    for n in range(1, 7):
        ax.text(0.2, -dy * n, f"n={n}", ha="right", va="center", fontsize=9, color=GREY)
    for k in range(1, 7):
        ax.text(k, 0.95, str(k), ha="center", va="center", fontsize=9, color=GREY)
    arrow(ax, cell(5, 3), cell(6, 3), color=BLUE, shrink=6, lw=1.4)
    arrow(ax, cell(5, 2), cell(6, 3), color=BLUE, shrink=6, lw=1.4)
    ax.text(-0.5, -dy * 6 - 0.9, r"$S(6,3)=3\,S(5,3)+S(5,2)=75+15=90$", ha="left", va="center", fontsize=10, color=GREEN)
    ax.text(-0.5, -dy * 6 - 1.6, "element 6 joins one of 3 blocks (3 ways), or starts a new block (1 way)",
            ha="left", va="center", fontsize=8.5, color=GREY)
    frame(ax, -1.0, 6.6, -dy * 6 - 2.1, 1.5)

# ---------------------------------------------------------------- Bell number row
@figure("f01_bell_row", w=4.4, h=2.3)
def _(ax):
    S5 = [1, 15, 25, 10, 1]
    ax.bar(range(1, 6), S5, color=BLUE, ec=INK, lw=0.7, width=0.6, zorder=3)
    for k, v in zip(range(1, 6), S5):
        ax.text(k, v + 0.6, str(v), ha="center", fontsize=9.5)
    ax.set_xticks(range(1, 6)); ax.set_xlabel("number of teams k"); ax.set_ylabel("S(5,k)")
    ax.set_ylim(0, 34)
    ax.text(0.6, 31, r"$B_5=\sum_k S(5,k)=52$", ha="left", va="center", fontsize=10)
    assert sum(S5) == 52

# ---------------------------------------------------------------- Dyck paths
@figure("f01_dyck_path", w=5.0, h=2.5)
def _(ax):
    steps = "UUUDDUDDUD"
    pts = _dyck_pts(steps)
    h = [y for _, y in pts]
    assert h[-1] == 0 and max(h) == 3
    xs = range(len(h))
    ax.step(xs, h, where="mid", color=BLUE, lw=2.2, zorder=3)
    returns = [i for i in range(1, len(h)) if h[i] == 0]
    ax.plot(returns, [0] * len(returns), "o", color=GREEN, ms=6.5, zorder=4)
    ax.axhline(0, color=INK, lw=0.9)
    ax.set_xticks(range(0, 11)); ax.set_yticks([0, 1, 2, 3])
    ax.set_xlabel("step"); ax.set_ylabel("height")
    ax.set_ylim(-0.6, 3.8)
    ax.text(returns[0] + 0.1, 3.3, "first return to 0 at step 8", fontsize=9.5, color=GREEN, ha="left")
    ax.text(0.2, -0.45, "Split at the first return: first arch (semilength 4) + rest (semilength 1)",
            fontsize=8.5, color=GREY, ha="left")

# ---------------------------------------------------------------- height at most 2 blocks
@figure("f01_height2_blocks", w=5.0, h=2.3)
def _(ax):
    steps = "UUDD" + "UD" + "UUDD"   # blocks of semilength 2, 1, 2
    pts = _dyck_pts(steps)
    h = [y for _, y in pts]
    assert h[-1] == 0 and max(h) == 2 and len(steps) == 10
    ax.step(range(len(h)), h, where="mid", color=BLUE, lw=2.2, zorder=3)
    for b in [4, 6]:
        ax.axvline(b, color=ORANGE, ls="--", lw=1.0)
    ax.plot([0, 4, 6, 10], [0, 0, 0, 0], "o", color=GREEN, ms=5.5, zorder=4)
    ax.axhline(0, color=INK, lw=0.9)
    ax.set_xticks(range(0, 11)); ax.set_yticks([0, 1, 2])
    ax.set_xlabel("step"); ax.set_ylabel("height")
    ax.set_ylim(-0.5, 2.9)
    ax.text(2, 2.45, "block 1: semilength 2", ha="center", fontsize=9.5, color=ORANGE)
    ax.text(5, 1.5, "block 2:\nsemilength 1", ha="center", fontsize=9.5, color=ORANGE)
    ax.text(8, 2.45, "block 3: semilength 2", ha="center", fontsize=9.5, color=ORANGE)

# ---------------------------------------------------------------- last split of 5 matrices
@figure("f01_last_split", w=5.2, h=2.0, axis=False)
def _(ax):
    for i in range(5):
        box(ax, (i + 1, 0), f"M{i+1}", w=0.7, h=0.55, fs=10)
    splits = [(1, 1, 5), (2, 1, 2), (3, 2, 1), (4, 5, 1)]
    for s, left, right in splits:
        xs = s + 0.5
        ax.plot([xs, xs], [-0.45, 0.45], ls="--", color=ORANGE, lw=1.2, zorder=1)
        ax.text(xs, -0.95, f"{left} x {right}\n= {left*right}", ha="center", va="center", fontsize=9, color=ORANGE)
    ax.text(3, 1.05, "last product splits the five matrices at one of 4 gaps",
            ha="center", va="center", fontsize=9.5, color=GREY)
    ax.text(3, -1.6, "left x right: C_0 x C_3, C_1 x C_2, C_2 x C_1, C_3 x C_0;  5+2+2+5 = 14 = C_4",
            ha="center", va="center", fontsize=9, color=GREY)
    frame(ax, 0, 6, -1.9, 1.4)

# ---------------------------------------------------------------- Catalan reflection
@figure("f01_catalan_reflect", w=4.6, h=3.0)
def _(ax):
    steps = "UURRURUR"
    pts = _steps_to_pts(steps)
    assert pts[-1] == (4, 4)
    first = next(i for i, (x, y) in enumerate(pts) if y == x + 1)
    assert pts[first] == (0, 1)
    tail = pts[first:]
    refl = [(y - 1, x + 1) for (x, y) in tail]
    assert refl[-1] == (3, 5)
    _grid(ax, 4, 5)
    xs = np.array([-0.2, 4.4])
    ax.plot(xs, xs, "--", color=GREEN, lw=1.2, zorder=2)
    ax.plot(xs, xs + 1, ":", color=ORANGE, lw=1.4, zorder=2)
    _path(ax, pts, RED)
    _path(ax, pts[:first + 1] + refl[1:], GREY, lw=1.6, ls="--")
    ax.plot([4], [4], "o", color=GREEN, ms=7, zorder=5)
    ax.plot([3], [5], "o", color=GREY, ms=7, zorder=5)
    ax.text(4.25, 4.05, "(4,4)", fontsize=9.5, color=GREEN, ha="left", va="center")
    ax.text(2.8, 5.25, "(3,5)", fontsize=9.5, color=GREY, ha="center", va="center")
    ax.text(-0.5, -0.95, "green dashed: y = x;  orange dotted: y = x+1\nred: bad path;  grey: its reflected tail",
            fontsize=8.5, color=GREY, ha="left", va="center")
    frame(ax, -0.5, 5.2, -1.5, 5.7)
    ax.set_axis_off()
    ax.set_xlim(-0.5, 5.2); ax.set_ylim(-1.5, 5.7)

# ---------------------------------------------------------------- ballot walks
@figure("f01_ballot_walk", w=5.0, h=2.7)
def _(ax):
    good = "AABAABABBA"
    bad = "ABAABABAAB"
    def lead(s):
        v = [0]
        for c in s:
            v.append(v[-1] + (1 if c == "A" else -1))
        return v
    g, b = lead(good), lead(bad)
    assert g[-1] == 2 and b[-1] == 2 and min(g[1:]) >= 1 and min(b[2:]) == 0 and b[1] == 1
    ax.step(range(11), g, where="post", color=BLUE, lw=2.2, zorder=3)
    ax.step(range(11), b, where="post", color=RED, lw=1.6, ls="--", zorder=3)
    ax.axhline(0, color=GREEN, lw=1.2, zorder=2)
    ax.axhline(-1, color=GREY, lw=1.0, ls=":", zorder=2)
    ax.text(10.1, 0.0, "strict: never 0 after step 0", fontsize=8.8, color=GREEN, va="bottom", ha="right")
    ax.text(10.1, -1.0, "weak: never -1 (ties allowed)", fontsize=8.8, color=GREY, va="bottom", ha="right")
    ax.set_xticks(range(0, 11)); ax.set_yticks([-1, 0, 1, 2, 3])
    ax.set_xlabel("vote count k"); ax.set_ylabel("A lead, S_k")
    ax.set_ylim(-1.6, 3.6)
    ax.set_title("blue: good ballot (A ahead after every vote); red: a bad path", fontsize=9.5)

# ---------------------------------------------------------------- return probabilities
@figure("f01_walk_returns", w=5.2, h=2.5, axis=False)
def _(ax):
    ns = [2, 4, 6, 8, 10]
    p0 = [Fr(comb(n, n // 2), 2 ** n) for n in ns]
    fr = [Fr(1, 2), Fr(1, 8), Fr(1, 16), Fr(5, 128), Fr(7, 256)]
    assert p0[-1] == Fr(63, 256) and fr[-1] == Fr(7, 256) == Fr(14, 2 ** 9)
    fig = ax.figure
    ax.set_axis_off()
    ax1 = fig.add_axes([0.13, 0.2, 0.34, 0.64]); ax2 = fig.add_axes([0.62, 0.2, 0.34, 0.64])
    for a_, vals, title, hl in [(ax1, p0, r"$\Pr(S_n=0)$, n even", BLUE), (ax2, fr, "Pr(first return at n)", ORANGE)]:
        cols = [GREY] * len(ns); cols[-1] = hl
        a_.bar(ns, [float(v) for v in vals], width=1.3, color=cols, ec=INK, lw=0.6, zorder=3)
        for n, v in zip(ns, vals):
            a_.text(n, float(v) + 0.02, f"{float(v):.3f}", ha="center", fontsize=8.5)
        a_.set_xticks(ns); a_.set_xlabel("step n"); a_.set_title(title, fontsize=9.5)
        a_.set_ylim(0, 0.62); a_.set_xlim(1, 11)
    ax1.set_ylabel("probability")

# ---------------------------------------------------------------- lattice obstacles
@figure("f01_grid_obstacle", w=4.2, h=3.1, axis=False)
def _(ax):
    _grid(ax, 5, 5)
    ax.text(-0.2, -0.3, "(0,0)", fontsize=9.5, ha="right", va="top")
    ax.text(5.2, 5.35, "(5,5)", fontsize=9.5, ha="left", va="bottom")
    ax.plot([2], [3], "x", color=RED, ms=13, mew=3, zorder=5)
    ax.text(2.25, 3.3, "blocked (2,3)", fontsize=9.5, color=RED, ha="left", va="bottom")
    frame(ax, -0.8, 6.0, -0.8, 6.0)

@figure("f01_grid_two_obstacles", w=4.4, h=3.1, axis=False)
def _(ax):
    _grid(ax, 5, 5)
    up = _steps_to_pts("UUURRUURRR")
    right = _steps_to_pts("RRRUURUUUR")
    assert up[-1] == (5, 5) and right[-1] == (5, 5)
    assert (2, 3) in up and (3, 2) in right and (3, 2) not in up and (2, 3) not in right
    _path(ax, [(x + 0.0, y) for x, y in up], BLUE, lw=2.2)
    _path(ax, [(x, y) for x, y in right], ORANGE, lw=2.2)
    for p in [(2, 3), (3, 2)]:
        ax.plot([p[0]], [p[1]], "x", color=RED, ms=13, mew=3, zorder=5)
    ax.text(2.2, 2.55, "(3,2)", fontsize=9.5, color=RED, ha="left", va="center")
    ax.text(1.7, 3.2, "(2,3)", fontsize=9.5, color=RED, ha="right", va="bottom")
    ax.text(-0.6, -0.95, "after (2,3) the path has y >= 3, so it misses (3,2)",
            fontsize=8.5, color=GREY, ha="left", va="center")
    frame(ax, -0.8, 6.0, -1.2, 6.0)

# ---------------------------------------------------------------- waypoint
@figure("f01_waypoint", w=4.6, h=2.6, axis=False)
def _(ax):
    _grid(ax, 6, 4)
    pts = _steps_to_pts("URURRURRUR")
    assert pts[-1] == (6, 4) and (3, 2) in pts
    _path(ax, pts, BLUE, lw=2.2)
    ax.plot([3], [2], "o", color=GREEN, ms=9, zorder=5)
    ax.text(3.15, 1.6, "(3,2)", fontsize=9.5, color=GREEN, ha="left", va="center")
    ax.text(-0.2, -0.35, "(0,0)", fontsize=9.5, ha="right", va="top")
    ax.text(6.2, 4.35, "(6,4)", fontsize=9.5, ha="left", va="bottom")
    ax.text(0, -1.0, "legs: C(5,2) x C(5,2) = 100 of C(10,4) = 210 paths",
            fontsize=9, color=GREY, ha="left", va="center")
    frame(ax, -0.8, 6.9, -1.3, 4.8)

# ---------------------------------------------------------------- poker categories
@figure("f01_poker_categories", w=5.4, h=3.0)
def _(ax):
    T = comb(52, 5)
    cats = [
        ("high card", 1302540, GREY),
        ("one pair", 1098240, BLUE),
        ("two pair", 123552, BLUE),
        ("three of a kind", 54912, BLUE),
        ("straight", 10200, GREY),
        ("flush", 5108, GREY),
        ("full house", 3744, BLUE),
        ("four of a kind", 624, BLUE),
        ("straight flush", 40, GREY),
    ]
    assert sum(c for _, c, _ in cats) == T
    pairs = sum(c for _, c, col in cats if col == BLUE)
    assert abs(pairs / T - (1 - 1317888 / T)) < 1e-12
    y = np.arange(len(cats))[::-1]
    for yi, (name, c, col) in zip(y, cats):
        p = c / T
        ax.barh(yi, p, height=0.62, color=col, ec=INK, lw=0.6, zorder=3, alpha=0.9)
        ax.text(p * 1.35, yi, f"{p:.5f}", va="center", fontsize=9)
    ax.set_yticks(y); ax.set_yticklabels([n for n, _, _ in cats], fontsize=9)
    ax.set_xscale("log"); ax.set_xlim(3e-6, 2.0)
    ax.set_xlabel("probability (log scale)\nblue: a rank repeated, total %.5f = 1 - 0.50708\ngrey: all five ranks different" % (pairs / T),
                  fontsize=8.5)

# ---------------------------------------------------------------- birthday curves
@figure("f01_birthday_curves", w=5.4, h=2.9)
def _(ax):
    N, nmax = 365, 100
    base = [2, 2, 1]                       # 2 + 2x + x^2 = 2*(1 + x + x^2/2)
    poly = [1] + [0] * nmax
    for _ in range(N):
        new = [0] * (nmax + 1)
        for i, a in enumerate(poly):
            if a:
                for j, b in enumerate(base):
                    if i + j <= nmax:
                        new[i + j] += a * b
        poly = new
    ns = np.arange(1, nmax + 1)
    no_pair = np.array([np.prod([(N - i) / N for i in range(int(n))]) for n in ns])
    no_triple = np.array([float(Fr(poly[int(n)] * factorial(int(n)), 2 ** N * N ** int(n))) for n in ns])
    assert abs(no_pair[22] - 0.4927) < 5e-4 and abs(no_triple[87] - 0.4889) < 5e-4
    approx = np.exp(-ns * (ns - 1) / (2 * N))
    ax.plot(ns, no_pair, color=BLUE, lw=2.0, label="no two share a birthday")
    ax.plot(ns, no_triple, color=ORANGE, lw=2.0, label="no three share a birthday")
    ax.plot(ns, approx, ":", color=BLUE, lw=1.3, label=r"$\exp(-n(n-1)/2N)$")
    ax.axhline(0.5, color=GREY, ls="--", lw=0.9)
    ax.plot([23], [no_pair[22]], "o", color=BLUE, ms=6, zorder=5)
    ax.plot([88], [no_triple[87]], "o", color=ORANGE, ms=6, zorder=5)
    ax.annotate("n=23: 0.4927", (23, no_pair[22]), xytext=(30, 0.66), fontsize=9, color=BLUE,
                arrowprops=dict(arrowstyle="-", color=BLUE, lw=0.7))
    ax.annotate("n=88: 0.4889", (88, no_triple[87]), xytext=(42, 0.3), fontsize=9, color=ORANGE,
                arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.7))
    ax.set_xlim(0, 100); ax.set_ylim(0, 1.02)
    ax.set_xlabel("number of people n"); ax.set_ylabel("probability")
    ax.legend(fontsize=8.5, frameon=False, loc="lower right")

# ---------------------------------------------------------------- prisoner cycles
@figure("f01_cycle_arrows", w=4.6, h=3.0, axis=False)
def _(ax):
    cycA = [1, 4, 7, 2, 9, 5]        # 6-cycle
    cycB = [3, 8, 6, 10]             # 4-cycle
    sigma = {}
    for cyc in (cycA, cycB):
        for i, a in enumerate(cyc):
            sigma[a] = cyc[(i + 1) % len(cyc)]
    assert sorted(sigma) == list(range(1, 11))
    pos = {i: (cos(pi / 2 - 2 * pi * (i - 1) / 10), sin(pi / 2 - 2 * pi * (i - 1) / 10)) for i in range(1, 11)}
    for a, b in sigma.items():
        col = RED if a in cycA else BLUE
        arrow(ax, pos[a], pos[b], color=col, rad=0.25, shrink=13, lw=1.2)
    for i, p in pos.items():
        col = RED if i in cycA else BLUE
        node(ax, p, str(i), r=0.13, fs=9.5, ec=col)
    ax.text(0, -1.5, "cutoff n/2 = 5; red 6-cycle has 6 > 5, so a prisoner fails", ha="center", fontsize=9, color=RED)
    frame(ax, -1.45, 1.45, -1.75, 1.45)

@figure("f01_prisoner_threshold", w=5.0, h=2.6)
def _(ax):
    n = 100
    def p_all_le(k):
        p = [1.0]
        for m in range(1, n + 1):
            p.append(sum(p[m - j] for j in range(1, min(k, m) + 1)) / m)
        return p[n]
    ks = np.arange(1, n + 1)
    ps = np.array([p_all_le(int(k)) for k in ks])
    assert abs(p_all_le(50) - 0.31183) < 1e-4 and abs(p_all_le(40) - 0.13477) < 1e-4
    ax.plot(ks, ps, color=BLUE, lw=2.0)
    ax.plot([50], [p_all_le(50)], "o", color=GREEN, ms=6.5, zorder=5)
    ax.plot([40], [p_all_le(40)], "o", color=ORANGE, ms=6.5, zorder=5)
    ax.annotate("k=50: 0.3118", (50, p_all_le(50)), xytext=(56, 0.45), fontsize=9, color=GREEN,
                arrowprops=dict(arrowstyle="-", color=GREEN, lw=0.7))
    ax.annotate("k=40: 0.1348", (40, p_all_le(40)), xytext=(8, 0.45), fontsize=9, color=ORANGE,
                arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.7))
    ax.axvline(50, color=GREY, ls=":", lw=0.9)
    ax.set_xlim(0, 100); ax.set_ylim(0, 1.02)
    ax.set_xlabel("boxes each prisoner may open, k (n = 100)")
    ax.set_ylabel("P(all succeed)")

# ---------------------------------------------------------------- K4 spanning trees
@figure("f01_k4_trees", w=5.0, h=2.4, axis=False)
def _(ax):
    P = {1: (0, 1), 2: (1, 1), 3: (1, 0), 4: (0, 0)}
    E = [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]
    def draw(off, chosen, col, text, tc):
        for a, b in E:
            pa = (P[a][0] + off, P[a][1]); pb = (P[b][0] + off, P[b][1])
            if (a, b) in chosen:
                ax.plot([pa[0], pb[0]], [pa[1], pb[1]], color=col, lw=3, zorder=2)
            else:
                ax.plot([pa[0], pb[0]], [pa[1], pb[1]], color=GREY, lw=1.0, ls="--", zorder=1)
        for i, p in P.items():
            node(ax, (p[0] + off, p[1]), str(i), r=0.13, fs=9.5)
        ax.text(off + 0.5, -0.6, text, ha="center", va="center", fontsize=9, color=tc)
    draw(0, [(1, 2), (2, 3), (3, 4)], BLUE, "connected, no loop: a tree", BLUE)
    draw(2.6, [(1, 2), (2, 3), (1, 3)], RED, "a loop; city 4 cut off", RED)
    frame(ax, -0.5, 4.2, -1.0, 1.5)

# ---------------------------------------------------------------- Burnside necklaces
@figure("f01_burnside_necklace", w=5.4, h=2.7)
def _(ax):
    rot = [3 ** g for g in [6, 1, 2, 3, 2, 1]]
    assert rot == [729, 3, 9, 27, 9, 3] and sum(rot) / 6 == 130
    refl = [3 ** 4, 3 ** 4, 3 ** 4, 3 ** 3, 3 ** 3, 3 ** 3]
    vals = rot + refl
    assert sum(vals) / 12 == 92
    cols = [BLUE] * 6 + [ORANGE] * 6
    x = list(range(12))
    ax.bar(x, vals, color=cols, ec=INK, lw=0.6, width=0.65, zorder=3)
    for i, v in zip(x, vals):
        ax.text(i, v + 15, str(v), ha="center", fontsize=8.5)
    ax.set_xticks(x)
    ax.set_xticklabels(["0", "1", "2", "3", "4", "5", "v", "v", "v", "e", "e", "e"], fontsize=9)
    ax.set_xlabel("rotations 0..5 (blue)\nreflections: v = through vertices, e = through edges (orange)", fontsize=8.5)
    ax.set_ylabel("colourings fixed"); ax.set_ylim(0, 860)
    ax.text(11.4, 760, "rotations: 780/6 = 130\nall 12: 1104/12 = 92", ha="right", va="center", fontsize=9,
            color=INK)

# ---------------------------------------------------------------- Vandermonde bars
@figure("f01_vandermonde_bars", w=4.8, h=2.6)
def _(ax):
    ks = list(range(7)); vals = [comb(6, k) ** 2 for k in ks]
    assert sum(vals) == comb(12, 6) == 924
    ax.bar(ks, vals, color=[BLUE if k != 3 else ORANGE for k in ks], ec=INK, lw=0.6, width=0.65, zorder=3)
    for k, v in zip(ks, vals):
        ax.text(k, v + 8, str(v), ha="center", fontsize=9)
    ax.set_xticks(ks); ax.set_xlabel("k men in the committee (6 men, 6 women)")
    ax.set_ylabel("ways"); ax.set_ylim(0, 470)
    ax.text(6, 430, "sum = 924 = C(12,6)", ha="right", fontsize=9.5)

# ---------------------------------------------------------------- hockey stick
@figure("f01_hockey_stick", w=5.0, h=2.6)
def _(ax):
    ms = list(range(4, 12)); vals = [comb(m - 1, 3) for m in ms]
    assert vals == [1, 4, 10, 20, 35, 56, 84, 120] and sum(vals) == comb(11, 4) == 330
    ax.bar(ms, vals, color=BLUE, ec=INK, lw=0.6, width=0.65, zorder=3)
    for m, v in zip(ms, vals):
        ax.text(m, v + 2.5, str(v), ha="center", fontsize=9)
    ax.set_xticks(ms); ax.set_xlabel("largest element m of the 4-subset")
    ax.set_ylabel("subsets with max m"); ax.set_ylim(0, 140)
    ax.text(4.0, 128, "total 330 = C(11,4)", ha="left", fontsize=9.5)

# ---------------------------------------------------------------- odd parts
@figure("f01_odd_part_boxes", w=5.0, h=2.9, axis=False)
def _(ax):
    rows = [1, 3, 5, 7, 9]
    for r, o in enumerate(rows):
        y = -r
        nums = [o * 2 ** a for a in range(5) if o * 2 ** a <= 10]
        ax.add_patch(Rectangle((-0.1, y - 0.36), 10.3, 0.72, fc="#f4f6f8", ec="none", zorder=0))
        ax.text(-0.35, y, f"odd {o}", ha="right", va="center", fontsize=9.5, color=GREY)
        for i, v in enumerate(nums):
            node(ax, (v, y), str(v), r=0.28, fs=9.5, fc=LIGHT_BLUE, ec=BLUE)
            if i < len(nums) - 1:
                arrow(ax, (v, y), (nums[i + 1], y), color=GREY, shrink=11, lw=0.9)
    ax.text(5, 0.85, "every integer 1..10 is 2^a x odd, one row per odd part",
            ha="center", va="center", fontsize=9.5, color=GREY)
    ax.text(5, -4.9, "6 numbers, 5 rows: two share a row; within a row each divides the next",
            ha="center", va="center", fontsize=9, color=GREY)
    frame(ax, -1.2, 10.9, -5.4, 1.3)

# ---------------------------------------------------------------- Ss with gaps
@figure("f01_gaps_s", w=5.0, h=1.9, axis=False)
def _(ax):
    letters = list("MIIIIPP")
    gaps = {0, 3, 5, 7}                    # gap j sits before letter j; gap 7 is the end
    seq = []
    for j in range(8):
        if j in gaps:
            seq.append("S")
        if j < 7:
            seq.append(letters[j])
    assert seq.count("S") == 4
    assert all(not (seq[i] == "S" and seq[i + 1] == "S") for i in range(len(seq) - 1))
    for i, ch in enumerate(seq):
        if ch == "S":
            box(ax, (i, 0), "S", w=0.62, h=0.62, fc=LIGHT_ORANGE, ec=ORANGE, fs=10)
        else:
            box(ax, (i, 0), ch, w=0.62, h=0.62, fc="white", ec=INK, fs=10)
    ax.text(5, 0.95, "7 letters M,I,I,I,I,P,P in a row: 8 gaps including both ends",
            ha="center", va="center", fontsize=9.5, color=GREY)
    ax.text(5, -0.95, "4 gaps of 8: C(8,4) = 70;  the 7 others: 7!/(4!2!) = 105",
            ha="center", va="center", fontsize=9, color=GREY)
    frame(ax, -0.8, len(seq) - 0.2, -1.3, 1.4)
