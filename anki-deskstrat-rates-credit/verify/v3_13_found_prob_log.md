# Verification log: cards/13_found_prob.json (50 cards)

Checked: all 50 cards (formulas, signs, conventions, worked numbers, cross-references, chain numbering, tags, HTML). Numbers recomputed with python3 (scipy norm, closed forms) and Monte Carlo (2e6 draws for GBM/GBM-drift/digital/first-to-default; 2e4 x 2000-step paths for reflection; 5000 paths for exit from (-1,2); 5000 x 1000-step paths for quadratic variation and Itô integral).

## Changes

| Card (0-based index) | Issue | Fix | Source |
|---|---|---|---|
| 16 (STOP 2/3) | Optional stopping justification said "τ is bounded in expectation" (the relevant property is that the stopped path is bounded on [-1,2]). Equation written as "2p-1(1-p)", ambiguous. | Justification now cites the stopped path lying in [-1,2]; equation written as 2p-(1-p). Result p=1/3 unchanged. | recomputed (MC P(hit 2 first)=0.331 vs 1/3) |
| 27 (NUM 3/3) | Dividend follow-up martingale wrong: S_t e^{-qt}/P(t,T). Under the T-forward measure the martingale is S_t e^{-q(T-t)}/P(t,T) = e^{-qT} S_t e^{qt}/P(t,T) (total-return asset is S e^{qt}). | Replaced with S_t e^{-q(T-t)}/P(t,T) and its equivalence to e^{-qT}S_t e^{qt}/P(t,T). | recomputed (Itô on S e^{qt}/B; F=S_0e^{-qT}/P(0,T) checked at t=0 and t=T) |
| 44 (cloze) | "It is the only copula-level link" overstated: Spearman also has a closed form (card 43). | Replaced with "It is a closed-form link". | recomputed (tau=2/pi asin rho=1/3; rho_S=0.4826) |
| 48 (OU 3/3) | "Why is normal volatility the convention after 2015?" date not supported; sources place the shift to normal quoting in the early-to-mid 2010s, with no single EUR switch date. | Question reworded to "early-to-mid 2010s". | WebSearch: "The new normal" actuarial report (4 Sep 2015) on Bachelier/shifted quotes emerging after ~2012; https://web.actuaries.ie/sites/default/files/erm-resources/2079LDP_20150911.pdf ; https://www.sciencedirect.com/science/article/abs/pii/S1544612317305974 |

## Recomputed, unchanged (examples)

- GBM 2/4: E[S_T]=117.35, E[S_T^2]=15,605, Var=1,833.6, sd=42.8 (MC mean 117.33, var 1831).
- GBM 3/4: median 110.24, ratio 1.0645 = e^{σ²T/2}; vol drag -4.5%.
- GBM 4/4: BS call 9.413 (MC Q 9.407); with μ=8% discounted at r: 12.73 (closed form 12.727), overstated 35.2%; θ=0.25.
- GIRS 3/4: P(S_1>120)=27.04% (MC 27.03%), Q=19.45% (MC 19.42%); digital 0.189 vs wrong 0.262.
- Risky bond: 0.7788 + 0.0354 = 0.8142.
- Poisson/first-default: 3.92%, 0.98%, 2.94%, share 0.25 (MC 0.2501; within-1y 0.0098 MC 0.0098).
- Normal anchors, one-sided 1.645/2.33, tails 15.87/2.28/0.135/0.99%; Mills estimate 0.00137 vs exact 0.00135 (overshoot 9.4%).
- Copula: tau=1/3, rho_S=0.4826. Bivariate normal: beta 1.2, E=1.8, Var 2.56.
- Jensen: E[e^X]=1.0202; E[1/(1+r)]=0.970965 vs 0.970874 (0.9bp).
- OU/Vasicek: mean 2.393%, sd 0.795%, P(r1<0)=0.13% (MC 0.12%); stationary sd 1%, P(r<0)=0.135%.
- Itô: d ln S drift 4.875%; with σ=50%, -4.5%. ∫W dW = (W_T^2-T)/2 (MC mean ~0); E[(∫W dW)^2]=T^2/2 (MC 0.504 at T=1). Quadratic variation mean 1.001, var 2T^2/n.
- Reflection: 2(1-Φ(1))=31.7% (discrete MC 30.5% at 2000 steps, consistent with discretisation bias).
- Cross-references checked (1-based): "card 2", "card 9", "card 11", "GIRS 2/4", "GBM 4/4" all point to the intended cards.

## Format checks

- 50 cards, types unchanged, valid JSON (ensure_ascii=False, indent=1).
- Every card has exactly one lvl_* tag; tag counts within 2-7.
- Chain prefixes and n/N numbering consistent across all 8 chains.
- No raw < or & outside tags/entities; no markdown; MathJax in \( \) / \[ \]; cloze syntax valid.

## Unverified / doubtful

- Card 48 normal-vol timing: the sources support "early-to-mid 2010s" only; no single EUR switch date was found.
- Card 23 (Heston vol-risk premium) and card 29 "weak sense" remark: qualitative statements, not checked against a primary source.
- Card 22 uses the digital price as e^{-r} Q(S_1>120); fine for this single-period case.
- Chain GIRS 2/4 and chain OU 1/3 are cloze cards inside chains (spec suggests basic); left as is.
