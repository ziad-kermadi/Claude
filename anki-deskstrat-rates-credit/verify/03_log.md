# Verify log: 03_rates_options (base and deep)

Checked: 59 base cards (03_rates_options.json) and 30 deep cards (03_rates_options_deep.json), 89 total. Card counts, types and JSON validity unchanged.

## Cards changed

| Index | File | What was wrong | Fix | Source or basis |
|---|---|---|---|---|
| 26 | 03_rates_options.json | Free-boundary SABR attributed to Doust (2012). Doust's paper is "No-arbitrage SABR" (absorbing boundary at zero, density as a sum of positive components, prices by numerical integration). Free-boundary SABR is Antonov, Konikov and Spector (2015). Text also overstated closed-form status. | Re-attributed each model. Free-boundary given to Antonov-Konikov-Spector; Doust described as no-arbitrage SABR. Stated that arbitrage-freeness of free-boundary SABR is not guaranteed in general. | https://www.risk.net/2423287 ; https://www.risk.net/journal-computational-finance/2164194/no-arbitrage-sabr (secondary summaries; full texts not retrieved) |
| 51 | 03_rates_options.json | Static replication lower integration limit was 0. Inconsistent with negative rates, and with deep card 16, which correctly uses -infinity. | Lower limit changed to -infinity in both integrals; one sentence added on negative rates. | Recomputed: the h(S)=S^2 check of the decomposition, as in deep card 16. |
| 47 | 03_rates_options.json | "2 or 3 factors capture about 90% or more" of variance: no source. | Tagged "(approx.; unverified)". | Not verified. |
| 2 (deep) | 03_rates_options_deep.json | Same Doust/free-boundary mis-attribution. "Closed-form prices remain" overstated. "Check exact spec in Doust" left unresolved. | Free-boundary attributed to Antonov-Konikov-Spector (exact at zero correlation, integral approximation otherwise). No-arbitrage SABR (Doust 2012) listed as a third route. | As for base 26. |
| 3 (deep) | 03_rates_options_deep.json | HKLW 2014 description claimed a "martingale constraint in the boundary treatment" and that non-negativity is a property of discretisation. Neither is supported by sources found. | Rewritten as density expansion plus Fokker-Planck solved numerically with absorbing boundary at zero. Tagged unverified. Non-negativity described as a design target. | Secondary summary only (search results); original 2014 paper not retrieved. |
| 22 (deep) | 03_rates_options_deep.json | "Expected to sit much nearer the lower bound" is an unsupported claim. | Tagged "(approx.; unverified)". | Not verified. |

## Checked and correct (no change)

- Base 0-25, 27-50, 52-58 and deep 0-1, 4-21, 23-29: formulas, signs, units and worked numbers checked by re-derivation or python.
- Hagan 2002 normal-vol SABR beta=0 T-correction (2-3rho^2)nu^2 T/24: confirmed (ATM normal vol = alpha[1 + (2-3rho^2)nu^2 T/24]; MathWorks normal-vol SABR example). Leading-order formula zeta/x(zeta) derived and checked.
- Deep 0 recomputed: ATM 102.7bp (card 103), K=-0.75% vol 218.8bp (card 219), butterfly -3.18e-7 (card -3.2e-7), density -0.051 (card -0.05). ATM butterfly positive.
- HW swap-rate loadings (flat 3%, 1y x 5y, annual payments at 2..6): |dS/dr| = 0.9303 at a=0.03 and 0.7381 at a=0.10. S = 3.0455%, A = 4.4386. Normal-vol equivalents for 100bp: 1.075% and 1.355% (cards say 1.07/1.35 in deep 7 and base 40; 1.075 rounds to 1.07 and 1.355 to 1.35). Recomputed, consistent.
- Deep 21 caplet strip recomputed: caplet 1 = 0.576%, 60bp caplet paying at 2y = 0.453%, 2y cap = 1.029%, 3y cap at 58bp = 1.587%, residual caplet 0.558%, implied sigma2 = 56.6bp (recomputed 56.59). Correct.
- Deep 22 Bermudan bounds recomputed: European values 122.5, 156.8, 141.7 (141.75), 91.3bp; sum 512.4; max 156.8. Bounds correct.
- Deep 19 (1y x 10y ATM): annuity 8.530, premium 3.40%, straddle 6.81%, vega 0.34bp per bp, delta 4.265. Correct.
- Deep 20 (6m x 5y delta-hedged payer): Gamma 370.8, expected P&L 38bp (about $382k), premium about $908k, vega identity 1.30 = 1.30. Correct.
- Base 55 range accrual: in-range probability 2N(1.25)-1 = 78.9%. Correct.
- Deep 23 vega bucketing: 340.3, 182.7, 258.4 $/bp per mm; hedge sizes -165.6mm and -14.6mm. Bucket checks net to zero. Correct.
- Deep 24 SABR K=2.00/2.50/ATM: 98.1, 93.6, 90.0bp leading order; 99.2, 94.7, 91.0bp with correction. Correct.
- Deep 14/29 Hull-White B(0,5): 4.643 at a=0.03, 3.935 at a=0.10. Correct.
- Deep 13 HJM drift and deep 10 Bachelier derivation: re-derived, correct.
- LMM terminal drift (base 45) and spot-LIBOR drift (deep 15): sign and sum ranges re-derived by Girsanov; consistent with standard BGM/Jamshidian results. Derivation check only, not checked against a text.

## Unverified items (kept, tagged or not web-checked)

1. HKLW 2014 arbitrage-free SABR: exact expansion, boundary treatment and the non-negativity mechanism (deep 3). Original not retrieved.
2. Doust 2012 "No-arbitrage SABR" and Antonov-Konikov-Spector 2015 free-boundary SABR: from secondary summaries only (Risk.net and Numerix pages), not full texts.
3. ZABR (Andreasen and Huge; base 26): attribution and dynamics not web-checked in this pass.
4. Base 47: "2 or 3 factors capture about 90% or more" of rate variance (tagged).
5. Deep 22: expectation that the Bermudan sits near its lower bound (tagged).
6. Deep 3: "desks usually fit a fast approximation to the PDE surface" (tagged).
7. Base 12, 36, 53-54 and base 46 (Rebonato frozen weights): general market practice statements, not individually web-checked.
8. Deep 16 step 5 (CMS density-ratio form): sketch only; the exact h(S) for a payment lag is not written out.
