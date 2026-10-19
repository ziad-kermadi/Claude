# Verify log 01: govies (cards/01_govies.json, cards/01_govies_deep.json)

Checked: 47 main cards + 30 deep cards = 77. Changed: 30 (main 21 edits across 17 cards; deep 10 edits across 9 cards; several cards carry more than one edit). Card counts and types unchanged; JSON validated.

## Cards changed

| Idx | File | What was wrong | Fix | Source |
|---|---|---|---|---|
| 4 | main | RPI-CPIH date stated only as "2030" | Feb 2030, Nov 2020 decision, no ILG compensation | Search: LCP, Linklaters, Gateley (2020 commentary) |
| 5 | main | "takes effect from 2030" | "February 2030" | same |
| 8 | main | "Redo at 4% yield" with a 5% coupon: D_mod "about 8.2" and DV01 "about £8,200" are the par-4% values, not this bond | Recomputed: price 108.18, D_mod 7.92, DV01 per £10m about £8,570 | recomputed (python) |
| 9 | main | D_mod "8", C "of order 70", duration term -8%, convexity +0.35% | D_mod 7.8, C 74 (73.6), term -7.8%, convexity +0.37% | recomputed |
| 13 | main | Carry "12.5bp per 100 face" (unit mix: yield bp vs price) | 0.125 price points per 100 face (0.125% of face) | recomputed |
| 14 | main | Roll-down price gain "24bp per 100 face" | 0.24 price points per 100 face | recomputed |
| 16 | main | Roll "8.2 x 3bp = 0.245" (unit mix); total 0.370 | 0.246 points; total 0.371; cushion 4.5bp unchanged | recomputed |
| 26 | main | March 2020 narrative: "trade unwound at a loss before converging", "leverage ratio constraints tighten the trade" presented as fact | Basis spike (>70bp vs ~5bp typical), about $62bn short-futures unwind 3 to 17 Mar; SLR claim labelled advocacy view | Brookings-based summary (via search); ICI commentary; OFR/Dallas Fed disagree on direction |
| 27 | main | Long Gilt range "about 8¾ to 13" (approx.) | 8y9m to 13y, 4% notional, GBP 100k (verified). Bund and UST ranges and 6% coupons marked unverified | ICE Long Gilt contract spec (ice.com/products/37650336) |
| 30 | main | UK leverage ratio "around 3.25% (approx.) for large banks" | 3.25% minimum of exposure for in-scope firms plus buffers (verified); SA-CCR marked unverified | PRA Rulebook leverage ratio pages; PS21/21 |
| 31 | main | "5bp adverse basis move" (yield bp vs price points) | 0.05 price points (5bp of price) on GBP 2bn about GBP 1.0m | recomputed |
| 32 | main | Auction tail definition stated as fact; uniform vs multiple price not addressed | Marked unverified (DMO tail definition and auction format not found) | search did not find DMO source |
| 42 | main | BoE cap "approx. GBP 65bn" | Dates 28 Sep to 14 Oct 2022 confirmed; Treasury authority up to GBP 100bn; actual purchases about GBP 19.3bn; GBP 65bn removed as unconfirmed | BoE/Treasury material via search (BoE statement on ending gilt operations, 17 Oct 2022) |
| 14 (deep idx 14) | deep | "All remaining exposure sits in curvature" contradicts a 2% parallel DV01 residual | Residual described as parallel exposure; PC3 0.054 marked unverified | recomputed (ratio 0.0458/0.0449) |
| 15 (deep) | deep | Simple forward used DF ratio 1.010259 | 1.010303 (F still 4.12%) | recomputed |
| 17 (deep) | deep | Convexity term at 4.46bp "about 1e-4 points" | 8e-4 points; break-even 4.47bp confirmed by quadratic | recomputed (C = 78.9, D = 8.18) |
| 18 (deep) | deep | At 4% repo "edge is 0.33%" | Edge is -0.17% (3.83% - 4.00%); 0.33% is the edge at 3.50% | recomputed |
| 20 (deep) | deep | a10 = 0.0300 | 0.0299 (N10 still 0.37) | recomputed |
| 23 (deep) | deep | Third-order asymmetry "about 0.1% of price" | About 0.2% (exact -15.45%, +19.69%) | recomputed |
| 25 (deep) | deep | "5bp" used as price basis move | 0.05 price points per 100 face | recomputed |
| 26 (deep) | deep | SONIA "observation shift of five days" | Five-day lookback; BoE Working Group recommends lookback without observation shift; payment lag 4 to 5 days, sources differ | BoE RFRWG statement; secondary sources (Cadwalader, Lloyds factsheet) |

## Verified, no change
- Main 0, 1, 2, 3, 6, 7, 10 to 12, 17 to 19, 20 to 25, 28, 29, 33 to 41, 43 to 46: formulas and numbers recomputed or consistent. Ex-dividend window is 7 business days (DMO; confirmed by search).
- Deep 0 to 13, 16, 19, 21, 22, 24, 27 to 29: recomputed; the figures in 4, 22 (92.3m sale, NAV 53.9m, 4.6bp feedback), 0 to 2 (CTD switch at 117.35, fly 110.047/110.198), 19 (708 contracts) and 16 (D_mac 2.886) match.

## Unverified (kept, marked in card text or noted here)
- DMO auction format (uniform vs multiple price) and tail definition (main 32).
- Bund (8.5 to 10.5y, 6%) and UST 10y (6.5 to 10y, 6%) deliverable ranges and notional coupons (main 27, 28): not checked against EUREX/CME specs.
- SA-CCR use for UK leverage exposure (main 30).
- March 2020 SLR causality: contested, kept as advocacy view (main 26).
- BoE GBP 65bn initial cap (main 42): not found in searched sources.
- Deep 12: par 10y at a dirty price of 100.5 is internally consistent but not a true par price on a coupon date; left as is.
- Deep 14 PC loadings are illustrative and not normalised; PC3 residual not recomputed.
- Deep 28: PC1 share "roughly 90% or more" is an approximate, sample-dependent figure.
- Deep 26 payment lag (4 vs 5 business days): sources differ.
