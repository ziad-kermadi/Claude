# Verification log: 06 credit models, CLN

Scope: cards/06_credit_models_cln.json (59 cards) and cards/06_credit_models_cln_deep.json (30 cards). 89 cards checked. Numbers recomputed with python3 (scipy). Two edits made; no card removed or added.

## Changed cards

| Index | File | What was wrong | Fix | Source or method |
|---|---|---|---|---|
| 46 | 06_credit_models_cln.json | BA-CVA card gave no value for the supervisory correlation rho | Added rho = 50% (approx.; unverified against MAR50 text) | Secondary sources only: ActiveViam BA-CVA guide (https://docs.activeviam.com/products/solutions/cvarc/5.0/online-help/regulatory-calcs/approach-ba.html) and a MAR50 mirror (https://www.sif.admin.ch/dam/sif/de/dokumente/basel-3/MAR50.pdf.download.pdf/MAR50.pdf). BIS chapter not reachable from this environment. |
| 18 | 06_credit_models_cln_deep.json | RPV01 for 5y, zero rates, 2% hazard printed as 4.754 | 4.758 (ratio A/RPV01 = 1.051 unchanged) | Recomputed: (1 - e^{-0.1})/0.02 = 4.7581 |

## Checked and confirmed, no change

- Merton (main 0-2; deep 12, 24): d1 0.947, d2 0.388, E 37.99, B 62.01, PD 34.9%, spread 209.6bp at V=100. At V=90: spread 274bp, PD 42.1%, gearing 2.33, sigma_E 58.3%. Confirmed.
- KMV, CIR++, Feller, bootstrap formulas, credit triangle derivation (deep 14: 2.492% vs 2.500%), first-pillar closed form artanh (deep 15, 20).
- CIR closed form (deep 13): gamma 0.5196, B 1.8130, A 0.9101, P 0.87766. Riccati signs checked. Confirmed.
- Vasicek and Basel IRB (main 28-30; deep 16, 23): 99.9% quantile 9.03%, UL 8.03%, b = 0.1375, MA = 1.260, K = 4.55%. Correlation weight w = 0.393 at PD 1%, R = 19.3%, quantile 14.0%. Basel formula confirmed by Fed 2006 memo and secondary sources; BCBS primary text not retrieved.
- Plackett derivatives and FTD (deep 9, 10, 19, 22): P(0.5) = 16.8%, dP/drho at 0, 0.5, 0.9, 0.99 match; P at 0.99 = 0.1099 and 0.999 = 0.1031; hedge table (0.95/0.90, 0.88/0.70, 1/0) matches; FTD 5y spreads 253bp, 220bp, 126bp match.
- Bootstrap chain (deep 0-3): lambda(1,3] = -0.289%, Lambda(3) = 4.42%, threshold S3 = 101.7bp. Confirmed.
- Case study (deep 20): lambda 1.333%, 2.090%, 2.913% at r = 0; Q(1), Q(3), Q(5) and 5y PD 10.7% match. Discount effect at 3%: about 1bp and 5bp (computed 1.2bp and 5.2bp).
- CVA case (deep 25): CVA 0.1153m, flat approximation 0.1201m (4.1% higher). Matches.
- Funded CLN (deep 21): lambda_R 3.333%, lambda_I 1.333%, s = 280bp, A = 2.680, PV split 5.36 / 2.14. Matches.
- CLN par spread derivation (main 50) and collateral basis ratio (deep 18). Confirmed.
- Principal-protected CLN (main 51): 91.39 and 8.61; spread income 17bp; loss 5.2. Confirmed.
- Duffie-Singleton RMV result (main 6, 7): constant intensity gives spread lambda*L exactly. Consistent with the RMV derivation.
- ATM swap EE peak at t = T/3 (main 45). Derivative check confirmed; card already says "about one-third".
- Clayton lower-tail 2^{-1/theta}, t-copula tail dependence formula (main 31, 32). Confirmed.
- Mental-math cards (main 12, 18, 42, 56, 58) and CDS basis / upfront / RPV01 conventions (main 20, 54, 55). Confirmed.

## Unverified or approximate items

1. BA-CVA rho = 50%: consistent across secondary sources but MAR50.20 primary text not retrieved. Marked "approx.; unverified" in card 46.
2. BA-CVA index-hedge treatment (80% correlation was in the query): no source found. Card does not state it, so nothing to fix. Left as unverified.
3. SA-CVA supervisory approval requirement (main 46): confirmed by MAR50 summary (BA-CVA applies unless the supervisor approves SA-CVA).
4. Jarrow-Turnbull (1995) as the source of recovery of treasury: supported by secondary sources only; original paper not retrieved.
5. Duffie-Singleton publication year: sources cite both 1997 and 1999. Card says 1999 (RFS). Not changed; flagged here.
6. Basel IRB formulas (main 29, 30): confirmed through Fed 2006 memo and secondary sources. BCBS primary text not retrieved. Basel's 1.06 scalar and any Basel III final changes are not mentioned in the cards and not checked.
7. Deep 21 PV split (5.36 / 2.14) is a proportional allocation of the spread leg, not a separate integral. The "numerical integration returns par" statement was not separately run here.
8. Main 18 and deep 0 use approximate and exact conventions respectively; the 3y and 5y thresholds (about 100bp and 101.7bp) are consistent but the main card uses the flat approximation.
9. Main 48 implicitly assumes 40% recovery for the seller default loss (0.6m); the card does not say so explicitly.
