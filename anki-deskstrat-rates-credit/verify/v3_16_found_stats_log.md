# Verification log: cards/16_found_stats.json (v3)

Card index is the 0-based position in the JSON array. 50 cards checked, 50 cards kept (count and types unchanged: 41 basic, 9 cloze).

## Changes

| File | Card index | Issue | Fix | Source URL or "recomputed" |
|---|---|---|---|---|
| 16_found_stats.json | 1 | "three factors typically explain above 99%" overstated for government curves | "about 98 to 99% or more" | https://resolve.cambridge.org/core/books/abs/bond-pricing-and-yield-curve-modeling/principal-components-empirical-results/EE31CBAC58AFD27A8777C5EC73B7594A (three PCs about 98 to 99%; first eigenvalue above 90%). Level share in a US Treasury sample was about 93.5% (secondary source, not used as a figure) |
| 16_found_stats.json | 11 | Simulated figures: 78% rejection at T=100, median R² and 90th percentile, DW | Rejection 77% (T=100), 93% (T=1000); 90th pct R² about 0.60; DW close to 0 (median 0.15 at T=100, 0.02 at T=1000) | recomputed (numpy, 1000 reps, seed 12345) |
| 16_found_stats.json | 13 | "half-life ranges from about 15 to about 45 days" is a one-SE range, not a 95% range (95% reaches phi of about 1) | Stated as the one-SE range 0.955 to 0.985 giving about 15 to 47 days; the 95% range reaches phi of about 1 | recomputed (SE = sqrt((1-phi^2)/250) = 0.0154; half-lives 14.9 and 47.0) |
| 16_found_stats.json | 14 | Simulated sd of overlapping mean given as 0.156 | 0.159 | recomputed (20,000 reps, T=1000, sigma=1; naive 0.071, true 0.158) |
| 16_found_stats.json | 16 | Newey–West "plug-in rule" called the full data-driven bandwidth; floor(4(T/100)^(2/9)) is the lag-count rule | Relabelled as the lag-count rule for the Bartlett kernel; value 6 and 77% kept | https://ideas.repec.org/a/oup/restud/v61y1994i4p631-653..html (Newey and West 1994, automatic lag selection); recomputed for 4(T/100)^(2/9) = 6.67, floor 6 |
| 16_found_stats.json | 24 | Annualised Sharpe SE sqrt((1+SR^2/2)/Y) stated for daily data; wrong by the factor 252 inside the SR^2 term | For annual observations keep sqrt((1+SR^2/2)/Y); for daily data with annual SR, sqrt((1+SR^2/504)/Y) (about 1/sqrt(Y)) | recomputed (daily SR = SR/sqrt(252); Var of annualised SR = (1+SR_d^2/2)/Y) |
| 16_found_stats.json | 42 (cloze front) | "Y years of i.i.d. data" ambiguous for the annual-observation formula | "Y years of annual i.i.d. observations" | recomputed (same derivation as index 24) |
| 16_found_stats.json | 11, 19, 26, 27 | Raw ">" and "<" in MathJax text | Escaped as &gt; and &lt; (no content change) | HTML validity |

## Checked and recomputed without change (no edit needed)

- 0, 2, 3: covariance quadratic forms (100, 16, 4, 32, 24), eigenpairs, PC shares 83.3% and 96.7%, steepener loadings, eigenvalue gaps 84 and 12.
- 4, 5, 6, 7: determinant -2.888, eigenvalues -0.8, 1.9, 1.9, witness -0.8, clip-and-rescale matrix (eigenvalues 0, 1.5, 1.5, Frobenius 0.98). Higham nearest correlation matrix (Dykstra) equals the same matrix, so the card 6 coincidence claim holds. Cholesky: L22 = 0.436, L32 = 3.923, pivot -15.2.
- 8, 9, 10: h = 1.108, residual sd 3.49, 81% variance removed, plim 0.5, SE 0.034, CI [1.04, 1.17].
- 12: DF critical values (-2.86 with constant, -3.41 with trend, -1.95 without, -3.43 at 1%). Standard MacKinnon asymptotic values; not separately web-checked in this pass.
- 15, 16, 28: gamma_k = (5-k) sigma^2, long-run variance 25, Bartlett fractions 20, 36, 49.3, 68, 77.1, 82.2, 92.4%, naive vs true t 6.12 and 2.74, CI [0.57, 3.43].
- 17, 18, 21, 22, 23, 25, 27, 29, 30, 31, 32, 33, 34, 35, 36-41, 43-49: OLS check (b = 1.99, a = 0.05, R² = 0.9973), MLE bias 9/10, Newton iterates 3.1662%, 3.1936%, root 3.1936%, error ratio 1.94, ES 2.665 sigma and ratio 1.146, t4 99% quantile 3.747, t4 ES 3.69 sigma (GBP 7.38m, 38% above normal), AR(1) half-life 22.8 and 45.5 days, innovation sd 0.97, stationary sd 4.11, Bonferroni z 3.48, best-of-100 Sharpe 1.12, t-stat 1.05, condition number 148 and 12.2, VIF 33.4 (sqrt 5.78), adjusted R² 0.157, Bartlett weights, AR(1) long-run ratio 1.5.
- 46: IR = 0.3; fundamental law 0.05 * sqrt(100) = 0.5 (Grinold 1989; not web-checked in this pass).

## Unverified or to watch

- Index 1: the claim "about 90% or more in PC1" rests on one government-curve source (Cambridge, first eigenvalue above 90%) and a US Treasury sample (93.5%). Presented as "about", so kept.
- Index 16: the full Newey–West automatic bandwidth is a data-driven plug-in; the card now says so and does not give its value.
- Index 12 and 31: Dickey–Fuller critical values and Politis–Romano stationary bootstrap were not re-checked against primary sources in this pass.
- Index 4/5/6: the nearest-correlation claims were confirmed numerically (Dykstra limit); Higham (2002) citation was not web-fetched.
- Index 24: the daily-to-annual conversion is a derivation, not a cited result (Lo 2002 abstract confirmed the paper; the exact SE expression was not retrieved).
