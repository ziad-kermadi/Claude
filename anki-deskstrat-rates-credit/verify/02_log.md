# Verification log: 02_swaps_curves (base and deep)

Checked: 85 cards (55 base, 30 deep). Changed: 12 cards (6 base, 6 deep). Deep card 22 was edited by mistake and restored to its original text, so it is not counted.

## Cards changed

| Index | File | What was wrong | Fix | Source or method |
|---|---|---|---|---|
| 5 | 02_swaps_curves.json | USD 3M LIBOR fallback spread given as "26bp" with no precision; "check against schedule" note left open | Front now "26.161bp"; back states the spread was fixed 5 March 2021 (5-year median) and that 1M, 6M, 12M are not verified | ARRC fallback summary and LSEG/ISDA-fallback documents (26.161bp for 3M confirmed); Bloomberg vendor fixing 5 Mar 2021 |
| 7 | 02_swaps_curves.json | Fallback coverage stated without the US statutory route | Added that US-law legacy contracts were covered by the Adjustable Interest Rate (LIBOR) Act (2022) | Standard US LIBOR transition fact; not separately web-checked |
| 28 | 02_swaps_curves.json | "10y PV01 almost nine times the 5y one" | Corrected to about 1.7 times (46k vs 80k per bp on 100m) | Recomputed: 100m x 4.6 x 1e-4 = 46,000; 100m x 8.0 x 1e-4 = 80,000 |
| 30 | 02_swaps_curves.json | "1% move in start DF" ambiguous; 1/A = 0.238 gives 24bp only for a 0.01 absolute move | Reworded to a 0.01 (one-point) move | Recomputed: 0.01/4.2 = 23.8bp |
| 40 | 02_swaps_curves.json | Trade direction wrong: receive fixed plus short Treasury is short the spread, not long. Also the eSLR status was left as "verify" | Long the spread = pay fixed and buy the Treasury (DV01-matched). eSLR status filled in (see below) | Sign derivation: P&L of pay-fixed + long bond is proportional to delta(swap) - delta(yield) = delta(spread) |
| 42 | 02_swaps_curves.json | LCH USD switch date given only as "2020" | Date added: go-live 16 October 2020; completion reported 20 October 2020 | LCH/LSEG press release 20 Oct 2020; CFTC filings on the SOFR discounting transition |

Deep file:

| Index | File | What was wrong | Fix | Source or method |
|---|---|---|---|---|
| 6 | 02_swaps_curves_deep.json | Discount-curve DV01 given as +2,600 per bp. The card's own expression 100m x (-0.0020) x (-13.1) x 1e-4 = +262 | Corrected to +260 per bp (dA/dy recomputed as -12.96 per unit yield) | Recomputed with python; cross-checked by finite difference of the annuity: 1e8 x (-0.002) x (-0.00130) = +260 |
| 10 | 02_swaps_curves_deep.json | CMS adjustment 14.3bp and 11.8bp; numbers were right but unchecked | Values kept; added a quadrature check line | Gauss-Hermite on the exact flat-yield expectation: 14.26bp (tau_p=0), 11.84bp (tau_p=0.5). Closed form matches |
| 14 | 02_swaps_curves_deep.json | "Both terms are positive" but the lag term -tau_p/(1+y) is negative | Reworded: lag term negative, annuity term positive, net positive | Algebra |
| 15 | 02_swaps_curves_deep.json | HW futures convexity used 0.5 x B^2 v; gave 4.44bp (3y) and 11.27bp (5y). Ho-Lee check claimed to reproduce 1/2 sigma^2 T1 T2 | Rewritten: CA = (B/(tau P)) (B v + I) with I = sigma^2(1-e^{-aT1})^2/(2a^2). Recomputed 4.78bp (3y) and 11.81bp (5y) before the 1/P factor (about 4.83 and 11.9 after) | Exact identity E^Q[F]-E^T2[F] = -Cov(F,D); Monte Carlo of the joint Gaussian law (r(T1), int r) gives 4.75bp and 11.73bp, agreeing to about 1% |
| 23 | 02_swaps_curves_deep.json | Uses 4.44 / 11.27 HW, 4.88 / 13.13 Ho-Lee | HW set to 4.8bp and 11.8bp (forwards 3.952% and 3.882%); Ho-Lee textbook values kept, first-order Gaussian value 5.25 / 13.75 added | As card 15 |
| 25 | 02_swaps_curves_deep.json | Cloze gives the Ho-Lee a-to-0 limit as 1/2 sigma^2 T1 T2 | Changed to sigma^2 T1 (T2 - T1/2). Agrees with 1/2 sigma^2 T1 T2 only when T2 = T1 | Girsanov drift under Q^T2 gives delta = -sigma^2 (T1 T2 - T1^2/2). The bond-based check (Ho-Lee bond formula, E^T2[1/P] = P(0,T1)/P(0,T2)) reproduces this |

Recomputed and confirmed without change: base 0 (telescoping), 1 (5% SOFR uplift 1.0bp, 12.6bp for a year), 4 (5.07%), 13 (DF2 = 0.9246), 26-27 (par 4.081% and payer PV), 29, 31-32 (Bachelier 1.8m), 36-37 (CIP, 1.1216 forward, 216 pips), 45-46 (FVA -42,500; MVA 340,000; KVA 850,000 illustrative), 53-54 (0.144 per 100; 62,500); deep 0-3 (DF1 0.960615, DF2 0.920973, zeros 4.2021%, 1y1y 4.3043%; 1.5y log-linear 0.940585 vs linear 0.940816, gap 1.7bp; Jacobian and 1.5y sensitivities -13,549 per bp confirmed by bump-and-reprice), 4-5 (receiver MTM -910,734 to -913,332, change -2,598; carry 2.53 per day), 7-9 (CIP 1.10547; implied 4.2512%; 47,135 EUR per bp), 18-22 (3y DF 0.882525; payer 2,289,854; PV01 45,797; 25bp move exact 1,136,800 vs first-order 1,144,927), 19-20 (10y annuity 8.5302; hedge residual zero), 26 (flat 4% cont. par 4.081%).

## Facts checked against sources

- ISDA USD 3M LIBOR fallback spread 26.161bp: confirmed (ARRC and LSEG documents). 1M 11.448bp, 6M 42.826bp, 12M 71.513bp: NOT confirmed; not stated on any card.
- LCH USD discounting EFFR to SOFR: go-live 16 October 2020, completion 20 October 2020 (LCH/LSEG press release; CFTC filings).
- LCH EUR discounting EONIA to €STR: effective 27 July 2020 (LCH notices; EONIA defined as €STR + 8.5bp). No card states this date; no change.
- USD LIBOR 1M/3M/6M/12M cessation 30 June 2023: standard fact, used as stated.
- US eSLR final rule: adopted 25 November 2025, published 1 December 2025, effective 1 April 2026, early adoption from 1 January 2026 (Federal Register; OCC bulletin 2025-41). Card 40 now states this.

## Unverified items (remaining)

1. ISDA fallback spreads for 1M, 6M and 12M USD LIBOR: not confirmed. Not on any card.
2. Ho-Lee convexity textbook form 1/2 sigma^2 T1 T2 (Hull). My first-order derivation gives sigma^2 T1 (T2 - T1/2), which differs by 1/2 sigma^2 T1 tau (0.37bp at 3y). I could not reproduce the textbook form. Confirm the exact statement in the Hull edition you cite before quoting either. Cards 15, 23 and 25 now show both.
3. HW convexity: first-order analytic formula and Monte Carlo agree to about 1%. The closed form was not checked against Hull's printed HW formula.
4. CMS lag direction (card 14 and 10): the adjustment falls with payment lag under this derivation. The quadrature confirms the algebra. Hagan (2003) "Convexity conundrums" was not checked for the sign of the lag term directly.
5. Hagan-West monotone-convex description (card 19): stated at a high level, not checked against the paper.
6. eSLR effect on the 10y swap spread (card 40): direction and size are not verified.
7. Illustrative figures in cards 9, 46 (capital cost, IM spread, KVA hurdle) are assumptions, labelled as illustrative. Not market facts.
8. Black-normal vol mapping sigma_B ~ sigma_N / S (deep 11): leading-order approximation, not checked against a smile.
9. Lockout and lookback PV-gap formulas (base 2, 3): leading-order approximations, not checked against an ISDA definition text.
