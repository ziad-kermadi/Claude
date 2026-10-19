"""Figures for cards/08_stats_regression_ml.json."""
import math
import numpy as np
from qcfig import *
from matplotlib.patches import Circle as _Circle

# ---------- small numeric helpers (no scipy dependency) ----------

def _phi(z):
    return np.exp(-np.asarray(z) ** 2 / 2) / np.sqrt(2 * np.pi)

_ERF = np.vectorize(math.erf)

def _Phi(z):
    return 0.5 * (1 + _ERF(np.asarray(z, dtype=float) / np.sqrt(2)))

def _rect_edge(a, b, hw, hh, pad=0.06):
    """Start/end points on the boundaries of two axis-aligned boxes centred at a and b."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    def t_of(d_x, d_y):
        ts = []
        if abs(d_x) > 1e-12: ts.append(hw / abs(d_x))
        if abs(d_y) > 1e-12: ts.append(hh / abs(d_y))
        return min(ts)
    ta = t_of(dx, dy)
    p0 = (a[0] + dx * ta * (1 + pad), a[1] + dy * ta * (1 + pad))
    p1 = (b[0] - dx * ta * (1 + pad), b[1] - dy * ta * (1 + pad))
    return p0, p1

def _dnode(ax, xy, label, fc="white", ec=INK, dashed=False, w=1.5, h=0.56, fs=10):
    x, y = xy
    ax.add_patch(Rectangle((x - w / 2, y - h / 2), w, h, fc=fc, ec=ec, lw=1.2, zorder=3,
                           ls="--" if dashed else "-"))
    ax.text(x, y, label, ha="center", va="center", fontsize=fs, zorder=4)

def _dedge(ax, a, b, color=INK, label=None, lab_off=(0, 0), fs=10, w=1.5, h=0.56, rad=0.0):
    p0, p1 = _rect_edge(a, b, w / 2, h / 2)
    ax.add_patch(FancyArrowPatch(p0, p1, connectionstyle=f"arc3,rad={rad}", arrowstyle="-|>",
                                 mutation_scale=13, color=color, lw=1.4, zorder=2))
    if label is not None:
        mx, my = (a[0] + b[0]) / 2 + lab_off[0], (a[1] + b[1]) / 2 + lab_off[1]
        ax.text(mx, my, label, ha="center", va="center", fontsize=fs, color=color,
                bbox=dict(fc="white", ec="none", pad=0.8), zorder=5)


# ======================================================================
# Unit 1: Uniform(0, theta) maximum (cards 0-2)
# ======================================================================

@figure("f08_unif_max_density", w=4.6, h=2.4)
def _(ax):
    n, theta = 5, 1.0
    m = np.linspace(0, theta, 800)
    f = n * m ** (n - 1) / theta ** n
    EM = np.trapezoid(m * f, m)
    assert abs(EM - n / (n + 1) * theta) < 1e-4, EM          # card 0: E[M] = 5/6 theta
    ax.fill_between(m, 0, f, color=LIGHT_BLUE, zorder=1)
    ax.plot(m, f, color=BLUE, lw=1.8)
    ax.axvline(EM, color=ORANGE, ls="--", lw=1.3)
    ax.axvline(theta, color=GREEN, ls="--", lw=1.3)
    ax.annotate("", xy=(theta - 0.01, 3.2), xytext=(EM + 0.01, 3.2),
                arrowprops=dict(arrowstyle="<->", color=INK, lw=1.0))
    ax.text(EM - 0.03, 3.45, r"bias $=-\theta/6$", ha="right", fontsize=9.5)
    ax.text(EM - 0.02, 0.35, r"$E[M]=\frac{5}{6}\theta$", ha="right", color=ORANGE, fontsize=10)
    ax.text(theta - 0.02, 1.0, r"$\theta$", ha="right", color=GREEN, fontsize=10)
    ax.set_xlim(0, 1.08); ax.set_ylim(0, 5.0)
    ax.set_xlabel("m"); ax.set_ylabel(r"density of $M$")
    ax.set_title(r"$n=5$, $\theta=1$: density $5m^4$ on $(0,\theta)$", fontsize=10)


# ======================================================================
# Card 10: bias-variance U-curve (degree-15 overfit)
# ======================================================================

@figure("f08_bias_variance_u", w=5.0, h=2.9)
def _(ax):
    rng = np.random.default_rng(3)
    degs = np.arange(1, 16)
    x_grid = np.linspace(0, 1, 300)
    f_true = lambda x: np.sin(2 * np.pi * x)
    sigma, n_pts, trials = 0.3, 20, 300
    tr = np.zeros(len(degs)); te = np.zeros(len(degs))
    for _ in range(trials):
        x = rng.uniform(0, 1, n_pts)
        y = f_true(x) + sigma * rng.standard_normal(n_pts)
        for j, d in enumerate(degs):
            p = np.polynomial.Polynomial.fit(x, y, d, domain=[0, 1])
            tr[j] += np.mean((p(x) - y) ** 2)
            te[j] += np.mean((p(x_grid) - f_true(x_grid)) ** 2)
    tr /= trials; te /= trials
    jstar = int(np.argmin(te))
    ax.semilogy(degs, tr, "o-", color=BLUE, ms=4, label="training error")
    ax.semilogy(degs, te, "o-", color=RED, ms=4, label="error on new points (vs truth)")
    ax.plot(degs[jstar], te[jstar], "o", color=ORANGE, ms=9, zorder=5)
    ax.annotate(f"min at degree {degs[jstar]}", (degs[jstar], te[jstar]), xytext=(degs[jstar] + 1.2, te[jstar] * 0.45),
                fontsize=9.5, color=ORANGE, arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.8))
    ax.text(15, 0.45, "degree 15: fits all 20 points\n(training error near 0)", ha="right", fontsize=9,
            color=BLUE)
    ax.set_xlabel("polynomial degree"); ax.set_ylabel("mean squared error")
    ax.set_xticks([1, 3, 5, 7, 9, 11, 13, 15]); ax.set_ylim(1e-3, 30)
    ax.legend(fontsize=9, frameon=False, loc="lower left")
    ax.set_title(r"$\mathrm{MSE}=\mathrm{bias}^2+\mathrm{variance}+\sigma^2$: averaged over 300 samples",
                 fontsize=10)


# ======================================================================
# Card 9: shrinkage factor c, MSE(c) = (c-1)^2 theta^2 + c^2 s^2
# ======================================================================

@figure("f08_shrink_mse", w=4.8, h=2.7)
def _(ax):
    theta2, s2 = 1.0, 1.0
    c = np.linspace(0, 1.25, 400)
    bias2 = (c - 1) ** 2 * theta2
    var = c ** 2 * s2
    mse = bias2 + var
    cstar = theta2 / (theta2 + s2)
    mse_star = theta2 * s2 / (theta2 + s2)
    assert abs(cstar - 0.5) < 1e-12 and abs(mse_star - 0.5) < 1e-12
    ax.plot(c, mse, color=INK, lw=2.0, label=r"$\mathrm{MSE}(c)$")
    ax.plot(c, bias2, color=BLUE, ls="--", lw=1.3, label=r"bias$^2=(c-1)^2\theta^2$")
    ax.plot(c, var, color=GREY, ls="--", lw=1.3, label=r"variance$=c^2 s^2$")
    ax.plot(cstar, mse_star, "o", color=ORANGE, ms=8, zorder=5)
    ax.text(cstar, mse_star + 0.07, r"$c^*=\frac{1}{2}$", ha="center", fontsize=9.5, color=ORANGE)
    ax.plot(1.0, 1.0, "s", color=GREEN, ms=6)
    ax.text(0.95, 1.12, r"$c=1$: MSE $=s^2=1$", ha="right", fontsize=9.5, color=GREEN)
    ax.set_xlim(0, 1.25); ax.set_ylim(0, 1.7)
    ax.set_xlabel("shrinkage factor $c$"); ax.set_ylabel(r"MSE (units of $\theta^2$)")
    ax.legend(fontsize=9, frameon=False, loc="upper left")
    ax.set_title(r"$c^*=\frac{\theta^2}{\theta^2+s^2}$, MSE$^*=\frac{\theta^2 s^2}{\theta^2+s^2}$",
                 fontsize=10)


# ======================================================================
# Card 11: divisor for variance MSE, n = 10
# ======================================================================

@figure("f08_divisor_mse", w=4.8, h=2.6)
def _(ax):
    n = 10
    c = np.linspace(7, 16, 400)
    mse = (((n - 1) / c - 1) ** 2 + 2 * (n - 1) / c ** 2)   # units of sigma^4
    vals = {d: ((n - 1) / d - 1) ** 2 + 2 * (n - 1) / d ** 2 for d in (9, 10, 11)}
    assert abs(vals[9] - 2 / 9) < 1e-12 and abs(vals[10] - 0.19) < 1e-12
    assert abs(vals[11] - 2 / 11) < 1e-12 and abs(2 / (n + 1) - vals[11]) < 1e-12
    ax.plot(c, mse, color=INK, lw=2.0)
    for d, col in [(9, GREY), (10, BLUE), (11, ORANGE)]:
        ax.plot(d, vals[d], "o", color=col, ms=7, zorder=5)
    ax.text(15.8, 0.345, f"c=9: {vals[9]:.3f}", ha="right", fontsize=9.5, color=GREY)
    ax.text(15.8, 0.322, f"c=10: {vals[10]:.3f}", ha="right", fontsize=9.5, color=BLUE)
    ax.text(15.8, 0.299, f"c=11: {vals[11]:.3f} (minimum)", ha="right", fontsize=9.5, color=ORANGE)
    ax.set_xlim(7, 16); ax.set_ylim(0.16, 0.36)
    ax.set_xlabel(r"divisor $c$ in $\sum(X_i-\bar X)^2/c$")
    ax.set_ylabel(r"MSE / $\sigma^4$")
    ax.set_title(r"$n=10$: minimum at $c=n+1=11$, MSE $=\frac{2}{n+1}\sigma^4$", fontsize=10)


# ======================================================================
# Cards 17-19: Cauchy averages never settle
# ======================================================================

@figure("f08_cauchy_running_mean", w=5.0, h=2.7)
def _(ax):
    N = 2000
    n = np.arange(1, N + 1)
    def run(seed, dist):
        r = np.random.default_rng(seed)
        x = dist(r, N)
        return np.cumsum(x) / n
    cauchy = lambda r, k: r.standard_cauchy(k)
    normal = lambda r, k: r.standard_normal(k)
    for seed in (2, 5):
        ax.semilogx(n, run(seed, cauchy), color=RED, lw=1.0, alpha=0.9)
    ax.semilogx(n, run(9, normal), color=GREEN, lw=1.4)
    ax.axhline(0, color=GREY, ls=":", lw=1.0)
    ax.axhline(1, color=GREY, ls="--", lw=0.8); ax.axhline(-1, color=GREY, ls="--", lw=0.8)
    ax.text(1.2, 1.15, r"$\pm 1$", fontsize=9, color=GREY)
    ax.text(2.2, -4.5, "Cauchy: average of n draws never settles", color=RED, fontsize=9.5)
    ax.text(2.2, 3.7, r"normal: settles at 0 like $1/\sqrt{n}$", color=GREEN, fontsize=9.5)
    # exact check of the card's claim: the Cauchy average has the law of one draw
    p_exact = 0.5
    r = np.random.default_rng(0)
    emp = np.mean(np.abs(r.standard_cauchy((200000, 100)).mean(axis=1)) > 1)
    assert abs(emp - p_exact) < 0.01, emp
    ax.set_ylim(-5, 5); ax.set_xlim(1, N)
    ax.set_xlabel("sample size $n$"); ax.set_ylabel(r"$\bar X_n$")
    ax.set_title(r"running mean; $P(|\bar X_{100}|>1)=\frac{1}{2}$ for every $n$", fontsize=10)


# ======================================================================
# Card 22: exact coverage of the Wald interval (n=10, p=0.1)
# ======================================================================

@figure("f08_wald_coverage", w=5.0, h=2.6)
def _(ax):
    n, p = 10, 0.1
    ks = np.arange(0, n + 1)
    pmf = np.array([math.comb(n, k) * p ** k * (1 - p) ** (n - k) for k in ks])
    covered = []
    for k in ks:
        ph = k / n
        half = 1.96 * math.sqrt(ph * (1 - ph) / n)
        covered.append(abs(ph - p) <= half)
    covered = np.array(covered)
    cov = pmf[covered].sum()
    assert abs(cov - 0.64969) < 1e-4, cov
    cols = [BLUE if c else RED for c in covered]
    ax.bar(ks, pmf, color=cols, width=0.7, zorder=2)
    for k, v in zip(ks, pmf):
        if v > 0.004:
            ax.text(k, v + 0.008, f"{v:.3f}", ha="center", fontsize=9)
    ax.set_xticks(ks); ax.set_ylim(0, 0.46)
    ax.set_xlabel("observed successes $k$ out of $n=10$")
    ax.set_ylabel(r"$P(X=k)$")
    ax.set_title(f"blue: interval covers $p=0.1$. Exact coverage {cov:.3f}", fontsize=10)


# ======================================================================
# Card 23: Beta(1,11) posterior after 0 successes in 10 trials
# ======================================================================

@figure("f08_beta_posterior", w=4.8, h=2.5)
def _(ax):
    a, b = 1, 11
    lo = 1 - 0.975 ** (1 / 11)
    hi = 1 - 0.025 ** (1 / 11)
    assert abs(lo - 0.0023) < 1e-4 and abs(hi - 0.285) < 1e-3
    u = np.unique(np.concatenate([np.linspace(0, 0.6, 800), [lo, hi]]))
    dens = b * (1 - u) ** (b - 1)            # Beta(1,11) density
    central = (u >= lo) & (u <= hi)
    mass = np.trapezoid(dens[central], u[central])
    assert abs(mass - 0.95) < 2e-3, mass
    ax.fill_between(u, 0, dens, where=(u <= lo) | (u >= hi), color=LIGHT_RED, zorder=1)
    ax.fill_between(u, 0, dens, where=central, color=LIGHT_BLUE, zorder=1)
    ax.plot(u, dens, color=INK, lw=1.8)
    ax.axvline(hi, color=RED, ls="--", lw=1.2)
    ax.axvline(lo, color=RED, ls="--", lw=1.2)
    ax.text(hi + 0.01, 8.0, f"upper {hi:.3f}", color=RED, fontsize=9.5)
    ax.text(0.12, 0.6, "95% of mass", ha="center", fontsize=9.5, color=BLUE)
    ax.text(0.45, 1.0, "2.5% tail", ha="center", fontsize=9, color=RED)
    ax.axvline(1 / 12, color=ORANGE, ls=":", lw=1.3)
    ax.text(1 / 12 + 0.01, 10.6, r"mean $\frac{1}{12}$", fontsize=9, color=ORANGE)
    ax.set_xlim(0, 0.6); ax.set_ylim(0, 12)
    ax.set_yticks([0, 4, 8, 12])
    ax.set_xlabel("$p$"); ax.set_ylabel("posterior density")
    ax.set_title(r"Beta(1,11) posterior, equal-tailed 95%: $[0.002,\,0.285]$", fontsize=10)


# ======================================================================
# Cards 24-25: base-rate probability tree
# ======================================================================

@figure("f08_base_rate_tree", w=5.2, h=2.9, axis=False)
def _(ax):
    prior, power, alpha = 0.10, 0.80, 0.05
    J = {"H1s": prior * power, "H1n": prior * (1 - power),
         "H0s": (1 - prior) * alpha, "H0n": (1 - prior) * (1 - alpha)}
    sig = J["H1s"] + J["H0s"]
    assert abs(J["H0s"] / sig - 9 / 25) < 1e-12
    P = {"root": (0.0, 0.0), "H1": (1.45, 1.15), "H0": (1.45, -1.15),
         "H1s": (3.0, 1.85), "H1n": (3.0, 0.45), "H0s": (3.0, -0.45), "H0n": (3.0, -1.85)}
    ax.text(*P["root"], "strategy", ha="center", va="center", fontsize=10,
            bbox=dict(fc="white", ec=INK, lw=1.2, boxstyle="round,pad=0.3"), zorder=4)
    ax.text(*P["H1"], "real edge", ha="center", va="center", fontsize=10, color=BLUE,
            bbox=dict(fc="white", ec=BLUE, lw=1.2, boxstyle="round,pad=0.3"), zorder=4)
    ax.text(*P["H0"], "no edge", ha="center", va="center", fontsize=10, color=INK,
            bbox=dict(fc="white", ec=INK, lw=1.2, boxstyle="round,pad=0.3"), zorder=4)
    for key, lab in [("H1s", "sig"), ("H1n", "not sig"), ("H0s", "sig"), ("H0n", "not sig")]:
        x, y = P[key]
        hl = key in ("H1s", "H0s")
        ax.text(x, y, lab, ha="center", va="center", fontsize=9.5,
                color=ORANGE if hl else GREY,
                bbox=dict(fc=LIGHT_ORANGE if hl else "white", ec=ORANGE if hl else GREY,
                          lw=1.0, boxstyle="round,pad=0.25"), zorder=4)
    def seg(a, b, label):
        ax.plot([P[a][0], P[b][0]], [P[a][1], P[b][1]], color=INK, lw=1.1, zorder=1)
        mx, my = (P[a][0] + P[b][0]) / 2, (P[a][1] + P[b][1]) / 2
        ax.text(mx, my + 0.12, label, ha="center", va="bottom", fontsize=9, color=INK,
                bbox=dict(fc="white", ec="none", pad=0.5), zorder=5)
    seg("root", "H1", "0.10"); seg("root", "H0", "0.90")
    seg("H1", "H1s", "0.80"); seg("H1", "H1n", "0.20")
    seg("H0", "H0s", "0.05"); seg("H0", "H0n", "0.95")
    xj = 4.45
    ax.text(xj, P["H1s"][1], f"{J['H1s']:.3f}", va="center", fontsize=10, color=BLUE)
    ax.text(xj, P["H1n"][1], f"{J['H1n']:.3f}", va="center", fontsize=10, color=GREY)
    ax.text(xj, P["H0s"][1], f"{J['H0s']:.3f}", va="center", fontsize=10, color=RED)
    ax.text(xj, P["H0n"][1], f"{J['H0n']:.3f}", va="center", fontsize=10, color=GREY)
    ax.text(3.9, 2.45, "joint probability", fontsize=9, color=GREY, ha="center")
    ax.text(2.4, -2.55, r"$P(H_0\mid\mathrm{sig})=\frac{0.045}{0.125}=\frac{9}{25}=0.36$",
            ha="center", va="center", fontsize=10.5, color=ORANGE)
    ax.set_xlim(-0.6, 5.3); ax.set_ylim(-2.9, 2.6)


# ======================================================================
# Card 26: optional stopping, five looks
# ======================================================================

@figure("f08_peeking_paths", w=5.0, h=2.8)
def _(ax):
    rng = np.random.default_rng(1)
    hits = 0
    for _ in range(5):                            # 2e6 paths in chunks
        big = np.cumsum(rng.standard_normal((400000, 5)), axis=1) / np.sqrt(np.arange(1, 6))
        hits += np.sum(np.any(np.abs(big) > 1.96, axis=1))
    p_stop = hits / 2000000
    assert abs(p_stop - 0.142) < 0.002, p_stop
    rng2 = np.random.default_rng(21)
    paths = np.cumsum(rng2.standard_normal((400, 5)), axis=1) / np.sqrt(np.arange(1, 6))
    crosses = np.abs(paths) > 1.96
    first = np.where(crosses.any(axis=1), crosses.argmax(axis=1) + 1, 0)
    show = [i for i in range(len(paths)) if first[i] == 3][:1]
    others = [i for i in range(len(paths)) if first[i] == 0][:3] + [i for i in range(len(paths)) if first[i] in (1, 2, 4, 5)][:1]
    k = np.arange(1, 6)
    for i in others:
        ax.plot(k, paths[i], color=GREY, lw=1.1, alpha=0.8, marker="o", ms=3)
    i0 = show[0]
    s0 = first[i0]                               # stopping look
    ax.plot(k[:s0], paths[i0][:s0], color=BLUE, lw=1.8, marker="o", ms=4)
    ax.plot(k[s0 - 1:], paths[i0][s0 - 1:], color=BLUE, lw=1.0, ls=":", alpha=0.6)
    ax.plot(s0, paths[i0][s0 - 1], "o", color=RED, ms=9, zorder=5)
    ax.axhline(1.96, color=RED, ls="--", lw=1.1); ax.axhline(-1.96, color=RED, ls="--", lw=1.1)
    ax.text(5.1, 2.1, r"$+1.96$", fontsize=9, color=RED, va="bottom")
    ax.text(5.1, -2.1, r"$-1.96$", fontsize=9, color=RED, va="top")
    ax.annotate("stop at look 3", (3, paths[i0][2]), xytext=(3.6, -3.1), fontsize=9.5, color=RED,
                arrowprops=dict(arrowstyle="-", color=RED, lw=0.8))
    ax.set_xticks(k); ax.set_xlim(0.7, 5.6); ax.set_ylim(-3.6, 3.6)
    ax.set_xlabel("look $k$ (sample size $20k$)"); ax.set_ylabel(r"$z_k=S_k/\sqrt{k}$")
    ax.set_title(rf"$P(\exists k:|z_k|>1.96)={p_stop:.3f}$ (independent looks: 0.226)", fontsize=10)


# ======================================================================
# Card 27: discrete binomial test sizes, Binomial(10, 1/2)
# ======================================================================

@figure("f08_binom_tail", w=4.8, h=2.6)
def _(ax):
    n = 10
    ks = np.arange(0, n + 1)
    pmf = np.array([math.comb(n, k) / 2 ** n for k in ks])
    assert abs(pmf[ks >= 9].sum() - 11 / 1024) < 1e-12
    assert abs(pmf[ks >= 8].sum() - 56 / 1024) < 1e-12
    ax.bar(ks[ks < 8], pmf[ks < 8], color=GREY, width=0.7, zorder=2)
    ax.bar(ks[ks == 8], pmf[ks == 8], color=LIGHT_ORANGE, edgecolor=ORANGE, hatch="///", width=0.7, zorder=2)
    ax.bar(ks[ks >= 9], pmf[ks >= 9], color=RED, width=0.7, zorder=2)
    ax.text(9, pmf[9] + 0.012, r"$X\geq 9$", ha="center", fontsize=9.5, color=RED)
    ax.text(8, 0.075, "cut at 8", ha="center", fontsize=9, color=ORANGE)
    ax.text(-0.4, 0.36, r"reject if $X\geq 9$: size $11/1024\approx0.011$", fontsize=9.5, color=RED)
    ax.text(-0.4, 0.32, r"reject if $X\geq 8$: size $56/1024\approx0.055$", fontsize=9.5, color=ORANGE)
    ax.set_xticks(ks); ax.set_ylim(0, 0.40); ax.set_xlim(-0.6, 10.6)
    ax.set_xlabel("$X$, successes under $H_0$"); ax.set_ylabel(r"$P(X=k)$")
    ax.set_title(r"no cut-off gives exactly $0.05$; randomise at $X=8$ with $\gamma=\frac{67}{75}$",
                 fontsize=10)


# ======================================================================
# Cards 28-29: family-wise error with m independent tests
# ======================================================================

@figure("f08_fwer_growth", w=4.8, h=2.6)
def _(ax):
    m = np.arange(1, 101)
    naive = 1 - 0.95 ** m
    bonf = 1 - (1 - 0.05 / m) ** m
    assert abs(naive[19] - 0.6415) < 1e-4 and abs(bonf[19] - 0.0488) < 1e-4
    assert np.all(bonf <= 0.05 + 1e-12)
    ax.plot(m, naive, color=RED, lw=1.8, label=r"naive $p\leq 0.05$: $1-0.95^m$")
    ax.plot(m, bonf, color=GREEN, lw=1.8, label=r"Bonferroni $p\leq 0.05/m$")
    ax.axhline(0.05, color=GREY, ls="--", lw=1.0)
    ax.text(100, 0.07, r"$\alpha=0.05$", ha="right", fontsize=9, color=GREY)
    ax.plot(20, naive[19], "o", color=RED, ms=6); ax.plot(20, bonf[19], "o", color=GREEN, ms=6)
    ax.text(21.5, naive[19] - 0.02, f"{naive[19]:.3f}", fontsize=9.5, color=RED, va="top")
    ax.text(21.5, bonf[19] + 0.05, f"{bonf[19]:.4f}", fontsize=9.5, color=GREEN)
    ax.set_xlim(1, 100); ax.set_ylim(0, 1.02)
    ax.set_xlabel("number of tests $m$ (all nulls true)"); ax.set_ylabel("P(at least one false positive)")
    ax.legend(fontsize=9, frameon=False, loc="center right")
    ax.set_title("FWER: naive rule grows with $m$; Bonferroni holds 0.05", fontsize=10)


# ======================================================================
# Card 31: Benjamini-Hochberg step-up vs Bonferroni
# ======================================================================

@figure("f08_bh_step_up", w=5.0, h=2.8)
def _(ax):
    p = np.array([0.001, 0.008, 0.039, 0.041, 0.042, 0.060, 0.074, 0.205, 0.212, 0.500])
    m, q = len(p), 0.05
    k = np.arange(1, m + 1)
    bh_line = k * q / m
    passes = p <= bh_line
    kstar = int(np.max(np.where(passes)[0]) + 1)
    assert kstar == 2, kstar
    bonf_rej = int(np.sum(p <= q / m))
    assert bonf_rej == 1, bonf_rej
    ax.semilogy(k, bh_line, color=ORANGE, lw=1.6, label=r"BH line $kq/m$")
    ax.axhline(q / m, color=GREY, ls="--", lw=1.1, label=r"Bonferroni $q/m=0.005$")
    ax.scatter(k[passes], p[passes], color=BLUE, s=34, zorder=5)
    ax.scatter(k[~passes], p[~passes], facecolors="white", edgecolors=RED, s=34, zorder=5, lw=1.3)
    ax.annotate(rf"largest $k$ with $p_{{(k)}}\leq kq/m$: $k={kstar}$" + "\nBH rejects 2; Bonferroni rejects 1",
                (2, 0.008), xytext=(3.3, 0.0012), fontsize=9.5, color=INK,
                arrowprops=dict(arrowstyle="-", color=INK, lw=0.8))
    ax.set_xticks(k); ax.set_xlim(0.5, 10.5); ax.set_ylim(5e-4, 1.2)
    ax.set_xlabel("rank $k$"); ax.set_ylabel(r"$p_{(k)}$")
    ax.legend(fontsize=9, frameon=False, loc="upper left")
    ax.set_title("sorted $p$-values: blue passes its BH threshold, red fails", fontsize=10)


# ======================================================================
# Cards 33, 34, 69: expected maximum of N zero-skill z-scores
# ======================================================================

@figure("f08_expected_max", w=4.8, h=2.6)
def _(ax):
    z = np.linspace(-8, 8, 16001)
    phi, Phi = _phi(z), _Phi(z)
    def emax(N):
        return np.trapezoid(z * N * phi * Phi ** (N - 1), z)
    Ns = np.unique(np.round(np.logspace(0, 3, 120)).astype(int))
    vals = np.array([emax(int(N)) for N in Ns])
    e100, e200 = emax(100), emax(200)
    assert abs(e100 - 2.5076) < 2e-3 and abs(e200 - 2.7460) < 2e-3
    ax.semilogx(Ns, vals, color=INK, lw=1.8, label=r"$E[\max]$ of $N$ normals")
    ax.semilogx(Ns[Ns >= 2], np.sqrt(2 * np.log(Ns[Ns >= 2])), color=GREY, ls="--", lw=1.1,
                label=r"$\sqrt{2\ln N}$ (too large at $N=100$)")
    ax.plot(100, e100, "o", color=BLUE, ms=7, zorder=5)
    ax.plot(200, e200, "o", color=ORANGE, ms=7, zorder=5)
    ax.text(80, e100 - 0.45, f"N=100: {e100:.3f}", ha="right", fontsize=9.5, color=BLUE)
    ax.text(260, e200 - 0.5, f"N=200: {e200:.3f}", ha="left", fontsize=9.5, color=ORANGE)
    ax.set_xlim(1, 1000); ax.set_ylim(0, 3.9)
    ax.set_xlabel("number of strategies $N$"); ax.set_ylabel("expected best $z$")
    ax.legend(fontsize=9, frameon=False, loc="lower right")
    ax.set_title(r"Sharpe SE $0.5$: best of 100 $\approx 0.5\times2.508=1.25$; of 200 $\approx 1.37$",
                 fontsize=9.5)


# ======================================================================
# Card 38: OLS as least-squares fit with orthogonal residuals
# ======================================================================

@figure("f08_ols_residuals", w=4.8, h=2.7)
def _(ax):
    x = np.array([1, 2, 3, 4, 5.0]); y = np.array([2, 3, 5, 4, 9.0])
    xb, yb = x.mean(), y.mean()
    b = np.sum((x - xb) * (y - yb)) / np.sum((x - xb) ** 2)
    a = yb - b * xb
    assert abs(b - 1.5) < 1e-12 and abs(a - 0.1) < 1e-12
    e = y - (a + b * x)
    assert abs(e.sum()) < 1e-12 and abs(np.sum(x * e)) < 1e-12
    xs = np.linspace(0.6, 5.4, 10)
    ax.plot(xs, a + b * xs, color=BLUE, lw=1.6, label=r"$\hat y=0.1+1.5x$")
    for xi, yi, ei in zip(x, y, e):
        ax.plot([xi, xi], [yi, a + b * xi], color=GREY, lw=1.2, zorder=2)
        if ei >= 0:
            ax.text(xi, yi + 0.35, f"{ei:+.1f}", fontsize=9.5, color=INK, ha="center", va="bottom")
        else:
            ax.text(xi, yi - 0.35, f"{ei:+.1f}", fontsize=9.5, color=INK, ha="center", va="top")
    ax.scatter(x, y, color=INK, s=34, zorder=5)
    ax.set_xlim(0.5, 5.6); ax.set_ylim(0, 10)
    ax.set_xlabel("$x$"); ax.set_ylabel("$y$")
    ax.legend(fontsize=9, frameon=False, loc="upper left")
    ax.set_title(r"residuals: $\sum e_i=0$ and $\sum x_i e_i=0$ (OLS is orthogonal projection)",
                 fontsize=9.5)


# ======================================================================
# Card 42: AR(1) long-run variance = sum of autocovariances
# ======================================================================

@figure("f08_ar1_acf", w=4.8, h=2.5)
def _(ax):
    rho = 0.5
    lags = np.arange(-8, 9)
    acf = rho ** np.abs(lags)
    full = np.sum(rho ** np.abs(np.arange(-200, 201)))
    assert abs(full - (1 + rho) / (1 - rho)) < 1e-9
    cols = [GREY if l == 0 else BLUE for l in lags]
    ax.bar(lags, acf, color=cols, width=0.65, zorder=2)
    ax.set_xticks(lags[::2]); ax.set_ylim(0, 1.1)
    ax.set_xlabel("lag $k$"); ax.set_ylabel(r"$\rho^{|k|}$")
    ax.set_title(r"AR(1), $\rho=0.5$: long-run variance $=\sigma_x^2\sum_k\rho^{|k|}=3\sigma_x^2$",
                 fontsize=9.5)


# ======================================================================
# Card 43: slope of y on x vs slope of x on y
# ======================================================================

@figure("f08_two_slopes", w=4.8, h=2.8)
def _(ax):
    x = np.array([1, 2, 3, 4, 5.0]); y = np.array([2, 3, 5, 4, 9.0])
    xb, yb = x.mean(), y.mean()
    Sxx = np.sum((x - xb) ** 2); Syy = np.sum((y - yb) ** 2); Sxy = np.sum((x - xb) * (y - yb))
    b_yx = Sxy / Sxx; b_xy = Sxy / Syy
    assert abs(b_yx - 1.5) < 1e-12 and abs(b_xy - 75 / 146) < 1e-12
    assert abs(b_yx * b_xy - 225 / 292) < 1e-12
    xs = np.linspace(0.5, 5.5, 50)
    ax.plot(xs, yb + b_yx * (xs - xb), color=BLUE, lw=1.7)
    ax.plot(xs, yb + (xs - xb) / b_xy, color=ORANGE, lw=1.7)
    ax.scatter(x, y, color=INK, s=34, zorder=5)
    ax.scatter([xb], [yb], marker="+", color=INK, s=80, zorder=6)
    ax.text(1.0, 8.4, r"$y$ on $x$: slope $\frac{3}{2}$", color=BLUE, fontsize=9.5)
    ax.text(1.0, 7.4, r"$x$ on $y$: slope $\frac{75}{146}$ (as $dy/dx=\frac{146}{75}$)", color=ORANGE, fontsize=9.5)
    ax.set_xlim(0.5, 5.5); ax.set_ylim(0, 10)
    ax.set_xlabel("$x$"); ax.set_ylabel("$y$")
    ax.set_title(r"$\hat\beta_{y|x}\,\hat\beta_{x|y}=\frac{225}{292}=R^2\approx0.771$", fontsize=10)


# ======================================================================
# Card 45: omitted variable = mediator path (total effect 2 + 0.5 * 3)
# ======================================================================

@figure("f08_dag_omitted", w=4.8, h=2.4, axis=False)
def _(ax):
    P = {"x1": (0.0, 0.0), "x2": (2.3, 1.25), "y": (4.6, 0.0)}
    _dnode(ax, P["x1"], r"$x_1$", w=0.9)
    _dnode(ax, P["x2"], r"$x_2$ (omitted)", w=1.6, dashed=True)
    _dnode(ax, P["y"], "$y$", w=0.9)
    _dedge(ax, P["x1"], P["y"], color=BLUE, label=r"direct $\beta_1=2$", lab_off=(0, -0.42), w=0.9)
    _dedge(ax, P["x1"], P["x2"], color=INK, label=r"$\delta=0.5$", lab_off=(-0.45, 0.2), w=0.9)
    _dedge(ax, P["x2"], P["y"], color=ORANGE, label=r"$\beta_2=3$", lab_off=(0.5, 0.2), w=0.9)
    ax.text(2.3, -0.9, r"$E[\hat b_{\mathrm{short}}]=2+0.5\times3=3.5$", ha="center", fontsize=10, color=INK)
    ax.set_xlim(-0.9, 5.5); ax.set_ylim(-1.2, 2.1)


# ======================================================================
# Card 46: collider (complaints) on the path price -> complaints <- effort -> sales
# ======================================================================

@figure("f08_dag_collider", w=4.8, h=2.4, axis=False)
def _(ax):
    P = {"price": (0.0, 0.0), "compl": (1.75, 0.95), "effort": (3.5, 1.7), "sales": (3.5, 0.0)}
    _dnode(ax, P["price"], "price", w=1.1)
    _dnode(ax, P["compl"], "complaints", w=1.5, fc=LIGHT_ORANGE, ec=ORANGE)
    _dnode(ax, P["effort"], "sales effort", w=1.4)
    _dnode(ax, P["sales"], "sales", w=1.1)
    _dedge(ax, P["price"], P["sales"], color=BLUE, label="price effect", lab_off=(0, -0.4), w=1.1)
    _dedge(ax, P["price"], P["compl"], color=GREY)
    _dedge(ax, P["effort"], P["compl"], color=GREY)
    _dedge(ax, P["effort"], P["sales"], color=GREY)
    ax.text(-0.8, 2.2, "orange = collider:\nconditioning on it opens\nthe price-effort path",
            ha="left", va="top", fontsize=9, color=ORANGE)
    ax.set_xlim(-0.9, 4.6); ax.set_ylim(-0.75, 2.3)


# ======================================================================
# Card 47: instrument z -> education, unobserved ability confounds
# ======================================================================

@figure("f08_dag_iv", w=4.8, h=2.4, axis=False)
def _(ax):
    P = {"z": (0.0, 0.0), "educ": (2.1, 0.0), "wage": (4.2, 0.0), "ab": (3.0, 1.45)}
    _dnode(ax, P["z"], "instrument $z$", w=1.4)
    _dnode(ax, P["educ"], "education $x$", w=1.4)
    _dnode(ax, P["wage"], "wage $y$", w=1.2)
    _dnode(ax, P["ab"], "ability (unobserved)", w=1.9, dashed=True, ec=GREY)
    _dedge(ax, P["z"], P["educ"], color=BLUE, label="relevance", lab_off=(0, 0.46), w=1.4)
    _dedge(ax, P["educ"], P["wage"], color=BLUE, label=r"$\beta$", lab_off=(0, 0.46), w=1.4)
    _dedge(ax, P["ab"], P["educ"], color=GREY, w=1.9, h=0.56)
    _dedge(ax, P["ab"], P["wage"], color=GREY, w=1.9, h=0.56)
    ax.text(0.9, 1.0, "no arrow from $z$ to $y$\n(exclusion)", ha="center", fontsize=9, color=GREY)
    ax.set_xlim(-0.9, 5.2); ax.set_ylim(-0.9, 2.2)


# ======================================================================
# Cards 49-50: regression to the mean, reliability 0.25
# ======================================================================

@figure("f08_regression_to_mean", w=4.8, h=2.9)
def _(ax):
    rng = np.random.default_rng(11)
    N = 400000
    T = 50 + 10 * rng.standard_normal(N)                  # Var(T)=100
    X = T + math.sqrt(300) * rng.standard_normal(N)       # Var(e)=300
    rel = 100 / 400
    band = np.abs(X - 90) <= 1.5
    mT = T[band].mean()                                    # exact E[T | X=90] = 60
    assert abs(mT - 60) < 0.3, mT
    sub = slice(0, 3000)                                   # draw a subsample only (small SVG)
    ax.scatter(X[sub], T[sub], s=2, color=GREY, alpha=0.25, lw=0)
    sel = band[sub]
    ax.scatter(X[sub][sel], T[sub][sel], s=5, color=ORANGE, lw=0, zorder=3)
    xs = np.linspace(-10, 110, 50)
    ax.plot(xs, 50 + rel * (xs - 50), color=BLUE, lw=1.8, zorder=4)
    ax.plot(90, 60, "o", color=ORANGE, ms=8, zorder=5, mec=INK)
    ax.annotate(rf"score 90: $E[T\mid X]=50+0.25\times40={mT:.0f}$", (90, 60), xytext=(25, 33),
                fontsize=9.5, color=ORANGE, arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.8))
    ax.text(105, 77, r"slope $\rho=0.25$", color=BLUE, fontsize=9.5, ha="right")
    ax.set_xlim(-10, 110); ax.set_ylim(20, 80)
    ax.set_xlabel("observed score $X$"); ax.set_ylabel("true score $T$")
    ax.set_title("pick an extreme $X$: the expected $T$ moves toward the mean", fontsize=9.5)


# ======================================================================
# Card 52: ridge path for one regressor, sum x^2 = 10, sum xy = 20
# ======================================================================

@figure("f08_ridge_path", w=4.8, h=2.6)
def _(ax):
    lam = np.linspace(0, 20, 300)
    beta = 20 / (10 + lam)
    assert abs(20 / (10 + 5) - 4 / 3) < 1e-12
    ax.plot(lam, beta, color=BLUE, lw=2.0)
    ax.axhline(2, color=GREY, ls="--", lw=1.0)
    ax.text(19.5, 2.05, "OLS $=2$", ha="right", fontsize=9.5, color=GREY)
    ax.plot(5, 4 / 3, "o", color=ORANGE, ms=8, zorder=5)
    ax.plot([5, 5], [0, 4 / 3], ":", color=ORANGE, lw=1.0)
    ax.annotate(r"$\lambda=5$: $\hat\beta_R=\frac{4}{3}$", (5, 4 / 3), xytext=(7.5, 1.75), fontsize=9.5,
                color=ORANGE, arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.8))
    ax.text(12, 0.35, r"$\lambda=\sigma^2/\tau^2=5\Rightarrow\tau^2=0.2$", fontsize=9, color=INK, ha="left")
    ax.set_xlim(0, 20); ax.set_ylim(0, 2.3)
    ax.set_xlabel(r"penalty $\lambda$"); ax.set_ylabel(r"$\hat\beta_R$")
    ax.set_title(r"ridge path $\hat\beta_R(\lambda)=\frac{20}{10+\lambda}$", fontsize=10)


# ======================================================================
# Card 53: orthonormal design, lasso soft threshold vs ridge
# ======================================================================

@figure("f08_soft_threshold", w=4.8, h=2.6)
def _(ax):
    lam = 0.5
    z = np.linspace(-1.2, 1.2, 600)
    lasso = np.sign(z) * np.maximum(np.abs(z) - lam, 0)
    ridge = z / (1 + lam)
    assert abs(np.sign(0.4) * max(0.4 - lam, 0)) < 1e-12 and abs(0.4 / 1.5 - 4 / 15) < 1e-12
    ax.axvspan(-lam, lam, color=LIGHT_ORANGE, zorder=0)
    ax.plot(z, z, color=GREY, ls=":", lw=1.0)
    ax.plot(z, ridge, color=GREY, ls="--", lw=1.6, label=r"ridge $z/(1+\lambda)$")
    ax.plot(z, lasso, color=BLUE, lw=2.0, label=r"lasso $\mathrm{sign}(z)(|z|-\lambda)_+$")
    ax.plot(0.4, 0.0, "o", color=BLUE, ms=7, zorder=5)
    ax.plot(0.4, 4 / 15, "o", color=ORANGE, ms=7, zorder=5)
    ax.annotate(r"ridge $=0.267$", (0.4, 4 / 15), xytext=(0.62, -0.42), fontsize=9.5, color=ORANGE,
                arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.8))
    ax.text(0.1, -0.2, "lasso $=0$", fontsize=9.5, color=BLUE, ha="left")
    ax.text(0.0, 0.92, r"dead zone $|z|\leq\lambda$", ha="center", fontsize=9, color=ORANGE)
    ax.axhline(0, color=INK, lw=0.6); ax.axvline(0, color=INK, lw=0.6)
    ax.set_xlim(-1.2, 1.2); ax.set_ylim(-0.9, 1.1)
    ax.set_xlabel("OLS coefficient $z$"); ax.set_ylabel(r"estimate $\hat\beta$")
    ax.legend(fontsize=9, frameon=False, loc="upper left")
    ax.set_title(r"$\lambda=0.5$, $z=0.4$: lasso is exactly 0; ridge is not", fontsize=10)


# ======================================================================
# Card 55: eigen geometry of Sigma = [[1, 0.8], [0.8, 1]]
# ======================================================================

@figure("f08_pca_ellipse", w=4.2, h=3.0)
def _(ax):
    S = np.array([[1, 0.8], [0.8, 1.0]])
    evals, evecs = np.linalg.eigh(S)
    order = np.argsort(evals)[::-1]
    lam, V = evals[order], evecs[:, order]
    assert abs(lam[0] - 1.8) < 1e-12 and abs(lam[1] - 0.2) < 1e-12
    assert abs(lam[0] / lam.sum() - 0.9) < 1e-12
    t = np.linspace(0, 2 * np.pi, 300)
    ell = np.outer(np.cos(t), np.sqrt(lam[0]) * V[:, 0]) + np.outer(np.sin(t), np.sqrt(lam[1]) * V[:, 1])
    ax.plot(ell[:, 0], ell[:, 1], color=INK, lw=1.4)
    ax.fill(ell[:, 0], ell[:, 1], color=LIGHT_BLUE, alpha=0.5, zorder=0)
    v1 = V[:, 0] * np.sqrt(lam[0]); v2 = V[:, 1] * np.sqrt(lam[1])
    ax.annotate("", xy=v1, xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=2.0))
    ax.annotate("", xy=v2, xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=2.0))
    ax.text(v1[0] + 0.05, v1[1] + 0.12, r"PC1: $\lambda_1=1.8$ (90%)", color=BLUE, fontsize=9.5)
    ax.annotate(r"PC2: $\lambda_2=0.2$ (10%)", (v2[0], v2[1]), xytext=(-1.95, 1.45), color=ORANGE,
                fontsize=9.5, arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.8))
    frame(ax, -2.0, 2.0, -2.0, 2.0)
    ax.axhline(0, color=GREY, lw=0.6); ax.axvline(0, color=GREY, lw=0.6)
    ax.set_xlabel("$X_1$ (standardised)"); ax.set_ylabel("$X_2$")
    ax.set_title(r"1-sd contour of $\rho=0.8$; eigenvectors are its axes", fontsize=9.5)


# ======================================================================
# Card 58: Marchenko-Pastur bulk for pure noise, p=500 stocks, n=250 days
# ======================================================================

@figure("f08_mp_bulk", w=4.8, h=2.7)
def _(ax):
    rng = np.random.default_rng(0)
    p, n = 500, 250
    X = rng.standard_normal((n, p))
    C = np.corrcoef(X, rowvar=False)
    ev = np.linalg.eigvalsh(C)
    nz = ev[ev > 1e-8]
    gamma = p / n
    a, b = (1 - math.sqrt(gamma)) ** 2, (1 + math.sqrt(gamma)) ** 2
    assert abs(a - 0.1716) < 1e-3 and abs(b - 5.8284) < 1e-3
    xs = np.linspace(a, b, 800)
    f = np.sqrt((b - xs) * (xs - a)) / (2 * np.pi * gamma * xs)    # density per eigenvalue, all p
    mass = np.trapezoid(f, xs)
    assert abs(mass - 1 / gamma) < 2e-3, mass                       # nonzero part has mass 1/gamma
    edges = np.linspace(0, 6.2, 52)
    width = edges[1] - edges[0]
    ax.hist(nz, bins=edges, weights=np.full(len(nz), 1 / (p * width)), color=LIGHT_BLUE,
            edgecolor=BLUE, lw=0.5, zorder=2, label="simulated eigenvalues")
    ax.plot(xs, f, color=ORANGE, lw=1.8, label="Marchenko-Pastur")
    ax.axvline(a, color=GREY, ls="--", lw=0.9); ax.axvline(b, color=GREY, ls="--", lw=0.9)
    ax.text(6.1, 0.12, f"bulk edges {a:.2f} and {b:.2f}\n(dashed lines)", ha="right", fontsize=9, color=GREY)
    top = ev[-1]
    ax.plot([top, top], [0, 0.02], color=RED, lw=2.5)
    ax.text(5.6, 0.075, f"top {top:.2f}", ha="right", fontsize=9.5, color=RED)
    ax.set_xlim(0, 6.2); ax.set_ylim(0, 0.24)
    ax.set_xlabel("eigenvalue of correlation matrix"); ax.set_ylabel("density (share of all 500)")
    ax.legend(fontsize=9, frameon=False, loc="upper right", bbox_to_anchor=(1.0, 0.93))
    ax.set_title(f"pure noise: {p - len(nz)} of 500 eigenvalues are exactly 0 (not shown)", fontsize=9.5)


# ======================================================================
# Cards 59, 60, 64: correlations as angles between unit vectors
# ======================================================================

@figure("f08_corr_angles", w=4.2, h=3.0, axis=False)
def _(ax):
    th = math.acos(0.9)                         # 25.84 degrees
    assert abs(math.cos(2 * th) - 0.62) < 1e-12
    ax.add_patch(_Circle((0, 0), 1.0, fill=False, ec=GREY, lw=1.0, ls="-"))
    def arrow(angle, col, ls="-", lw=2.0):
        xy = (math.cos(angle), math.sin(angle))
        ax.annotate("", xy=xy, xytext=(0, 0),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=lw, linestyle=ls))
        return xy
    yv = arrow(0.0, INK)
    xv = arrow(-th, BLUE)
    zv = arrow(th, GREEN)
    ax.text(yv[0] + 0.02, yv[1] + 0.1, "$Y$", fontsize=11, ha="left")
    ax.text(xv[0], xv[1] - 0.12, "$X$", fontsize=11, color=BLUE, ha="center", va="top")
    ax.text(zv[0] + 0.02, zv[1] + 0.06, "$Z$", fontsize=11, color=GREEN, ha="left")
    arc = np.linspace(-th, th, 60)
    ax.plot(0.35 * np.cos(arc), 0.35 * np.sin(arc), color=ORANGE, lw=1.2)
    ax.text(-1.2, -1.28, r"angle from $Y$ to $X$ and to $Z$: $\theta=\arccos0.9=25.8^\circ$",
            ha="left", fontsize=9, color=INK)
    ax.text(-1.2, -1.5, r"so $\mathrm{corr}(X,Z)\geq\cos2\theta=0.62$ (orange arc)",
            ha="left", fontsize=9, color=ORANGE)
    ax.text(-1.2, -1.72, r"$\mathrm{corr}(X,Z)=0.5$ needs $60^\circ$: impossible",
            ha="left", fontsize=9, color=RED)
    frame(ax, -1.25, 1.25, -1.9, 1.2)
