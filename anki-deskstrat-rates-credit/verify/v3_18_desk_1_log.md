# Verification log: cards/18_desk_1.json and cards/18_desk_6.json

Cards checked: 30 + 30 = 60. Cards changed: 11 (desk_1: 4; desk_6: 8, with card 9 and card 25 sharing edits). Card count and types unchanged. Both files validated as JSON; every card has exactly one lvl_* tag.

## Changes

| File | Idx | Issue | Fix | Source / basis |
|---|---|---|---|---|
| 18_desk_1 | 17 | Follow-up premise wrong: the book does not lose in GBP overall (total is positive); only the translation line is negative. | Reworded to ask why the translation line costs a long-USD book money despite positive local P&L. | Recomputed: 952,381 − 63,492 = 888,889 |
| 18_desk_1 | 20 | "Receiver pays" (a receiver receives); "compounded" but computed as simple interest; "overpayment" wrong term for an overbooked receipt. | Receives a 3-month fixed coupon; title "SONIA-style 3-month coupon"; "overstatement of the coupon". | Recomputed: 2,493,151 (ACT/365F) vs 2,527,778 (ACT/360), difference 34,627 = 1.39%. ACT/365F for SONIA is the standard convention (not web-checked this run). |
| 18_desk_1 | 24 | 10y DV01 of about £55k/bp on £55m is too high for a 10y swap at about 4%. | Changed to about £45k/bp (annuity about 8). | Recomputed: annuity 8.11 at 4.0%, 55m × 8.11 × 1e-4 = £44.6k |
| 18_desk_6 | 7 | Basis direction wrong. Implied repo 3.09% below GC 4.00% means the futures are cheap, not rich. | "Cheap relative to the CTD"; fair F about 118.52 at 4.00% repo; reverse trade is the one that earns. | Recomputed: fair F = 100.30 × (1 + 0.04 × 40/365) / 0.85 = 118.52 vs market 118.40 |
| 18_desk_6 | 9 | Front labelled a "receiver" swap but the payoff V = NA(S − K) is a payer. Duplicate "Where it breaks" label. | "Payer forward-starting swap"; merged the duplicate label. | Logic check |
| 18_desk_6 | 11 | Net statement wrong: £10.25m − £4.10m = £6.15m is not the benefit over no lock. The £4.10m spread cost is incurred with or without the lock. | The lock adds £10.25m against no lock; spread cost applies either way. | Recomputed: 410,000 × 25 = 10.25m; 500m × 0.10% × 8.2 = 4.10m |
| 18_desk_6 | 17 | Bank Rate stated as 4.00%. Current Bank Rate is 3.75% (held Sept 2026); 4.00% is the hike outcome. | Bank Rate 3.75%; the 25bp hike still gives 4.00%. | https://www.mtsinsights.com/summaries/10990/ (Sept 2026 MPC: hold at 3.75%, 6-3 vote) |
| 18_desk_6 | 22 | Residual-risk logic wrong: once the deal is pulled and the payer swap is cancelled, the receive-fixed hedge is a naked rates position, not a swap-spread position. DV01 about £65k is high for a 7y swap at about 4.2%. | Rewritten: naked receiver of about £60k/bp; 5bp rise costs about £300k; follow-up now asks why this is rates risk. Tag swap_spread renamed hedge_residual. | Recomputed: 7y annuity 5.96 at 4.2%, 100m × 5.96 × 1e-4 = £59.6k |
| 18_desk_6 | 24 | Margin direction ambiguous ("sell-off"): a receiver posts margin when yields fall. | "A 30bp fall in yields ... costs the scheme about £7.7m of variation margin." | Recomputed: 255k × 30 = 7.65m |
| 18_desk_6 | 25 | Duplicate "Where it breaks" label. | Second label changed to "Also, the derivation treats ...". | Format only |
| 18_desk_6 | 26 | Half-spread cost 0.75bp × 111.1m × 14 = £116.7k, shown as £116k. | £117k. | Recomputed: 116,667 |

## Checked and unchanged (recomputed or verified)

- 18_desk_1: 0, 1, 2 (explained 236k, actual 308k, residual 72k; interpolation −4.8bp), 3 (−90k vega line), 4, 5 (−84k), 6 (bucket −63.6k vs parallel −67.2k), 7 (40k/70k/110k), 8 (overnight +45k; parallel 82k), 9, 10, 11, 12 (2,015k, gap −85k), 13, 14 (edge 23k, net 20.5k), 15 (23k), 16 (45k vs 82k), 18 (swaption: full reval 1,537,443, change 45,399, explained 44,987, residual 412; Greeks recomputed), 19 (five-day explain, totals −60,500 / −60,800, residual −300, gamma 8,500 vs 1,000), 21, 22, 23, 25, 26, 27, 28, 29.
- 18_desk_6: 0 (160,704), 1 (CTD DV01 76.23, futures DV01 89.68, 1,792 contracts, residual −£3), 2 (+3,389 net, 37 contracts), 3, 4 (10.25m, 1.25m/yr), 5 (4.1m), 6 (LTD 29 Dec 2026, last notice 30 Dec 2026; source https://www.ice.com/api/productguide/spec/37650336/pdf), 8 (roll 716,800), 10 (6,779 net; residual 3,389), 12 (cloze, notional £100k, 4%), 13 (cloze, 89.68), 14 (111m, f = 0.56%), 15 (18.0m, 18.1m, net 0.10m), 16 (155k), 18, 19 (70k residual, 3.7bp), 20 (SSA swapped issuance, cash flows), 21 (42bp), 23 (3bp × 170k = 0.5m; 0.2 duration on £2bn = 40k), 24 (255k DV01, 17 modified duration), 27 (cloze: MPC 12:00 London per BoE practice, source https://mpamag.com/uk/news/general/mpc-base-rate-announcement/353884; FOMC 14:00 ET recalled, not web-checked), 28 (IMM 16 Dec 2026, recomputed), 29.

## Unverified or approximate items (kept, not marked)

- 18_desk_1 card 20: ACT/365F for SONIA is the standard convention, not web-checked in this run.
- 18_desk_1 card 17: the \& in the MathJax \text{local P\&L} is intentional (MathJax form). Not an HTML issue.
- 18_desk_6 cards 0, 3, 4, 5, 11: modified duration "approx. 8.20" at 4.10%; recomputed 10y annuity is 8.07 (about 1.6% lower). Within "approx." tolerance; not changed.
- 18_desk_6 card 9: the claim that the annuity-convexity error is "typically a small fraction of a percent" is not quantified. Kept as a qualitative statement.
- 18_desk_6 card 16: "the index preview is public" is a general practice statement, not checked against a specific provider.
- 18_desk_6 card 17: Bank Rate of 3.75% is from one secondary summary, not the BoE's own page.
- 18_desk_6 card 27: FOMC 14:00 Eastern is recalled, not web-checked.
