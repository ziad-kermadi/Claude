# Verification log: 10_xva_funding__v3.json and 07_converts_loans__v3.json

Cards: 25 (XVA) and 20 (converts/loans). Card count and types unchanged. Both files re-validated (JSON load, one lvl_* tag per card, no raw < or & in HTML, MathJax delimiters balanced).

## cards/10_xva_funding__v3.json

| Card idx | Issue | Fix | Source or basis |
|---|---|---|---|
| 5 | Explain: spread line 6.30 should be 5 x 1.263 = 6.32. Residual 0.22 did not match first-order Greeks at start-of-day (residual = 11.787 - 11.578 = 0.20). | Spread 6.32, residual 0.20, sum 11.80 stated with the basis. | recomputed |
| 6 | Sign and direction error. With V = sigma Z and default when X < k (X positively correlated with Z), E[V given default] is negative (right-way risk), so the stated multiplier rho*phi(k)/p was a wrong-way formula on the wrong tail. | Default redefined as X > k with Phi(-k) = p, k = Phi^-1(1-p). Table values (0.666/1.333/1.999 etc.) re-checked and unchanged. Table labels k shown positive. Inverse-Mills text corrected to the upper tail. | recomputed |
| 7 | "Monte Carlo (4m paths)" claim not reproducible; I cannot attest to a run. Interviewer probe asserted a super-linear rise in b that the numbers do not show (excess ratio roughly doubles as b doubles). | Ratios 1.67 (b=0.5) and 2.31 (b=1) kept and reproduced by quadrature over Z against the independent case with constant hazard lambda0. MC wording replaced by quadrature. Probe changed to the b to 0 limit (ratio tends to 1). | recomputed (quadrature) |
| 8 | Used the CVA value ratio (1.67) as the CS01 ratio. Spread CS01 ratio recomputed = 1.59 (d/dlambda0 of the lognormal-hazard CVA over the independent CS01). Notional recomputed: 2.00e3/4.5e-4 = 4.4m; independent 2.8m; about 59% larger. | Front and steps updated. | recomputed |
| 12 | "Monte Carlo with 2m paths gives 0.3950m" is a run claim I could not verify. Closed form 0.3956 is correct. | Replaced with a checkable identity at H=0 (sigma phi(0) = 0.798m). | recomputed |
| 13 | Source caveat said rho=0.5 unconfirmed. Structure and rho confirmed in vendor documentation of the BA-CVA rules. K = 13.0 for S=(10,5,2) recomputed. | Caveat replaced with the confirmed rho and a scope note (DS and beta are outside the card). | https://docs.activeviam.com/products/solutions/cvarc/4.0/online-help/regulatory-calcs/approach-ba.html (search result, ActiveViam BA-CVA docs; BCBS MAR50 cross-check via search only) |
| 18 | Mechanism overstated: eligible external CVA hedges are recognised without a matching trade. The matching-external-trade requirement applies to internal CVA-desk/trading-desk hedges for curvature, DRC and residual-risk-add-on instruments. "Basic Approach" naming and approval requirement (SA-CVA needs approval; otherwise BA-CVA) confirmed. | Front and mechanism rewritten. Approval line corrected. | https://rulebook.sama.gov.sa/en/node/4462 (SAMA copy of MAR50, search result); https://www.sif.admin.ch/dam/sif/de/dokumente/basel-3/MAR50.pdf.download.pdf/MAR50.pdf (search result) |
| 19 | ISDA SIMM 10-day margin period at 99% confidence confirmed. Verify clause removed. | Removed "verify" parenthetical. | https://www.isda.org/2025/11/11/isda-simm-the-trusted-standard-for-initial-margin-calculations/ (search result) |
| 21 | Cloze back said "verify before quoting". rho=50% now confirmed. | Replaced with the confirmed value. | as card 13 |

Checked and correct (no change): 0 (SIMM IM 10, cross term), 1 (exact 9.592, Euler -1.2, gap), 2 (MVA 0.0152m), 3 (sign convention), 4 (CVA 0.1593m, theta -0.000111m = +GBP 111/day), 9-11 (grid, forward measure identity, CRN), 14 (vega = phi(d), 0.3521), 15 (CS01 7.58 per unit lambda, 1.26k/bp, naive 1.33k/bp), 16 (EE 0.3989, sd 0.5838, 2.1m paths), 17 (KVA concept, no figures), 20, 22-24 (cloze math checked).

## cards/07_converts_loans__v3.json

| Card idx | Issue | Fix | Source or basis |
|---|---|---|---|
| 1 | Raw "<0" inside MathJax, which HTML can parse as a tag. | Escaped as &lt;0. | HTML rule |
| 3 | Non-accruing par used a fee of 0.15% of performing par; card 0 used 0.60 on the full 400 pool. Inconsistent. Recomputed: 0.075P - 0.60 = 21.50, P = 294.7, non-accruing 105.3 = 26.3%. | Fee basis made consistent with card 0; figures and sanity-line percentage updated. | recomputed |
| 7 | Raw "<1" inside MathJax. | Escaped as &lt;1. | HTML rule |
| 6 | Stray ",." typo. | Fixed. | — |
| 13 | Caveat stated 7.5% and market value as the typical rule. Sources: 7.5% typical, some deals 5%; excess CCC valued at market or at agency recovery if lower, varies by deal. | Caveat rewritten to match. | https://casact.org/sites/default/files/presentation/affiliates_cae_0610_jodin.pdf ; https://spglobal.com/ratings/en/research/articles/200709-european-clos-the-true-impact-of-ccc-assets-on-overcollateralization-ratios-11563599 (search results) |
| 14 | Clean-up threshold "typically 10% (approx.)" not supported for broadly syndicated CLOs (search found only auto-ABS and CRE CLO 10% tests). | Threshold stated as the example's assumption, indenture sets the real level. Case numbers recomputed and unchanged: residual 5.00, break-even 91.0. | recomputed; no source for 10% |
| 18 | Cloze gave a 10% clean-up threshold as typical. Not supported (see 14). | Threshold made a deal-specific cloze. Structure kept. | as card 14 |

Checked and correct (no change): 0 (IC 164%, failure at 21.50, cushion 7.9), 1 (IC(S) derivative and limit 125%, values 273/167/150%), 2 (IC 106.0%, redemption 37.3, residual 1.08), 4-6 (BDR 16.7%; excess spread 8.5 = 1.7% of pool; D* 28%; mezz 8x sensitivity), 7-9 (delta 8.93, gamma 0.0885, peak near S=40 at 0.175/bond, dividend carry -143), 10-11 (floorlet formula; 3y floor 0.67 per 100, 24bp; F=2% 0.18; F=4% 0.01; annuity 2.81), 12-13 (OC 155.6% to 156.3%; CCC OC 124.1%, fails by 3), 15-17 (cloze math), 19 (vega 6.80 per vol point, 5.96 at S=60, 6.42 at S=100).

## Still doubtful / not verified

- BA-CVA discount scalar DS = 0.65 and the full-BA-CVA beta: not verified (bis.org unreachable from this session); not used in any card.
- MAR50.37-39 eligibility detail for SA-CVA: relied on search summaries only.
- Clean-up call threshold: no source for a standard broadly syndicated CLO figure; cards now state it as deal-specific.
- Cards 9-11 and 17 (expo-sim, KVA) are conceptual; no external source checked.
- Card 14 uses "par plus accrued interest" for the call price; accrued interest is not modelled in the numbers.
