# Verification log: 05 credit CDS

Files: `cards/05_credit_cds.json` (56 cards), `cards/05_credit_cds_deep.json` (31 cards). Total checked: 87. Changed: 16 (12 basic, 4 deep). Card count and types unchanged; both files re-validated as JSON.

## Cards changed

| Idx | File | What was wrong | Fix | Source / method |
|---|---|---|---|---|
| 10 | basic | Only NA coupon (100bp) given; EUR standard coupons omitted | Added NA 100/500 and EUR 25/100/500/1000bp | https://www.bis.org/publ/qtrpdf/r_qt1012z.htm (Big Bang / European fixed-coupon move) |
| 20 | basic | MM14 limit stated as "60m bonds, 30m loans" | 60 months for restructured bonds and loans; 30 months for all other obligations (the 2003 MMR structure, which secondary sources say the 2014 Definitions keep) | https://jollycontrarian.com/index.php/3.32_-_Credit_Derivatives_Provision ; https://corpgov.law.harvard.edu/2014/08/24/new-isda-2014-credit-derivatives-definitions/ (confirm against ISDA text) |
| 22 | basic | Governmental intervention said to apply to "Financial Reference Entity or Sovereign" | Applies to Financial Reference Entities only; sovereign analogue is restructuring with asset package delivery | https://corpgov.law.harvard.edu/2014/08/24/new-isda-2014-credit-derivatives-definitions/ ; https://www.rimonlaw.com/?p=1608 |
| 24 | basic | Succession description pre-2014 only | Added: 2014 Definitions use a Steps Plan; 75% or more of obligations makes a sole Successor (approx.) | Section 2.2(a) as summarised at https://jollycontrarian.com/index.php/Template:2014_ISDA_Credit_Derivatives_Definitions_2.2(a) |
| 25 | basic | "Narrowed Reference Obligation" term could not be found in any retrieved source | Tagged "(approx.; unverified)" | No source found |
| 26 | basic | iTraxx Crossover 75-name count conflicts across sources | Tagged "(approx.; unverified current count)" | Sources conflicted (75 vs 40-50) |
| 31 | basic | Index-intrinsic trade direction reversed: "buy index at 65, sell constituents at 58" pays 7bp, not earns it | Sell index protection at 65, buy constituent protection at 58; +7bp carry; gains as index tightens | Recomputed sign logic (seller of protection gains when spreads fall); matches deep card 5 |
| 32 | basic | Interview question "Is a wide index a buy?" contradicts the sell-index trade on the same card | "Is a wide index always a sell?" | Internal consistency |
| 38 | basic | No attribution for the FEP feature | Added Pedersen (2003), "Valuation of Portfolio Credit Default Swaptions", Lehman Brothers | Secondary sources: https://arxiv.org/pdf/1201.0111 (primary paper not retrieved) |
| 43 | basic | Recovery lock sign wrong: buyer's adjustment written as (R_lock - R_actual) and buyer described as gaining when recovery is low. With payout (1-R_lock)N, the buyer gains when realised recovery is high | Adjustment = (R_actual - R_lock)N; buyer is long recovery; counterparty expects recovery below the lock | Recomputed from payout (1-R_lock)N vs (1-R_actual)N; consistent with ECB Financial Stability Review, Dec 2006 (https://ECB.eu/pub/financial-stability/fsr/focus/2006/pdf/ecb~c2aea4ddc2.fsrbox200612_10.pdf) |
| 49 | basic | "Redenomination handled as restructuring-type event" stated without source | 2003 treatment (binding change to non-permitted currency as restructuring); 2014 adds express redenomination language and asset package delivery; tagged approx./unverified | https://www.rimonlaw.com/?p=1608 ; Cambridge Journal of Financial and Quantitative Analysis internet appendix S002210902300087X (via search; URL at static.cambridge.org) |
| 52 | basic | "Basel III removes DVA ... (check)" was vague | Basel III (BCBS July 2012 final rule on para 75) fully derecognises DVA on derivative liabilities from CET1, phase-in 2014 to full deduction 2018 (approx.) | https://www.bis.org/press/p120725b.htm |
| 8 (deep) | deep | Interview question "Is a wide index always a buying opportunity?" contradicts the sell-index trade | "...always a selling opportunity?" | Internal consistency |
| 18 (deep) | deep | FEP decomposition presented as exact | Added caveat: Pedersen (2003) makes exercise depend on accrued loss, so the closed form is a simplification | https://arxiv.org/pdf/1201.0111 (secondary) |
| 22 (deep) | deep | Mark-to-market arithmetic: roll-down -3,661 (should be -3,657) | Corrected to -3,657; total -11,990 (~-12.0k unchanged) | Recomputed: 0.00008333 x 4.39 x 10m = 3,657 |
| 23 (deep) | deep | Notional ratio "2.1x" wrong; N_I = 32.8m vs 10m is 3.3x | Changed to 3.3x (RPV01 ratio 4.3/4.5 trims it) | Recomputed: 1.6 x 150/70 x 4.3/4.5 = 3.28 |

## Verified with no change (recomputed or sourced)

- Index composition and coupons: CDX IG 125 / 100bp; CDX HY 100 / 500bp; iTraxx Main 125 / 100bp; Crossover 75 / 500bp (Crossover count flagged).
- Index roll dates 20 March and 20 September (IMM-style, S&P DJI roll notices: https://www.spglobal.com/spdji/en/documents/index-news-and-announcements/20260902-cdx-and-iTraxx-tranche-september-2026-roll-dates.pdf).
- 2014 credit events list, Determinations Committees, Failure to Pay, Restructuring optional.
- XR14/CR14/MR14 (30 months) rows.
- Par-spread, upfront, RPV01 derivation (deep 15-17): 303.0 / 301.1 / 300.0bp; RPV01 4.106 vs 4.121 (recomputed in python).
- Credit triangle, 5y PD 22%, hazard 5%, recovery sensitivity 1.667% vs 1.639% (recomputed).
- Tranche ELs at rho=0.3: 54.1 / 19.6 / 5.8 / 0.15% sum to 3.00% of index (recomputed by quadrature). Equity EL 73.8 / 54.1 / 39.9% and mezz 17.2 / 19.6 / 17.8% at rho 0.1 / 0.3 / 0.5 (recomputed). Mezz peak near rho 0.3; mezz EL to 5% as rho to 1 (recomputed).
- FEP 0.195% (1m) and 0.477% (1y), P(no default) 0.59 / 0.002 (recomputed).
- Roll PV 5bp x 4.4 x 10m = $22k; index factor 124/125 and 0.48% loss; beta-adjusted notional formula; CS01 figures ($5,880; $4,800; $12,000; $72k); 5s10s JTD and carry-neutral figures (-1.2m JTD, -$30k carry, +$34k carry, -2.55m JTD); JTD -$77k; negative basis case (-$440k with 5pt mismatch).
- Convention checks: ASW approximation, upfront sign, JTD definition, DVA formula sign, copula conditional PD.

## Unverified items (kept, tagged or flagged)

1. "Narrowed Reference Obligation" (basic 25): term not found in any retrieved source; tagged.
2. iTraxx Crossover name count, 75 (basic 26): sources conflict; tagged.
3. 2014 MM14 caps (basic 20): from secondary summaries; confirm against ISDA 2014 Definitions text.
4. 2014 redenomination operative wording (basic 49): tagged.
5. Basel III DVA phase-in and final text (basic 52): from BIS press release and secondary sources; current Basel Framework CAP30 wording not checked.
6. Pedersen (2003) primary paper not retrieved; attribution is from secondary sources (basic 38, deep 18).
7. Recovery lock payoff: sign derived from payout definition; ISDA template terms not checked (basic 43).
8. EUR coupon "25, 100, 500, 1000bp" from BIS Quarterly Review secondary summary; not checked against EU dealer agreement text.
9. Basic 19 sovereign credit-event list (Repudiation/Moratorium, Restructuring) not expanded to Failure to Pay / acceleration; not changed.
10. Basic 37 and deep 14 use an illustrative 25%/40%/60% base-correlation curve; not a market quote.
