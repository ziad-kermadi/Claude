"""Figures for staging/gap_A.json (gap batch A: pigeonhole, stars and bars, parity/invariants)."""
import math
import numpy as np
from matplotlib.patches import Arc, Rectangle, Circle
from qcfig import *


@figure("fgA_square_cells", w=3.4, h=3.5, axis=False)
def _(ax):
    # Four closed sub-squares of side 1/2; corners + centre attains min distance sqrt(2)/2
    for (x0, y0), fc in zip([(0, 0), (0.5, 0), (0, 0.5), (0.5, 0.5)],
                            [LIGHT_BLUE, LIGHT_ORANGE, LIGHT_GREEN, LIGHT_RED]):
        ax.add_patch(Rectangle((x0, y0), 0.5, 0.5, fc=fc, ec="none", alpha=0.55, zorder=1))
    ax.add_patch(Rectangle((0, 0), 1, 1, fc="none", ec=INK, lw=1.4, zorder=2))
    ax.plot([0.5, 0.5], [0, 1], ls="--", color=GREY, lw=1.0, zorder=2)
    ax.plot([0, 1], [0.5, 0.5], ls="--", color=GREY, lw=1.0, zorder=2)
    for p in [(0, 0), (1, 0), (0, 1), (1, 1)]:
        ax.plot(*p, "o", color=INK, ms=6, zorder=4)
    ax.plot(0.5, 0.5, "o", color=ORANGE, ms=7, zorder=4)
    for p in [(0, 0), (1, 0), (0, 1), (1, 1)]:
        ax.plot([0.5, p[0]], [0.5, p[1]], color=ORANGE, lw=1.6, zorder=3)
    ax.text(0.27, 0.27, r"$\frac{\sqrt{2}}{2}$", color=ORANGE, fontsize=10, ha="center", va="center",
            bbox=dict(fc="white", ec="none", pad=0.5), zorder=5)
    ax.text(0.5, -0.12, "side $\\frac{1}{2}$ cells: any two points in a cell are within $\\frac{\\sqrt{2}}{2}$",
            ha="center", va="top", fontsize=8.5, color=GREY)
    frame(ax, -0.15, 1.15, -0.35, 1.15)


@figure("fgA_prefix_clock", w=3.2, h=3.2, axis=False)
def _(ax):
    # Residues mod 7 on a circle: prefix sums S_0..S_6 of six 1s occupy all 7 residues once
    n = 7
    for k in range(n):
        ang = math.pi / 2 - 2 * math.pi * k / n
        x, y = math.cos(ang), math.sin(ang)
        node(ax, (x, y), str(k), r=0.2, fc=LIGHT_BLUE, ec=BLUE, fs=11)
        ax.text(1.42 * x, 1.42 * y, f"$S_{k}={k}$", ha="center", va="center", fontsize=9, color=BLUE)
    ax.add_patch(Circle((0, 0), 1.0, fill=False, ec=GREY, lw=1.0, ls="--", zorder=1))
    ax.text(0, 0, "mod 7", ha="center", va="center", fontsize=10, color=GREY)
    frame(ax, -1.9, 1.9, -1.9, 1.9)
    ax.text(0, -1.78, "six 1s: all 7 prefix sums differ mod 7", ha="center", fontsize=8.5, color=GREY)


@figure("fgA_chain_pairs", w=5.2, h=2.3, axis=False)
def _(ax):
    # Pairs {x, x+2} partition 1..12 into 6 pairs; a 7-subset must contain a pair
    xs = list(range(1, 13))
    ax.plot([0.5, 12.5], [0, 0], color=INK, lw=0.8, zorder=1)
    for x in xs:
        node(ax, (x, 0), str(x), r=0.28, fc="white", ec=INK, fs=9)
    for a, b in [(1, 3), (5, 7), (9, 11)]:
        ax.add_patch(Arc(((a + b) / 2, 0), b - a, 2.0, theta1=0, theta2=180, color=BLUE, lw=1.6, zorder=2))
    for a, b in [(2, 4), (6, 8), (10, 12)]:
        ax.add_patch(Arc(((a + b) / 2, 0), b - a, 2.0, theta1=180, theta2=360, color=ORANGE, lw=1.6, zorder=2))
    ax.text(6.5, -1.45, "6 pairs $\\{x,x+2\\}$ cover $1,\\dots,12$; 7 numbers force a pair",
            ha="center", fontsize=9, color=GREY)
    frame(ax, 0, 13, -1.8, 1.8)


@figure("fgA_residue_boxes", w=5.6, h=2.1, axis=False)
def _(ax):
    # Nine residue boxes; three tickets each, then a fourth forces a repeat
    for r in range(9):
        ax.add_patch(Rectangle((r * 1.0, 0), 0.9, 1.4, fc="white", ec=INK, lw=1.1, zorder=1))
        ax.text(r * 1.0 + 0.45, -0.22, f"{r}", ha="center", va="center", fontsize=9)
        for k in range(3):
            ax.plot(r * 1.0 + 0.22 + 0.22 * k, 0.5, "o", color=BLUE, ms=6.5, zorder=3)
    ax.plot(0.22 + 0.22 * 0 + 0.0, 0.95, "o", color=ORANGE, ms=8, zorder=4)
    ax.text(0.45, 1.6, "4th", ha="center", color=ORANGE, fontsize=9)
    ax.text(4.5, 1.9, "27 tickets, 3 per remainder: safe. The 28th must repeat a box.",
            ha="center", fontsize=8.5, color=GREY)
    frame(ax, -0.2, 9.2, -0.5, 2.1)


@figure("fgA_monotone_path", w=4.4, h=2.9)
def _(ax):
    # Non-decreasing sequence (1,1,3,6,6) as a lattice path: N = an entry equal to the current value,
    # E = move from value v to v+1. Five N steps and seven E steps: C(12,5) such paths.
    seq = (1, 1, 3, 6, 6)
    x, y = 0, 0
    pts = [(0, 0)]
    for v in range(1, 9):
        for _ in range(seq.count(v)):
            y += 1
            pts.append((x, y))
        if v < 8:
            x += 1
            pts.append((x, y))
    ax.set_xlim(-0.4, 7.4)
    ax.set_ylim(-0.4, 5.4)
    ax.set_aspect("equal")
    ax.set_xticks(range(0, 8))
    ax.set_xticklabels([str(v) for v in range(1, 9)])
    ax.set_yticks(range(0, 6))
    ax.grid(True, color=GREY, lw=0.4, alpha=0.5)
    px, py = zip(*pts)
    ax.plot(px, py, color=BLUE, lw=2.0, zorder=3)
    ax.plot(px, py, "o", color=BLUE, ms=3.5, zorder=4)
    ax.plot(7, 5, "o", color=GREEN, ms=7, zorder=5)
    ax.set_xlabel("value $v$ (1 to 8): east step moves to the next value")
    ax.set_ylabel("entries so far")
    ax.set_title("sample $(1,1,3,6,6)$: north step per entry", fontsize=9.5)


@figure("fgA_tromino_4x4", w=3.2, h=3.4, axis=False)
def _(ax):
    # 4x4 minus bottom-left corner: five L-trominoes. Central tromino takes the inner corner of
    # the three full quadrants; the remaining quadrants are L-shaped after one cell is removed.
    rows = 4
    def y_of(r):  # row 0 at top
        return rows - 1 - r
    pieces = [
        ([(0, 0), (0, 1), (1, 0)], LIGHT_BLUE),
        ([(0, 2), (0, 3), (1, 3)], LIGHT_BLUE),
        ([(2, 3), (3, 2), (3, 3)], LIGHT_BLUE),
        ([(2, 0), (2, 1), (3, 1)], LIGHT_BLUE),
        ([(1, 1), (1, 2), (2, 2)], LIGHT_ORANGE),
    ]
    for cells, fc in pieces:
        for (r, c) in cells:
            ax.add_patch(Rectangle((c, y_of(r)), 1, 1, fc=fc, ec=INK, lw=1.2, zorder=1))
    ax.add_patch(Rectangle((0, y_of(3)), 1, 1, fc="white", ec=GREY, lw=1.0, ls="--", zorder=1))
    ax.text(0.5, y_of(3) + 0.5, "missing", ha="center", va="center", fontsize=7.5, color=GREY)
    ax.text(2.0, -0.45, "orange: central tromino (the key move)", ha="center", fontsize=8.5, color=GREY)
    frame(ax, -0.1, 4.1, -0.8, 4.1)
    ax.set_xlim(-0.1, 4.1)
    ax.set_ylim(-0.8, 4.1)


@figure("fgA_lamp_weights", w=4.6, h=1.9, axis=False)
def _(ax):
    # Lamp weights c_j = 1,1,0,1,1,0,1,1,0,1: every button covers three consecutive lamps,
    # whose weights sum to 2 (mod 2 = 0), so the weighted parity never changes.
    c = [1, 1, 0, 1, 1, 0, 1, 1, 0, 1]
    for j, cj in enumerate(c, start=1):
        fc = LIGHT_ORANGE if cj == 1 else "white"
        node(ax, (j, 0), str(j), r=0.32, fc=fc, ec=INK, fs=10)
        ax.text(j, -0.75, f"$c_{{{j}}}={cj}$", ha="center", va="center", fontsize=8.5, color=INK)
    ax.add_patch(Arc((2, 0), 2.0, 1.6, theta1=0, theta2=180, color=BLUE, lw=1.5, zorder=2))
    ax.text(2, 1.05, "button 1: $c_1+c_2+c_3=2\\equiv 0$", ha="center", fontsize=8.5, color=BLUE)
    frame(ax, 0, 11, -1.2, 1.6)
    ax.set_xlim(0.2, 10.8)
