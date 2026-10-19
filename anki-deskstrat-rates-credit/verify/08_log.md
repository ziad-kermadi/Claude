# Verification log: 08 coding and numerics cards

Files: `cards/08_coding_numerics.json` (44 cards), `cards/08_coding_numerics_deep.json` (30 cards).
Checked: 74 cards. Changed: 16 cards (7 in the main file, 9 in the deep file). Fronts, card types and tags are unchanged. Both files validated as JSON.

## Changed cards

| Index | File | What was wrong | Fix | Source or method |
|---|---|---|---|---|
| 7 | main | Said the naive in-sample LSM estimate has "no guaranteed sign". | In-sample policy overfits the same paths, so the price is biased upward. Tagged approx.; unverified. | Reasoning. Glasserman-Yu search did not return the statement. |
| 13 | main | Said the boundary error is dominated by the K e^{-rτ} N(-d2) term. At S=250 the two terms are about 3.6e-4 and 3.7e-4 and nearly cancel. | Explanation rewritten. Added S_max ≈ 280 for error ≈ 1e-6 (the error at 280 is 8.0e-7). | Recomputed in Python. Errors 1.46e-5 (S=250) and 1.17e-7 (S=300) confirmed. |
| 15 | main | Said the p-in-(0,1) condition fails when Δt is "large relative to σ". | Exact condition: r·Δt ≥ σ√Δt, i.e. Δt ≥ (σ/r)². Ritchken reference tagged unverified. | Recomputed algebra. |
| 24 | main | "2 to 5 times" stated as a rule of thumb with no constant. | Tagged approx.; unverified. Baur-Strassen constant is quoted as 4 or 5 depending on the cost model. | WebSearch: no clean 5x source found (3L, 4L and 3L+n variants). |
| 29 | main | PCA variance shares given without source. | Tagged approx.; unverified. | WebSearch: Litterman-Scheinkman (1991) not retrieved. Secondary source (Piazzesi, via Pérignon et al.) gives over 96% for the first three PCs in a later sample. |
| 35 | main | std::list footprint "two to three times" a vector of doubles. | About four times per double: a 24-byte node plus allocator overhead, about 32 bytes against 8. Tagged approx. | Arithmetic. |
| 40 | main | Said -0.0 and 0.0 "hash differently and break lookups". | Tested with g++ 13 (libstdc++): they hash equal and lookup succeeds. Replaced with the real failure: NaN keys duplicate in unordered_map (size 2 after two inserts). | Compiled and run. |
| 2 | deep | In-sample LSM bias direction (consistency with main 7). | Tagged approx.; unverified. | Reasoning. |
| 8 | deep | Adjoint toy used undefined weights c_j; the value -0.88680 could not be reproduced (c=(1,1,1) gives -1.7371). | Specified toy V = P_2 with quotes 4.00, 4.10, 4.20%. Adjoint and 1e-7 bump both give -1.81007. | Recomputed (Python). |
| 11 | deep | Test labelled "Black case" but uses normal vol σ_N = 1.20%. | Relabelled Bachelier. Price 2.405e-5 and 7 iterations confirmed. | Recomputed. |
| 14 | deep | Quoted MC means (39.842, 39.748) did not reproduce on a fresh 2M-path run. | Replaced with a seeded run (default_rng(1)): pathwise 39.856 ± 0.052, LR 39.875 ± 0.176, variance ratio 11.3. | Recomputed. Score formula (z²-1)/σ - z√T rederived and checked. |
| 15 | deep | Baur-Strassen "roughly five times" stated as fact. | Tagged approx.; unverified (4 to 5 depending on cost model). | WebSearch (see main 24). |
| 17 | deep | OU simulation numbers (mean 0.961, bias -0.019, median half-life 19.5 days) not reproduced. | 20,000 reps, seed 7: mean 0.962, bias -0.018, median half-life 20.1 days, 0.05% of replications above 1. Kendall formula -(1+3φ)/n checked against the intercept-case first-order formula in the literature (approx.). | Simulation (NumPy). WebSearch (Amsterdam DP 2004-08 and 2009-09). |
| 21 | deep | Simulated bias -0.019 (now -0.018 per the recomputed run). | Updated to match. | Simulation. |
| 25 | deep | Code docstring said "antithetic pairing", which the code does not implement. | Docstring corrected. Numbers unchanged (closed form 0.0120545, plain 0.0120601 ± 0.0000206, CV 0.0120585 ± 0.0000120, ρ = 0.812 all reproduced). | Run. |
| 26 | deep | sd factor sqrt(1/2 - 1/(2π)) is 0.5838, not 0.5833; per-unit SD 0.02364. | Corrected. N ≈ 5.6e6 unchanged. | Closed form and 4M-path MC (0.02363). |

## Checked and confirmed without change (selected)

- Deep 5 (OIS bootstrap): P = 0.961538, 0.922744, 0.883743, 0.846387, 0.807641 reproduced by running the code.
- Deep 6 (Newton on pillars): residual norms 3.1e-2, 2.0e-4, 9.4e-9, 1.1e-16 reproduced. Analytic Jacobian vs forward difference (h = 1e-7): max difference 5.2e-8, matching the card.
- Deep 9 and 11 (Bachelier IV): price 0.0053434, 4 iterations, error 3e-14, bisection 34 iterations, OTM case recovered in 7 iterations. All reproduced.
- Deep 18 and 23 (complex step): Im f(1+ih)/h = 3.7560492270947 at h = 1e-20, matching exact. Central difference agrees to about 10 digits. O(h²) error confirmed.
- Deep 19 (Black-to-Bachelier ATM): approx. 0.740234%, exact root 0.740348%. Card's 0.74023% and 0.74035% confirmed.
- Deep 27 and 28 and 29 (C++ and pandas): both C++ programs compile cleanly under g++ -std=c++17 with -Wall. Cache: builds = 1, then 2 after invalidation. AD: price 7.128065, vega 39.893498. Pandas loop vs vectorised: maximum difference 0; ratio about 500x on this machine.
- Main 13 numbers at S_max = 250 and 300: confirmed (see table).
- Main 16 (Brenner-Subrahmanyam ATM approximation σ ≈ √(2π/T)·C/F): confirmed numerically to about 0.2%.
- Main 36 (naive variance): numerical cancellation confirmed (naive 0.0100136 vs 0.0100134 true at mean 1e5).
- Main 39 (pandas fan-out, groupby dropna, Series.sum skipna): fan-out gives 3 rows and notional sum 40; validate='many_to_one' raises; dropna=True drops the null key; sum(skipna=False) returns NaN. All confirmed.
- Main 41 (interval sweep, [0,1),[1,2),[1,3) gives 2): confirmed.
- Main 42 (NaN and signed zero in a set): confirmed.
- Main 43 (Kendall tau for n=50, 653 inversions): tau = -0.0661. C(10^6,2) = 5e11. Confirmed.
- Deep 12 (θ-scheme amplification factor): algebra checked.
- Deep 15 (AAD worked example): gradient (x2 + cos x1, x1) rederived.
- Deep 16 (2x2 Cholesky): algebra checked.
- Deep 20 (annuity measure): algebra checked.
- Main 1, 2, 3, 5, 6, 12, 20, 22, 23: formulas checked by derivation; no numerical error found.

## Unverified items (kept, tagged or flagged)

1. Baur-Strassen gradient cost constant (main 24, deep 15). Sources give 3L, 4L and 3L+n; the card's "5x" is not confirmed.
2. Direction of the in-sample LSM bias (main 7, deep 2). The upward direction is from the standard argument; Glasserman-Yu search did not confirm it.
3. Yield-curve PCA variance shares (main 29). Litterman-Scheinkman (1991) figures not retrieved. Ranges are rules of thumb.
4. Ritchken reference for boundary smoothing (main 15). Not checked.
5. Brent vs safeguarded Newton cost (deep 11). Not benchmarked; already tagged in the card.
6. Andersen-Broadie (main 8, 10; deep 3), Rannacher smoothing (main 11), Leisen-Reimer (main 15): checked against the standard formulas by derivation. No web source was fetched for these.
7. Kendall AR(1) bias: the first-order formula is consistent with the intercept-case literature (approx.). The simulated bias (-0.018) is larger in magnitude than the formula (-0.016), which the card now states.
