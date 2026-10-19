"""Figures for cards/05_continuous_geometric.json."""
import math
import numpy as np
from matplotlib.patches import Wedge
from qcfig import *

TWO_PI = 2 * np.pi
LIGHT_GREY = "#e6e6e6"


def _circle(ax, cx, cy=0.0, r=1.0):
    t = np.linspace(0, TWO_PI, 360)
    ax.plot(cx + r * np.cos(t), cy + r * np.sin(t), color=INK, lw=1.0, zorder=1)


def _pt(cx, deg, r=1.0):
    a = math.radians(deg)
    return (cx + r * math.cos(a), r * math.sin(a))


def _Phi(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def _phi(x):
    return math.exp(-x * x / 2) / math.sqrt(2 * math.pi)


# ---------- Card 2, 24, 43: chord readings of Bertrand's paradox ----------

@figure("f05_bertrand_readings", w=5.6, h=2.4, axis=False)
def _(ax):
    # (a) two uniform endpoints: long chord iff arc separation in (120, 240) degrees
    cx = 0.0
    _circle(ax, cx)
    tri = [_pt(cx, a) for a in (90, 210, 330)]
    ax.add_patch(Polygon(tri, closed=True, fc="none", ec=GREY, lw=1.0, ls="--", zorder=2))
    p1, p2 = _pt(cx, 0), _pt(cx, 150)
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=BLUE, lw=2.0, zorder=3)
    for p in (p1, p2):
        ax.plot(p[0], p[1], "o", color=BLUE, ms=4, zorder=4)
    ax.text(cx, -1.45, r"(a) endpoints: $\frac{1}{3}$", ha="center", fontsize=9.5)

    # (b) uniform distance d from centre: long chord iff d < 1/2
    cx = 3.0
    _circle(ax, cx)
    d = 0.3
    half = math.sqrt(1 - d * d)
    ax.plot([cx - half, cx + half], [d, d], color=BLUE, lw=2.0, zorder=3)
    ax.plot([cx, cx], [0, d], color=ORANGE, lw=1.4, zorder=3)
    ax.text(cx + 0.07, d / 2, r"$d$", color=ORANGE, fontsize=10, va="center")
    d2 = 0.7
    half2 = math.sqrt(1 - d2 * d2)
    ax.plot([cx - half2, cx + half2], [d2, d2], color=GREY, lw=1.6, zorder=3)
    ax.plot([cx - 1.15, cx + 1.15], [0.5, 0.5], color=RED, lw=1.0, ls=":", zorder=2)
    ax.text(cx + 0.0, -1.45, r"(b) distance: $\frac{1}{2}$", ha="center", fontsize=9.5)

    # (c) uniform midpoint in the disk: long chord iff midpoint in the disk of radius 1/2
    cx = 6.0
    _circle(ax, cx)
    ax.add_patch(Circle((cx, 0), 0.5, fc=LIGHT_BLUE, ec=BLUE, lw=1.0, ls="--", zorder=1.5))
    for m, col, lw in ((0.3, BLUE, 1.8), (0.7, GREY, 1.4)):
        hh = math.sqrt(1 - m * m)
        ax.plot([cx + m, cx + m], [-hh, hh], color=col, lw=lw, zorder=3)
        ax.plot(cx + m, 0, "o", color=ORANGE, ms=4, zorder=4)
    ax.text(cx, -1.45, r"(c) midpoint: $\frac{1}{4}$", ha="center", fontsize=9.5)

    frame(ax, -1.3, 7.3, -1.9, 1.35)


# ---------- Card 23, 59: meeting problem, symmetric window ----------

@figure("f05_meeting_band", w=3.8, h=3.1)
def _(ax):
    x = np.linspace(0, 1, 400)
    ax.fill_between(x, np.maximum(0, x - 0.25), np.minimum(1, x + 0.25), color=LIGHT_GREEN, lw=0, zorder=1)
    xs = x[x <= 0.75]
    ax.plot(xs, xs + 0.25, color=GREEN, lw=1.2)
    xs = x[x >= 0.25]
    ax.plot(xs, xs - 0.25, color=GREEN, lw=1.2)
    ax.plot([0, 1], [0, 1], color=GREY, lw=0.8, ls="--")
    ax.text(0.6, 0.5, "meet", color=GREEN, fontsize=10, ha="center", va="center")
    ax.text(0.75, 0.05, r"$\frac{3}{4}$", color=GREY, fontsize=9, ha="center", va="bottom")
    ax.text(0.04, 0.9, r"$\frac{3}{4}$", color=GREY, fontsize=9, ha="left", va="center")
    ticks = [0, 0.25, 0.5, 0.75, 1]
    labels = ["0", r"$\frac{1}{4}$", r"$\frac{1}{2}$", r"$\frac{3}{4}$", "1"]
    ax.set_xticks(ticks, labels)
    ax.set_yticks(ticks, labels)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_aspect("equal")
    ax.set_xlabel("X: first arrival"); ax.set_ylabel("Y: second arrival")
    ax.set_title(r"meet iff $|X-Y|\leq\frac{1}{4}$" + "\n" + r"$P=1-\frac{9}{16}=\frac{7}{16}$", fontsize=10)


# ---------- Card 48: meeting problem, shifted window (15 vs 30 min) ----------

@figure("f05_meeting_shifted", w=3.8, h=3.1)
def _(ax):
    x = np.linspace(0, 1, 400)
    ax.fill_between(x, np.maximum(0, x - 0.5), np.minimum(1, x + 0.25), color=LIGHT_GREEN, lw=0, zorder=1)
    xs = x[x <= 0.75]
    ax.plot(xs, xs + 0.25, color=GREEN, lw=1.2)
    xs = x[x >= 0.5]
    ax.plot(xs, xs - 0.5, color=GREEN, lw=1.2)
    ax.plot([0, 1], [0, 1], color=GREY, lw=0.8, ls="--")
    ax.text(0.55, 0.72, "meet", color=GREEN, fontsize=10, ha="center", va="center")
    ax.text(0.72, 0.04, r"$\frac{1}{2}$", color=GREY, fontsize=9, ha="center", va="bottom")
    ax.text(0.05, 0.92, r"$\frac{3}{4}$", color=GREY, fontsize=9, ha="left", va="center")
    ticks = [0, 0.25, 0.5, 0.75, 1]
    labels = ["0", r"$\frac{1}{4}$", r"$\frac{1}{2}$", r"$\frac{3}{4}$", "1"]
    ax.set_xticks(ticks, labels)
    ax.set_yticks(ticks, labels)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_aspect("equal")
    ax.set_xlabel("X: Alice arrives"); ax.set_ylabel("Y: Bob arrives")
    ax.set_title(r"$-\frac{1}{2}\leq Y-X\leq\frac{1}{4}$" + "\n" + r"$P=1-\frac{9}{32}-\frac{4}{32}=\frac{19}{32}$",
                 fontsize=10)


# ---------- Card 21: broken stick, triangle condition ----------

@figure("f05_stick_triangle", w=3.6, h=3.1)
def _(ax):
    # cuts a < b; pieces a, b-a, 1-b. Triangle iff each piece < 1/2.
    tri1 = [(0, 0.5), (0.5, 0.5), (0.5, 1.0)]     # a < b
    tri2 = [(0.5, 0), (0.5, 0.5), (1.0, 0.5)]     # b < a (mirror)
    for t in (tri1, tri2):
        ax.add_patch(Polygon(t, closed=True, fc=LIGHT_GREEN, ec=GREEN, lw=1.2, zorder=2))
    ax.plot([0, 1], [0, 1], color=GREY, lw=0.8, ls="--", zorder=1)
    ax.plot([0.5, 0.5], [0, 1], color=GREY, lw=0.8, ls=":", zorder=1)
    ax.plot([0, 1], [0.5, 0.5], color=GREY, lw=0.8, ls=":", zorder=1)
    ax.text(0.2, 0.7, "a < b", color=GREEN, fontsize=9, ha="center")
    ax.text(0.78, 0.3, "b < a", color=GREEN, fontsize=9, ha="center")
    ticks = [0, 0.5, 1]
    labels = ["0", r"$\frac{1}{2}$", "1"]
    ax.set_xticks(ticks, labels)
    ax.set_yticks(ticks, labels)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_aspect("equal")
    ax.set_xlabel("first cut a"); ax.set_ylabel("second cut b")
    ax.set_title("pieces $a$, $|b-a|$, $1-b$ all $<\\frac{1}{2}$\narea $2\\cdot\\frac{1}{8}=\\frac{1}{4}$", fontsize=9.5)


# ---------- Card 42: expected longest piece of a broken stick ----------

@figure("f05_stick_max_tail", w=4.6, h=2.6)
def _(ax):
    t = np.linspace(0, 1, 600)
    P = 3 * (1 - t) ** 2 - 3 * np.clip(1 - 2 * t, 0, None) ** 2 + np.clip(1 - 3 * t, 0, None) ** 2
    area = np.sum((P[1:] + P[:-1]) / 2 * np.diff(t))
    assert abs(area - 11 / 18) < 1e-4, area
    ax.fill_between(t, 0, P, color=LIGHT_BLUE, lw=0, zorder=1)
    ax.plot(t, P, color=BLUE, lw=2.0, zorder=2)
    ax.axhline(1, color=GREY, lw=0.6, ls=":")
    ax.text(0.02, 0.2, r"$E[M]=\int_0^1 P(M>t)\,dt=\frac{11}{18}\approx 0.611$",
            ha="left", va="center", fontsize=9.5)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1.08)
    ax.set_xlabel(r"$t$"); ax.set_ylabel(r"$P(M>t)$")
    ax.set_title(r"$M$ = longest of 3 pieces; flat at 1 for $t\leq\frac{1}{3}$", fontsize=9.5)


# ---------- Card 74, 75, 76: nine uniform points, ten gaps ----------

@figure("f05_spacings_nine", w=5.0, h=2.0, axis=False)
def _(ax):
    rng = np.random.default_rng(3)
    pts = np.sort(rng.uniform(size=9))
    edges = np.concatenate([[0.0], pts, [1.0]])
    gaps = np.diff(edges)
    k = int(np.argmax(gaps))
    ax.add_patch(Rectangle((0, -0.2), 0.3, 0.4, fc=LIGHT_ORANGE, ec="none", zorder=1))
    ax.plot([0, 1], [0, 0], color=INK, lw=1.2, zorder=2)
    ax.plot(pts, np.zeros_like(pts), "o", color=BLUE, ms=5, zorder=3)
    for i, (a, b) in enumerate(zip(edges[:-1], edges[1:])):
        col = ORANGE if i == k else GREY
        ax.plot([a, b], [0.42, 0.42], color=col, lw=1.4 if i == k else 1.0)
        ax.plot([a, a], [0.36, 0.48], color=col, lw=1.0)
        ax.plot([b, b], [0.36, 0.48], color=col, lw=1.0)
    ax.text((edges[k] + edges[k + 1]) / 2, 0.55, f"largest gap {gaps[k]:.2f} (this draw)",
            color=ORANGE, fontsize=9, ha="center")
    ax.text(0.3, 0.26, r"$0.3$", ha="center", va="bottom", fontsize=9.5)
    ax.text(-0.03, -0.42, "shaded: no point here if the first gap exceeds 0.3", ha="left", va="top", fontsize=8.5, color=ORANGE)
    ax.text(0.5, -0.82, r"first gap $>0.3$: all 9 points beyond $0.3$, $P=0.7^{9}$", ha="center", va="center", fontsize=9.5)
    ax.text(0.5, -1.12, r"some gap $>\frac{1}{2}$: $P=10\cdot(\frac{1}{2})^{9}$", ha="center", va="center", fontsize=9.5)
    ax.set_xlim(-0.05, 1.05); ax.set_ylim(-1.3, 0.8)


# ---------- Card 22: five points, all in one semicircle ----------

def _find_half(n, seed):
    rng = np.random.default_rng(seed)
    while True:
        ang = rng.uniform(0, TWO_PI, n)
        for i in range(n):
            rel = np.delete((ang - ang[i]) % TWO_PI, i)
            if np.all(rel <= np.pi):
                return ang, i


def _draw_half(ax, n, seed):
    ang, ref = _find_half(n, seed)
    _circle(ax, 0.0)
    a0 = math.degrees(ang[ref])
    ax.add_patch(Wedge((0, 0), 1.0, a0, a0 + 180, fc=LIGHT_BLUE, ec="none", zorder=0.5))
    _circle(ax, 0.0)
    for i, a in enumerate(ang):
        x, y = _pt(0.0, math.degrees(a), 1.0)
        if i == ref:
            ax.plot(x, y, "o", color=ORANGE, ms=7, zorder=4)
        else:
            ax.plot(x, y, "o", color=BLUE, ms=6, zorder=4)
    x, y = _pt(0.0, a0, 1.3)
    ax.text(x, y, "reference", color=ORANGE, fontsize=9, ha="center", va="center")
    frame(ax, -1.45, 1.45, -1.45, 1.45)


@figure("f05_semicircle_ref", w=3.2, h=3.0, axis=False)
def _(ax):
    _draw_half(ax, 5, 1)
    ax.set_title(r"5 points: $5\cdot(\frac{1}{2})^{4}=\frac{5}{16}$", fontsize=10)


@figure("f05_semicircle_three", w=3.2, h=3.0, axis=False)
def _(ax):
    _draw_half(ax, 3, 2)
    ax.set_title(r"3 points: $3\cdot(\frac{1}{2})^{2}=\frac{3}{4}$", fontsize=10)


# ---------- Card 58: triangle on the rim contains the hub ----------

@figure("f05_hub_triangle", w=4.6, h=2.4, axis=False)
def _(ax):
    for cx, angs, fc, ec, lab in ((0.0, (90, 210, 330), LIGHT_GREEN, GREEN, "hub inside"),
                                  (3.0, (0, 60, 120), LIGHT_RED, RED, "all three in one half")):
        _circle(ax, cx)
        tri = [_pt(cx, a) for a in angs]
        ax.add_patch(Polygon(tri, closed=True, fc=fc, ec=ec, lw=1.4, zorder=2))
        ax.plot(cx, 0, "o", color=INK, ms=5, zorder=4)
        for p in tri:
            ax.plot(p[0], p[1], "o", color=INK, ms=4, zorder=4)
        ax.text(cx, -1.45, lab, ha="center", fontsize=9.5, color=ec)
    frame(ax, -1.3, 4.3, -1.9, 1.35)


# ---------- Card 49: arc of fraction f on the rim ----------

@figure("f05_arc_fraction", w=3.4, h=2.9, axis=False)
def _(ax):
    f = 1 / 3
    arc_deg = 360 * f
    ref = 90
    _circle(ax, 0.0)
    ax.add_patch(Wedge((0, 0), 1.0, ref, ref + arc_deg, fc=LIGHT_BLUE, ec="none", zorder=0.5))
    _circle(ax, 0.0)
    for a in (150, 200):
        x, y = _pt(0.0, a)
        ax.plot(x, y, "o", color=BLUE, ms=6, zorder=4)
    x, y = _pt(0.0, ref)
    ax.plot(x, y, "o", color=ORANGE, ms=7, zorder=4)
    ax.text(x + 0.1, y + 0.12, "reference", color=ORANGE, fontsize=9, ha="left")
    x, y = _pt(0.0, ref + arc_deg / 2, 0.55)
    ax.text(x, y, r"$\frac{1}{3}$ of rim", ha="center", va="center", fontsize=9.5)
    frame(ax, -1.3, 1.3, -1.45, 1.3)
    caption(ax, r"$P=n\,f^{\,n-1}=3\cdot(\frac{1}{3})^{2}=\frac{1}{3}$", fs=9.5)


# ---------- Card 4: needle of length 3d crossing two lines ----------

@figure("f05_buffon_long", w=4.6, h=2.7, axis=False)
def _(ax):
    d, l = 1.0, 3.0
    th = math.radians(60)
    cxn, cyn = 0.2, 0.4
    dx, dy = (l / 2) * math.cos(th), (l / 2) * math.sin(th)
    p1, p2 = (cxn - dx, cyn - dy), (cxn + dx, cyn + dy)
    crossings = [k for k in range(-2, 4) if min(p1[1], p2[1]) <= k * d <= max(p1[1], p2[1])]
    assert len(crossings) == 2, crossings
    for k in range(-2, 4):
        ax.plot([-2.2, 3.2], [k * d, k * d], color=GREY, lw=0.9, zorder=1)
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=BLUE, lw=2.2, zorder=3)
    for k in crossings:
        s = (k * d - cyn) / math.sin(th)
        ax.plot(cxn + s * math.cos(th), k * d, "o", color=ORANGE, ms=6, zorder=4)
    ax.text(3.25, 0.4, "lines\n$d=1$", fontsize=9, va="center", ha="left")
    ax.set_xlim(-2.4, 4.4); ax.set_ylim(-1.5, 2.3)
    ax.text(-2.3, -1.3, r"needle $3d$: 2 crossings here; $E=\frac{2\cdot 3d}{\pi d}=\frac{6}{\pi}\approx 1.91$",
            fontsize=9, ha="left", va="center")


# ---------- Card 25: needle of length d/2, crossing condition ----------

@figure("f05_buffon_geometry", w=4.2, h=2.6, axis=False)
def _(ax):
    d, l = 1.0, 0.5
    th = math.radians(60)
    cxn, cyn = 0.5, 0.2
    h = cyn  # distance to the line y=0
    a = (l / 2) * math.sin(th)
    assert h <= a  # this draw crosses
    for k in (0, 1):
        ax.plot([-0.3, 1.3], [k * d, k * d], color=GREY, lw=1.0, zorder=1)
    dx, dy = (l / 2) * math.cos(th), (l / 2) * math.sin(th)
    ax.plot([cxn - dx, cxn + dx], [cyn - dy, cyn + dy], color=BLUE, lw=2.4, zorder=3)
    ax.plot(cxn, cyn, "o", color=INK, ms=4, zorder=4)
    ax.plot([cxn, cxn], [0, cyn], color=ORANGE, lw=1.6, ls="--", zorder=2)
    ax.text(cxn + 0.05, cyn / 2, r"$h$", color=ORANGE, fontsize=10, va="center")
    ax.text(1.32, 0.5, "line", fontsize=9, va="center")
    ax.text(1.32, 1.0, "line", fontsize=9, va="center")
    ax.set_xlim(-0.35, 1.9); ax.set_ylim(-0.45, 1.35)
    ax.text(-0.3, 1.25, r"cross iff $h\leq\frac{l}{2}|\sin\theta|$", fontsize=9.5, ha="left", va="center")
    ax.text(-0.3, -0.33, r"$h\sim U[0,\frac{1}{2}]$: $P=E\left[\frac{l|\sin\theta|}{d}\right]=\frac{2l}{\pi d}=\frac{1}{\pi}$",
            fontsize=9, ha="left", va="center")


# ---------- Card 16, 28: superposition / which type comes next ----------

@figure("f05_race_chain", w=5.0, h=2.1, axis=False)
def _(ax):
    pA, pB = 2 / 5, 3 / 5
    S = [(0.0, 0.0), (2.2, 0.0), (4.4, 0.0)]
    for i, (x, y) in enumerate(S):
        node(ax, (x, y), str(i), r=0.3, fc=LIGHT_ORANGE if i == 2 else "white", ec=ORANGE if i == 2 else INK)
    arrow(ax, S[0], S[1], r"$A$  $\frac{2}{5}$", color=ORANGE, shrink=18)
    arrow(ax, S[1], S[2], r"$A$  $\frac{2}{5}$", color=ORANGE, shrink=18)
    for i, (x, y) in enumerate(S):
        col = ORANGE if i == 2 else GREY
        ax.annotate("", xy=(x, -1.05), xytext=(x, -0.33),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=1.4, mutation_scale=12))
        ax.text(x + 0.12, -0.7, r"$B$  $\frac{3}{5}$", color=col, fontsize=9.5, va="center")
        ax.text(x, -1.3, "B first", color=col, fontsize=9, ha="center", va="top")
    ax.text(0.0, 0.62, "start", fontsize=9, ha="center", color=GREY)
    ax.text(2.2, 0.62, "1 A so far", fontsize=9, ha="center", color=GREY)
    ax.text(4.4, 0.62, "2 A so far", fontsize=9, ha="center", color=GREY)
    ax.text(2.2, -2.0, r"exactly two $A$ then $B$: $P=\left(\frac{2}{5}\right)^{2}\frac{3}{5}=\frac{12}{125}$",
            fontsize=9.5, ha="center", va="center")
    ax.set_xlim(-0.5, 5.0); ax.set_ylim(-2.35, 0.95)


# ---------- Card 26: three racing clocks, rates 1, 2, 3 ----------

@figure("f05_race_rates", w=5.0, h=2.0, axis=False)
def _(ax):
    rates = [1, 2, 3]
    total = sum(rates)
    W = 5.0
    x = 0.0
    cols = [LIGHT_BLUE, LIGHT_BLUE, LIGHT_ORANGE]
    for r, c in zip(rates, cols):
        w = W * r / total
        ax.add_patch(Rectangle((x, 0), w, 0.7, fc=c, ec=INK, lw=1.0, zorder=2))
        ax.text(x + w / 2, 0.35, rf"rate {r}: $\frac{{{r}}}{{{total}}}$", ha="center", va="center", fontsize=9.5, zorder=3)
        x += w
    ax.text(W / 2, 1.05, r"clock $i$ rings first: $P=\frac{\lambda_i}{\lambda_1+\lambda_2+\lambda_3}$",
            ha="center", va="center", fontsize=9.5)
    ax.add_patch(Rectangle((0, -1.0), W, 0.5, fc=LIGHT_GREY, ec=INK, lw=0.8, zorder=2))
    ax.text(W / 2, -0.75, r"first ring: $\mathrm{Exp}(6)$, mean $\frac{1}{6}$ minute", ha="center", va="center", fontsize=9.5)
    ax.set_xlim(-0.2, W + 0.2); ax.set_ylim(-1.2, 1.4)


# ---------- Card 10 contrast: memoryless vs bounded uniform (cards 51, 67) ----------

@figure("f05_memoryless_contrast", w=5.0, h=2.7)
def _(ax):
    r = np.linspace(0, 10, 400)
    ax.plot(r, np.exp(-r / 5) / 5, color=BLUE, lw=2.0,
            label="exponential (mean 5), remaining wait after 3 min")
    ax.plot([0, 6], [1 / 6, 1 / 6], color=ORANGE, lw=2.0,
            label="uniform on [0,10], remaining wait after 4 min")
    ax.plot([6, 6], [0, 1 / 6], color=ORANGE, lw=1.0, ls=":")
    ax.plot(3, 1 / 6, "o", color=ORANGE, ms=5)
    ax.text(3.3, 1 / 6 + 0.012, r"mean $3$", color=ORANGE, fontsize=9.5)
    ax.set_xlim(0, 10); ax.set_ylim(0, 0.26)
    ax.set_xlabel("minutes still to wait, $r$"); ax.set_ylabel("density")
    ax.legend(loc="upper right", fontsize=8.5, frameon=False)


# ---------- Card 29: alternating headways 5 and 15 ----------

@figure("f05_bus_alternating", w=5.0, h=2.4, axis=False)
def _(ax):
    times = [0, 5, 20, 25, 40]
    ax.set_xlim(-2, 42); ax.set_ylim(-3.2, 1.0)
    waits = {}
    for a, b in zip(times[:-1], times[1:]):
        g = b - a
        col = LIGHT_ORANGE if g == 15 else LIGHT_GREY
        ax.add_patch(Rectangle((a, -0.4), g, 0.8, fc=col, ec="none", zorder=1))
        ax.text((a + b) / 2, -0.9, f"{g} min gap", ha="center", va="center", fontsize=9)
    ax.plot([0, 40], [0, 0], color=INK, lw=1.0, zorder=2)
    ax.plot(times, np.zeros(len(times)), "o", color=BLUE, ms=6, zorder=4)
    ax.text(0, 0.45, "bus", fontsize=9, ha="center", color=BLUE)
    # expected wait given landing in a gap of length g is g/2; long gaps are hit more often
    p15 = 15 * 2 / 40
    e_wait = p15 * (15 / 2) + (1 - p15) * (5 / 2)
    assert abs(e_wait - 6.25) < 1e-9
    ax.text(-1.5, -1.95, r"land in a 15-min gap with prob. $\frac{3}{4}$: mean wait $7.5$",
            fontsize=9.5, ha="left", va="center")
    ax.text(-1.5, -2.5, r"land in a 5-min gap with prob. $\frac{1}{4}$: mean wait $2.5$",
            fontsize=9.5, ha="left", va="center")
    ax.text(-1.5, -3.05, r"$E[\mathrm{wait}]=\frac{3}{4}\cdot 7.5+\frac{1}{4}\cdot 2.5=6.25$ (regular 10-min route: 5)",
            fontsize=9.5, ha="left", va="center")


# ---------- Card 15, 50: Poisson buses, length-biased gap ----------

@figure("f05_inspection_density", w=4.8, h=2.6)
def _(ax):
    x = np.linspace(0, 50, 500)
    f = np.exp(-x / 10) / 10            # headway density, mean 10
    g = x * f / 10                      # density of the gap you land in (length-biased)
    xx = np.linspace(0, 200, 20001)
    gg = xx * np.exp(-xx / 10) / 100
    assert abs(np.sum((gg[1:] + gg[:-1]) / 2 * np.diff(xx)) - 1) < 1e-4
    ax.plot(x, f, color=BLUE, lw=2.0, label=r"headway $X$ (mean $10$)")
    ax.plot(x, g, color=ORANGE, lw=2.0, label=r"gap you land in (mean $20$)")
    ax.axvline(10, color=BLUE, lw=0.9, ls=":")
    ax.axvline(20, color=ORANGE, lw=0.9, ls=":")
    ax.set_xlim(0, 50); ax.set_ylim(0, 0.105)
    ax.set_xlabel("gap length (min)"); ax.set_ylabel("density")
    ax.legend(loc="upper right", fontsize=9, frameon=False)
    ax.set_title(r"landed gap: mean $20$; wait is half of it: mean $10$", fontsize=9.5)


# ---------- Card 27, 61: exponential failure times, stages with rates 3, 2, 1 ----------

@figure("f05_failure_timeline", w=5.0, h=2.3, axis=False)
def _(ax):
    t1 = 1 / 3
    t2 = t1 + 1 / 2
    t3 = t2 + 1
    ax.set_xlim(-0.12, 2.18); ax.set_ylim(-1.55, 1.45)
    stages = [(0, t1, LIGHT_BLUE, 3, "E = 1/3"), (t1, t2, LIGHT_GREY, 2, "E = 1/2"), (t2, t3, LIGHT_BLUE, 1, "E = 1")]
    for a, b, c, n, lab in stages:
        ax.add_patch(Rectangle((a, -0.32), b - a, 0.64, fc=c, ec=INK, lw=0.8, zorder=1))
        ax.text((a + b) / 2, 0.0, lab, ha="center", va="center", fontsize=8.5, zorder=3)
        ax.text((a + b) / 2, -0.5, f"{n} alive\nrate {n}", ha="center", va="top", fontsize=8.5)
    ax.plot([0, t3], [0, 0], color=INK, lw=0.8, zorder=0)
    for t, lab, col in ((t1, r"1st $\frac{1}{3}$", BLUE), (t2, r"2nd $\frac{5}{6}$", ORANGE), (t3, r"3rd $\frac{11}{6}$", GREEN)):
        ax.plot(t, 0.32, "v", color=col, ms=7, zorder=4)
        ax.text(t, 0.62, lab, ha="center", va="bottom", fontsize=9, color=col)
    ax.text(0.0, 1.2, "expected failure times (minutes)", fontsize=9, color=GREY, ha="left")


# ---------- Card 6, 30: tail-sum formula for the running-sum stopping time ----------

@figure("f05_tail_sum_bars", w=4.8, h=2.5)
def _(ax):
    from math import factorial
    tail = {n: 1 / factorial(n) for n in range(0, 7)}
    tail[1] = 1.0  # P(U_1 <= 1) = 1
    pmf = {n: tail[n - 1] - tail[n] for n in range(2, 7)}
    assert abs(pmf[3] - 1 / 3) < 1e-12
    ns = list(pmf)
    cols = [ORANGE if n == 3 else BLUE for n in ns]
    ax.bar(ns, [pmf[n] for n in ns], color=cols, width=0.55, zorder=2)
    for n in ns:
        lab = r"$\frac{1}{3}$" if n == 3 else ""
        if lab:
            ax.text(n, pmf[n] + 0.02, lab, ha="center", va="bottom", fontsize=10, color=ORANGE)
    xs = list(range(0, 7))
    ax.plot(xs, [tail[n] for n in xs], "o--", color=GREY, ms=4, lw=0.9, zorder=3)
    ax.text(0.5, 0.8, r"dots: $P(N>n)=\frac{1}{n!}$", fontsize=9, color=GREY, transform=ax.transAxes)
    ax.set_xticks(xs)
    ax.set_xlim(-0.5, 6.5); ax.set_ylim(0, 1.12)
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_xlabel("$n$"); ax.set_ylabel("probability")
    ax.set_title(r"bars: $P(N=n)$; $E[N]=e$", fontsize=9.5)


# ---------- Card 37, 63: exponential shares are uniform ----------

@figure("f05_exp_share_wedge", w=4.2, h=3.0)
def _(ax):
    rng = np.random.default_rng(11)
    X = rng.exponential(1.0, 400)
    Y = rng.exponential(1.0, 400)
    share = X / (X + Y)
    frac = np.mean(share <= 0.25)
    ax.fill([0, 0, 5 / 3], [0, 5, 5], color=LIGHT_ORANGE, lw=0, zorder=0)
    ax.plot([0, 5 / 3], [0, 5], color=ORANGE, lw=1.2, zorder=1)
    ev = share <= 0.25
    ax.scatter(X[~ev], Y[~ev], s=8, color=GREY, zorder=2)
    ax.scatter(X[ev], Y[ev], s=8, color=ORANGE, zorder=3)
    ax.set_xlim(0, 5); ax.set_ylim(0, 5)
    ax.set_xlabel("$X$"); ax.set_ylabel("$Y$")
    ax.set_title(rf"$\frac{{X}}{{X+Y}}\leq\frac{{1}}{{4}}$ iff $Y\geq 3X$; $P=\frac{{1}}{{4}}$" + f"\n(400 draws, shown {frac:.3f})", fontsize=9.5)
    print("exp share fraction in event:", frac)


# ---------- Card 38: product of two uniforms ----------

@figure("f05_product_hyperbola", w=3.6, h=3.1)
def _(ax):
    u = np.linspace(1e-4, 1, 1000)
    ax.fill_between(u, 0, np.minimum(1, 0.25 / u), color=LIGHT_BLUE, lw=0, zorder=1)
    ax.plot(u[u >= 0.25], 0.25 / u[u >= 0.25], color=ORANGE, lw=1.6, zorder=2)
    ax.text(0.62, 0.18, r"$UV\leq\frac{1}{4}$", color=BLUE, fontsize=10, ha="center")
    ax.text(0.42, 0.85, r"$UV>\frac{1}{4}$", color=INK, fontsize=10, ha="center")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_aspect("equal")
    ax.set_xlabel("$U$"); ax.set_ylabel("$V$")
    ax.set_title(r"$P(UV\leq\frac{1}{4})=\frac{1+\ln 4}{4}\approx 0.597$", fontsize=10)


# ---------- Card 11, 36: ratio of two normals is a tangent of a uniform angle ----------

@figure("f05_ratio_wedges", w=5.0, h=2.5, axis=False)
def _(ax):
    # X/Y = cot(theta) for (X,Y) = (cos theta, sin theta)
    for cx, wedges, title in (
        (0.0, [(45, 135), (225, 315)], r"$|X/Y|\leq 1$: $\frac{1}{2}$"),
        (3.0, [(-30, 30), (150, 210)], r"$|X/Y|>\sqrt{3}$: $\frac{1}{3}$"),
    ):
        for a0, a1 in wedges:
            ax.add_patch(Wedge((cx, 0), 1.0, a0, a1, fc=LIGHT_ORANGE, ec="none", zorder=1))
        _circle(ax, cx)
        ax.plot([cx - 1.2, cx + 1.2], [0, 0], color=GREY, lw=0.8, zorder=0)
        ax.plot([cx, cx], [-1.2, 1.2], color=GREY, lw=0.8, zorder=0)
        ax.text(cx, -1.45, title, ha="center", fontsize=9.5)
    ax.text(1.25, -0.12, "X", fontsize=9, color=GREY)
    ax.text(0.04, 1.2, "Y", fontsize=9, color=GREY)
    frame(ax, -1.4, 4.4, -1.7, 1.4)


# ---------- Card 8, 33: correlated normals, sign events ----------

@figure("f05_normal_orthant", w=3.8, h=3.0)
def _(ax):
    rng = np.random.default_rng(5)
    Z = rng.multivariate_normal([0, 0], [[1, 0.5], [0.5, 1]], size=600)
    same = Z[:, 0] * Z[:, 1] > 0
    ax.scatter(Z[~same, 0], Z[~same, 1], s=7, color=GREY, zorder=2)
    ax.scatter(Z[same, 0], Z[same, 1], s=7, color=BLUE, zorder=3)
    ax.axhline(0, color=INK, lw=0.6); ax.axvline(0, color=INK, lw=0.6)
    ax.set_xlim(-3.5, 3.5); ax.set_ylim(-3.5, 3.5); ax.set_aspect("equal")
    ax.set_xlabel("$X$"); ax.set_ylabel("$Y$")
    ax.set_title(r"$\rho=\frac{1}{2}$: $P(XY>0)=\frac{2}{3}$, $P(X>0,Y>0)=\frac{1}{3}$", fontsize=9.5)
    print("orthant fractions:", np.mean(same), np.mean((Z[:, 0] > 0) & (Z[:, 1] > 0)))


# ---------- Card 35, 62: conditional normal N(1/2, 1/2) ----------

@figure("f05_cond_normal_tail", w=4.6, h=2.5)
def _(ax):
    mu, sd = 0.5, math.sqrt(0.5)
    x = np.linspace(-2.5, 3.5, 500)
    pdf = np.array([_phi((v - mu) / sd) / sd for v in x])
    tail = 1 - _Phi((1 - mu) / sd)
    ax.plot(x, pdf, color=BLUE, lw=2.0)
    m = x > 1
    ax.fill_between(x[m], 0, pdf[m], color=LIGHT_ORANGE, lw=0, zorder=1)
    ax.axvline(mu, color=BLUE, lw=0.9, ls=":")
    ax.text(mu, 0.66, r"mean $\frac{1}{2}$", color=BLUE, fontsize=9.5, ha="center")
    ax.text(1.9, 0.12, rf"$P(X>1)={tail:.4f}$", color=ORANGE, fontsize=9.5)
    ax.set_xlim(-2.5, 3.5); ax.set_ylim(0, 0.9)
    ax.set_xlabel("$x$"); ax.set_ylabel("density")
    ax.set_title(r"$X\mid X+Y=1\sim N\left(\frac{1}{2},\frac{1}{2}\right)$", fontsize=10)
    print("P(X>1 | sum=1) =", round(tail, 6))


# ---------- Card 17, 47: density 2x on [0,1] ----------

@figure("f05_density_2x", w=4.6, h=2.6)
def _(ax):
    x = np.linspace(0, 1, 300)
    f = 2 * x
    s = (1 - x ** 2) ** 2
    ax.fill_between(x, 0, f, color=LIGHT_BLUE, lw=0, zorder=1)
    ax.plot(x, f, color=BLUE, lw=2.0, label=r"density $f(x)=2x$")
    ax.plot(x, s, color=ORANGE, lw=2.0, label=r"$P(\min>x)=(1-x^{2})^{2}$")
    ax.axvline(2 / 3, color=BLUE, lw=0.9, ls=":")
    ax.text(2 / 3 + 0.02, 1.85, r"$E=\frac{2}{3}$", color=BLUE, fontsize=9.5)
    ax.set_xlim(0, 1); ax.set_ylim(0, 2.1)
    ax.set_xlabel("$x$")
    ax.legend(loc="upper left", fontsize=9, frameon=False)
    ax.set_title(r"$E[\min]=\int_0^1(1-x^2)^2dx=\frac{8}{15}$", fontsize=9.5)


# ---------- Card 0: expected order statistics sit at k/(n+1) ----------

@figure("f05_uniform_ladder", w=5.0, h=1.7, axis=False)
def _(ax):
    n = 7
    ax.plot([0, 1], [0, 0], color=INK, lw=1.2, zorder=1)
    for k in range(1, n + 1):
        x = k / (n + 1)
        col = ORANGE if k == 3 else GREY
        ax.plot(x, 0, "o", color=col, ms=6 if k == 3 else 4.5, zorder=3)
        ax.text(x, -0.22, rf"$\frac{{{k}}}{{{n + 1}}}$", ha="center", va="top", fontsize=9,
                color=col)
    ax.text(3 / 8, 0.35, r"$E[U_{(3)}]=\frac{3}{8}$", ha="center", va="bottom", fontsize=10, color=ORANGE)
    ax.text(0.5, 0.95, "7 iid uniforms: the k-th sorted value sits at k/8 on average", ha="center", fontsize=9, color=GREY)
    ax.set_xlim(-0.05, 1.05); ax.set_ylim(-0.65, 1.2)
