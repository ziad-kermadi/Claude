"""Figures for cards/00_toolkit.json."""
import itertools
import math
import numpy as np
from qcfig import *


def fit(ax, xmin, xmax, ymid, w, h):
    """Limits that keep the figure's w:h proportions with equal aspect (for node/circle figures)."""
    yr = (xmax - xmin) * h / w
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymid - yr / 2, ymid + yr / 2)
    ax.set_aspect("equal")


def tag(ax, xy, s, color=INK, fs=10, ha="center", va="center"):
    ax.text(xy[0], xy[1], s, color=color, fontsize=fs, ha=ha, va=va, zorder=6,
            bbox=dict(fc="white", ec="none", pad=0.8))


def bar_box(ax, xy, s, w, h, fc="white", ec=INK, fs=9.5):
    x, y = xy
    ax.add_patch(Rectangle((x - w / 2, y - h / 2), w, h, fc=fc, ec=ec, lw=1.1, zorder=3))
    ax.text(x, y, s, ha="center", va="center", fontsize=fs, zorder=4)


def line(ax, a, b, color=INK, lw=1.1):
    ax.plot([a[0], b[0]], [a[1], b[1]], color=color, lw=lw, zorder=2)


# ---------------------------------------------------------------- card 3: first-step conditioning
@figure("f00_first_step_walk", w=5.0, h=2.0, axis=False)
def _(ax):
    h = [k / 4 for k in range(5)]  # h_k = k/4 solves h_k = (h_{k-1}+h_{k+1})/2, h_0=0, h_4=1
    assert all(abs(h[k] - (h[k - 1] + h[k + 1]) / 2) < 1e-12 for k in range(1, 4))
    X = [1.2 * k for k in range(5)]
    for k in range(4):
        arrow(ax, (X[k], 0), (X[k + 1], 0), rad=0.45, color=BLUE, shrink=16)
        arrow(ax, (X[k + 1], 0), (X[k], 0), rad=0.45, color=RED, shrink=16)
        tag(ax, ((X[k] + X[k + 1]) / 2, 0.5), r"$\frac{1}{2}$", color=BLUE)
        tag(ax, ((X[k] + X[k + 1]) / 2, -0.5), r"$\frac{1}{2}$", color=RED)
    labels = [r"$h_0=0$", r"$h_1=\frac{1}{4}$", r"$h_2=\frac{1}{2}$", r"$h_3=\frac{3}{4}$", r"$h_4=1$"]
    for k in range(5):
        fc, ec = "white", INK
        if k == 0:
            fc, ec = LIGHT_RED, RED
        if k == 4:
            fc, ec = LIGHT_GREEN, GREEN
        if k == 1:
            ec = ORANGE
        node(ax, (X[k], 0), str(k), fc=fc, ec=ec)
        tag(ax, (X[k], -0.8), labels[k], fs=9.5)
    fit(ax, -0.8, 5.6, -0.1, 5.0, 2.0)
    caption(ax, r"$h_k=\frac{1}{2}(h_{k-1}+h_{k+1})$ for $k=1,2,3$", fs=9.5)


# ---------------------------------------------------------------- card 5: Markov chain
@figure("f00_two_state_chain", w=4.2, h=2.2, axis=False)
def _(ax):
    P = np.array([[0.7, 0.3], [0.1, 0.9]])
    A = np.vstack([P.T - np.eye(2), np.ones(2)])
    pi = np.linalg.lstsq(A, np.array([0.0, 0.0, 1.0]), rcond=None)[0]
    assert np.allclose(pi, [0.25, 0.75])
    X = [0.0, 2.6]
    arrow(ax, (X[0], 0), (X[1], 0), rad=0.35, color=ORANGE, shrink=22)
    arrow(ax, (X[1], 0), (X[0], 0), rad=0.35, color=RED, shrink=22)
    tag(ax, (1.3, -0.62), "0.3", color=ORANGE)
    tag(ax, (1.3, 0.62), "0.1", color=RED)
    self_loop(ax, (X[0], 0), "0.7", r=0.45, color=INK)
    self_loop(ax, (X[1], 0), "0.9", r=0.45, color=INK)
    for k, s in enumerate([r"$\pi_0=\frac{1}{4}$", r"$\pi_1=\frac{3}{4}$"]):
        node(ax, (X[k], 0), str(k), r=0.42, fc=LIGHT_ORANGE if k == 0 else "white", ec=INK)
        tag(ax, (X[k], -0.95), s, fs=9.5)
    fit(ax, -1.0, 3.6, 0.0, 4.2, 2.2)
    caption(ax, r"$\pi_0\cdot 0.3=\pi_1\cdot 0.1$, $\pi_0+\pi_1=1$", fs=9.5)


# ---------------------------------------------------------------- cards 8, 48: stars and bars
@figure("f00_stars_bars", w=5.0, h=1.8, axis=False)
def _(ax):
    n, k = 10, 3
    assert math.comb(n + k - 1, k - 1) == 66
    seq = "***" + "|" + "****" + "|" + "***"  # x=3, y=4, z=3: 10 stars, 2 bars, 12 slots
    assert seq.count("*") == n and seq.count("|") == k - 1
    for i, ch in enumerate(seq):
        if ch == "*":
            ax.plot(i, 0, "o", color=INK, ms=7, zorder=4)
        else:
            ax.plot([i, i], [-0.36, 0.36], color=ORANGE, lw=2.6, zorder=4)
    tag(ax, (1, 0.85), "$x=3$", fs=10)
    tag(ax, (5.5, 0.85), "$y=4$", fs=10)
    tag(ax, (10, 0.85), "$z=3$", fs=10)
    fit(ax, -0.8, 11.8, 0.1, 5.0, 1.8)
    caption(ax, r"$x+y+z=10$: place 2 bars in 12 slots, $\binom{12}{2}=66$ solutions", fs=9.5)


# ---------------------------------------------------------------- card 9: inclusion-exclusion
@figure("f00_ie_venn", w=4.8, h=3.2, axis=False)
def _(ax):
    cnt = {}
    for n in range(1, 101):
        key = (n % 2 == 0, n % 3 == 0, n % 5 == 0)
        cnt[key] = cnt.get(key, 0) + 1
    union = sum(v for k, v in cnt.items() if any(k))
    assert union == 50 + 33 + 20 - 16 - 10 - 6 + 3 == 74
    C = {"2": (-0.6, 0.35), "3": (0.6, 0.35), "5": (0.0, -0.45)}
    for name, col in [("2", BLUE), ("3", ORANGE), ("5", GREY)]:
        ax.add_patch(Circle(C[name], 1.0, fc=col, ec="none", alpha=0.15, zorder=1))
        ax.add_patch(Circle(C[name], 1.0, fc="none", ec=col, lw=1.4, zorder=2))
    pos = {(True, False, False): (-1.2, 0.55), (False, True, False): (1.2, 0.55),
           (False, False, True): (0.0, -1.2), (True, True, False): (0.0, 0.95),
           (True, False, True): (-0.9, -0.45), (False, True, True): (0.9, -0.45),
           (True, True, True): (0.0, 0.05)}
    for key, xy in pos.items():
        tag(ax, xy, str(cnt[key]), fs=11)
    tag(ax, (-1.9, 1.35), "$A_2$", color=BLUE, fs=11)
    tag(ax, (1.9, 1.35), "$A_3$", color=ORANGE, fs=11)
    tag(ax, (1.55, -1.25), "$A_5$", color=GREY, fs=11)
    tag(ax, (-1.9, -1.2), f"none: {100 - union}", fs=10)
    fit(ax, -2.45, 2.45, -0.2, 4.8, 3.2)
    caption(ax, r"$|A_2\cup A_3\cup A_5|=50+33+20-16-10-6+3=74$", fs=9.5)


# ---------------------------------------------------------------- card 10, 69: Bayes
@figure("f00_bayes_tree", w=5.0, h=2.8, axis=False)
def _(ax):
    p, sens, fpr = 0.01, 0.95, 0.05
    dp, dn = p * sens, p * (1 - sens)
    hp, hn = (1 - p) * fpr, (1 - p) * (1 - fpr)
    assert abs(dp / (dp + hp) - 19 / 118) < 1e-12
    # (x, y, label, width)
    root = (0.2, 0.0, "all", 0.9)
    d = (1.7, 0.8, "disease 1%", 1.3)
    hl = (1.7, -0.8, "healthy 99%", 1.3)
    dpos = (3.3, 1.2, "test +", 0.8)
    dneg = (3.3, 0.4, "test -", 0.8)
    hpos = (3.3, -0.4, "test +", 0.8)
    hneg = (3.3, -1.2, "test -", 0.8)
    leaves = [(4.7, 1.2, f"{dp:.4f}", True), (4.7, 0.4, f"{dn:.4f}", False),
              (4.7, -0.4, f"{hp:.4f}", True), (4.7, -1.2, f"{hn:.4f}", False)]
    def edge(a, b, s):
        line(ax, (a[0] + a[3] / 2, a[1]), (b[0] - b[3] / 2, b[1]))
        tag(ax, ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + 0.16), s, fs=8.5, color=GREY)
    for b, s in [(d, "1%"), (hl, "99%")]:
        edge(root, b, s)
    for par, kids in [(d, [("95%", dpos), ("5%", dneg)]), (hl, [("5%", hpos), ("95%", hneg)])]:
        for s, c in kids:
            edge(par, c, s)
    for x, y, s, w in [root, d, hl]:
        bar_box(ax, (x, y), s, w, 0.42)
    for x, y, s, w in [dpos, dneg, hpos, hneg]:
        bar_box(ax, (x, y), s, w, 0.36)
    for x, y, s, pos in leaves:
        bar_box(ax, (x, y), s, 0.95, 0.36, fc=LIGHT_ORANGE if pos else "white",
                ec=ORANGE if pos else INK, fs=9.5)
    tag(ax, (4.7, 1.62), "joint", fs=8.5, color=GREY)
    fit(ax, -0.5, 5.3, 0.0, 5.0, 2.8)
    caption(ax, r"$P(D\mid +)=\frac{0.0095}{0.0095+0.0495}=\frac{19}{118}\approx0.161$", fs=9.5)


# ---------------------------------------------------------------- card 12: parity and colouring
@figure("f00_coloring_board", w=4.6, h=3.0, axis=False)
def _(ax):
    sq = 0.85
    even_total = odd_total = 0
    for i in range(8):
        for j in range(8):
            even = (i + j) % 2 == 0
            removed = (i, j) in [(0, 0), (7, 7)]
            if even and not removed:
                even_total += 1
            if not even:
                odd_total += 1
            fc = LIGHT_BLUE if even else "white"
            ax.add_patch(Rectangle((i * sq, j * sq), sq, sq, fc=fc, ec=GREY, lw=0.6, zorder=2))
            if removed:
                ax.add_patch(Rectangle((i * sq, j * sq), sq, sq, fc="white", ec=RED, lw=1.4, zorder=3))
                x0, y0 = i * sq, j * sq
                ax.plot([x0 + 0.15, x0 + sq - 0.15], [y0 + 0.15, y0 + sq - 0.15], color=RED, lw=1.6, zorder=4)
                ax.plot([x0 + 0.15, x0 + sq - 0.15], [y0 + sq - 0.15, y0 + 0.15], color=RED, lw=1.6, zorder=4)
    assert (even_total, odd_total) == (30, 32)
    tag(ax, (7.2, 5.6), r"blue (even) squares", ha="left", fs=9.5, color=INK)
    tag(ax, (7.2, 5.1), r"$32-2=30$ left", ha="left", fs=9.5, color=INK)
    tag(ax, (7.2, 3.9), r"white (odd) squares", ha="left", fs=9.5, color=INK)
    tag(ax, (7.2, 3.4), r"$32$", ha="left", fs=9.5, color=INK)
    tag(ax, (7.2, 2.2), "each domino covers", ha="left", fs=9.5, color=INK)
    tag(ax, (7.2, 1.7), "one of each: no tiling", ha="left", fs=9.5, color=INK)
    fit(ax, -0.4, 11.0, 3.4, 4.6, 3.0)


# ---------------------------------------------------------------- cards 14, 59: pigeonhole
@figure("f00_pigeonhole_pairs", w=5.0, h=2.4, axis=False)
def _(ax):
    chosen = [1, 3, 4, 6, 7]
    pairs = [(1, 8), (2, 7), (3, 6), (4, 5)]
    per_box = {p: sum(1 for c in chosen if c in p) for p in pairs}
    assert sum(per_box.values()) == len(chosen) and max(per_box.values()) == 2
    X = lambda n: float(n - 1)
    t = np.linspace(0, np.pi, 80)
    for a, b in pairs:
        r = (X(b) - X(a)) / 2
        c = (X(a) + X(b)) / 2
        col = ORANGE if per_box[(a, b)] == 2 else GREY
        ax.plot(c + r * np.cos(t), 0.42 * r * np.sin(t), color=col, lw=1.6 if col == ORANGE else 1.1, zorder=1)
        tag(ax, (c, 0.42 * r + 0.2), f"{{{a},{b}}}", color=col, fs=9)
    for n in range(1, 9):
        ch = n in chosen
        ax.add_patch(Circle((X(n), 0), 0.3, fc=LIGHT_BLUE if ch else "white", ec=BLUE if ch else GREY,
                            lw=1.3, zorder=3))
        ax.text(X(n), 0, str(n), ha="center", va="center", fontsize=10, zorder=4)
    fit(ax, -0.8, 7.8, 1.1, 5.0, 2.4)
    caption(ax, r"5 numbers, 4 boxes: $\{3,6\}$ holds two, and $3+6=9$", fs=9.5)


# ---------------------------------------------------------------- card 15: backward induction
@figure("f00_pile_game", w=5.0, h=2.2, axis=False)
def _(ax):
    losing = lambda n: n % 3 == 0  # mover loses at multiples of 3 (take 1 or 2)
    assert losing(0) and losing(9) and not losing(10)
    for n in range(11):
        if n == 10:
            fc, ec, lab = LIGHT_ORANGE, ORANGE, "W"
        elif losing(n):
            fc, ec, lab = LIGHT_RED, RED, "L"
        else:
            fc, ec, lab = LIGHT_BLUE, BLUE, "W"
        node(ax, (n, 0), str(n), r=0.3, fc=fc, ec=ec, fs=10)
        tag(ax, (n, -0.85), lab, color=ec, fs=9.5)
    arrow(ax, (10, 0), (9, 0), rad=0.9, color=ORANGE, shrink=9)
    arrow(ax, (10, 0), (8, 0), rad=1.6, color=GREY, shrink=9)
    tag(ax, (9.75, 0.75), "take 1", color=ORANGE, fs=9)
    tag(ax, (8.6, 1.75), "take 2", color=GREY, fs=9)
    fit(ax, -0.8, 10.8, 0.9, 5.0, 2.2)
    caption(ax, "stones left; W = mover wins, L = mover loses", fs=9.5)


# ---------------------------------------------------------------- cards 18, 50: reflection principle
@figure("f00_reflection", w=5.0, h=2.6, axis=True)
def _(ax):
    rng = np.random.default_rng(5)
    S = np.concatenate([[0], np.cumsum(rng.choice([-1, 1], size=10))])
    tau = int(np.where(S == 3)[0][0])
    assert tau < 10 and S[-1] == 2 and S[:tau].max() < 3
    P =(sum(math.comb(10, h) for h in range(11) if 2 * h - 10 >= 3)
         + sum(math.comb(10, h) for h in range(11) if 2 * h - 10 > 3)) / 1024
    assert abs(P - 11 / 32) < 1e-12
    n = np.arange(11)
    ax.axhline(3, color=ORANGE, ls="--", lw=1.1)
    ax.text(0.15, 3.3, "a = 3", color=ORANGE, va="bottom", fontsize=9)
    ax.plot(n, S, "o-", color=BLUE, ms=3.5, lw=1.6, zorder=3)
    ax.plot(n[tau:], 6 - S[tau:], "o--", color=GREY, ms=3, lw=1.3, zorder=2)
    ax.plot(tau, 3, "o", color=ORANGE, ms=6, zorder=4)
    ax.annotate("first hit", (tau, 3), xytext=(tau - 3.2, 4.6), fontsize=9, color=ORANGE,
                arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.8))
    ax.text(10.1, S[-1], f"$S_{{10}}={S[-1]}$", color=BLUE, va="center", fontsize=9)
    ax.text(10.1, 6 - S[-1], f"$6-S_{{10}}={6 - S[-1]}$", color=GREY, va="center", fontsize=9)
    ax.set_xlim(-0.3, 12.3)
    ax.set_ylim(-3.5, 6.2)
    ax.set_xticks([0, 2, 4, 6, 8, 10])
    ax.set_yticks([-2, 0, 2, 4])
    ax.set_xlabel("step $n$")
    ax.set_ylabel("$S_n$")
    ax.set_title(r"after the first hit, reflect: $S'_n=6-S_n$", fontsize=10)


# ---------------------------------------------------------------- card 19: geometric probability
@figure("f00_square_gap", w=4.4, h=3.0, axis=False)
def _(ax):
    band = [(0, 0), (0.5, 0), (1, 0.5), (1, 1), (0.5, 1), (0, 0.5)]
    ax.add_patch(Polygon(band, closed=True, fc=LIGHT_BLUE, ec=BLUE, lw=1.2, zorder=2))
    for tri in ([(0, 0.5), (0, 1), (0.5, 1)], [(0.5, 0), (1, 0), (1, 0.5)]):
        ax.add_patch(Polygon(tri, closed=True, fc=LIGHT_RED, ec=RED, lw=1.0, zorder=2))
    ax.add_patch(Rectangle((0, 0), 1, 1, fc="none", ec=INK, lw=1.0, zorder=3))
    tag(ax, (0.5, 0.5), r"$|X-Y|<\frac{1}{2}$", fs=10)
    tag(ax, (0.15, 0.85), r"$\frac{1}{8}$", color=RED, fs=10)
    tag(ax, (0.85, 0.15), r"$\frac{1}{8}$", color=RED, fs=10)
    tag(ax, (0.5, -0.12), "X", fs=10)
    tag(ax, (-0.14, 0.5), "Y", fs=10)
    tag(ax, (1.6, 0.5), "uniform on", ha="left", fs=9.5, color=GREY)
    tag(ax, (1.6, 0.3), "the unit square", ha="left", fs=9.5, color=GREY)
    tag(ax, (1.6, 0.85), r"$P=1-2\cdot\frac{1}{8}=\frac{3}{4}$", ha="left", fs=9.5)
    fit(ax, -0.35, 2.35, 0.5, 4.4, 3.0)


# ---------------------------------------------------------------- card 52: Bertrand chord
@figure("f00_chord_sqrt3", w=4.4, h=3.0, axis=False)
def _(ax):
    ax.add_patch(Circle((0, 0), 1.0, fc="none", ec=INK, lw=1.2, zorder=2))
    V = [(math.cos(math.radians(a)), math.sin(math.radians(a))) for a in (90, 210, 330)]
    ax.add_patch(Polygon(V, closed=True, fc="none", ec=GREY, ls="--", lw=1.0, zorder=2))
    t = np.linspace(math.radians(210), math.radians(330), 100)
    ax.plot(np.cos(t), np.sin(t), color=ORANGE, lw=3.2, zorder=3)
    A = V[0]
    ax.plot(*A, "o", color=BLUE, ms=6, zorder=4)
    tag(ax, (A[0] + 0.22, A[1] + 0.05), "$A$", color=BLUE, fs=10)
    ax.plot([A[0], 0.5], [A[1], -math.sqrt(3) / 2], color=BLUE, lw=0.9, ls=":", zorder=2)
    tag(ax, (0.0, -1.32), "arc of 120 degrees", color=ORANGE, fs=9)
    tag(ax, (1.42, 0.45), "$B$ here:", ha="left", fs=9.5)
    tag(ax, (1.42, 0.05), r"chord $>\sqrt{3}$", ha="left", fs=9.5)
    tag(ax, (1.42, -0.35), r"probability $\frac{1}{3}$", ha="left", fs=9.5)
    fit(ax, -1.6, 2.2, -0.1, 4.4, 3.0)


# ---------------------------------------------------------------- card 53: order statistics
@figure("f00_spacings", w=5.0, h=1.9, axis=False)
def _(ax):
    rng = np.random.default_rng(3)
    u = np.sort(rng.uniform(0, 1, 4))
    ax.plot([-0.02, 1.02], [0, 0], color=INK, lw=1.2, zorder=2)
    for k in range(1, 5):
        ax.plot(k / 5, 0.0, "o", mfc="white", mec=ORANGE, ms=9, mew=1.6, zorder=3)
        tag(ax, (k / 5, 0.3), rf"$\frac{{{k}}}{{5}}$", color=ORANGE, fs=9.5)
    for k, x in enumerate(u, 1):
        ax.plot(x, -0.42, "o", color=BLUE, ms=6, zorder=4)
        tag(ax, (x, -0.75), rf"$U_{{({k})}}$", color=BLUE, fs=9)
    tag(ax, (1.0, -0.95), "", fs=9)
    ax.set_xlim(-0.08, 1.08)
    ax.set_ylim(-1.1, 0.85)
    ax.set_axis_off()
    ax.set_title(r"sorted draws $U_{(k)}$ (blue) against $E[U_{(k)}]=\frac{k}{n+1}$ (orange); "
                 r"$E[\max]=\frac{4}{5}$", fontsize=9.5, pad=2)


# ---------------------------------------------------------------- card 56: race of exponentials
@figure("f00_race_rates", w=5.0, h=1.8, axis=False)
def _(ax):
    rates = [1, 2, 3]
    tot = sum(rates)
    assert tot == 6 and abs(rates[0] / tot - 1 / 6) < 1e-12
    x = 0.0
    styles = [(LIGHT_ORANGE, ORANGE), (LIGHT_BLUE, BLUE), ("white", GREY)]
    for i, (r, (fc, ec)) in enumerate(zip(rates, styles), 1):
        ax.add_patch(Rectangle((x, -0.3), r, 0.6, fc=fc, ec=ec, lw=1.3, zorder=2))
        tag(ax, (x + r / 2, 0.0), f"rate {r}", fs=9.5)
        tag(ax, (x + r / 2, -0.62), rf"$\frac{{{r}}}{{6}}$", color=ec, fs=9.5)
        x += r
    tag(ax, (3.0, 0.62), "total rate 6", fs=9.5, color=GREY)
    fit(ax, -0.3, 6.3, 0.0, 5.0, 1.8)
    caption(ax, r"$P(i\ \mathrm{first})=\frac{\lambda_i}{\sum_j\lambda_j}$: clock 1 rings first with $\frac{1}{6}$",
            fs=9.5)


# ---------------------------------------------------------------- cards 22, 51: three dice
@figure("f00_three_dice_sum", w=5.0, h=2.6, axis=True)
def _(ax):
    counts = {}
    for d in itertools.product(range(1, 7), repeat=3):
        counts[sum(d)] = counts.get(sum(d), 0) + 1
    assert counts[10] == 27 and sum(counts.values()) == 216
    sums = sorted(counts)
    cols = [ORANGE if s == 10 else GREY for s in sums]
    ax.bar(sums, [counts[s] for s in sums], color=cols, width=0.8, zorder=2)
    ax.text(10, counts[10] + 1.5, "27", ha="center", color=ORANGE, fontsize=10)
    ax.set_xticks(sums[::2])
    ax.set_xlabel("sum of three dice")
    ax.set_ylabel("ordered outcomes")
    ax.set_ylim(0, 33)
    ax.set_title(r"$[x^{10}]\,(x+x^2+\cdots+x^6)^3=27$ of 216 outcomes", fontsize=10)


# ---------------------------------------------------------------- card 24: tail sum (die)
@figure("f00_tail_sum_die", w=5.0, h=2.6, axis=True)
def _(ax):
    ks = list(range(1, 7))
    tails = [(7 - k) / 6 for k in ks]  # P(X >= k)
    assert abs(sum(tails) - 3.5) < 1e-12
    ax.bar(ks, tails, color=LIGHT_ORANGE, edgecolor=ORANGE, lw=1.2, width=0.7, zorder=2)
    labs = [r"$\frac{6}{6}$", r"$\frac{5}{6}$", r"$\frac{4}{6}$", r"$\frac{3}{6}$", r"$\frac{2}{6}$", r"$\frac{1}{6}$"]
    for k, t, s in zip(ks, tails, labs):
        ax.text(k, t + 0.04, s, ha="center", fontsize=9.5)
    ax.set_xticks(ks)
    ax.set_xlabel("$k$")
    ax.set_ylabel("$P(X\\geq k)$")
    ax.set_ylim(0, 1.25)
    ax.set_title(r"$E[X]=\sum_{k\geq1}P(X\geq k)=\frac{21}{6}=3.5$", fontsize=10)


# ---------------------------------------------------------------- card 25: change of measure
@figure("f00_change_measure", w=5.0, h=2.6, axis=True)
def _(ax):
    phi = lambda x, m: np.exp(-(x - m) ** 2 / 2) / np.sqrt(2 * np.pi)
    x = np.linspace(-3, 9, 800)
    xs = np.linspace(5, 9, 300)
    ax.fill_between(xs, 0, phi(xs, 5), color=LIGHT_ORANGE, zorder=1)
    ax.plot(x, phi(x, 0), color=GREY, lw=1.6, label="P: N(0,1)")
    ax.plot(x, phi(x, 5), color=BLUE, lw=1.6, label="Q: N(5,1)")
    ax.axvline(5, color=ORANGE, ls="--", lw=1.0)
    tail_p = 0.5 * math.erfc(5 / math.sqrt(2))
    assert abs(tail_p - 2.8665e-7) < 1e-10
    tag(ax, (6.9, 0.45), "Q: mass 1/2 above 5", color=BLUE, fs=9)
    tag(ax, (-1.2, 0.3), "P: N(0,1)", color=GREY, fs=9)
    ax.annotate(r"$P(Z>5)\approx2.9\times10^{-7}$", (5.0, 0.002), xytext=(1.0, 0.12), fontsize=9,
                arrowprops=dict(arrowstyle="-", color=INK, lw=0.7))
    ax.set_xlim(-3, 9)
    ax.set_ylim(0, 0.5)
    ax.set_xlabel("$z$")
    ax.set_yticks([0, 0.2, 0.4])
    ax.set_title(r"$P(Z>5)=E_Q[\mathbf{1}_{Z>5}\,e^{-5Z+12.5}]$", fontsize=10)


# ---------------------------------------------------------------- cards 26, 64: replication
@figure("f00_replication_tree", w=5.0, h=2.6, axis=False)
def _(ax):
    S0, up, dn, K = 100, 120, 80, 100
    cup, cdn = max(up - K, 0), max(dn - K, 0)
    delta = (cup - cdn) / (up - dn)
    cash = -(delta * dn - cdn)
    price = delta * S0 + cash
    assert (delta, cash, price) == (0.5, -40, 10)
    assert abs(delta * up + cash - cup) < 1e-12 and abs(delta * dn + cash - cdn) < 1e-12
    root, U, D = (0.0, 0.0), (2.2, 0.9), (2.2, -0.9)
    line(ax, (root[0] + 0.5, 0), (U[0] - 0.6, U[1]), color=INK)
    line(ax, (root[0] + 0.5, 0), (D[0] - 0.6, D[1]), color=INK)
    bar_box(ax, root, f"stock {S0}", 1.0, 0.42, fc=LIGHT_BLUE, ec=BLUE)
    bar_box(ax, U, f"stock {up}", 1.2, 0.42)
    bar_box(ax, D, f"stock {dn}", 1.2, 0.42)
    tag(ax, (3.5, 1.08), f"call payoff {cup}", fs=9.5, color=ORANGE, ha="left")
    tag(ax, (3.5, -0.72), f"call payoff {cdn}", fs=9.5, color=INK, ha="left")
    tag(ax, (0.0, 0.85), "call = ?", fs=9.5, color=BLUE)
    tag(ax, (3.5, 0.72), f"$\\Delta\\cdot{up}-40={delta * up + cash:.0f}$", fs=9, color=ORANGE, ha="left")
    tag(ax, (3.5, -1.08), f"$\\Delta\\cdot{dn}-40={delta * dn + cash:.0f}$", fs=9, color=INK, ha="left")
    fit(ax, -0.8, 5.6, 0.0, 5.0, 2.6)
    caption(ax, r"$\Delta=\frac{20-0}{120-80}=\frac{1}{2}$, cash $=-40$, price $=50-40=10$", fs=9.5)


# ---------------------------------------------------------------- card 29: Jensen
@figure("f00_jensen_points", w=4.8, h=2.8, axis=True)
def _(ax):
    X = np.array([1.0, 2.0, 3.0])
    assert abs((1 / X).mean() - 11 / 18) < 1e-12
    xs = np.linspace(0.75, 3.4, 300)
    ax.plot(xs, 1 / xs, color=BLUE, lw=1.6, zorder=2)
    ax.plot(X, 1 / X, "o", color=ORANGE, ms=6, zorder=3)
    for x0, y0, s in [(1, 1, "1"), (2, 0.5, r"$\frac{1}{2}$"), (3, 1 / 3, r"$\frac{1}{3}$")]:
        ax.text(x0 + 0.1, y0 + 0.07, s, fontsize=9.5, color=ORANGE)
    ax.axhline(11 / 18, color=ORANGE, ls="--", lw=1.0)
    ax.text(0.8, 11 / 18 + 0.04, r"$E[1/X]=\frac{11}{18}$", fontsize=9, color=ORANGE)
    ax.plot(2, 0.5, "o", mfc="white", mec=GREY, ms=7, mew=1.5, zorder=4)
    ax.text(2.1, 0.36, r"$1/E[X]=\frac{1}{2}$", fontsize=9, color=GREY)
    ax.set_xlim(0.6, 3.4)
    ax.set_ylim(0, 1.25)
    ax.set_xticks([1, 2, 3])
    ax.set_xlabel("$x$")
    ax.set_ylabel("height $f(x)$")
    ax.yaxis.set_label_coords(-0.2, 0.5)
    ax.set_title(r"$E[1/X]\geq 1/E[X]$: average of the three heights", fontsize=10)


# ---------------------------------------------------------------- cards 32, 62: Kelly
@figure("f00_kelly_growth", w=4.6, h=2.6, axis=True)
def _(ax):
    p, b = 0.6, 1.0
    g = lambda f: p * math.log(1 + b * f) + (1 - p) * math.log(1 - f)
    fstar = p - (1 - p) / b
    assert abs(fstar - 0.2) < 1e-12
    f = np.linspace(0.0, 0.8, 400)
    ax.plot(f, [g(v) for v in f], color=BLUE, lw=1.7, zorder=2)
    ax.axvline(fstar, color=ORANGE, ls="--", lw=1.0)
    for v in (0.1, 0.2, 0.3):
        ax.plot(v, g(v), "o", color=ORANGE if v == 0.2 else GREY, ms=5.5, zorder=3)
        ax.text(v + 0.035, g(v) + 0.0008, f"{g(v):.4f}", fontsize=9, ha="left",
                color=ORANGE if v == 0.2 else GREY)
    ax.set_xlim(0, 0.8)
    ax.set_ylim(0, 0.026)
    ax.set_xlabel("fraction $f$ bet")
    ax.set_ylabel("expected log growth")
    ax.set_title(r"$f^*=p-\frac{1-p}{b}=0.6-0.4=0.2$", fontsize=10)


# ---------------------------------------------------------------- cards 35, 38, 65, 66: random N, then N coins
@figure("f00_mixture_decomp", w=5.0, h=2.8, axis=True)
def _(ax):
    N = np.arange(1, 7)
    mean = N / 2
    sd = np.sqrt(N) / 2  # Var(X | N) = N/4
    EX = mean.mean()
    assert abs(EX - 7 / 4) < 1e-12
    assert abs((N / 4).mean() - 7 / 8) < 1e-12 and abs(mean.var() - 35 / 48) < 1e-12
    ax.errorbar(N, mean, yerr=sd, fmt="o", color=BLUE, ecolor=GREY, elinewidth=1.4,
                capsize=4, ms=5.5, zorder=3)
    ax.axhline(EX, color=ORANGE, ls="--", lw=1.0)
    ax.text(0.45, EX - 0.42, r"$E[X]=\frac{7}{4}$", color=ORANGE, fontsize=9.5)
    ax.set_xticks(N)
    ax.set_xlabel("$N$ (number of coins)")
    ax.set_ylabel(r"$E[X\mid N]\pm\mathrm{sd}$")
    ax.set_xlim(0.4, 6.6)
    ax.set_ylim(-0.2, 5.0)
    ax.set_title(r"$\operatorname{Var}X=\frac{7}{8}+\frac{35}{48}=\frac{77}{48}$", fontsize=10)


# ---------------------------------------------------------------- cards 36, 67: CLT with continuity
@figure("f00_clt_tail", w=5.2, h=2.6, axis=True)
def _(ax):
    n = 100
    ks = np.arange(36, 65)
    pmf = np.array([math.comb(n, k) / 2 ** n for k in ks])
    exact = sum(math.comb(n, k) for k in range(60, n + 1)) / 2 ** n
    assert abs(exact - 0.0284) < 1e-4
    ax.bar(ks, pmf, width=0.85, color=[ORANGE if k >= 60 else LIGHT_BLUE for k in ks],
           edgecolor=[ORANGE if k >= 60 else BLUE for k in ks], lw=0.5, zorder=2)
    x = np.linspace(34, 66, 400)
    dens = np.exp(-(x - 50) ** 2 / 50) / (5 * np.sqrt(2 * np.pi))
    ax.plot(x, dens, color=INK, lw=1.2, zorder=3)
    ax.axvline(59.5, color=GREY, ls="--", lw=1.0)
    ax.text(59.1, 0.052, "59.5", ha="right", fontsize=9, color=GREY)
    ax.set_xlim(35, 65)
    ax.set_ylim(0, 0.085)
    ax.set_xlabel("heads $k$ in 100 flips")
    ax.set_title(r"$P(X\geq60)\approx\Phi^c(\frac{59.5-50}{5})=\Phi^c(1.9)\approx0.0287$ (exact 0.0284)",
                 fontsize=9.5)


# ---------------------------------------------------------------- card 39: matching pennies
@figure("f00_mp_indifference", w=4.6, h=2.6, axis=True)
def _(ax):
    p = np.linspace(0, 1, 100)
    ax.plot(p, 2 * p - 1, color=BLUE, lw=1.7, label="row Heads")
    ax.plot(p, 1 - 2 * p, color=RED, lw=1.7, label="row Tails")
    ax.plot(0.5, 0, "o", color=ORANGE, ms=7, zorder=4)
    ax.axhline(0, color=GREY, lw=0.8)
    ax.text(0.03, 0.75, r"row Heads: $2p-1$", color=BLUE, fontsize=9.5)
    ax.text(0.55, -0.82, r"row Tails: $1-2p$", color=RED, fontsize=9.5)
    ax.set_xlim(0, 1)
    ax.set_ylim(-1.1, 1.1)
    ax.set_xlabel("$p$ = P(opponent plays heads)")
    ax.set_ylabel("row payoff")
    ax.set_xticks([0, 0.5, 1])
    ax.set_title(r"indifference at $p=\frac{1}{2}$, mixed value $0$", fontsize=10)


# ---------------------------------------------------------------- card 40: information design
@figure("f00_info_design", w=4.8, h=2.6, axis=True)
def _(ax):
    prior = 1 / 3
    q = np.array([0.0, 0.5, 0.5, 1.0])
    step = np.array([0.0, 0.0, 1.0, 1.0])
    ax.plot(q, step, color=GREY, ls="--", lw=1.2, label="no commitment value")
    ax.plot([0, 0.5, 1.0], [0, 1, 1], color=ORANGE, lw=1.8, zorder=2)
    val = 2 / 3  # signal 'good' w.p. 2/3; posterior 1/2 there, receiver acts
    assert abs((1 / 3) + (2 / 3) * 0.5 - 2 / 3) < 1e-12 and abs((1 / 3) / (2 / 3) - 0.5) < 1e-12
    ax.axvline(prior, color=GREY, ls=":", lw=1.0)
    ax.plot(prior, val, "o", color=ORANGE, ms=6.5, zorder=4)
    ax.plot(prior, 0.0, "o", color=RED, ms=5.5, zorder=4)
    ax.text(prior + 0.03, val + 0.04, r"$\frac{2}{3}$ with signal", color=ORANGE, fontsize=9.5)
    ax.text(prior + 0.03, 0.06, "0 without", color=RED, fontsize=9.5)
    ax.text(0.52, 0.45, "concave\nenvelope", color=ORANGE, fontsize=9)
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.1, 1.2)
    ax.set_xticks([0, 0.5, 1])
    ax.set_yticks([0, 1])
    ax.set_xlabel("posterior $q=P(\\mathrm{good})$")
    ax.set_ylabel("sender payoff")
    ax.set_title(r"prior $q=\frac{1}{3}$: the envelope gives $\frac{2}{3}$", fontsize=10)


# ---------------------------------------------------------------- cards 41, 61: dice DP
@figure("f00_die_keep", w=4.8, h=2.6, axis=True)
def _(ax):
    faces = np.arange(1, 7)
    cont = 3.5
    assert abs((4 + 5 + 6) / 6 + 0.5 * 3.5 - 17 / 4) < 1e-12
    cols = [LIGHT_RED if f < cont else LIGHT_BLUE for f in faces]
    ec = [RED if f < cont else BLUE for f in faces]
    ax.bar(faces, faces, color=cols, edgecolor=ec, lw=1.2, width=0.6, zorder=2)
    ax.axhline(cont, color=ORANGE, ls="--", lw=1.2, zorder=3)
    ax.text(0.6, cont + 0.15, "roll again: 3.5", color=ORANGE, fontsize=9.5)
    ax.text(1, 0.25, "re-roll", ha="center", color=RED, fontsize=8.5)
    ax.text(5, 0.25, "keep", ha="center", color=BLUE, fontsize=8.5)
    ax.set_xticks(faces)
    ax.set_xlabel("first roll")
    ax.set_ylabel("value")
    ax.set_ylim(0, 6.8)
    ax.set_title(r"$V=\frac{4+5+6}{6}+\frac{3}{6}\cdot\frac{7}{2}=\frac{17}{4}$", fontsize=10)


# ---------------------------------------------------------------- cards 44, 45: walk on {0,...,10} from 3
@figure("f00_walk_0_10", w=5.0, h=2.6, axis=True)
def _(ax):
    N, start = 10, 3
    # exact: h_k = P(hit 10 before 0), tau_k = E[time to absorption]
    idx = range(1, N)
    A = np.eye(N - 1)
    for i in idx:
        for j in (i - 1, i + 1):
            if 1 <= j <= N - 1:
                A[i - 1, j - 1] -= 0.5
    hvec = np.linalg.solve(A, np.array([0.5 if i == N - 1 else 0.0 for i in idx]))
    tvec = np.linalg.solve(A, np.ones(N - 1))
    assert abs(hvec[start - 1] - 0.3) < 1e-12 and abs(tvec[start - 1] - 21) < 1e-9
    rng = np.random.default_rng(13)
    s, path = start, [start]
    while 0 < s < N:
        s += int(rng.choice([-1, 1]))
        path.append(s)
    assert s == N
    ax.axhline(0, color=RED, lw=1.6)
    ax.axhline(N, color=GREEN, lw=1.6)
    ax.plot(range(len(path)), path, "o-", color=BLUE, ms=4, lw=1.6, zorder=3)
    ax.plot(0, start, "o", color=ORANGE, ms=7, zorder=4)
    ax.text(0.3, start - 1.0, "start 3", color=ORANGE, fontsize=9)
    ax.text(len(path) - 1.2, N + 0.5, "win: absorb at 10", color=GREEN, fontsize=9, ha="right")
    ax.text(0.2, 0.5, "ruin: absorb at 0", color=RED, fontsize=9)
    ax.set_ylim(-1.2, 11.8)
    ax.set_xlim(-0.5, len(path) + 0.5)
    ax.set_yticks([0, 3, 10])
    ax.set_xlabel("flip $n$")
    ax.set_ylabel("fortune")
    ax.set_title(r"hit 10 first: $h_3=\frac{3}{10}$;  expected flips $E[\tau]=3\cdot7=21$", fontsize=10)


# ---------------------------------------------------------------- card 76: Monte Carlo error
@figure("f00_mc_error", w=4.8, h=2.6, axis=True)
def _(ax):
    N = np.logspace(2, 7, 200)
    half = 1.96 * np.sqrt(0.25 / N)
    ax.loglog(N, half, color=GREY, lw=1.7)
    assert abs(1.96 * math.sqrt(0.25 / 1e4) - 0.0098) < 1e-4
    n_need = (1.96 * 0.5 / 0.001) ** 2
    assert abs(n_need - 960400) < 1
    ax.loglog([1e4], [1.96 * math.sqrt(0.25 / 1e4)], "o", color=ORANGE, ms=6, zorder=3)
    ax.loglog([n_need], [0.001], "o", color=GREEN, ms=6, zorder=3)
    ax.axhline(0.001, color=GREEN, ls="--", lw=0.9)
    ax.text(1.2e2, 0.0046, r"$N=10^4$: $\pm0.01$", color=ORANGE, fontsize=9)
    ax.text(1.2e2, 0.0013, r"$N\approx960000$ for $\pm0.001$", color=GREEN, fontsize=9)
    ax.set_xlabel("trials $N$")
    ax.set_ylabel("95% half-width")
    ax.set_xlim(1e2, 1e7)
    ax.set_ylim(3e-4, 0.2)
    ax.set_title(r"$1.96\sqrt{p(1-p)/N}$ with $p=\frac{1}{2}$", fontsize=10)


# ---------------------------------------------------------------- card 78: broken stick
@figure("f00_stick_triangle", w=4.4, h=3.0, axis=True)
def _(ax):
    big = [(0, 0), (0, 1), (1, 1)]
    ax.add_patch(Polygon(big, closed=True, fc="white", ec=GREY, lw=1.1, zorder=1))
    ev = [(0, 0.5), (0.5, 0.5), (0.5, 1)]
    ax.add_patch(Polygon(ev, closed=True, fc=LIGHT_GREEN, ec=GREEN, lw=1.3, zorder=2))
    area_ev = 0.5 * 0.5 * 0.5
    assert abs(area_ev / 0.5 - 0.25) < 1e-12
    tag(ax, (0.28, 0.72), r"all three $<\frac{1}{2}$", fs=8.5, color=GREEN)
    ax.text(0.7, 0.3, r"$\frac{1}{8}$ of $\frac{1}{2}$", color=GREY, fontsize=9)
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.05, 1.05)
    ax.set_xticks([0, 0.5, 1])
    ax.set_yticks([0, 0.5, 1])
    ax.set_xlabel("first cut $a$")
    ax.set_ylabel("second cut $b$")
    ax.set_title(r"$P=\frac{1/8}{1/2}=\frac{1}{4}$", fontsize=10)


# ---------------------------------------------------------------- card 70: subsets with no two consecutive
@figure("f00_no_adj_strings", w=5.0, h=1.9, axis=False)
def _(ax):
    strings = [format(v, "03b") for v in range(8)]
    valid = [s for s in strings if "11" not in s]
    assert len(valid) == 5  # a_3 = 5
    assert [len([s for s in [format(v, f"0{n}b") for v in range(2 ** n)] if "11" not in s]) for n in (1, 2, 3)] == [2, 3, 5]
    for i, s in enumerate(strings):
        ok = "11" not in s
        bar_box(ax, (i * 1.0, 0), s, 0.82, 0.5, fc=LIGHT_GREEN if ok else LIGHT_RED,
                ec=GREEN if ok else RED, fs=10)
    tag(ax, (1.5, -0.7), f"valid: {len(valid)}", color=GREEN, fs=9.5)
    tag(ax, (5.5, -0.7), f"invalid: {8 - len(valid)}", color=RED, fs=9.5)
    tag(ax, (3.5, 0.62), "1 = in the set, no two adjacent 1s", color=GREY, fs=9)
    fit(ax, -0.7, 7.7, 0.0, 5.0, 1.9)
    caption(ax, r"$a_n=a_{n-1}+a_{n-2}$ with $a_1=2,\ a_2=3,\ a_3=5$", fs=9.5)
