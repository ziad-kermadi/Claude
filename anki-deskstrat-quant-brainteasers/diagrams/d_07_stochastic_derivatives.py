"""Figures for cards/07_stochastic_derivatives.json."""
import math
import numpy as np
from qcfig import *

# ---------- numerical helpers (vectorised; values checked against the cards) ----------
_erf = np.vectorize(math.erf)

def Phi(x):
    return 0.5 * (1.0 + _erf(np.asarray(x, float) / math.sqrt(2.0)))

def phi(x):
    x = np.asarray(x, float)
    return np.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)

def d12(S, K, r, sig, T, q=0.0):
    S = np.asarray(S, float)
    d1 = (np.log(S / K) + (r - q + 0.5 * sig * sig) * T) / (sig * math.sqrt(T))
    return d1, d1 - sig * math.sqrt(T)

def call(S, K, r, sig, T, q=0.0):
    d1, d2 = d12(S, K, r, sig, T, q)
    return np.asarray(S, float) * math.exp(-q * T) * Phi(d1) - K * math.exp(-r * T) * Phi(d2)

def put(S, K, r, sig, T, q=0.0):
    d1, d2 = d12(S, K, r, sig, T, q)
    return K * math.exp(-r * T) * Phi(-d2) - np.asarray(S, float) * math.exp(-q * T) * Phi(-d1)

def trap(y, x):
    y, x = np.asarray(y, float), np.asarray(x, float)
    return float(np.sum(0.5 * (y[1:] + y[:-1]) * np.diff(x)))

R, SIG, S0, K0 = 0.05, 0.20, 100.0, 100.0


# ---------- 1. exit of driftless BM from (-2, 1)  (cards 0, 1, 65) ----------
@figure("f07_exit_levels", w=5.0, h=2.6)
def _(ax):
    rng = np.random.default_rng(3)
    dt = 0.005
    want = {1: 2, -2: 2}
    paths = []
    while want[1] or want[-2]:
        x, t = [0.0], [0.0]
        while -2 < x[-1] < 1 and t[-1] < 6.0:
            x.append(x[-1] + math.sqrt(dt) * rng.standard_normal())
            t.append(t[-1] + dt)
        if t[-1] >= 6.0:
            continue
        hit = 1 if x[-1] >= 1 else -2
        x[-1] = hit
        if want[hit]:
            want[hit] -= 1
            paths.append((np.array(t), np.array(x), hit))
    for t, x, hit in paths:
        ax.plot(t, x, color=GREEN if hit == 1 else RED, lw=1.3)
    ax.axhline(1, color=GREEN, ls="--", lw=1.0)
    ax.axhline(-2, color=RED, ls="--", lw=1.0)
    ax.plot(0, 0, "o", color=INK, ms=4, zorder=5)
    tmax = max(t[-1] for t, _, _ in paths)
    ax.text(tmax, 1.15, "absorb at +1", ha="right", va="bottom", fontsize=9, color=GREEN)
    ax.text(tmax, -2.15, "absorb at -2", ha="right", va="top", fontsize=9, color=RED)
    ax.set_yticks([-2, 0, 1]); ax.set_ylim(-2.9, 1.9)
    ax.set_xlabel("time $t$"); ax.set_ylabel(r"$W_t$")
    ax.set_title(r"$P(\mathrm{hit}\ +1\ \mathrm{first})=\frac{2}{3}\qquad E[\tau]=ab=2$", fontsize=10)


# ---------- 2. reflection principle, T=4, level 2  (cards 2, 67) ----------
@figure("f07_reflection", w=5.0, h=2.8)
def _(ax):
    a, T, n = 2.0, 4.0, 400
    dt = T / n
    t = np.linspace(0, T, n + 1)
    k = 0
    while True:
        rng = np.random.default_rng(k)
        k += 1
        W = np.concatenate([[0.0], np.cumsum(math.sqrt(dt) * rng.standard_normal(n))])
        hit = np.where(W >= a)[0]
        if len(hit) and hit[0] > 0.25 * n and -0.6 < W[-1] < a - 0.6:
            break
    tau = hit[0]
    refl = W.copy()
    refl[tau:] = 2 * a - W[tau:]
    ax.plot(t, W, color=BLUE, lw=1.6, label="path $W_t$")
    ax.plot(t[tau:], refl[tau:], color=ORANGE, lw=1.4, ls="--", label="reflected after $\\tau$")
    ax.axhline(a, color=ORANGE, lw=1.0, ls=":")
    ax.plot(t[tau], a, "o", color=ORANGE, ms=4, zorder=5)
    ax.plot(T, W[-1], "o", color=BLUE, ms=4, zorder=5)
    ax.plot(T, refl[-1], "o", color=ORANGE, ms=4, zorder=5)
    ax.text(T + 0.08, W[-1], r"$W_4$", va="center", fontsize=9.5, color=BLUE)
    ax.text(T + 0.08, refl[-1], r"$4-W_4$", va="center", fontsize=9.5, color=ORANGE)
    ax.text(0.05, a + 0.12, "$a=2$", fontsize=9.5, color=ORANGE)
    ax.set_xlim(-0.1, T + 0.9)
    ax.set_xlabel("time $t$"); ax.set_ylabel(r"$W_t$")
    ax.legend(loc="upper left", fontsize=9, frameon=False)
    val = 2 * (1 - float(Phi(1.0)))
    assert abs(val - 0.3173) < 5e-4
    ax.set_title(r"$P(M_4\geq 2)=2P(W_4\geq 2)=2\,(1-\Phi(1))\approx 0.3173$", fontsize=10)


# ---------- 3. Brownian bridge maximum tail, a=1  (cards 6, 68) ----------
@figure("f07_bridge_max", w=5.0, h=2.7)
def _(ax):
    n = 500
    t = np.linspace(0, 1, n + 1)
    rng = np.random.default_rng(1)
    bridges = []
    for _ in range(60):
        W = np.concatenate([[0.0], np.cumsum(math.sqrt(1 / n) * rng.standard_normal(n))])
        bridges.append(W - t * W[-1])
    cross = [B for B in bridges if B.max() >= 1.0]
    for B in bridges[:30]:
        ax.plot(t, B, color=GREY, lw=0.8, alpha=0.5)
    for B in cross[:3]:
        ax.plot(t, B, color=BLUE, lw=1.5)
    ax.axhline(1, color=ORANGE, ls="--", lw=1.1)
    ax.text(0.01, 1.08, "$a=1$", color=ORANGE, fontsize=9.5)
    ax.set_xlabel("time $t$"); ax.set_ylabel(r"$B_t$")
    ax.set_ylim(-2.4, 2.4)
    assert abs(math.exp(-2) - 0.1353) < 5e-5
    ax.set_title(r"$P(\max_{0\leq t\leq 1} B_t\geq a)=e^{-2a^2}$; $a=1$ gives $e^{-2}\approx 0.1353$", fontsize=10)


# ---------- 4. layer-cake integral of the bridge maximum  (card 25) ----------
@figure("f07_bridge_layer_cake", w=5.0, h=2.6)
def _(ax):
    a = np.linspace(0, 2.4, 600)
    tail = np.exp(-2 * a * a)
    ax.fill_between(a, 0, tail, color=LIGHT_BLUE, lw=0)
    ax.plot(a, tail, color=BLUE, lw=1.8)
    ax.plot(1, math.exp(-2), "o", color=ORANGE, ms=5, zorder=5)
    ax.text(1.06, math.exp(-2) + 0.03, r"$P(M\geq 1)=e^{-2}$", fontsize=9.5, color=ORANGE)
    ax.text(1.35, 0.45, r"area $=E[M]$", fontsize=10, color=BLUE)
    ax.set_xlim(0, 2.4); ax.set_ylim(0, 1.05)
    ax.set_xlabel("level $a$"); ax.set_ylabel("P(M ≥ a)")
    mean = trap(tail, a)
    assert abs(mean - math.sqrt(math.pi / 8)) < 1e-3
    ax.set_title("E[M] = ∫₀^∞ P(M ≥ a) da = √(π/8) ≈ 0.6267", fontsize=10)


# ---------- 5. bridge pinned to c=1 at t=1, level a=2  (card 55) ----------
@figure("f07_bridge_pinned", w=5.0, h=2.7)
def _(ax):
    n, c, a = 500, 1.0, 2.0
    t = np.linspace(0, 1, n + 1)
    mean = c * t
    sd = np.sqrt(t * (1 - t))
    ax.fill_between(t, mean - 2 * sd, mean + 2 * sd, color=GREY, alpha=0.18, lw=0)
    ax.plot(t, mean, color=INK, lw=1.0, ls=":", label="mean $ct$")
    k = 0
    while True:
        rng = np.random.default_rng(100 + k)
        k += 1
        W = np.concatenate([[0.0], np.cumsum(math.sqrt(1 / n) * rng.standard_normal(n))])
        X = W - t * W[-1] + mean
        if X.max() >= a and X.max() < a + 0.4:
            break
    for j in range(25):
        rng2 = np.random.default_rng(900 + j)
        Wj = np.concatenate([[0.0], np.cumsum(math.sqrt(1 / n) * rng2.standard_normal(n))])
        ax.plot(t, Wj - t * Wj[-1] + mean, color=GREY, lw=0.7, alpha=0.45)
    ax.plot(t, X, color=BLUE, lw=1.6)
    ax.axhline(a, color=ORANGE, ls="--", lw=1.1)
    ax.text(0.01, a + 0.08, "$a=2$", color=ORANGE, fontsize=9.5)
    ax.set_xlabel("time $t$"); ax.set_ylabel(r"$X_t$")
    ax.set_ylim(-1.4, 2.5)
    ax.legend(loc="lower right", fontsize=9, frameon=False)
    val = math.exp(-2 * a * (a - c))
    assert abs(val - 0.0183) < 5e-5
    ax.set_title(r"$P(\max_{0\leq t\leq 1}X_t\geq a)=e^{-2a(a-c)}$; $a=2$, $c=1$: $e^{-4}\approx 0.0183$", fontsize=10)


# ---------- 6. conditional variance of a bridge  (card 50) ----------
@figure("f07_bridge_var", w=5.0, h=2.7)
def _(ax):
    n = 400
    t = np.linspace(0, 1, n + 1)
    sd = np.sqrt(t * (1 - t))
    ax.fill_between(t, -sd, sd, color=LIGHT_BLUE, alpha=0.7, lw=0)
    ax.plot(t, sd, color=BLUE, lw=0.9, ls="--")
    ax.plot(t, -sd, color=BLUE, lw=0.9, ls="--")
    for j in range(4):
        rng = np.random.default_rng(20 + j)
        W = np.concatenate([[0.0], np.cumsum(math.sqrt(1 / n) * rng.standard_normal(n))])
        ax.plot(t, W - t * W[-1], color=INK, lw=0.8, alpha=0.7)
    ax.plot([0.5, 0.5], [-0.5, 0.5], color=ORANGE, lw=2.0)
    ax.text(0.5, 0.74, r"$\mathrm{sd}=\frac{1}{2}$, variance $\frac{1}{4}$", color=ORANGE, fontsize=9.5, ha="center")
    ax.set_xlabel("time $s$"); ax.set_ylabel(r"$W_s\mid W_1=0$")
    ax.set_ylim(-1.1, 1.1)
    assert abs(0.5 * 0.5 - 0.25) < 1e-12
    ax.set_title(r"$\mathrm{Var}(W_s\mid W_1=0)=s(1-s)$; at $s=\frac{1}{2}$ this is $\frac{1}{4}$", fontsize=10)


# ---------- 7. GBM terminal density: median, mean, P(S_T>100)  (cards 11, 28) ----------
@figure("f07_gbm_mean_median", w=5.0, h=2.7)
def _(ax):
    mu, sig, T = 0.10, 0.30, 2.0
    m = math.log(S0) + (mu - 0.5 * sig * sig) * T
    s = sig * math.sqrt(T)
    x = np.linspace(20, 280, 3000)
    f = phi((np.log(x) - m) / s) / (x * s)
    p_above = 1 - float(Phi((math.log(100) - m) / s))
    median, mean = math.exp(m), S0 * math.exp(mu * T)
    assert abs(p_above - 0.602) < 5e-4 and abs(median - 111.63) < 5e-3 and abs(mean - 122.14) < 5e-3
    ax.plot(x, f, color=BLUE, lw=1.8)
    ax.fill_between(x, 0, f, where=x > 100, color=LIGHT_BLUE, lw=0)
    ymax = f.max()
    ax.axvline(100, color=GREY, ls=":", lw=1.1)
    ax.axvline(median, color=ORANGE, ls="--", lw=1.2)
    ax.axvline(mean, color=INK, ls="-.", lw=1.0)
    ax.text(98, 0.04 * ymax, "$S_0=100$", ha="right", color=GREY, fontsize=9.5)
    ax.text(median + 2, 0.92 * ymax, f"median {median:.2f}", color=ORANGE, fontsize=9.5)
    ax.text(mean + 2, 0.72 * ymax, f"mean {mean:.2f}", color=INK, fontsize=9.5)
    ax.text(160, 0.30 * ymax, f"$P(S_T>100)={p_above:.3f}$", color=BLUE, fontsize=9.5)
    ax.set_xlim(20, 280); ax.set_ylim(0, 1.05 * ymax)
    ax.set_xlabel(r"$S_T$"); ax.set_ylabel("density")
    ax.set_title(r"lognormal $S_T$: $\mu=10\%$, $\sigma=30\%$, $T=2$", fontsize=10)


# ---------- 8. butterfly tent  (cards 10, 40) ----------
@figure("f07_butterfly", w=5.0, h=2.6)
def _(ax):
    S = np.linspace(70, 130, 601)
    tent = np.maximum(S - 90, 0) - 2 * np.maximum(S - 100, 0) + np.maximum(S - 110, 0)
    ax.fill_between(S, 0, tent, color=LIGHT_BLUE, lw=0)
    ax.plot(S, tent, color=BLUE, lw=1.8)
    for k in (90, 100, 110):
        ax.plot([k, k], [-0.4, 11], color=GREY, ls=":", lw=1.0)
        ax.text(k, -1.2, f"{k}", ha="center", fontsize=9.5, color=GREY)
    ax.plot(100, 10, "o", color=ORANGE, ms=5, zorder=5)
    ax.text(102, 10.0, "payoff 10 at $S_T=100$", fontsize=9.5, color=ORANGE, va="center")
    c90, c100, c110 = (float(call(100, k, R, SIG, 1.0)) for k in (90, 100, 110))
    fly = c90 - 2 * c100 + c110
    assert abs(fly - 1.8384) < 5e-4
    ax.set_ylim(-2.4, 12); ax.set_xlim(70, 130)
    ax.axhline(0, color=INK, lw=0.6)
    ax.set_xlabel(r"$S_T$"); ax.set_ylabel("payoff")
    ax.text(72, 8.8, f"$C(90)={c90:.4f}$\n$C(100)={c100:.4f}$\n$C(110)={c110:.4f}$", fontsize=9, va="top")
    ax.set_title(rf"butterfly: $C(90)-2C(100)+C(110)={fly:.4f}\geq 0$", fontsize=10)


# ---------- 9. digital as a limit of call spreads  (card 9) ----------
@figure("f07_digital_spread", w=5.0, h=2.6)
def _(ax):
    S = np.linspace(80, 120, 801)
    K = 100.0
    for h, c in [(16, GREY), (6, ORANGE), (1.5, BLUE)]:
        pay = (np.maximum(S - K, 0) - np.maximum(S - K - h, 0)) / h
        ax.plot(S, pay, color=c, lw=1.5, label=f"width $h={h:g}$")
    ax.step(S, (S > K).astype(float), where="post", color=GREEN, lw=1.3, ls="--",
            label=r"$\mathbf{1}\{S_T>K\}$")
    ax.axvline(K, color=GREY, ls=":", lw=1.0)
    ax.text(K + 0.8, -0.13, "$K$", fontsize=9.5, color=GREY)
    ax.set_ylim(-0.2, 1.15)
    ax.set_xlabel(r"$S_T$"); ax.set_ylabel("payoff")
    ax.legend(loc="upper left", fontsize=9, frameon=False)
    ax.set_title(r"$[(S_T-K)^+-(S_T-K-h)^+]/h\ \to\ \mathbf{1}\{S_T>K\}=-\partial_K(S_T-K)^+$", fontsize=9.5)


# ---------- 10. risk-neutral density from the second strike derivative  (cards 41, 72) ----------
@figure("f07_bl_density", w=5.0, h=2.6)
def _(ax):
    x = np.linspace(60, 160, 2000)
    mu_q = math.log(S0) + (R - 0.5 * SIG * SIG)
    f = phi((np.log(x) - mu_q) / SIG) / (x * SIG)
    h = 0.5
    c_m, c_0, c_p = (float(call(S0, k, R, SIG, 1.0)) for k in (K0 - h, K0, K0 + h))
    bl = math.exp(R) * (c_p - 2 * c_0 + c_m) / h ** 2
    exact = float(phi((math.log(100) - mu_q) / SIG) / (100 * SIG))
    assert abs(bl - 0.01972) < 1e-4 and abs(exact - 0.01972) < 1e-4
    ax.plot(x, f, color=BLUE, lw=1.8)
    ax.fill_between(x, 0, f, where=(x > 95) & (x < 105), color=LIGHT_BLUE, lw=0)
    ax.plot(100, exact, "o", color=ORANGE, ms=5, zorder=5)
    ax.text(103, exact + 0.0015, r"$f_{S_T}(100)=0.01972$", color=ORANGE, fontsize=9.5)
    ax.text(160, 0.016, r"$f_{S_T}(K)=e^{rT}\,\partial_K^2 C(K)$", ha="right", fontsize=9.5, color=INK)
    ax.set_xlim(60, 160); ax.set_ylim(0, 0.03)
    ax.set_xlabel(r"$S_T$"); ax.set_ylabel("risk-neutral density")
    ax.set_title(r"$S_0=100$, $r=5\%$, $\sigma=20\%$, $T=1$: second difference in $K$ at $K=100$", fontsize=9.5)


# ---------- 11. variance-swap strip weights, flat 20% smile  (cards 14, 87) ----------
@figure("f07_var_strip", w=5.0, h=2.7)
def _(ax):
    T = 1.0
    F = S0 * math.exp(R * T)
    K = np.linspace(50, 200, 3001)
    otm = np.where(K < F, put(S0, K, R, SIG, T), call(S0, K, R, SIG, T))
    q = 2 * math.exp(R * T) / T * otm / K ** 2
    lo, hi = K < F, K >= F
    ax.fill_between(K[lo], 0, q[lo], color=RED, alpha=0.35, lw=0, label="puts, $K<F$")
    ax.fill_between(K[hi], 0, q[hi], color=BLUE, alpha=0.35, lw=0, label="calls, $K>F$")
    ax.plot(K, q, color=INK, lw=1.0)
    ax.axvline(F, color=ORANGE, ls=":", lw=1.2, label=f"$F={F:.2f}$")
    area = trap(q, K)
    assert abs(area - 0.04) < 1e-4, area
    ax.set_xlim(50, 200); ax.set_ylim(0, 1.15 * q.max())
    ax.set_xlabel("strike $K$"); ax.set_ylabel(r"$2e^{rT}\,\mathrm{OTM}(K)/K^2$")
    ax.legend(loc="upper right", fontsize=9, frameon=False)
    ax.set_title(r"$K_{var}=2e^{rT}\int \mathrm{OTM}(K)\,K^{-2}\,dK=0.20^2$", fontsize=10)


# ---------- 12. static replication of a log contract  (card 44) ----------
@figure("f07_log_replication", w=5.0, h=2.7)
def _(ax):
    T = 1.0
    F = S0 * math.exp(R * T)
    S = np.linspace(50, 200, 800)
    tangent = math.log(F) + (S - F) / F
    ax.fill_between(S, tangent, np.log(S), color=LIGHT_ORANGE, lw=0)
    ax.plot(S, np.log(S), color=BLUE, lw=1.8, label=r"$\ln S_T$")
    ax.plot(S, tangent, color=ORANGE, lw=1.2, ls="--", label="tangent at $F$")
    ax.axvline(F, color=GREY, ls=":", lw=1.0)
    ax.text(F + 2, 3.9, f"$F={F:.2f}$", color=GREY, fontsize=9.5)
    # price from the strip: e^{-rT} ln F - sum of OTM option prices weighted by 1/K^2
    K = np.linspace(1e-3, 1200, 600001)
    otm = np.where(K < F, put(S0, K, R, SIG, T), call(S0, K, R, SIG, T))
    A = trap(otm / K ** 2, K)
    price = math.exp(-R * T) * math.log(F) - A
    assert abs(price - 4.4091) < 5e-4, price
    ax.set_xlim(50, 200)
    ax.set_xlabel(r"$S_T$"); ax.set_ylabel("payoff")
    ax.legend(loc="lower right", fontsize=9, frameon=False)
    ax.set_title(r"$\ln S_T$ = tangent at $F$ minus OTM options weighted by $1/K^2$", fontsize=9.5)


# ---------- 13. chooser at t=1/2  (cards 45, 71) ----------
@figure("f07_chooser", w=5.0, h=2.7)
def _(ax):
    tau = 0.5
    S = np.linspace(70, 130, 601)
    C = call(S, K0, R, SIG, tau)
    P = put(S, K0, R, SIG, tau)
    M = np.maximum(C, P)
    dec = C + np.maximum(K0 * math.exp(-R * tau) - S, 0)
    assert np.allclose(M, dec)
    ax.plot(S, C, color=BLUE, lw=1.2, label="call value at $t$")
    ax.plot(S, P, color=RED, lw=1.2, label="put value at $t$")
    ax.plot(S, M, color=INK, lw=2.6, alpha=0.9, label=r"chooser $=\max(C_t,P_t)$")
    ax.plot(S, dec, color=ORANGE, lw=1.1, ls="--",
            label=r"$C_t+(Ke^{-r(T-t)}-S_t)^+$")
    ax.axvline(K0, color=GREY, ls=":", lw=1.0)
    val0 = float(call(S0, K0, R, SIG, 1.0)) + float(put(S0, K0 * math.exp(-R * tau), R, SIG, tau))
    assert abs(val0 - 13.8513) < 1e-3, val0
    ax.set_xlim(70, 130); ax.set_ylim(0, 50)
    ax.set_xlabel(r"$S_t$ at $t=\frac{1}{2}$"); ax.set_ylabel("value at $t$")
    ax.legend(loc="upper center", ncol=2, fontsize=8.5, frameon=False)
    ax.set_title(r"$\max(C_t,P_t)=C_t+(Ke^{-r(T-t)}-S_t)^+$: two curves coincide", fontsize=9.5)


# ---------- 14. put-call parity as a synthetic forward  (cards 15, 39) ----------
@figure("f07_parity", w=5.0, h=2.6)
def _(ax):
    S = np.linspace(60, 140, 401)
    call_pay = np.maximum(S - K0, 0)
    short_put = -np.maximum(K0 - S, 0)
    ax.plot(S, call_pay, color=BLUE, lw=1.3, ls="--", label="long call payoff")
    ax.plot(S, short_put, color=RED, lw=1.3, ls="--", label="short put payoff")
    ax.plot(S, call_pay + short_put, color=INK, lw=2.0, label=r"$S_T-K$")
    ax.axhline(0, color=GREY, lw=0.7)
    ax.axvline(K0, color=GREY, ls=":", lw=1.0)
    ax.text(K0 + 1, -36, "$K=100$", color=GREY, fontsize=9.5)
    C, P = float(call(S0, K0, R, SIG, 1.0)), float(put(S0, K0, R, SIG, 1.0))
    assert abs(C - 10.4506) < 5e-4 and abs(P - 5.5735) < 5e-4 and abs(C - P - (100 - 100 * math.exp(-0.05))) < 1e-3
    ax.set_xlim(60, 140); ax.set_ylim(-40, 42)
    ax.set_xlabel(r"$S_T$"); ax.set_ylabel("payoff at $T$")
    ax.legend(loc="upper left", fontsize=8.5, frameon=False)
    ax.set_title(rf"$C-P=Se^{{-qT}}-Ke^{{-rT}}$: ${C:.4f}-{P:.4f}={C-P:.4f}=100-95.1229$", fontsize=9.5)


# ---------- 15. delta and gamma against spot  (card 36) ----------
@figure("f07_greeks_spot", w=5.0, h=2.7)
def _(ax):
    S = np.linspace(60, 140, 401)
    d1, _ = d12(S, K0, R, SIG, 1.0)
    delta = Phi(d1)
    gamma = phi(d1) / (S * SIG)
    l1 = ax.plot(S, delta, color=BLUE, lw=1.8, label=r"$\Delta_C=N(d_1)$ (left)")
    ax.set_ylim(0, 1.05)
    ax2 = ax.twinx()
    ax2.spines["right"].set_visible(True)
    l2 = ax2.plot(S, gamma, color=ORANGE, lw=1.8, label=r"$\Gamma$ (right)")
    ax2.set_ylim(0, 0.025)
    ax2.set_ylabel("Gamma", color=ORANGE)
    ax2.tick_params(axis="y", colors=ORANGE)
    d1_0, _ = d12(100.0, K0, R, SIG, 1.0)
    dl0, g0 = float(Phi(d1_0)), float(phi(d1_0) / (100 * SIG))
    assert abs(dl0 - 0.6368) < 5e-5 and abs(g0 - 0.01876) < 5e-6
    ax.plot(100, dl0, "o", color=BLUE, ms=4, zorder=5)
    ax2.plot(100, g0, "o", color=ORANGE, ms=4, zorder=5)
    ax.axvline(100, color=GREY, ls=":", lw=1.0)
    ax.set_xlabel("spot $S$"); ax.set_ylabel(r"$\Delta$")
    lines = l1 + l2
    ax.legend(lines, [l.get_label() for l in lines], loc="upper left", fontsize=9, frameon=False)
    ax.set_title(r"$S=K=100$: $\Delta=0.6368$, $\Gamma=0.01876$", fontsize=10)


# ---------- 16. digital delta equals call gamma at the strike  (card 37) ----------
@figure("f07_digital_delta", w=5.0, h=2.6)
def _(ax):
    S = np.linspace(70, 130, 601)
    d1, d2 = d12(S, K0, R, SIG, 1.0)
    dig_delta = math.exp(-R) * phi(d2) / (S * SIG)
    call_gamma = phi(d1) / (S * SIG)
    ax.plot(S, dig_delta, color=ORANGE, lw=1.8, label=r"digital delta $\partial_S(e^{-rT}N(d_2))$")
    ax.plot(S, call_gamma, color=BLUE, lw=1.3, ls="--", label=r"call gamma $\Gamma$")
    ax.axvline(100, color=GREY, ls=":", lw=1.0)
    d1_0, d2_0 = d12(100.0, K0, R, SIG, 1.0)
    v_dig = float(math.exp(-R) * phi(d2_0) / (100 * SIG))
    v_gam = float(phi(d1_0) / (100 * SIG))
    assert abs(v_dig - 0.01876) < 5e-6 and abs(v_gam - 0.01876) < 5e-6
    ax.plot(100, v_dig, "o", color=INK, ms=4, zorder=5)
    ax.text(102, v_dig + 0.0008, "0.01876 at $S=K$", fontsize=9.5)
    ax.set_xlim(70, 130); ax.set_ylim(0, 0.031)
    ax.set_xlabel("spot $S$"); ax.set_ylabel("per unit spot")
    ax.legend(loc="upper right", fontsize=8.5, frameon=False)
    ax.set_title(r"digital delta and call gamma agree at $S=K$", fontsize=10)


# ---------- 17. digital gamma changes sign at d_1=0  (card 62) ----------
@figure("f07_digital_gamma", w=5.0, h=2.6)
def _(ax):
    S = np.linspace(85, 115, 601)
    r0, sig, T = 0.0, 0.20, 1.0
    d1, d2 = d12(S, K0, r0, sig, T)
    gd = -math.exp(-r0 * T) * phi(d2) * d1 / (S * S * sig * sig * T) * 1e4
    S_zero = K0 * math.exp(-0.5 * sig * sig * T)
    ax.axhline(0, color=INK, lw=0.7)
    ax.fill_between(S, gd, 0, where=S < S_zero, color=LIGHT_BLUE, lw=0)
    ax.fill_between(S, gd, 0, where=S > S_zero, color=LIGHT_RED, lw=0)
    ax.plot(S, gd, color=INK, lw=1.8)
    ax.axvline(S_zero, color=ORANGE, ls="--", lw=1.1)
    ax.text(86, -1.6, f"$d_1=0$ at $S={S_zero:.2f}$", ha="left", color=ORANGE, fontsize=9.5)
    d1_100, d2_100 = d12(100.0, K0, r0, sig, T)
    g100 = float(-math.exp(-r0 * T) * phi(d2_100) * d1_100 / (100.0 ** 2 * sig * sig * T) * 1e4)
    assert abs(g100 / 1e4 - (-0.0000992)) < 1e-7, g100
    ax.plot(100, g100, "o", color=RED, ms=5, zorder=5)
    ax.text(101.2, -1.3, r"$\Gamma_D(100)\approx -0.0000992$", color=RED, fontsize=9.5)
    ax.set_xlim(85, 115); ax.set_ylim(-3.0, 3.0)
    ax.set_xlabel("spot $S$"); ax.set_ylabel(r"$\Gamma_D\ (\times 10^{-4})$")
    ax.set_title(r"$\Gamma_D=-e^{-rT}\varphi(d_2)\,d_1/(S^2\sigma^2T)$ with $r=0$, $\sigma=20\%$, $T=1$", fontsize=9.5)


# ---------- 18. P&L rate of a delta-hedged long call over the first year  (cards 21, 38) ----------
@figure("f07_gamma_window", w=5.0, h=2.6)
def _(ax):
    sig_i, sig_r = 0.20, 0.25
    t = np.linspace(0, 0.9, 500)
    tau = 1 - t
    gam = phi(sig_i * np.sqrt(tau) / 2) / (S0 * sig_i * np.sqrt(tau))
    rate = 0.5 * gam * S0 * S0 * (sig_r ** 2 - sig_i ** 2)
    win = t <= 0.25
    ax.fill_between(t[win], 0, rate[win], color=LIGHT_ORANGE, lw=0)
    ax.plot(t, rate, color=BLUE, lw=1.8)
    ax.axvline(0.25, color=ORANGE, ls="--", lw=1.1)
    tt = np.linspace(0, 0.25, 2001)
    gg = phi(sig_i * np.sqrt(1 - tt) / 2) / (S0 * sig_i * np.sqrt(1 - tt))
    integral = trap(0.5 * gg * S0 * S0 * (sig_r ** 2 - sig_i ** 2), tt)
    assert abs(integral - 0.60) < 0.01, integral
    rate0 = float(0.5 * phi(0.1) / (S0 * sig_i) * S0 * S0 * (sig_r ** 2 - sig_i ** 2))
    assert abs(rate0 - 2.2) < 0.05
    ax.text(0.28, 0.9, "first 3 months\n$\\approx 0.60$", color=ORANGE, fontsize=9.5)
    ax.plot(0, rate0, "o", color=BLUE, ms=4, zorder=5)
    ax.text(0.02, 3.4, f"{rate0:.2f} per year at inception", color=BLUE, fontsize=9.5)
    ax.set_xticks([0, 0.2, 0.4, 0.6, 0.8])
    ax.set_xlim(0, 0.9); ax.set_ylim(0, rate.max() * 1.05)
    ax.set_xlabel("time elapsed $t$ (years)"); ax.set_ylabel("P&L rate per year")
    ax.set_title(r"$\frac{1}{2}\Gamma S^2(\sigma_r^2-\sigma_i^2)$ with $\sigma_r=25\%$, $\sigma_i=20\%$", fontsize=9.5)


# ---------- 19. gap through a delta hedge  (card 58) ----------
@figure("f07_gap_hedge", w=5.0, h=2.7)
def _(ax):
    S = np.linspace(80, 120, 401)
    V = call(S, K0, R, SIG, 1.0)
    V0 = float(call(S0, K0, R, SIG, 1.0))
    d1_0, _ = d12(100.0, K0, R, SIG, 1.0)
    delta = float(Phi(d1_0))
    tan = V0 + delta * (S - 100)
    ax.plot(S, V, color=BLUE, lw=1.8, label="call value $V(S)$")
    ax.plot(S, tan, color=ORANGE, lw=1.2, ls="--", label="delta line at $S=100$")
    v90 = float(call(90.0, K0, R, SIG, 1.0))
    t90 = V0 + delta * (90 - 100)
    gain = v90 - t90
    assert abs(gain - 1.009) < 5e-4, gain
    ax.plot([90, 90], [t90, v90], color=INK, lw=1.4)
    ax.plot(90, v90, "o", color=BLUE, ms=4, zorder=5)
    ax.plot(90, t90, "o", color=ORANGE, ms=4, zorder=5)
    ax.annotate("", xy=(90, v90), xytext=(90, t90),
                arrowprops=dict(arrowstyle="<->", color=INK, lw=1.0))
    ax.text(91.5, 1.0, f"hedged P&L ${gain:.3f}$ (vertical gap at $S=90$)", ha="left", fontsize=9)
    ax.plot(100, V0, "o", color=INK, ms=3, zorder=5)
    ax.set_xlim(80, 120); ax.set_ylim(-3, 25)
    ax.set_xlabel("spot after gap $S$"); ax.set_ylabel("value")
    ax.legend(loc="upper left", fontsize=9, frameon=False)
    ax.set_title(r"gap $100\to 90$ with a short hedge of $\Delta=0.6368$ shares", fontsize=10)


# ---------- 20. drifted Brownian motion and its barrier questions  (cards 51, 52, 53) ----------
@figure("f07_drift_paths", w=5.0, h=2.7)
def _(ax):
    mu, n, T = 0.5, 200, 2.0
    dt = T / n
    t = np.linspace(0, T, n + 1)
    for j in range(25):
        rng = np.random.default_rng(300 + j)
        W = np.concatenate([[0.0], np.cumsum(math.sqrt(dt) * rng.standard_normal(n))])
        ax.plot(t, W + mu * t, color=GREY, lw=0.7, alpha=0.5)
    k = 0
    while True:
        rng = np.random.default_rng(700 + k)
        k += 1
        W = np.concatenate([[0.0], np.cumsum(math.sqrt(dt) * rng.standard_normal(n))])
        X = W + mu * t
        up = np.where(X >= 1)[0]
        dn = np.where(X <= -2)[0]
        if len(up) and (not len(dn) or up[0] < dn[0]) and up[0] > 0.3 * n and up[0] < 0.7 * n:
            break
    ax.plot(t[:up[0] + 1], X[:up[0] + 1], color=BLUE, lw=1.6)
    ax.plot(t, mu * t, color=INK, lw=1.0, ls=":", label=r"$E[X_t]=\frac{1}{2}t$")
    ax.axhline(1, color=GREEN, ls="--", lw=1.1)
    ax.axhline(-2, color=RED, ls="--", lw=1.1)
    ax.text(0.02, 1.08, "$+1$", ha="left", color=GREEN, fontsize=9.5)
    ax.text(0.02, -2.1, "$-2$", ha="left", va="top", color=RED, fontsize=9.5)
    ax.set_xlim(0, T); ax.set_ylim(-2.6, 3.6)
    ax.set_xlabel("time $t$"); ax.set_ylabel(r"$X_t$")
    ax.legend(loc="upper left", fontsize=9, frameon=False)
    # card 51: scale-function answer with mu=1/2, levels +1 and -2
    p_up = (1 - math.exp(-2 * mu * (-2))) / (math.exp(-2 * mu * 1) - math.exp(-2 * mu * (-2)))
    assert abs(p_up - 0.9100) < 5e-5, p_up
    # card 52: P(max_{[0,1]} X >= 1)
    a = 1.0
    p_max = (1 - float(Phi((a - mu) / 1.0))) + math.exp(2 * mu * a) * float(Phi((-a - mu) / 1.0))
    assert abs(p_max - 0.4901) < 5e-4, p_max
    ax.set_title(r"$X_t=W_t+\frac{1}{2}t$: $P(\mathrm{hit}\ +1\ \mathrm{first})=0.9100$, $E[X_1^2]=1.25$", fontsize=9.5)


# ---------- 21. biased walk as a Markov chain  (card 54) ----------
@figure("f07_biased_chain", w=5.0, h=1.9, axis=False)
def _(ax):
    p, q = 0.6, 0.4
    # h(x)=P(hit +1 before -2 | start x) for states -2,-1,0,1 (h(-2)=0, h(1)=1)
    A = np.array([[1, 0, 0, 0], [-q, 1, -p, 0], [0, -q, 1, -p], [0, 0, 0, 1]], float)
    b = np.array([0, 0, 0, 1], float)
    h = np.linalg.solve(A, b)
    assert abs(h[2] - 15 / 19) < 1e-12
    xs = {-2: 0.0, -1: 1.6, 0: 3.2, 1: 4.8}
    node(ax, (xs[-2], 0), "-2", fc=LIGHT_RED, ec=RED)
    node(ax, (xs[-1], 0), "-1")
    node(ax, (xs[0], 0), "0", ec=ORANGE, lw=2.0)
    node(ax, (xs[1], 0), "+1", fc=LIGHT_GREEN, ec=GREEN)
    for lo, hi in [(-2, -1), (-1, 0), (0, 1)]:
        arrow(ax, (xs[lo], 0), (xs[hi], 0), None, rad=-0.35, color=BLUE, shrink=16)
        arrow(ax, (xs[hi], 0), (xs[lo], 0), None, rad=-0.35, color=RED, shrink=16)
        mid = (xs[lo] + xs[hi]) / 2
        ax.text(mid, 0.62, "0.6", ha="center", color=BLUE, fontsize=10)
        ax.text(mid, -0.62, "0.4", ha="center", color=RED, fontsize=10)
    frame(ax, -0.7, 5.5, -1.05, 1.15)
    caption(ax, r"$P_0=\frac{1-(q/p)^2}{1-(q/p)^3}=\frac{15}{19}\approx 0.7895$ (fair walk: $\frac{2}{3}$)")


# ---------- 22. exponential martingale versus its mean  (cards 7, 27) ----------
@figure("f07_exp_martingale", w=5.0, h=2.6)
def _(ax):
    n, T = 400, 2.0
    t = np.linspace(0, T, n + 1)
    dt = T / n
    shown = 0
    k = 0
    while shown < 12:
        rng = np.random.default_rng(40 + k)
        k += 1
        W = np.concatenate([[0.0], np.cumsum(math.sqrt(dt) * rng.standard_normal(n))])
        M = np.exp(W - 0.5 * t)
        if M.max() < 4.0:
            ax.plot(t, M, color=GREY, lw=0.7, alpha=0.6)
            shown += 1
    ax.plot(t, np.exp(t / 2), color=RED, lw=1.8, label=r"$E[e^{W_t}]=e^{t/2}$, $=1.6487$ at $t=1$")
    ax.axhline(1, color=BLUE, lw=1.8, ls="--", label=r"$E[e^{W_t-t/2}]=1$")
    ax.plot(1, math.exp(0.5), "o", color=RED, ms=4, zorder=5)
    ax.set_xlim(0, T); ax.set_ylim(0, 4.0)
    ax.set_xlabel("time $t$"); ax.set_ylabel("value")
    ax.legend(loc="upper right", fontsize=9, frameon=False)
    ax.set_title(r"$e^{W_t-t/2}$ is a martingale (grey paths); $e^{W_t}$ is not", fontsize=9.5)


# ---------- 23. Feynman-Kac for E[W_T^2 | W_t=x]  (cards 16, 33) ----------
@figure("f07_feynman_kac", w=5.0, h=2.6)
def _(ax):
    T = 2.0
    x = np.linspace(-2.5, 2.5, 301)
    ax.plot(x, x * x + (T - 0.0), color=BLUE, lw=1.6, label=r"$t=0$: $u=x^2+2$")
    ax.plot(x, x * x + (T - 1.0), color=ORANGE, lw=1.6, label=r"$t=1$: $u=x^2+1$")
    ax.plot(x, x * x, color=GREEN, lw=1.4, ls="--", label=r"$t=T=2$: payoff $x^2$")
    ax.plot(0, 2.0, "o", color=BLUE, ms=5, zorder=5)
    ax.text(0.3, 3.1, r"$u(0,0)=2$", color=BLUE, fontsize=9.5)
    ax.set_xlim(-2.5, 2.5); ax.set_ylim(-0.2, 8.5)
    ax.set_xlabel("state $x=W_t$"); ax.set_ylabel(r"$u(t,x)$")
    ax.legend(loc="upper center", fontsize=8.5, frameon=False)
    assert abs((0 + T) - 2.0) < 1e-12
    ax.set_title(r"$u_t+\frac{1}{2}u_{xx}=0$, $u(T,x)=x^2$, so $u(t,x)=x^2+(T-t)$", fontsize=9.5)


# ---------- 24. static replication of max(S, K)  (card 43) ----------
@figure("f07_static_max", w=5.0, h=2.6)
def _(ax):
    S = np.linspace(60, 140, 401)
    ax.plot(S, np.maximum(K0 - S, 0), color=RED, lw=1.4, ls="--", label=r"put $(K-S_T)^+$")
    ax.plot(S, np.maximum(S, K0), color=INK, lw=2.2, label=r"$\max(S_T,K)$")
    ax.axvline(K0, color=GREY, ls=":", lw=1.0)
    ax.text(K0 + 1, 62, "$K=100$", color=GREY, fontsize=9.5)
    price = S0 + float(put(S0, K0, R, SIG, 1.0))
    assert abs(price - 105.5735) < 5e-4, price
    ax.set_xlim(60, 140); ax.set_ylim(-2, 70)
    ax.set_xlabel(r"$S_T$"); ax.set_ylabel("payoff")
    ax.legend(loc="upper left", fontsize=9, frameon=False)
    ax.set_title(r"$\max(S_T,K)=S_T+(K-S_T)^+$: price $100+5.5735=105.5735$", fontsize=9.5)


# ---------- 25. static replication of S_T^2  (card 42) ----------
@figure("f07_sq_strip", w=5.0, h=2.7)
def _(ax):
    F = S0 * math.exp(R)
    S = np.linspace(40, 180, 561)
    tangent = F * F + 2 * F * (S - F)
    ax.fill_between(S, tangent, S * S, color=LIGHT_BLUE, lw=0)
    ax.plot(S, S * S, color=BLUE, lw=1.8, label=r"$S_T^2$")
    ax.plot(S, tangent, color=ORANGE, lw=1.2, ls="--", label=r"tangent at $F$")
    ax.axvline(F, color=GREY, ls=":", lw=1.0)
    ax.text(F + 2, 2000, f"$F={F:.2f}$", color=GREY, fontsize=9.5)
    Kg = np.linspace(1e-3, 1000, 400001)
    pt = trap(2 * np.where(Kg < F, put(S0, Kg, R, SIG, 1.0), 0.0), Kg)
    ct = trap(2 * np.where(Kg >= F, call(S0, Kg, R, SIG, 1.0), 0.0), Kg)
    price = math.exp(-R) * F * F + pt + ct
    assert abs(price - 10941.74) < 0.02, price
    ax.set_xlim(40, 180); ax.set_ylim(0, 32000)
    ax.set_xlabel(r"$S_T$"); ax.set_ylabel("payoff")
    ax.legend(loc="upper left", fontsize=9, frameon=False)
    ax.set_title(r"$S_T^2=F^2+2F(S_T-F)+(S_T-F)^2$: the wings are $2\times$ OTM options", fontsize=9.5)
