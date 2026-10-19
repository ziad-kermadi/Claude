"""Figures for cards/02_conditioning_bayes.json."""
import numpy as np
from fractions import Fraction as Fr
from matplotlib.patches import Rectangle
from qcfig import *

FS = 9.5  # minimum label size in schematic figures
_SIZES = {}  # node centre -> (w, h), so edges can stop at the box border


def _nb(ax, xy, label, w=1.0, h=0.46, fc="white", ec=INK, fs=FS, lw=1.0, tc=INK):
    _SIZES[xy] = (w, h)
    box(ax, xy, label, w=w, h=h, fc=fc, ec=ec, fs=fs, lw=lw)
    ax.texts[-1].set_color(tc)


def _clip(c, t, size, pad=0.05):
    w, h = size
    dx, dy = t[0] - c[0], t[1] - c[1]
    hw, hh = w / 2 + pad, h / 2 + pad
    s = []
    if abs(dx) > 1e-9:
        s.append(hw / abs(dx))
    if abs(dy) > 1e-9:
        s.append(hh / abs(dy))
    k = min(s) if s else 0.0
    return (c[0] + dx * k, c[1] + dy * k)


# Recompute every result the figures state, and check it against the card answers.
def _post(prior, lik):
    tot = sum(p * l for p, l in zip(prior, lik))
    return [p * l / tot for p, l in zip(prior, lik)]


def _verify():
    F = Fr
    third = [F(1, 3)] * 3
    # Monty Hall variants (cards 0, 2, 3): posterior on car location given the reveal
    assert _post(third, [F(1, 2), 1, 0])[1] == F(2, 3)            # card 0: switch wins 2/3
    assert _post(third, [F(1, 4), 0, 1])[2] == F(4, 5)            # card 3: switch wins 4/5
    assert _post(third, [F(1, 2), 0, F(1, 2)])[0] == F(1, 2)      # card 2: random host, 1/2 each
    # Bertrand box (23, 24): P(GG | gold)
    assert _post(third, [1, F(1, 2), 0])[0] == F(2, 3)
    # Dice and types, by enumeration (13, 14, 17, 18, 8)
    pairs = [(a, b) for a in range(1, 7) for b in range(1, 7)]
    six = [q for q in pairs if 6 in q]
    assert F(sum(q == (6, 6) for q in six), len(six)) == F(1, 11)     # 13
    assert F(sum(q == (6, 6) for q in pairs if q[0] == 6), 6) == F(1, 6)  # 14
    assert F(sum(a + b >= 11 for a, b in six), len(six)) == F(3, 11)  # 18
    s7 = [q for q in pairs if sum(q) == 7]
    assert F(sum(6 in q for q in s7), len(s7)) == F(1, 3)             # 17: sum 7
    s11 = [q for q in pairs if sum(q) == 11]
    assert F(sum(6 in q for q in s11), len(s11)) == 1                 # 17: sum 11
    types = [(i, j) for i in range(14) for j in range(14)]
    ev = [(i, j) for i, j in types if i == 1 or j == 1]               # boy-Tuesday type is index 1
    assert len(ev) == 27 and sum(i < 7 and j < 7 for i, j in ev) == 13   # 8
    # Base rates (29-31, 34): natural frequencies and Bayes
    assert F(1, 1000) * F(99, 100) / (F(1, 1000) * F(99, 100) + F(999, 1000) * F(5, 100)) == F(11, 566)
    assert F(1, 10) * F(99, 100) / (F(1, 10) * F(99, 100) + F(9, 10) * F(5, 100)) == F(11, 16)
    assert F(150, 1000) * F(8, 10) / (F(150, 1000) * F(8, 10) + F(850, 1000) * F(2, 10)) == F(12, 29)
    # Two tests (32, 53): independent vs shared error source
    o = F(1, 999) * F(99, 5) ** 2
    assert o / (1 + o) == F(363, 1288)
    o = F(1, 999) * F(99, 5)
    assert o / (1 + o) == F(11, 566)
    # Odds walk (51): odds 1:4 -> 3:4 -> 1:4
    assert F(1, 4) * 3 / (1 + F(1, 4) * 3) == F(3, 7)
    assert F(3, 4) * F(1, 3) / (1 + F(3, 4) * F(1, 3)) == F(1, 5)
    # Prisoners (27, 28)
    assert _post(third, [F(1, 2), 0, 1])[0] == F(1, 3)
    assert _post(third, [F(1, 2), 0, 1])[2] == F(2, 3)
    assert _post(third, [1, 0, 1])[0] == F(1, 2)
    # Polya urn (39): P(R2 | R1) = (1/2 * 2/3) / (1/2)
    assert (F(1, 2) * F(2, 3)) / F(1, 2) == F(2, 3)
    # Uniform prior counts (41) and P(p > 1/2 | HHH) (46)
    assert sum(F(1, 4) for _ in range(4)) == 1
    assert 1 - F(1, 2) ** 4 == F(15, 16)
    # Normal-normal (48): precision 1 + 1 = 2, mean (0 + 2) / 2 = 1, variance 1/2
    assert F(0 + 2, 2) == 1 and F(1, 1) / 2 == F(1, 2)            # mean 1, variance 1/2
    # Bias 0.2 / 0.8 (64, 65)
    p_hh = F(1, 2) * F(2, 10) ** 2 + F(1, 2) * F(8, 10) ** 2
    assert p_hh == F(34, 100) and F(1, 2) ** 2 == F(1, 4)
    # Phi range (71, 72)
    pA, pB = F(3, 10), F(1, 2)
    sd2 = pA * (1 - pA) * pB * (1 - pB)
    assert (F(2, 10) - pA * pB) == F(1, 20)                          # Cov at P(A and B) = 0.2
    assert abs(float((F(1, 20)) / (sd2 ** 0.5)) - 0.218) < 1e-3
    assert abs(float((F(0) - pA * pB) / sd2 ** 0.5) + 0.6547) < 1e-3
    # Borel sphere (68, 69): P(latitude > 45 deg) under density cos/2
    import math
    lat = np.linspace(math.pi / 4, math.pi / 2, 20001)
    assert abs(np.trapezoid(0.5 * np.cos(lat), lat) - (2 - math.sqrt(2)) / 4) < 1e-6
    # Two coins (75): P(B | HH) = 0.405 / 0.530
    assert F(405, 1000) / F(53, 100) == F(81, 106)
    # Simpson's (59-61)
    assert F(81 + 192, 87 + 263) == F(273, 350) and F(234 + 55, 270 + 80) == F(289, 350)
    assert F(18 + 2, 20 + 10) == F(20, 30) and F(170, 210) == F(17, 21)
    # Inspection paradox (55, 56)
    assert F(5 * 5 + 15 * 15, 20) == F(25, 2)                          # class size at a random pupil
    assert F(125, 2 * 10) == F(25, 4)                                  # E[G^2]/(2E[G]) = bus wait 6.25
    # Envelopes (20): E[B | A=a] from the four equally likely ordered pairs
    outs = [(1, 2), (2, 1), (2, 4), (4, 2)]
    cond = {a: [b for x, b in outs if x == a] for a in (1, 2, 4)}
    assert [F(sum(v), len(v)) for a, v in sorted(cond.items())] == [2, F(5, 2), 2]
    return True


_verify()


def _edge(ax, a, b, label=None, color=INK, lo=(0.0, 0.0), fs=FS):
    p = _clip(a, b, _SIZES.get(a, (1.0, 0.46)))
    q = _clip(b, a, _SIZES.get(b, (1.0, 0.46)))
    ax.annotate("", xy=q, xytext=p,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=1.2, shrinkA=0, shrinkB=0))
    if label:
        mx, my = (p[0] + q[0]) / 2 + lo[0], (p[1] + q[1]) / 2 + lo[1]
        ax.text(mx, my, label, ha="center", va="center", fontsize=fs, color=color,
                bbox=dict(fc="white", ec="none", pad=0.5), zorder=5)


def _leaf(ax, xy, label, hi=False, w=1.75, grey=False):
    fc = LIGHT_ORANGE if hi else "white"
    ec = ORANGE if hi else (GREY if grey else INK)
    _nb(ax, xy, label, w=w, h=0.42, fc=fc, ec=ec, lw=1.3 if hi else 1.0, tc=GREY if grey else INK)


# ---------------------------------------------------------------- Monty Hall

@figure("f02_monty_tree", w=5.0, h=2.9, axis=False)
def _(ax):
    # Player picks door 1. Car is at 1, 2 or 3 with prob 1/3 each.
    # Host (knows the car) opens 2 or 3, never the car, never door 1.
    R = (0.5, 1.7)
    C = {1: (2.3, 2.9), 2: (2.3, 1.5), 3: (2.3, 0.5)}
    L = {"1a": (4.35, 3.3), "1b": (4.35, 2.5), "2": (4.35, 1.5), "3": (4.35, 0.5)}
    _nb(ax, R, "car door", w=1.1, h=0.46)
    for k in (1, 2, 3):
        _nb(ax, C[k], f"car at {k}", w=1.1, h=0.46)
    _leaf(ax, L["1a"], "host opens 2:  1/6", grey=True)
    _leaf(ax, L["1b"], "host opens 3:  1/6", hi=True)
    _leaf(ax, L["2"], "host opens 3:  1/3", hi=True)
    _leaf(ax, L["3"], "host opens 2:  1/3", grey=True)
    _edge(ax, R, C[1], "1/3", lo=(-0.12, 0.2))
    _edge(ax, R, C[2], "1/3", lo=(0.0, 0.2))
    _edge(ax, R, C[3], "1/3", lo=(-0.12, -0.2))
    _edge(ax, C[1], L["1a"], "1/2", lo=(0.0, 0.17))
    _edge(ax, C[1], L["1b"], "1/2", lo=(0.0, -0.17))
    _edge(ax, C[2], L["2"], "1", lo=(0.0, 0.17))
    _edge(ax, C[3], L["3"], "1", lo=(0.0, 0.17))
    ax.text(2.55, -0.5, r"given host opens 3: car at 1 : car at 2 = $\frac{1}{6}:\frac{1}{3}$, so switch wins $\frac{2}{3}$",
            ha="center", va="center", fontsize=FS)
    ax.set_xlim(-0.3, 5.4); ax.set_ylim(-0.8, 3.7)


@figure("f02_monty_habit", w=5.0, h=2.9, axis=False)
def _(ax):
    # Host habit: car at your door (1) -> he opens 2 w.p. 1/4, 3 w.p. 3/4.
    R = (0.5, 1.7)
    C = {1: (2.3, 2.9), 2: (2.3, 1.5), 3: (2.3, 0.5)}
    L = {"1a": (4.35, 3.3), "1b": (4.35, 2.5), "2": (4.35, 1.5), "3": (4.35, 0.5)}
    _nb(ax, R, "car door", w=1.1, h=0.46)
    for k in (1, 2, 3):
        _nb(ax, C[k], f"car at {k}", w=1.1, h=0.46)
    _leaf(ax, L["1a"], "host opens 2:  1/12", hi=True)
    _leaf(ax, L["1b"], "host opens 3:  1/4", grey=True)
    _leaf(ax, L["2"], "host opens 3:  1/3", grey=True)
    _leaf(ax, L["3"], "host opens 2:  1/3", hi=True)
    _edge(ax, R, C[1], "1/3", lo=(-0.12, 0.2))
    _edge(ax, R, C[2], "1/3", lo=(0.0, 0.2))
    _edge(ax, R, C[3], "1/3", lo=(-0.12, -0.2))
    _edge(ax, C[1], L["1a"], "1/4", lo=(0.0, 0.17))
    _edge(ax, C[1], L["1b"], "3/4", lo=(0.0, -0.17))
    _edge(ax, C[2], L["2"], "1", lo=(0.0, 0.17))
    _edge(ax, C[3], L["3"], "1", lo=(0.0, 0.17))
    ax.text(2.55, -0.5, r"given host opens 2: car at 1 : car at 3 = $\frac{1}{12}:\frac{1}{3}$, switch to 3 wins $\frac{4}{5}$",
            ha="center", va="center", fontsize=FS)
    ax.set_xlim(-0.3, 5.4); ax.set_ylim(-0.8, 3.7)


@figure("f02_monty_random", w=5.0, h=3.2, axis=False)
def _(ax):
    # Host opens 2 or 3 at random (not knowing the car). Each of 6 outcomes has prob 1/6.
    R = (0.5, 2.0)
    C = {1: (2.2, 3.6), 2: (2.2, 2.0), 3: (2.2, 0.4)}
    _nb(ax, R, "car door", w=1.1, h=0.46)
    for k in (1, 2, 3):
        _nb(ax, C[k], f"car at {k}", w=1.1, h=0.46)
    _edge(ax, R, C[1], "1/3", lo=(-0.12, 0.2))
    _edge(ax, R, C[2], "1/3", lo=(0.0, 0.2))
    _edge(ax, R, C[3], "1/3", lo=(-0.12, -0.2))
    rows = {(1, 2): 4.0, (1, 3): 3.2, (2, 2): 2.4, (2, 3): 1.6, (3, 2): 0.8, (3, 3): 0.0}
    for (k, d), y in rows.items():
        xy = (4.2, y)
        if k == d:  # the host opens the car's door
            _leaf(ax, xy, f"opens {d}: car shown", grey=True, w=2.0)
        elif d == 2:  # goat at 2 (key outcome)
            _leaf(ax, xy, "opens 2: goat  1/6", hi=True, w=2.0)
        else:
            _leaf(ax, xy, "opens 3: goat  1/6", grey=True, w=2.0)
        _edge(ax, C[k], xy)
    ax.text(2.55, -0.55, r"each outcome $\frac{1}{6}$; goat at 2 (orange): car at 1 and car at 3 each $\frac{1}{2}$",
            ha="center", va="center", fontsize=FS)
    ax.set_xlim(-0.3, 5.3); ax.set_ylim(-0.9, 4.3)


@figure("f02_hundred_doors", w=5.2, h=2.3, axis=False)
def _(ax):
    # 100 doors. Door 1 keeps 1/100; the other 99/100 sits behind the one unopened door.
    unopened = 73  # door index 1..100 (illustrative position)
    cols = 50
    for d in range(1, 101):
        r, c = divmod(d - 1, cols)
        x, y = c * 0.1, 1.2 - r * 0.5
        if d == 1:
            fc, ec = ORANGE, ORANGE
        elif d == unopened:
            fc, ec = BLUE, BLUE
        else:
            fc, ec = "white", GREY
        if d != 1 and d != unopened:
            fc = (0.55, 0.55, 0.55, 0.25)  # opened: goat (context)
        ax.add_patch(Rectangle((x, y), 0.08, 0.36, fc=fc, ec=ec, lw=0.6, zorder=2))
    ax.annotate("your door: 1/100", xy=(0.04, 1.6), xytext=(0.2, 2.25), fontsize=FS, ha="left",
                color=ORANGE, arrowprops=dict(arrowstyle="-", color=ORANGE, lw=1))
    ur, uc = divmod(unopened - 1, cols)
    ax.annotate("unopened: 99/100", xy=(uc * 0.1 + 0.04, 1.2 - ur * 0.5 + 0.36), xytext=(2.6, 2.25),
                fontsize=FS, ha="left", color=BLUE, arrowprops=dict(arrowstyle="-", color=BLUE, lw=1))
    ax.text(2.5, -0.5, "host opens 98 goats (grey); the car is behind door 1 or the unopened door",
            ha="center", va="center", fontsize=FS)
    ax.set_xlim(-0.1, 5.1); ax.set_ylim(-0.8, 2.6)


# ----------------------------------------------------------- Bayes odds forms

@figure("f02_odds_walk", w=4.6, h=2.6)
def _(ax):
    prior = Fr(1, 5)       # odds 1:4
    after1 = Fr(3, 7)      # odds 3:4 after LR 3
    after2 = Fr(1, 5)      # odds 1:4 after LR 1/3
    xs = [0, 1, 2]
    ps = [float(prior), float(after1), float(after2)]
    ax.plot(xs, ps, color=BLUE, marker="o", ms=7, lw=2)
    labels = [r"odds $1:4$" + "\n" + r"$P=\frac{1}{5}$",
              r"odds $3:4$" + "\n" + r"$P=\frac{3}{7}$",
              r"odds $1:4$" + "\n" + r"$P=\frac{1}{5}$"]
    for x, p, l in zip(xs, ps, labels):
        ax.annotate(l, (x, p), xytext=(0, 9), textcoords="offset points", ha="center", va="bottom", fontsize=FS)
    ax.text(0.5, 0.12, r"LR $3$", color=ORANGE, ha="center", fontsize=FS)
    ax.text(1.5, 0.12, r"LR $\frac{1}{3}$", color=ORANGE, ha="center", fontsize=FS)
    ax.set_xticks(xs)
    ax.set_xticklabels(["prior", "after signal 1", "after signal 2"], fontsize=FS)
    ax.set_xlim(-0.4, 2.4); ax.set_ylim(0, 0.75)
    ax.set_ylabel(r"$P(A)$", fontsize=FS)


# ---------------------------------------------------------- Bertrand's box

@figure("f02_bertrand_faces", w=4.6, h=2.2, axis=False)
def _(ax):
    boxes = [("GG", ["G", "G"]), ("GS", ["G", "S"]), ("SS", ["S", "S"])]
    for k, (name, faces) in enumerate(boxes):
        x0 = 0.4 + k * 1.6
        hi = name == "GG"
        ax.add_patch(Rectangle((x0 - 0.12, -0.12), 1.24, 1.04, fill=False,
                               ec=BLUE if hi else GREY, lw=1.6 if hi else 1.0, zorder=1))
        for j, f in enumerate(faces):
            gold = f == "G"
            fc = LIGHT_ORANGE if gold else "white"
            ec = ORANGE if gold else GREY
            ax.add_patch(Rectangle((x0 + j * 0.6, 0.2), 0.5, 0.5, fc=fc, ec=ec, lw=1.2, zorder=2))
            ax.text(x0 + j * 0.6 + 0.25, 0.45, f, ha="center", va="center", fontsize=11,
                    color=ORANGE if gold else GREY, zorder=3)
        ax.text(x0 + 0.5, -0.45, f"box {name}", ha="center", va="center", fontsize=FS,
                color=BLUE if hi else INK)
    ax.text(2.75, -1.05, r"3 gold faces; 2 of them are in box GG: $P(\mathrm{GG}\mid\mathrm{gold})=\frac{2}{3}$",
            ha="center", va="center", fontsize=FS)
    ax.set_xlim(0.1, 5.2); ax.set_ylim(-1.3, 1.1)


# ------------------------------------------------------ boy-girl sample spaces

def _grid2(ax, x0, y0, keep, cell=0.9):
    names = {("B", "B"): "BB", ("B", "G"): "BG", ("G", "B"): "GB", ("G", "G"): "GG"}
    for c, b in enumerate(["B", "G"]):
        ax.text(x0 + c * cell + cell / 2, y0 + 2 * cell + 0.12, b, ha="center", va="center", fontsize=FS)
    for r, a in enumerate(["B", "G"]):
        ax.text(x0 - 0.2, y0 + (1 - r) * cell + cell / 2, a, ha="center", va="center", fontsize=FS)
        for c, b in enumerate(["B", "G"]):
            x, y = x0 + c * cell, y0 + (1 - r) * cell
            k = (a, b) in keep
            ax.add_patch(Rectangle((x, y), cell, cell, fc=LIGHT_BLUE if k else "white",
                                   ec=INK if k else GREY, lw=1.0, zorder=2))
            ax.text(x + cell / 2, y + cell / 2, names[(a, b)], ha="center", va="center", fontsize=10,
                    color=INK if k else GREY, zorder=3)


@figure("f02_boygirl_atleast", w=4.0, h=2.4, axis=False)
def _(ax):
    keep = {("B", "B"), ("B", "G"), ("G", "B")}
    _grid2(ax, 0.5, 0.2, keep)
    ax.text(1.4, -0.45, "first child (rows), second child (columns)", ha="center", va="center", fontsize=FS)
    ax.text(1.4, -0.85, r"at least one boy: 3 outcomes, $P(\mathrm{BB})=\frac{1}{3}$",
            ha="center", va="center", fontsize=FS)
    ax.set_xlim(-0.3, 2.9); ax.set_ylim(-1.1, 2.5)


@figure("f02_boygirl_older", w=5.0, h=2.5, axis=False)
def _(ax):
    _grid2(ax, 0.5, 0.2, {("B", "B"), ("B", "G")})
    ax.text(1.4, 2.6, "older child is a boy", ha="center", va="center", fontsize=FS)
    ax.text(1.4, -0.45, r"$P(\mathrm{BB})=\frac{1}{2}$", ha="center", va="center", fontsize=FS)
    _grid2(ax, 3.4, 0.2, {("B", "B"), ("B", "G"), ("G", "B")})
    ax.text(4.3, 2.6, "at least one boy", ha="center", va="center", fontsize=FS)
    ax.text(4.3, -0.45, r"$P(\mathrm{BB})=\frac{1}{3}$", ha="center", va="center", fontsize=FS)
    ax.set_xlim(-0.4, 5.5); ax.set_ylim(-0.8, 2.9)


@figure("f02_sampled_child", w=4.8, h=3.0, axis=False)
def _(ax):
    # (family, sampled child index) pairs, each with probability 1/8
    rows = [("BB", 1, "yes", "yes"), ("BB", 2, "yes", "yes"),
            ("BG", 1, "yes", "no"), ("BG", 2, "no", "-"),
            ("GB", 1, "no", "-"), ("GB", 2, "yes", "no"),
            ("GG", 1, "no", "-"), ("GG", 2, "no", "-")]
    heads = ["family", "sampled", "sampled boy?", "other boy?"]
    xs = [0.2, 1.3, 2.5, 3.85]
    for x, h in zip(xs, heads):
        ax.text(x, 8.4, h, ha="left", va="center", fontsize=FS)
    for i, (fam, idx, sb, ob) in enumerate(rows):
        y = 7.3 - i * 0.95
        if sb == "yes" and ob == "yes":
            ax.add_patch(Rectangle((0.1, y - 0.4), 4.7, 0.8, fc=LIGHT_BLUE, ec="none", zorder=1))
        elif sb == "yes":
            ax.add_patch(Rectangle((0.1, y - 0.4), 4.7, 0.8, fc="white", ec=GREY, lw=0.6, zorder=1))
        tc = INK if sb == "yes" else GREY
        ax.text(xs[0], y, fam, ha="left", va="center", fontsize=FS, color=tc)
        ax.text(xs[1] + 0.1, y, str(idx), ha="left", va="center", fontsize=FS, color=tc)
        ax.text(xs[2] + 0.2, y, sb, ha="left", va="center", fontsize=FS, color=tc)
        ax.text(xs[3] + 0.2, y, ob, ha="left", va="center", fontsize=FS, color=tc)
    ax.text(2.1, -0.6, r"sampled child is a boy: 4 cases, other is a boy in 2: $P=\frac{1}{2}$",
            ha="center", va="center", fontsize=FS)
    ax.set_xlim(0.0, 5.0); ax.set_ylim(-1.0, 8.9)


# ------------------------------------------------------------------ dice

def _grid6(ax, x0, y0, cell, colour):
    for a in range(1, 7):      # first die -> column
        for b in range(1, 7):  # second die -> row
            x, y = x0 + (a - 1) * cell, y0 + (b - 1) * cell
            fc, ec = colour(a, b)
            ax.add_patch(Rectangle((x, y), cell, cell, fc=fc, ec=ec, lw=0.6, zorder=2))
    for v in range(1, 7):
        ax.text(x0 + (v - 0.5) * cell, y0 - 0.2, str(v), ha="center", va="center", fontsize=FS)
        ax.text(x0 - 0.2, y0 + (v - 0.5) * cell, str(v), ha="center", va="center", fontsize=FS)


@figure("f02_dice_six_grid", w=5.0, h=2.9, axis=False)
def _(ax):
    cell = 0.36

    def at_least_six(a, b):
        if a == 6 and b == 6:
            return BLUE, INK
        if a + b >= 11 and (a == 6 or b == 6):
            return ORANGE, INK
        if a == 6 or b == 6:
            return LIGHT_BLUE, INK
        return "white", GREY

    def first_six(a, b):
        if a == 6 and b == 6:
            return BLUE, INK
        if a == 6:
            return LIGHT_BLUE, INK
        return "white", GREY

    _grid6(ax, 0.5, 0.7, cell, at_least_six)
    _grid6(ax, 3.2, 0.7, cell, first_six)
    ax.text(0.5 + 3 * cell, 4.25, r"at least one six (11 outcomes)", ha="center", va="center", fontsize=FS)
    ax.text(3.2 + 3 * cell, 4.25, r"first die is six (6 outcomes)", ha="center", va="center", fontsize=FS)
    ax.text(0.5 + 3 * cell, -0.1, r"$P(\mathrm{both}\,6)=\frac{1}{11}$; sum $\geq 11$ (orange): $\frac{3}{11}$",
            ha="center", va="center", fontsize=FS)
    ax.text(3.2 + 3 * cell, -0.1, r"$P(\mathrm{both}\,6)=\frac{1}{6}$",
            ha="center", va="center", fontsize=FS)
    ax.set_xlim(-0.2, 5.4); ax.set_ylim(-0.4, 4.5)


@figure("f02_dice_sum_diagonals", w=4.2, h=3.0, axis=False)
def _(ax):
    # Condition on the sum. Sum 7 and sum 11 are highlighted; blue cells contain a six.
    for a in range(1, 7):
        for b in range(1, 7):
            s = a + b
            x, y = a - 1, b - 1
            if s in (7, 11):
                fc = LIGHT_BLUE if (a == 6 or b == 6) else LIGHT_ORANGE
                ec = ORANGE
            else:
                fc, ec = "white", GREY
            ax.add_patch(Rectangle((x, y), 1, 1, fc=fc, ec=ec, lw=0.8, zorder=2))
            ax.text(x + 0.5, y + 0.5, str(s), ha="center", va="center", fontsize=10,
                    color=INK if s in (7, 11) else GREY, zorder=3)
    for v in range(1, 7):
        ax.text(v - 0.5, -0.4, str(v), ha="center", va="center", fontsize=FS)
        ax.text(-0.4, v - 0.5, str(v), ha="center", va="center", fontsize=FS)
    ax.text(-0.4, 6.4, "die 2", ha="center", va="center", fontsize=FS)
    ax.text(3.0, -0.95, "die 1 across, die 2 up; the number in each cell is the sum",
            ha="center", va="center", fontsize=FS)
    ax.text(3.0, -1.5, r"sum 7: $P(\mathrm{six}\mid S=7)=\frac{2}{6}$;  sum 11: $\frac{2}{2}$",
            ha="center", va="center", fontsize=FS)
    ax.set_xlim(-0.8, 6.2); ax.set_ylim(-1.9, 6.8)


@figure("f02_types_grid", w=4.6, h=3.2, axis=False)
def _(ax):
    # Each child has 14 equally likely types: boy-Mon..Sun (0-6), girl-Mon..Sun (7-13).
    # Event A: at least one boy born on a Tuesday (type index 1 in the boy block).
    cell = 1.0
    x0, y0 = 2.2, 0.4
    for i in range(14):
        for j in range(14):
            inA = (i == 1) or (j == 1)
            both = (i < 7) and (j < 7)
            if inA and both:
                fc, ec = BLUE, BLUE
            elif inA:
                fc, ec = LIGHT_BLUE, GREY
            else:
                fc, ec = "white", "#dddddd"
            ax.add_patch(Rectangle((x0 + j * cell, y0 + (13 - i) * cell), cell, cell,
                                   fc=fc, ec=ec, lw=0.4, zorder=2))
    ax.text(x0 + 3.5 * cell, y0 + 14.6 * cell, "boy", ha="center", va="center", fontsize=FS)
    ax.text(x0 + 10.5 * cell, y0 + 14.6 * cell, "girl", ha="center", va="center", fontsize=FS)
    ax.text(x0 + 1.5 * cell, y0 + 14.6 * cell, "Tu", ha="center", va="center", fontsize=FS, color=ORANGE)
    ax.text(x0 + 7 * cell, y0 + 15.8 * cell, "child 2 type", ha="center", va="center", fontsize=FS)
    ax.text(x0 - 0.9 * cell, y0 + 10.4 * cell, "boy", ha="center", va="center", fontsize=FS)
    ax.text(x0 - 0.9 * cell, y0 + 3.4 * cell, "girl", ha="center", va="center", fontsize=FS)
    ax.text(x0 - 0.45 * cell, y0 + 12.9 * cell, "Tu", ha="center", va="center", fontsize=FS, color=ORANGE)
    ax.text(x0 - 2.0 * cell, y0 + 7.4 * cell, "child 1 type", ha="center", va="center", fontsize=FS, rotation=90)
    ax.text(x0 + 7 * cell, y0 - 0.9, r"$P=\frac{13}{27}$;  blue: both boys in A (13);  light: A (27)",
            ha="center", va="center", fontsize=FS)
    ax.set_xlim(-1.2, 16.8); ax.set_ylim(-1.5, 16.8)


# ------------------------------------------------------------ base rates

@figure("f02_base_rate_bars", w=5.0, h=2.3, axis=False)
def _(ax):
    total = 5094.0          # positives out of 100,000 people
    W = 4.4
    sick_pos, healthy_pos = 99.0, 4995.0
    wb = sick_pos / total * W
    ax.add_patch(Rectangle((0, 0.0), wb, 0.6, fc=BLUE, ec="none", zorder=2))
    ax.add_patch(Rectangle((wb, 0.0), W - wb, 0.6, fc=RED, ec="none", zorder=2))
    ax.text(W - (W - wb) / 2, 0.3, "4,995 healthy positive", ha="center", va="center", fontsize=FS,
            color="white", zorder=3)
    ax.annotate("99 sick positive", xy=(wb / 2, 0.6), xytext=(0.2, 1.25), fontsize=FS, color=BLUE,
                arrowprops=dict(arrowstyle="-", color=BLUE, lw=1))
    ax.add_patch(Rectangle((0, -0.9), 4.4, 0.45, fc=GREY, ec="none", alpha=0.35, zorder=2))
    ax.text(2.2, -0.68, "100,000 people: 100 sick (0.1%), 99,900 healthy", ha="center", va="center", fontsize=FS)
    ax.text(2.2, -1.25, "5,094 positive tests in total", ha="center", va="center", fontsize=FS)
    ax.text(2.2, -1.8, r"$P(\mathrm{sick}\mid\mathrm{positive})=\frac{99}{5094}=\frac{11}{566}\approx1.94\%$",
            ha="center", va="center", fontsize=FS)
    ax.set_xlim(-0.1, 4.5); ax.set_ylim(-2.1, 1.9)


@figure("f02_customs_icons", w=4.8, h=2.7, axis=False)
def _(ax):
    # 1000 parcels: 150 contraband (sniffer alerts 80%), 850 legitimate (alerts 20%).
    groups = [(120, BLUE), (30, LIGHT_BLUE), (170, RED), (680, "#cfcfcf")]
    colours = [c for n, c in groups for _ in range(n)]
    cols = 40
    for k, c in enumerate(colours):
        r, cc = divmod(k, cols)
        ax.add_patch(Rectangle((cc, 24 - r), 0.8, 0.8, fc=c, ec="none", zorder=2))
    ax.text(0, 26.6, r"290 flagged; $P(\mathrm{contraband}\mid\mathrm{flagged})=\frac{120}{290}=\frac{12}{29}$",
            ha="left", va="center", fontsize=FS)
    leg = [(0, -2.2, BLUE, "contraband, flagged: 120"), (0, -3.9, LIGHT_BLUE, "contraband, not flagged: 30"),
           (0, -5.6, RED, "legitimate, flagged: 170"), (0, -7.3, "#cfcfcf", "legitimate, not flagged: 680")]
    for x, y, c, t in leg:
        ax.add_patch(Rectangle((x, y), 1.2, 1.2, fc=c, ec="none"))
        ax.text(x + 1.8, y + 0.6, t, ha="left", va="center", fontsize=FS)
    ax.set_xlim(-0.5, 40.5); ax.set_ylim(-8.5, 27.5)


@figure("f02_two_tests_compare", w=5.0, h=2.2, axis=True)
def _(ax):
    labels = ["one positive test", "two positive tests,\nindependent errors", "two positive tests,\nshared error source"]
    vals = [11 / 566 * 100, 363 / 1288 * 100, 11 / 566 * 100]
    cols = [GREY, BLUE, ORANGE]
    y = np.arange(3)[::-1]
    ax.barh(y, vals, color=cols, height=0.6)
    for yi, v in zip(y, vals):
        ax.text(v + 0.6, yi, f"{v:.1f}%", va="center", fontsize=FS)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=FS)
    ax.set_xlim(0, 36)
    ax.set_xlabel(r"$P(\mathrm{disease}\mid\mathrm{positive\ results})$, prevalence $\frac{1}{1000}$", fontsize=FS)


@figure("f02_kidney_simpson", w=5.0, h=2.8, axis=True)
def _(ax):
    small = {"A": (81, 87), "B": (234, 270)}
    large = {"A": (192, 263), "B": (55, 80)}
    overall = {k: ((small[k][0] + large[k][0]), (small[k][1] + large[k][1])) for k in "AB"}
    cats = ["small stones", "large stones", "overall"]
    data = {"A": [100 * small["A"][0] / small["A"][1], 100 * large["A"][0] / large["A"][1],
                  100 * overall["A"][0] / overall["A"][1]],
            "B": [100 * small["B"][0] / small["B"][1], 100 * large["B"][0] / large["B"][1],
                  100 * overall["B"][0] / overall["B"][1]]}
    n = {"A": [87, 263, 350], "B": [270, 80, 350]}
    x = np.arange(3)
    w = 0.36
    for off, k, c in [(-w / 2, "A", BLUE), (w / 2, "B", GREY)]:
        ax.bar(x + off, data[k], width=w, color=c, label=f"treatment {k}", zorder=2)
        for xi, v, m in zip(x + off, data[k], n[k]):
            ax.text(xi, v + 1.2, f"{v:.1f}%", ha="center", va="bottom", fontsize=FS)
            ax.text(xi, 4, f"n={m}", ha="center", va="bottom", fontsize=FS - 0.5, color="white" if k == "A" else INK)
    ax.set_xticks(x)
    ax.set_xticklabels(cats, fontsize=FS)
    ax.set_ylim(0, 112)
    ax.set_ylabel("cure rate", fontsize=FS)
    ax.legend(fontsize=FS, frameon=False, loc="upper center", ncol=2, bbox_to_anchor=(0.5, 1.02))


@figure("f02_shots_simpson", w=4.6, h=2.7, axis=True)
def _(ax):
    cats = ["2-pointers", "3-pointers", "overall"]
    X = [90.0, 20.0, 100 * 20 / 30]
    Y = [85.0, 0.0, 100 * 170 / 210]
    nX = ["18/20", "2/10", "20/30"]
    nY = ["170/200", "0/10", "170/210"]
    x = np.arange(3)
    w = 0.36
    for off, vals, labs, c, name in [(-w / 2, X, nX, BLUE, "player X"), (w / 2, Y, nY, GREY, "player Y")]:
        ax.bar(x + off, vals, width=w, color=c, label=name, zorder=2)
        for xi, v in zip(x + off, vals):
            ax.text(xi, v + 1.5, f"{v:.0f}%" if v == int(v) else f"{v:.1f}%", ha="center", va="bottom", fontsize=FS)
    ax.set_xticks(x)
    ax.set_xticklabels([f"{c}\nX {a}, Y {b}" for c, a, b in zip(cats, nX, nY)], fontsize=FS)
    ax.set_ylim(0, 115)
    ax.set_ylabel("make rate", fontsize=FS)
    ax.legend(fontsize=FS, frameon=False, loc="upper center", ncol=2, bbox_to_anchor=(0.5, 1.02))


@figure("f02_size_bias", w=5.0, h=2.6, axis=True)
def _(ax):
    cats = ["length 5", "length 15"]
    x = np.arange(2)
    w = 0.36
    equal = [0.5, 0.5]
    landed = [5 / 20, 15 / 20]
    ax.bar(x - w / 2, equal, width=w, color=GREY, label="each length equally likely", zorder=2)
    ax.bar(x + w / 2, landed, width=w, color=ORANGE, label="chance you land in it", zorder=2)
    for xi, v in zip(x - w / 2, equal):
        ax.text(xi, v + 0.02, f"{v:.2f}", ha="center", va="bottom", fontsize=FS)
    for xi, v in zip(x + w / 2, landed):
        ax.text(xi, v + 0.02, ["1/4", "3/4"][int(xi > 0.5)], ha="center", va="bottom", fontsize=FS)
    ax.set_xticks(x)
    ax.set_xticklabels(cats, fontsize=FS)
    ax.set_ylim(0, 1.0)
    ax.set_ylabel("probability", fontsize=FS)
    ax.set_title(r"bus: $E[W]=\frac{1}{4}\cdot2.5+\frac{3}{4}\cdot7.5=6.25$;  class: $E=\frac{1}{4}\cdot5+\frac{3}{4}\cdot15=12.5$",
                 fontsize=FS)
    ax.legend(fontsize=FS, frameon=False, loc="upper left")


# -------------------------------------------------------- prisoners / Polya

@figure("f02_prisoners", w=4.8, h=2.5, axis=True)
def _(ax):
    names = ["A", "B", "C"]
    prior = [1 / 3, 1 / 3, 1 / 3]
    coin = [1 / 3, 0.0, 2 / 3]   # guard flips a coin when A is pardoned
    fixed = [1 / 2, 0.0, 1 / 2]  # guard always names B when A is pardoned
    x = np.arange(3)
    w = 0.26
    series = [(prior, GREY, "prior"), (coin, BLUE, "coin rule"), (fixed, ORANGE, "fixed rule")]
    for k, (vals, c, lab) in enumerate(series):
        ax.bar(x + (k - 1) * w, vals, width=w, color=c, label=lab, zorder=2)
        for xi, v in zip(x + (k - 1) * w, vals):
            txt = {0.0: "0", 1 / 3: "1/3", 2 / 3: "2/3", 0.5: "1/2"}[round(v, 9) if v == 0 else v]
            ax.text(xi, v + 0.015, txt, ha="center", va="bottom", fontsize=FS - 0.5)
    ax.set_xticks(x)
    ax.set_xticklabels(names, fontsize=FS)
    ax.set_ylim(0, 0.85)
    ax.set_ylabel(r"$P(\mathrm{pardoned}\mid\mathrm{says}\ B)$", fontsize=FS)
    ax.legend(fontsize=FS, frameon=False, loc="upper left", ncol=3)


@figure("f02_polya_tree", w=5.0, h=2.9, axis=False)
def _(ax):
    # Urn starts 1 red, 1 black; draw, return it plus one more of the same colour.
    start = (0.5, 1.8)
    N1, N2 = (2.0, 2.8), (2.0, 0.8)
    L = {"RR": (4.0, 3.3), "RB": (4.0, 2.3), "BR": (4.0, 1.3), "BB": (4.0, 0.3)}
    _nb(ax, start, "1R 1B", w=1.0, h=0.46)
    _nb(ax, N1, "2R 1B", w=1.0, h=0.46)
    _nb(ax, N2, "1R 2B", w=1.0, h=0.46)
    _leaf(ax, L["RR"], r"RR:  $\frac{1}{3}$", hi=True, w=1.2)
    _leaf(ax, L["RB"], r"RB:  $\frac{1}{6}$", hi=True, w=1.2)
    _leaf(ax, L["BR"], r"BR:  $\frac{1}{6}$", grey=True, w=1.2)
    _leaf(ax, L["BB"], r"BB:  $\frac{1}{3}$", grey=True, w=1.2)
    _edge(ax, start, N1, r"R  $\frac{1}{2}$", lo=(0.0, 0.2))
    _edge(ax, start, N2, r"B  $\frac{1}{2}$", lo=(0.0, -0.2))
    _edge(ax, N1, L["RR"], r"R  $\frac{2}{3}$", lo=(0.0, 0.18))
    _edge(ax, N1, L["RB"], r"B  $\frac{1}{3}$", lo=(0.0, -0.18))
    _edge(ax, N2, L["BR"], r"R  $\frac{1}{3}$", lo=(0.0, 0.18))
    _edge(ax, N2, L["BB"], r"B  $\frac{2}{3}$", lo=(0.0, -0.18))
    ax.text(2.3, -0.55, r"$P(\mathrm{R}_2\mid\mathrm{R}_1)=\frac{1/3}{1/2}=\frac{2}{3}$",
            ha="center", va="center", fontsize=FS)
    ax.set_xlim(-0.3, 4.9); ax.set_ylim(-0.9, 3.8)


@figure("f02_uniform_counts", w=4.6, h=2.5, axis=True)
def _(ax):
    k = np.arange(4)
    uni = [Fr(1, 4)] * 4
    fixed = [Fr(1, 8), Fr(3, 8), Fr(3, 8), Fr(1, 8)]
    w = 0.36
    ax.bar(k - w / 2, [float(v) for v in uni], width=w, color=BLUE, label=r"unknown $p$, uniform prior", zorder=2)
    ax.bar(k + w / 2, [float(v) for v in fixed], width=w, color=GREY, label=r"fixed $p=\frac{1}{2}$", zorder=2)
    for xi, v in zip(k - w / 2, uni):
        ax.text(xi, float(v) + 0.008, "1/4", ha="center", va="bottom", fontsize=FS)
    for xi, v in zip(k + w / 2, fixed):
        ax.text(xi, float(v) + 0.008, f"{v.numerator}/{v.denominator}", ha="center", va="bottom", fontsize=FS)
    ax.set_xticks(k)
    ax.set_xlabel("number of heads $k$ in 3 flips", fontsize=FS)
    ax.set_ylabel(r"$P(k)$", fontsize=FS)
    ax.set_ylim(0, 0.5)
    ax.legend(fontsize=FS, frameon=False, loc="upper center", ncol=2)


# --------------------------------------------------- Bayesian continuous priors

@figure("f02_hhh_density", w=4.6, h=2.5, axis=True)
def _(ax):
    p = np.linspace(0, 1, 400)
    post = 4 * p ** 3
    ax.plot(p, post, color=BLUE, lw=2, label=r"posterior $4p^3$")
    ax.axhline(1, color=GREY, ls="--", lw=1.2, label="uniform prior")
    m = p >= 0.5
    ax.fill_between(p[m], 0, post[m], color=LIGHT_BLUE, zorder=1)
    ax.text(0.73, 0.5, r"$P(p>\frac{1}{2})=\frac{15}{16}$", fontsize=FS, ha="center")
    ax.set_xlabel("bias $p$", fontsize=FS)
    ax.set_ylabel("density", fontsize=FS)
    ax.set_xlim(0, 1); ax.set_ylim(0, 4.4)
    ax.legend(fontsize=FS, frameon=False, loc="upper left")


@figure("f02_normal_posterior", w=4.6, h=2.5, axis=True)
def _(ax):
    mu = np.linspace(-3, 4.5, 500)
    pdf = lambda x, m, v: np.exp(-(x - m) ** 2 / (2 * v)) / np.sqrt(2 * np.pi * v)
    prior = pdf(mu, 0, 1)
    post = pdf(mu, 1, 0.5)
    lik = np.exp(-(2 - mu) ** 2 / 2)
    lik = lik * post.max() / lik.max()
    ax.plot(mu, prior, color=GREY, ls="--", lw=1.4, label=r"prior $N(0,1)$")
    ax.plot(mu, lik, color=ORANGE, lw=1.4, label=r"likelihood at $x=2$ (scaled)")
    ax.plot(mu, post, color=BLUE, lw=2, label=r"posterior $N(1,\frac{1}{2})$")
    ax.fill_between(mu, 0, post, color=LIGHT_BLUE, alpha=0.6, zorder=0)
    ax.set_xlabel(r"$\mu$", fontsize=FS)
    ax.set_ylabel("density", fontsize=FS)
    ax.set_ylim(0, 0.75)
    ax.legend(fontsize=FS - 0.5, frameon=False, loc="upper left")


# ------------------------------------------------------ conditional independence

@figure("f02_bias_tree", w=4.8, h=3.0, axis=False)
def _(ax):
    # Bias is 0.2 or 0.8 with prob 1/2; flips independent given the bias.
    root = (0.4, 1.5)
    B = {0.2: (1.5, 2.6), 0.8: (1.5, 0.4)}
    H = {0.2: (2.9, 2.6), 0.8: (2.9, 0.4)}
    LF = {0.2: (4.6, 2.6), 0.8: (4.6, 0.4)}
    _nb(ax, root, "bias", w=0.8, h=0.46)
    for p in (0.2, 0.8):
        _nb(ax, B[p], f"bias {p}", w=1.1, h=0.46)
        _nb(ax, H[p], "H_1", w=0.8, h=0.46)
        _leaf(ax, LF[p], f"H_1 H_2: {0.5 * p * p:.2f}", w=1.6, hi=(p == 0.8))
    for p in (0.2, 0.8):
        up = p == 0.2
        _edge(ax, root, B[p], r"$\frac{1}{2}$", lo=(-0.15, 0.15) if up else (-0.15, -0.15))
        _edge(ax, B[p], H[p], f"{p}", lo=(0.0, 0.2 if up else -0.2))
        _edge(ax, H[p], LF[p], f"{p}", lo=(0.0, 0.2 if up else -0.2))
    ax.text(2.6, -0.8, r"$P(H_1H_2)=0.02+0.32=0.34$ vs $P(H_1)^2=0.25$",
            ha="center", va="center", fontsize=FS)
    ax.set_xlim(-0.2, 5.8); ax.set_ylim(-1.1, 3.4)


@figure("f02_phi_range", w=5.0, h=2.7, axis=True)
def _(ax):
    pA, pB = 0.3, 0.5
    sd = np.sqrt(pA * (1 - pA) * pB * (1 - pB))
    pab = np.linspace(0, 0.3, 200)
    rho = (pab - pA * pB) / sd
    ax.plot(pab, rho, color=BLUE, lw=2)
    ax.axhline(0, color=GREY, lw=0.8)
    ax.plot([0.15], [0.0], "o", color=GREY, ms=6)
    ax.annotate("independent", (0.15, 0), xytext=(0.04, 0.3), fontsize=FS, arrowprops=dict(arrowstyle="-", color=GREY))
    ax.plot([0.2], [(0.2 - 0.15) / sd], "o", color=ORANGE, ms=7)
    ax.annotate(r"$P(A\cap B)=0.2$: $\rho\approx0.218$", (0.2, (0.2 - 0.15) / sd),
                xytext=(0.012, 0.5), fontsize=FS, color=ORANGE, arrowprops=dict(arrowstyle="-", color=ORANGE))
    ax.plot([0.0, 0.3], [rho[0], rho[-1]], "o", color=INK, ms=4)
    ax.text(0.01, rho[0] - 0.05, r"$-0.655$", fontsize=FS, ha="left", va="top")
    ax.text(0.3, rho[-1] + 0.06, r"$+0.655$", fontsize=FS, ha="right", va="bottom")
    ax.set_xlabel(r"$P(A\cap B)$", fontsize=FS)
    ax.set_ylabel(r"$\rho(A,B)$", fontsize=FS)
    ax.yaxis.set_label_coords(-0.16, 0.5)
    ax.set_xlim(-0.01, 0.31); ax.set_ylim(-0.85, 0.85)


@figure("f02_borel_sphere", w=5.2, h=2.7, axis=False)
def _(ax):
    L = ax.inset_axes([0.03, 0.30, 0.43, 0.60])
    R = ax.inset_axes([0.55, 0.30, 0.43, 0.60])
    th = np.linspace(-90, 90, 400)
    dens = 0.5 * np.cos(np.radians(th))
    L.plot(th, dens, color=INK, lw=1.6)
    m = th > 45
    L.fill_between(th[m], 0, dens[m], color=LIGHT_BLUE, zorder=1)
    L.set_xlabel("latitude (deg)", fontsize=FS)
    L.set_ylabel("density per radian", fontsize=FS)
    L.set_title("meridian: $\\frac{1}{2}\\cos\\theta$", fontsize=FS)
    L.set_xticks([-90, -45, 0, 45, 90])
    L.tick_params(labelsize=FS)
    lon = np.linspace(-180, 180, 2)
    u = 1 / (2 * np.pi)  # uniform longitude on (-pi, pi), per radian, same scale as the meridian
    R.plot(lon, [u, u], color=INK, lw=1.6)
    R.fill_between([-90, 90], 0, u, color=LIGHT_BLUE, zorder=1)
    R.set_xlim(-180, 180)
    R.set_ylim(0, 0.55)
    L.set_ylim(0, 0.55)
    R.set_xlabel("longitude (deg)", fontsize=FS)
    R.set_title("equator: uniform longitude", fontsize=FS)
    R.set_xticks([-180, -90, 0, 90, 180])
    R.tick_params(labelsize=FS)
    R.set_yticks([])
    ax.text(0.5, 0.03, r"$P(\mathrm{lat}>45^\circ)=\frac{2-\sqrt{2}}{4}\approx0.146$;   $P(|\mathrm{lon}|<90^\circ)=\frac{1}{2}$",
            transform=ax.transAxes, ha="center", va="center", fontsize=FS)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)


@figure("f02_two_coins_tree", w=4.8, h=2.7, axis=False)
def _(ax):
    # Coin A fair, coin B P(H)=0.9, each chosen with prob 1/2; two flips both heads.
    root = (0.4, 1.4)
    nA, hA, lA = (1.6, 2.5), (2.9, 2.5), (4.5, 2.5)
    nB, hB, lB = (1.6, 0.3), (2.9, 0.3), (4.5, 0.3)
    _nb(ax, root, "coin", w=0.8, h=0.46)
    _nb(ax, nA, "coin A", w=1.1, h=0.46)
    _nb(ax, hA, "H", w=0.7, h=0.46)
    _nb(ax, nB, "coin B", w=1.1, h=0.46)
    _nb(ax, hB, "H", w=0.7, h=0.46)
    _leaf(ax, lA, "A, HH: 0.125", grey=True, w=1.6)
    _leaf(ax, lB, "B, HH: 0.405", hi=True, w=1.6)
    _edge(ax, root, nA, r"$\frac{1}{2}$", lo=(-0.15, 0.15))
    _edge(ax, root, nB, r"$\frac{1}{2}$", lo=(-0.15, -0.15))
    _edge(ax, nA, hA, r"$\frac{1}{2}$", lo=(0.0, 0.2))
    _edge(ax, hA, lA, r"$\frac{1}{2}$", lo=(0.0, 0.2))
    _edge(ax, nB, hB, "0.9", lo=(0.0, 0.2))
    _edge(ax, hB, lB, "0.9", lo=(0.0, 0.2))
    ax.text(2.6, -0.8, r"$P(B\mid HH)=\frac{0.405}{0.530}=\frac{81}{106}\approx0.764$",
            ha="center", va="center", fontsize=FS)
    ax.set_xlim(-0.2, 5.5); ax.set_ylim(-1.1, 3.2)


# ------------------------------------------------------------- two envelopes

@figure("f02_envelope_naive", w=4.6, h=2.5, axis=True)
def _(ax):
    a = np.array([1, 2, 4])
    naive = 5 * a / 4
    true = np.array([2.0, 2.5, 2.0])  # E[B | A=a]
    x = np.arange(3)
    w = 0.36
    ax.bar(x - w / 2, naive, width=w, color=GREY, label="naive 5a/4", zorder=2)
    ax.bar(x + w / 2, true, width=w, color=BLUE, label="true E[B | A=a]", zorder=2)
    for xi, v in zip(x - w / 2, naive):
        ax.text(xi, v + 0.1, f"{v:g}" if v == int(v) else f"{v:.2f}", ha="center", va="bottom", fontsize=FS)
    for xi, v in zip(x + w / 2, true):
        ax.text(xi, v + 0.1, f"{v:g}" if v == int(v) else f"{v:.1f}", ha="center", va="bottom", fontsize=FS)
    ax.set_xticks(x)
    ax.set_xticklabels([f"$a={v}$" for v in a], fontsize=FS)
    ax.set_ylim(0, 6.2)
    ax.set_ylabel("expected other amount", fontsize=FS)
    ax.legend(fontsize=FS, frameon=False, loc="upper left")
