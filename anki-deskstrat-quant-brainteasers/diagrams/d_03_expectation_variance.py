"""Figures for cards/03_expectation_variance.json."""
import math
import numpy as np
from math import comb, factorial
from qcfig import *

# ---------- indicators and linearity ----------

@figure("f03_hat_matching", w=4.8, h=2.6, axis=False)
def _(ax):
    # one example permutation: person i receives hat sigma[i]; fixed points are matches
    sigma = {1: 1, 2: 4, 3: 3, 4: 2}
    for i in range(1, 5):
        y = 4 - i
        box(ax, (0.0, y), f"person {i}", w=1.5, h=0.5, fs=10)
        box(ax, (3.0, y), f"hat {sigma[i]}", w=1.5, h=0.5, fs=10)
    for i in range(1, 5):
        y0, y1 = 4 - i, 4 - sigma[i]
        hit = sigma[i] == i
        col = GREEN if hit else GREY
        arrow(ax, (0.78, y0), (2.22, y1), color=col, shrink=0, lw=1.6 if hit else 1.1)
        ax.text(4.25, 4 - i, f"$I_{i}={1 if hit else 0}$", va="center", ha="left", fontsize=10,
                color=col if hit else INK)
    frame(ax, -0.9, 5.3, -0.9, 4.0)
    caption(ax, r"$M=\sum_i I_i=2$ here;  $E[M]=4\cdot\frac{1}{4}=1$,  $\mathrm{Var}(M)=1$")


@figure("f03_records", w=4.6, h=2.4)
def _(ax):
    i = np.arange(1, 6)
    p = 1 / i
    ax.bar(i, p, width=0.55, color=[BLUE] * 5, edgecolor=BLUE)
    labels = [r"$1$", r"$\frac{1}{2}$", r"$\frac{1}{3}$", r"$\frac{1}{4}$", r"$\frac{1}{5}$"]
    for x, y, t in zip(i, p, labels):
        ax.text(x, y + 0.04, t, ha="center", va="bottom", fontsize=10)
    ax.set_xticks(i)
    ax.set_xlabel("draw $i$")
    ax.set_ylabel(r"$P(\mathrm{record\ at}\ i)$")
    ax.set_ylim(0, 1.3)
    ax.text(5.4, 1.2, r"$E[\mathrm{records}]=\sum_i\frac{1}{i}=H_5=\frac{137}{60}$",
            ha="right", va="top", fontsize=9.5)


@figure("f03_ascent_chain", w=5.2, h=2.3, axis=False)
def _(ax):
    n = 10
    for k in range(1, n + 1):
        box(ax, (k, 0), rf"$\pi_{{{k}}}$", w=0.72, h=0.5, fs=9.5)
    for k in range(1, n):
        ax.annotate("", xy=(k + 1, 0.3), xytext=(k, 0.3),
                    arrowprops=dict(arrowstyle="-", color=BLUE, lw=1.3,
                                    connectionstyle="arc3,rad=-0.7"))
        ax.text(k + 0.5, 0.78, rf"$A_{{{k}}}$", ha="center", va="center", fontsize=9.5, color=BLUE)
    ax.text(1.0, -0.62, r"$\mathrm{Cov}(A_k,A_{k+1})=\frac{1}{6}-\frac{1}{4}=-\frac{1}{12}$;"
            r"  $\mathrm{Cov}=0$ if $|k-j|\geq 2$", ha="left", va="center", fontsize=9.5, color=RED)
    ax.text(1.0, -1.25, r"$\mathrm{Var}(A)=9\cdot\frac{1}{4}+2\cdot 8\cdot\left(-\frac{1}{12}\right)"
            r"=\frac{9}{4}-\frac{4}{3}=\frac{11}{12}$", ha="left", va="center", fontsize=9.5)
    frame(ax, 0.2, 10.8, -1.7, 1.2)


@figure("f03_derangement_series", w=5.0, h=2.6)
def _(ax):
    # inclusion-exclusion partial sums for P(no fixed point), n = 10
    n = 10
    j = np.arange(n + 1)
    partial = np.cumsum([(-1) ** jj / factorial(jj) for jj in j])
    ax.axhline(1 / math.e, color=GREY, ls="--", lw=1.1)
    ax.text(9.8, 1 / math.e + 0.06, r"$\frac{1}{e}\approx 0.3679$", ha="right", va="bottom", fontsize=9.5,
            color=GREY)
    ax.plot(j, partial, "o-", color=BLUE, ms=4, lw=1.4)
    ax.plot([n], [partial[-1]], "o", color=ORANGE, ms=7, zorder=5)
    ax.text(n - 0.25, partial[-1] - 0.2, r"$j=10:\ \frac{16481}{44800}\approx 0.36788$", ha="right",
            va="top", fontsize=9.5, color=ORANGE)
    ax.set_xticks(j)
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-0.1, 1.15)
    ax.set_xlabel(r"$j$ (number of terms kept)")
    ax.set_ylabel(r"partial sum $S_j$")
    ax.text(10.3, 1.02, r"$S_j=\sum_{i\leq j}\frac{(-1)^i}{i!}$", ha="right", va="top", fontsize=9.5)
    assert abs(partial[-1] - 16481 / 44800) < 1e-12


# ---------- coupon-collector stage timelines ----------

def _timeline(ax, means, labels, total_text, xmax):
    t = 0.0
    edges = []
    for j, (m, lab) in enumerate(zip(means, labels)):
        col = ORANGE if j == len(means) - 1 else BLUE
        fill = LIGHT_ORANGE if j == len(means) - 1 else LIGHT_BLUE
        ax.broken_barh([(t, m)], (0, 0.6), facecolors=fill, edgecolors=col, linewidth=1.2)
        ax.text(t + m / 2, 0.3, lab, ha="center", va="center", fontsize=9.5, color=INK)
        t += m
        edges.append(t)
    for j, x in enumerate(edges, start=1):
        ax.plot([x, x], [0, -0.15], color=INK, lw=0.9)
        ax.text(x, -0.22, str(j), ha="center", va="top", fontsize=9.5)
    ax.text(0.0, -0.55, "distinct values seen (tick)", ha="left", va="top", fontsize=9, color=GREY)
    ax.text(xmax, 0.95, total_text, ha="right", va="bottom", fontsize=10)
    ax.set_xlim(-0.2, xmax + 0.2)
    ax.set_ylim(-0.9, 1.4)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.set_xlabel("expected rolls (cumulative)")


@figure("f03_coupon_stages", w=5.2, h=2.4)
def _(ax):
    # stage j: go from j-1 to j distinct faces, success prob (6-(j-1))/6, mean 6/(7-j)
    means = [6 / (7 - j) for j in range(1, 7)]
    labels = ["1", r"$\frac{6}{5}$", r"$\frac{3}{2}$", "2", "3", "6"]
    _timeline(ax, means, labels, r"$E[T]=6H_6=\frac{147}{10}=14.7$", 15.0)


@figure("f03_coupon_10_k4", w=5.2, h=2.4)
def _(ax):
    # collect 4 of 10 types: stage j (j distinct held) has mean 10/(10-j), j=0..3
    means = [10 / (10 - j) for j in range(0, 4)]
    labels = ["1", r"$\frac{10}{9}$", r"$\frac{10}{8}$", r"$\frac{10}{7}$"]
    _timeline(ax, means, labels, r"$E[T]=\frac{1207}{252}\approx 4.79$", 5.2)


# ---------- tail sums: area under the survival function ----------

@figure("f03_tail_max_dice", w=5.0, h=2.6)
def _(ax):
    k = np.arange(1, 7)
    surv = np.array([1 - ((kk - 1) / 6) ** 2 for kk in k])
    ax.bar(k, surv, width=1.0, color=LIGHT_BLUE, edgecolor=BLUE, lw=1.2)
    labs = [r"$1$", r"$\frac{35}{36}$", r"$\frac{8}{9}$", r"$\frac{3}{4}$", r"$\frac{5}{9}$",
            r"$\frac{11}{36}$"]
    for x, y, t in zip(k, surv, labs):
        ax.text(x, y + 0.03, t, ha="center", va="bottom", fontsize=9.5)
    ax.set_xticks(k)
    ax.set_xlim(0.4, 6.6)
    ax.set_ylim(0, 1.4)
    ax.set_xlabel(r"$k$")
    ax.set_ylabel(r"$P(M\geq k)$")
    ax.text(6.5, 1.35, r"$E[M]=\sum_{k\geq 1}P(M\geq k)=\frac{161}{36}\approx 4.47$",
            ha="right", va="top", fontsize=9.5)


@figure("f03_tail_stick_min", w=4.8, h=2.6)
def _(ax):
    t = np.linspace(0, 1 / 3, 300)
    s = (1 - 3 * t) ** 2
    ax.fill_between(t, 0, s, color=LIGHT_BLUE, zorder=1)
    ax.plot(t, s, color=BLUE, lw=1.8)
    ax.set_xlim(-0.01, 0.42)
    ax.set_ylim(0, 1.15)
    ax.set_xlabel(r"$t$")
    ax.set_ylabel(r"$P(L_{\min}>t)$")
    ax.text(0.2, 0.62, r"$\int_0^{1/3}(1-3t)^2\,dt=\frac{1}{9}$", ha="left", va="center", fontsize=10,
            color=INK)


@figure("f03_tail_max9", w=4.8, h=2.6)
def _(ax):
    x = np.linspace(0, 1, 300)
    surv = 1 - x ** 9
    ax.fill_between(x, 0, surv, color=LIGHT_BLUE, zorder=1)
    ax.plot(x, surv, color=BLUE, lw=1.8, label=r"$P(M>x)=1-x^9$")
    ax.plot(x, x ** 9, color=GREY, lw=1.3, ls="--", label=r"$P(M\leq x)=x^9$")
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(0, 1.12)
    ax.set_xlabel(r"$x$")
    ax.set_ylabel("probability")
    ax.text(0.2, 0.62, r"$E[M]=\int_0^1(1-x^9)\,dx=\frac{9}{10}$", ha="left", va="center", fontsize=10)
    ax.legend(loc="lower left", bbox_to_anchor=(0.0, 0.0), fontsize=9, frameon=True, facecolor="white", edgecolor="none", framealpha=1.0)


@figure("f03_max_density", w=4.6, h=2.5)
def _(ax):
    x = np.linspace(0, 1, 300)
    ax.fill_between(x[x <= 2 / 3], 0, 2 * x[x <= 2 / 3], color=LIGHT_BLUE, zorder=1)
    ax.plot(x, 2 * x, color=BLUE, lw=1.8)
    ax.axvline(2 / 3, color=ORANGE, ls="--", lw=1.2)
    ax.axvline(1 / math.sqrt(2), color=GREY, ls=":", lw=1.2)
    ax.text(2 / 3 - 0.02, 2.25, r"$E[M]=\frac{2}{3}$", ha="right", va="center", fontsize=9.5, color=ORANGE)
    ax.text(1 / math.sqrt(2) + 0.02, 2.25, "median", ha="left", va="center", fontsize=9, color=GREY)
    ax.text(0.33, 0.22, r"$P(M\leq\frac{2}{3})=\frac{4}{9}$", ha="center", va="center", fontsize=9.5)
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(0, 2.5)
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"density of $M$")


@figure("f03_distinct_pmf", w=4.8, h=2.6)
def _(ax):
    def surj(n, k):
        return sum((-1) ** j * comb(k, j) * (k - j) ** n for j in range(k + 1))
    ks = np.arange(1, 6)
    pmf = np.array([comb(6, k) * surj(5, k) / 6 ** 5 for k in ks])
    mean = float(np.sum(ks * pmf))
    ax.bar(ks, pmf, width=0.55, color=LIGHT_BLUE, edgecolor=BLUE)
    labs = [r"$\frac{1}{1296}$", r"$\frac{25}{432}$", r"$\frac{125}{324}$", r"$\frac{25}{54}$",
            r"$\frac{5}{54}$"]
    for x, y, t in zip(ks, pmf, labs):
        ax.text(x, y + 0.012, t, ha="center", va="bottom", fontsize=9)
    ax.axvline(mean, color=ORANGE, ls="--", lw=1.2)
    ax.text(mean - 0.08, 0.52, rf"$E[D]={mean:.3f}$", ha="right", va="center", fontsize=9.5, color=ORANGE)
    ax.set_xticks(ks)
    ax.set_xlim(0.4, 5.6)
    ax.set_ylim(0, 0.56)
    ax.set_xlabel(r"distinct values $D=k$")
    ax.set_ylabel(r"$P(D=k)$")
    assert abs(mean - 4651 / 1296) < 1e-12


# ---------- optimal stopping ----------

@figure("f03_dice_policy", w=5.2, h=2.5, axis=False)
def _(ax):
    # threshold with r rolls left after this one: keep x if x >= V_r, V_2=17/4, V_1=7/2
    keep_from = {2: 5, 1: 4, 0: 1}   # keyed by row y; roll 1: keep 5,6 (>= 17/4); roll 2: keep 4,5,6 (>= 7/2); roll 3: keep all
    rows = [(2, "roll 1:  keep if $X\\geq\\frac{17}{4}$"),
            (1, "roll 2:  keep if $X\\geq\\frac{7}{2}$"),
            (0, "roll 3:  keep all")]
    for face in range(1, 7):
        ax.text(face - 0.5, 3.0, str(face), ha="center", va="center", fontsize=10)
    for r, label in rows:
        y = r
        ax.text(-0.15, y, label, ha="right", va="center", fontsize=9.5)
        for face in range(1, 7):
            keep = face >= keep_from[r]
            fc = LIGHT_BLUE if keep else "white"
            ec = BLUE if keep else GREY
            ax.add_patch(Rectangle((face - 1 + 0.04, y - 0.38), 0.92, 0.76, fc=fc, ec=ec, lw=1.1, zorder=2))
            ax.text(face - 0.5, y, "keep" if keep else "roll", ha="center", va="center", fontsize=9,
                    color=BLUE if keep else GREY, zorder=3)
    ax.text(3.0, -0.95, r"values:  $V_1=\frac{7}{2}$,  $V_2=\frac{17}{4}$,  $V_3=\frac{14}{3}\approx 4.67$",
            ha="center", va="center", fontsize=9.5)
    frame(ax, -3.2, 6.1, -1.3, 3.5)


# ---------- random walk with a barrier ----------

@figure("f03_wald_path", w=5.0, h=2.6)
def _(ax):
    rng = np.random.default_rng(2)
    s, path = 0, [0]
    while s < 10:
        s += int(rng.integers(1, 7))
        path.append(s)
    n = len(path) - 1
    ax.step(range(n + 1), path, where="post", color=BLUE, lw=1.6)
    ax.plot(range(n + 1), path, "o", color=BLUE, ms=4)
    ax.axhline(10, color=GREEN, ls="--", lw=1.1)
    ax.text(0.05, 10.35, "stop at first $S_n\\geq 10$", color=GREEN, fontsize=9, va="bottom")
    ax.plot(n, path[-1], "o", color=ORANGE, ms=7, zorder=5)
    ax.text(n + 0.25, path[-1], rf"$S_N={path[-1]}$, overshoot", ha="left", va="center",
            fontsize=9.5, color=ORANGE)
    ax.text(0.0, 13.2, r"$E[S_N]=\frac{7}{2}E[N]\approx 11.63$  (from Wald's identity)", ha="left",
            va="center", fontsize=9.5, color=INK)
    ax.set_xticks(range(0, n + 1))
    ax.set_xlim(-0.2, n + 2.2)
    ax.set_ylim(-0.8, 14)
    ax.set_xlabel("roll $n$")
    ax.set_ylabel(r"running total $S_n$")


# ---------- St Petersburg levels ----------

@figure("f03_stpete_levels", w=5.2, h=2.5)
def _(ax):
    k = np.arange(1, 21)
    ax.bar(k, np.ones(20), width=0.7, color=LIGHT_BLUE, edgecolor=BLUE)
    ax.bar([21], [1.0], width=0.7, color=LIGHT_ORANGE, edgecolor=ORANGE)
    ax.set_xticks([1, 5, 10, 15, 20])
    ax.text(21, 0.5, "tail", ha="center", va="center", fontsize=9, color=ORANGE, rotation=90)
    ax.set_ylim(0, 1.45)
    ax.set_xlim(0, 22.2)
    ax.set_xlabel(r"level $K=k$")
    ax.set_ylabel("contribution")
    ax.text(0.5, 1.38, r"$P(K{=}k)\,2^k=1$ for each $k\leq 20$;  tail $2^{20}P(K>20)=1$",
            ha="left", va="top", fontsize=9.5)
    ax.text(21.5, 1.2, "total\n$=21$", ha="center", va="center", fontsize=9.5, color=ORANGE)


# ---------- log utility ----------

@figure("f03_log_fee", w=5.0, h=2.6)
def _(ax):
    c = np.linspace(0, 20, 400)
    ks = np.arange(1, 60)
    g = np.array([np.sum(2.0 ** -ks * np.log(1000 - cc + 2.0 ** ks)) for cc in c])
    lw0 = math.log(1000)
    ax.plot(c, g, color=BLUE, lw=1.8)
    ax.axhline(lw0, color=ORANGE, ls="--", lw=1.1)
    # root of g(c) = log(1000), by bisection
    lo, hi = 0.0, 999.0
    for _ in range(200):
        mid = (lo + hi) / 2
        val = np.sum(2.0 ** -ks * np.log(1000 - mid + 2.0 ** ks))
        if val > lw0:
            lo = mid
        else:
            hi = mid
    cstar = (lo + hi) / 2
    ax.plot([cstar], [lw0], "o", color=ORANGE, ms=6, zorder=5)
    ax.plot([cstar, cstar], [6.89, lw0], color=ORANGE, lw=0.9, ls=":")
    ax.text(cstar + 0.4, 6.9155, rf"$c^*\approx {cstar:.2f}$", ha="left", va="center", fontsize=10,
            color=ORANGE)
    ax.text(18.8, lw0 + 0.0022, r"$\log 1000$", ha="right", va="bottom", fontsize=9, color=ORANGE)
    ax.set_xlim(0, 20)
    ax.set_ylim(6.89, 6.925)
    ax.set_xlabel("fee $c$ (dollars)")
    ax.set_ylabel(r"$E[\log(1000-c+2^K)]$")
    assert abs(cstar - 10.954) < 0.01


# ---------- Jensen ----------

@figure("f03_jensen_chord", w=5.0, h=2.6)
def _(ax):
    x = np.linspace(0.7, 6.4, 300)
    ax.plot(x, 1 / x, color=BLUE, lw=1.8)
    xs = np.arange(1, 7)
    ax.plot([1, 6], [1, 1 / 6], color=GREY, ls="--", lw=1.1)
    ax.text(1.5, 0.88, "chord", color=GREY, fontsize=9, ha="left", va="bottom")
    ax.plot(xs, 1 / xs, "o", color=BLUE, ms=5, zorder=4)
    mean_val = sum(1 / v for v in xs) / 6
    ax.axhline(mean_val, color=ORANGE, ls="--", lw=1.1)
    ax.text(6.35, 0.92, r"orange: $E[1/X]=\frac{49}{120}\approx 0.408$", ha="right", va="center",
            fontsize=9.5, color=ORANGE)
    ax.plot([3.5], [1 / 3.5], "o", color=GREEN, ms=6, zorder=5)
    ax.text(3.2, 0.06, r"green: $1/E[X]=\frac{2}{7}$ at $x=\frac{7}{2}$", ha="left", va="center", fontsize=9.5,
            color=GREEN)
    ax.set_xticks(xs)
    ax.set_xlim(0.6, 6.5)
    ax.set_ylim(0, 1.12)
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$1/x$")
    assert abs(mean_val - 49 / 120) < 1e-12


# ---------- law of total variance ----------

def _mixture(ax, n, p1, p2, mean_fmt, total_text):
    k = np.arange(0, n + 1)
    pmf1 = np.array([comb(n, j) * p1 ** j * (1 - p1) ** (n - j) for j in k])
    pmf2 = np.array([comb(n, j) * p2 ** j * (1 - p2) ** (n - j) for j in k])
    mix = 0.5 * (pmf1 + pmf2)
    ax.bar(k, mix, width=0.7, color=LIGHT_BLUE, edgecolor=GREY, lw=0.6, zorder=1,
           label=r"mixture $P(X=x)$")
    ax.plot(k, 0.5 * pmf1, "o-", color=BLUE, lw=1.4, ms=3.5, zorder=3, label=mean_fmt[0])
    ax.plot(k, 0.5 * pmf2, "o-", color=ORANGE, lw=1.4, ms=3.5, zorder=3, label=mean_fmt[1])
    m1, m2 = n * p1, n * p2
    ax.axvline(m1, color=BLUE, ls="--", lw=1.0, ymax=0.55)
    ax.axvline(m2, color=ORANGE, ls="--", lw=1.0, ymax=0.55)
    ax.set_xticks(k)
    ax.set_xlabel(r"$X$ (heads)")
    ax.set_ylabel(r"$P(X=x)$")
    ax.set_ylim(0, mix.max() * 1.75)
    ax.legend(loc="upper left", fontsize=9, frameon=False, handlelength=1.6)
    ax.text(n + 0.5, mix.max() * 1.7, total_text, ha="right", va="top", fontsize=9.5)


@figure("f03_var_mixture", w=5.2, h=2.7)
def _(ax):
    _mixture(ax, 10, 0.25, 0.75,
             (r"$p=\frac{1}{4}$: $E[X\mid p]=\frac{5}{2}$", r"$p=\frac{3}{4}$: $E[X\mid p]=\frac{15}{2}$"),
             r"$\mathrm{Var}(X)=\frac{15}{8}+\frac{25}{4}=\frac{65}{8}$")


@figure("f03_var_mixture_5", w=5.2, h=2.7)
def _(ax):
    _mixture(ax, 5, 0.1, 0.9,
             (r"$p=0.1$: $E[X\mid p]=0.5$", r"$p=0.9$: $E[X\mid p]=4.5$"),
             r"$\mathrm{Var}(X)=0.45+4=4.45$")


# ---------- Markov chains for patterns ----------

def _pattern_chain(ax, pH, pT, lab_H, lab_T, a_val, b_val):
    """States: start (S), last flip H (H), done (D). Absorbing D in green."""
    S, Hs, D = (0.0, 0.0), (2.6, 0.0), (5.2, 0.0)
    node(ax, S, f"$a={a_val}$", r=0.4)
    node(ax, Hs, f"$b={b_val}$", r=0.4)
    node(ax, D, "done", fc=LIGHT_GREEN, ec=GREEN, fs=10, r=0.4)
    ax.text(S[0], -0.7, "start", ha="center", va="center", fontsize=9.5, color=GREY)
    ax.text(Hs[0], -0.7, "last flip H", ha="center", va="center", fontsize=9.5, color=GREY)
    arrow(ax, S, Hs, lab_H, color=BLUE, rad=0.0)
    arrow(ax, Hs, S, lab_T, color=RED, rad=-0.35)
    arrow(ax, Hs, D, lab_H, color=BLUE)
    self_loop(ax, S, lab_T, color=RED)
    frame(ax, -0.6, 5.8, -1.0, 1.25)


@figure("f03_hh_chain", w=4.8, h=2.2, axis=False)
def _(ax):
    # HH: a = 1 + a/2 + b/2, b = 1 + a/2  =>  a = 6, b = 4
    _pattern_chain(ax, 0.5, 0.5, r"$H\ \frac{1}{2}$", r"$T\ \frac{1}{2}$", 6, 4)
    caption(ax, r"$a=1+\frac{1}{2}a+\frac{1}{2}b,\quad b=1+\frac{1}{2}a\ \Rightarrow\ a=6$")


@figure("f03_hh_chain_biased", w=4.8, h=2.2, axis=False)
def _(ax):
    # P(H)=2/3: a = 1 + (2/3) b + (1/3) a, b = 1 + (1/3) a  =>  a = 15/4, b = 9/4
    _pattern_chain(ax, 2 / 3, 1 / 3, r"$H\ \frac{2}{3}$", r"$T\ \frac{1}{3}$",
                   r"\frac{15}{4}", r"\frac{9}{4}")
    caption(ax, r"$a=1+\frac{2}{3}b+\frac{1}{3}a,\quad b=1+\frac{1}{3}a\ \Rightarrow\ a=\frac{15}{4}$")


@figure("f03_ht_chain", w=4.8, h=2.2, axis=False)
def _(ax):
    # HT: states start / last H / done. a = 1 + a/2 + b/2, b = 1 + b/2 => b = 2, a = 4
    S, Hs, D = (0.0, 0.0), (2.6, 0.0), (5.2, 0.0)
    node(ax, S, r"$a=4$", r=0.4)
    node(ax, Hs, r"$b=2$", r=0.4)
    node(ax, D, "done", fc=LIGHT_GREEN, ec=GREEN, fs=10, r=0.4)
    ax.text(S[0], -0.7, "start", ha="center", va="center", fontsize=9.5, color=GREY)
    ax.text(Hs[0], -0.7, "last flip H", ha="center", va="center", fontsize=9.5, color=GREY)
    arrow(ax, S, Hs, r"$H\ \frac{1}{2}$", color=BLUE)
    arrow(ax, Hs, D, r"$T\ \frac{1}{2}$", color=RED)
    self_loop(ax, S, r"$T\ \frac{1}{2}$", color=RED)
    self_loop(ax, Hs, r"$H\ \frac{1}{2}$", color=BLUE)
    frame(ax, -0.6, 5.8, -1.0, 1.25)
    caption(ax, r"$b=1+\frac{1}{2}b\Rightarrow b=2,\quad a=1+\frac{1}{2}a+\frac{1}{2}b\Rightarrow a=4$")


@figure("f03_61_chain", w=4.8, h=2.2, axis=False)
def _(ax):
    # pattern 6 then 1 (no self-overlap): s = 1 + (5/6)s + (1/6)a, a = 1 + (1/6)a + (4/6)s => s=36, a=30
    S, A, D = (0.0, 0.0), (2.6, 0.0), (5.2, 0.0)
    node(ax, S, r"$s=36$", r=0.4)
    node(ax, A, r"$a=30$", r=0.4)
    node(ax, D, "done", fc=LIGHT_GREEN, ec=GREEN, fs=10, r=0.4)
    ax.text(S[0], -0.7, "start", ha="center", va="center", fontsize=9.5, color=GREY)
    ax.text(A[0], -0.7, "last roll 6", ha="center", va="center", fontsize=9.5, color=GREY)
    arrow(ax, S, A, r"$6\ \frac{1}{6}$", color=BLUE, rad=0.0)
    arrow(ax, A, S, r"$2..5\ \frac{4}{6}$", color=RED, rad=-0.35)
    arrow(ax, A, D, r"$1\ \frac{1}{6}$", color=BLUE)
    self_loop(ax, S, r"$\neq 6\ \frac{5}{6}$", color=RED)
    self_loop(ax, A, r"$6\ \frac{1}{6}$", color=BLUE)
    frame(ax, -0.6, 5.8, -1.0, 1.25)
    caption(ax, r"$s=1+\frac{5}{6}s+\frac{1}{6}a,\quad a=1+\frac{1}{6}a+\frac{4}{6}s\ \Rightarrow\ s=36$")


# ---------- geometric probability ----------

@figure("f03_triangle_square", w=4.4, h=3.1)
def _(ax):
    # cuts U, V uniform on the unit square; pieces are min(U,V), |U-V|, 1-max(U,V)
    ax.add_patch(Rectangle((0, 0), 1, 1, fc="white", ec=INK, lw=0.9, zorder=1))
    ax.add_patch(Polygon([(0, 0.5), (0.5, 0.5), (0.5, 1.0)], closed=True, fc=LIGHT_GREEN, ec=GREEN,
                         lw=1.1, zorder=2))
    ax.add_patch(Polygon([(0.5, 0), (0.5, 0.5), (1.0, 0.5)], closed=True, fc=LIGHT_GREEN, ec=GREEN,
                         lw=1.1, zorder=2))
    ax.text(0.31, 0.7, "triangle", ha="center", va="center", fontsize=9, color=GREEN, zorder=3)
    ax.text(0.69, 0.3, "triangle", ha="center", va="center", fontsize=9, color=GREEN, zorder=3)
    ax.plot([0.5, 0.5], [0, 1], color=GREY, ls=":", lw=0.9)
    ax.plot([0, 1], [0.5, 0.5], color=GREY, ls=":", lw=0.9)
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.05, 1.05)
    ax.set_aspect("equal")
    ax.set_xticks([0, 0.5, 1])
    ax.set_xticklabels(["0", r"$\frac{1}{2}$", "1"])
    ax.set_yticks([0, 0.5, 1])
    ax.set_yticklabels(["0", r"$\frac{1}{2}$", "1"])
    ax.set_xlabel(r"first cut $U$")
    ax.set_ylabel(r"second cut $V$")
    ax.text(0.5, -0.36, r"area of green $=2\cdot\frac{1}{8}=\frac{1}{4}$", ha="center", va="top",
            fontsize=9.5, transform=ax.transData)
