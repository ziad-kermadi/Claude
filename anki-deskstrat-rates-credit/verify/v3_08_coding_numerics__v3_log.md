# Verification log: cards/08_coding_numerics__v3.json

25 cards checked. 6 cards changed. Structure unchanged (25 cards, same types, one lvl_* tag each, valid JSON).

## Changes

| file | card index | issue | fix | source URL or "recomputed" |
|---|---|---|---|---|
| 08_coding_numerics__v3.json | 2 | Segment length given as about 3163 steps; N/k* = sqrt(10^7) = 3162.3 | changed to about 3162 steps | recomputed (python) |
| 08_coding_numerics__v3.json | 5 | Back said a plain assignment gives 7.389056 for df/dx. Compiled a plain-assignment variant: result is 7.389056 only because g++ evaluates vexp(x) before x*y. C++ leaves operand order unspecified, so the claim was order-dependent | reworded: plain assignment overwrites one contribution; which survives depends on unspecified operand order; with this g++ it is 7.389056 | recomputed (compiled and run) |
| 08_coding_numerics__v3.json | 13 | Simulated mean of best-of-100 Sharpe stated as 1.13. Simulation (4,000 x 100 draws, sd 0.447) gives 1.121; exact E[max of 100 std normals] = 2.508 x 0.447 = 1.121. Formula gives 1.13 (about 1% high) | simulated mean changed to 1.12 and the formula's bias stated; sd 0.20 confirmed (0.198) | recomputed (python); exact E[max] value for N=100 is a standard result |
| 08_coding_numerics__v3.json | 13 | Sharpe SE formula is for T annual observations. The daily-data form was not stated | added daily form sqrt((1+SR^2/(2*252))/T); equals 1/sqrt(T) at zero Sharpe, so the card value 0.447 is unchanged | derived (Lo-type SE, daily sr scaled by sqrt(252)); matches the formula in the task brief |
| 08_coding_numerics__v3.json | 16 | "values-only leaves a degree-7 fit under-determined": 8 points with 8 coefficients is an exact interpolant, not under-determined. Protocol behind the numbers not stated | corrected the wording; stated protocol (uniform points on [-1,1], default_rng(1), 300 sets, 2001-point grid, lambda = Var f / Var f' = 0.109). Medians 2.17e-3 / 7.36e-4 and means 0.039 / 0.022 reproduced exactly with that seed | recomputed (python) |
| 08_coding_numerics__v3.json | 21 | Legendre basis "in S/S0" is undefined on [0.5, 1.5] (Legendre polynomials live on [-1,1]). Condition numbers: 1.8e13 raw, 3.2e26 normal, 5.2e4 monomial in x, 3.3 Legendre all reproduced on a 1,001-point uniform grid | basis specified as Legendre in 2S/S0 - 2; note added that condition numbers are for uniform 1,001-point grids | recomputed (python) |
| 08_coding_numerics__v3.json | 24 | Pseudo-random MC RMSE 4.1e-3 over 40 runs not reproduced. Theory sqrt(((1+1/48)^5-1)/4096) = 5.15e-3 and 4000-run simulation 5.06e-3. Scrambled Sobol RMSE 7e-6 not reproduced: 40 scrambles give 1.1e-5 | MC RMSE changed to about 5.1e-3 (theory, confirmed); Sobol changed to about 1.1e-5 (40 scrambles). The 16-scramble mean 1.0000013 and SE 2.6e-6 reproduced exactly and kept | recomputed (python, scipy Sobol scramble) |

## Checked, no change needed

- 0, 1: AAD reverse sweep. v3 = 6, v4 = 7.389056, v5 = 13.389056, dbar1 = 10.389056, dbar2 = 2. Matches closed form.
- 3: digital AAD. Qualitative and correct (pathwise derivative zero a.e.; LR and smoothing fixes).
- 4: tape memory. 10^5 x 250 x 10 x 32 B = 8.0 GB = 7.45 GiB; per path 80,000 B. Correct.
- 5: compiled with g++ -std=c++20 -Wall -Wextra -O2, no warnings. Output f = 13.389056, df/dx = 10.389056, df/dy = 2.000000, tape nodes = 5. Matches card.
- 6, 7, 8: PCA DV01. g = (-5000, -20124.6, 25000, 73790.2). Sum g^2 = 6.5e9 = |p|^2. Hedge (-20000 at 2y, +30000 at 10y) clears level, slope and curvature; residual 20000 x sqrt(20) = 89,443. Unhedged sigma-weighted std 85,037 per day; hedged 44,721 (fall of 47.4%). All recomputed.
- 9, 14, 17, 20: qualitative desk and model-risk content. No checkable figures. Left as is.
- 10, 11, 12: backtest. Gross Sharpe 0.833; drag 2.0%; net Sharpe 0.50; break-even 12.5 bp; 3 bp net Sharpe 0.633; 1 - 0.98^5 = 9.6%; PD x LGD = 1.2%. Recomputed.
- 15: Huge and Savine (arXiv:2005.02347, Brian Huge and Antoine Savine) confirmed by web search. Loss form (value MSE + lambda x derivative MSE) matches the card. See doubts below.
- 18, 19: Tikhonov/SVD. Step (J^T J + alpha I) delta = -J^T r - alpha(theta - theta0) and filter factors f_i = sigma_i^2/(sigma_i^2+alpha) verified. Case study: sv 2.5495 and 1.21e-4, cond 2.1e4; with residual +-1e-3 alternating, step norm 14.89 (split -10.53, +10.53), alpha=1e-6 norm 0.214, alpha=1e-4 norm 0.0022; f2 = 0.0144 and 1.46e-4. All reproduced.
- 22, 23: Brownian bridge and KL. Conditional law N(tb/T, t(T-t)/T) correct. Terminal-normal share 67% (pointwise) and 75% (average) correct. KL first eigenvalue 4/pi^2 and share 8/pi^2 = 81%; 98.6% of Var of the average (32/pi^4 / (1/3)). Recomputed.
- 24: 16-scramble mean 1.0000013, SE 2.6e-6, t_15 = 2.131, interval covers 1. Reproduced.

## Unverified / doubtful

- 15: the Risk venue for Huge and Savine was not confirmed by search (only the arXiv record). The lambda rule "lambda approx Var(v)/Var(z)" is offered as an example choice, not as the paper's rule. Search found no 2020 paper rule for lambda.
- 2: "binomial (Griewank-type) schedules do better when the memory budget is fixed in advance" is a qualitative claim, not checked against Griewank and Walther (revolve). Left as is.
- 10: "a same-bar bias typically collapses toward zero" is qualitative.
- 11: "about 1.2% per year overstated return" is an approximation, already labelled approximate.
- 16: the Other-seeds sentence says means move by about 30%. Seeds 0 to 4 give values-only means 0.027 to 0.040 and derivative means 0.016 to 0.025, so the spread is about +-20% to -30%. Approximate.
- 19: the card does not state the residual vector; it is reproduced with alternating +-1e-3 residuals, which matches the card's description.
