# Verification log: cards/14_found_fi.json

Cards checked: 50 (39 basic, 11 cloze). Cards changed: 7. Card count, types and lvl_* tags unchanged (40 lvl_foundation, 10 lvl_vp_core).

| Card index | Issue | Fix | Source or method |
|---|---|---|---|
| 2 | Context said "£/$100 face" for a US corporate bond, and the reconciliation line said "£10,000 face" | Changed to $100 face and $10,000 face | Source: 30/360 for US corporates (Duke WWWFinance day-count notes; FIU lecture). Recomputed accrual 1.50 (30/360) vs 1.5123 (ACT/365F) |
| 8 | "0.37 points on a par bond" is the principal-only DF gap (0.003740). The par bond priced continuously at the same 5% is 99.51 vs 100, a 0.49 gap | Rewrote to state both figures | Recomputed (python) |
| 9 | "the same figure for 10m of any currency" is false: GBP is ACT/365F, so tau differs | Replaced with ACT/360 qualifier and the ACT/365F tau = 90/365 note | Reasoning; recomputed 12,360.94 |
| 17 | Newton step with rounded inputs gives 5.454%, not 5.455%. The 5.455% and 0.75bp error come from unrounded P=95.7349 and D=4.3414 | Show unrounded inputs in the front and step; P'(y) = -415.6 now reproducible | Recomputed (python): P(6%)=95.7349, D_mod=4.3414, step 5.4550%, exact 5.4625% |
| 24 | DF(2) shown as 0.920; sum 1.87936 needs 0.920127 | Displayed 0.920127 | Recomputed: 1/1.0425^2 = 0.920127 |
| 28 | "A bullet at the same DV01 costs more in carry or in the market" is unsupported | Replaced with convexity vs carry/roll trade-off statement | Reasoning; figures 25.0/5.41/80.75, barbell 36.5, P&L diff 0.057 recomputed |
| 28 | Front contained unescaped "&" | Escaped as &amp; | HTML rule |
| 46 (cloze) | Back did not note that FRA rates fix two business days before the start | Added fixing-lag note to back | Market convention (ISDA/market practice) |

Recomputed with no change needed (python): cards 0, 1, 3, 4, 5, 6, 7, 10, 11, 12, 13, 14 (YTM 5.4625%, annual 5.537%), 15 (3.854%), 16 (dirty 97.0512, clean 95.8512), 18, 19 (DF(1) 0.963038, z 3.802%, cont 3.766%), 21 (par 4.935%), 22, 23, 24 (value -469,840, DV01 18,794), 25, 26 (4.452, 44,518), 27, 29 (104.45, 103.63, return 4.00%), 30 (exact 99.064), 31 (exact 102.053), 32 (98.9889), 33 (BEY 4.0970%, MMY 4.0409%), 34 (4.14bp), 35/45 ($25/bp), 36 (5.0024%), 37 (5.00%), 38 (F 4.124%, dF/dDF2 -4.17), 39-44, 47-49.

Sources used:
- SR3 contract terms (compounded SOFR, price = 100 minus rate, $25/bp): https://www.cmegroup.com/education/articles-and-reports/understanding-sofr-futures
- T-bill bond-equivalent yield 365d/(360 - d t): https://support.microsoft.com/office/tbilleq-function-2ab72d90-9b4d-4efe-9fc2-0f81f2c19c8c
- Treasury notes/bonds ACT/ACT, corporates and agencies 30/360, T-bills ACT/360: https://people.duke.edu/~charvey/Classes/ba350_1997/pricing/daycount.htm and https://app.certfuel.com/series7/learn/debt-securities/us-government-and-agency-securities/accrued-interest

Unverified items (kept as written, no precise external figure claimed):
- Card 0 and 2: 30/360 formula is the simple bond-basis form (day-of-month 31 set to 30). Full US and EU 30/360 variants differ at end-of-month edge cases.
- Card 35: convexity adjustment statement is qualitative; no size given.
- Card 11: bond DV01 comparison uses D_mod approx 0.5 for a 6-month bond (approximate).
- Card 31: "long bonds are worth owning in volatile rates markets" is a view, not a fact.
- Card 3: Treasury ACT/ACT accrual cited as "similar principle" to ICMA; the sources confirm actual/actual but not the exact roll rules.
