# v3 verification log: 18_desk_7, 18_desk_8, 18_desk_9

Cards checked: 90 (30 per file). Cards changed: 23 in total (7: 7, 8: 2, 9: 14). Card counts and card types unchanged. Every file has exactly one lvl_* tag per card.

## Changes

| file | card | issue | fix | source URL or "recomputed" |
|---|---|---|---|---|
| 18_desk_7 | 4 | Client "receives fixed" would reduce the long 10y bucket, but the arithmetic added the DV01. Annuity 8.1 gave 8.18 when recomputed. | Client pays fixed on £60m 10y (desk receives fixed, adds long DV01). Annuity 8.2; PV01 £820 per £1m; add £49.2k/bp; bucket £267.2k/bp = 106.9%; max notional 32,000/820 = £39.0m. | recomputed |
| 18_desk_7 | 7 | P&L sign convention not stated, and it differs from other cards in the deck. | Front now says DV01 is P&L per +1bp rise. The formula P&L = Σ d_i Δy_i is consistent with that. | recomputed (convention) |
| 18_desk_7 | 13 | "gilt-swap spread (the asset-swap spread)" conflated two different measures. | Parenthetical removed. | conceptual |
| 18_desk_7 | 18 | IAS 39 80–125% claim was given without noting that IFRS 9 removed it. | Now states that IAS 39 used the 80–125% offset as a bright line, and IFRS 9 removed it: economic-relationship test, hedge ratio aligned to risk management, prospective-only assessment. Checked: the claim is correct. | https://www.iasplus.com/en-gb/publications/uk/need-to-know/2013/need-to-know-ifrs-9-hedge-accounting |
| 18_desk_7 | 23 | Sign convention not stated. | Front states P&L per +1bp rise, so negative means long duration. Sum recomputed: −22.6m, 151% of limit, 2y share 80%. | recomputed |
| 18_desk_7 | 24 | Convention not stated. Text called the book "short" when it is long duration under the stated convention. | Convention stated; "short" changed to "position". Loss −6.84m recomputed. | recomputed |
| 18_desk_7 | 25 | "Sum of the two legs" wording was unclear. | Changed to: a call and a put at the same strike have equal gamma, so the straddle has twice one leg's gamma. | conceptual |
| 18_desk_8 | 0 | P(4.205%) written as 98.3406. Recomputed price is 98.3404 (ΔP = −0.04009 confirmed). | 98.3406 changed to 98.3404. | recomputed |
| 18_desk_8 | 24 | "Relative error about 10^-11" applied to the £1bn trade. The trade's relative change is about 10^-15. The 10^-11 figure belongs to the summation example. | Sentence corrected. The 1e6 × 0.1 sum = 100000.00000133288 is confirmed. | recomputed |
| 18_desk_9 | 0 | "30 January 2012" date not supported; sources say late January, with model approval on 28 Jan. The $129m was attributed to Q2, but the 10-Q/A gives $129m as the restated Q1 average. | Date changed to "January 2012". Restated CIO VaR about $129m vs $67m first reported. | https://www.sec.gov/Archives/edgar/data/0000019617/000001961712000262/jpm-2012033110qamended.htm ; https://www.ifre.com/story/1744757/derivatives-jpm-report-unveils-var-errors |
| 18_desk_9 | 3 | Net futures shorts "$900bn", repo "$1.4trn" and basis "5bp to above 70bp" not verified. | Replaced with a qualitative statement that the position was very large and the basis widened sharply. | unverified figures removed |
| 18_desk_9 | 5 | OFR and CFTC attributions not verified. | Replaced with "the literature disagrees on how much the basis unwind amplified the dash for cash; its causal role is contested." | unverified attribution removed |
| 18_desk_9 | 6 | Archegos figures attributed to an "independent report summarised by Risk.net". The report is the Paul Weiss-led review of Credit Suisse. 9.4% margin and $7bn to $21bn gross swap value confirmed. | Attribution corrected. Figures kept. | https://www.risk.net/risk-management/7861786/archegos-report-details-margin-failings-at-credit-suisse |
| 18_desk_9 | 9 | Cloze wording "settlement for protection sellers" is ambiguous. | "Protection sellers therefore pay about 91.375% of notional." Figure confirmed. | https://www.felixsalmon.com/2008/10/lehman-cds-low-price-low-volume/ |
| 18_desk_9 | 10 | "Gross exposure around $400bn" not verified. Lehman auction figures confirmed: midpoint 9.75, net open interest $4.92bn, final 8.625. | "$400bn" changed to "hundreds of billions". | https://creditwritedowns.com/2008/10/initial-results-of-lehman-cds-auction.html |
| 18_desk_9 | 14 and 15 | Reserves "below $1.4trn" not verified. Repo prints 5.25% and 2.4% not checked. Cost (2bn × 3% / 360 = $166,667) recomputed. | Reserves figure removed (cloze now "multi-year low"). Prior-day rate rounded to 2.4%. | recomputed (cost) |
| 18_desk_9 | 18 | Court ruling described as "partly revoked the order", and the ruling was reported as final. Ruling is a Federal Administrative Court decision of 1 Oct 2025 that found the write-off unlawful and annulled FINMA's order. It is not final. | Wording corrected, with the appeal status flagged. | https://www.jurist.org/news/2025/10/swiss-court-rules-20-billion-credit-bonds-write-off-unlawful/ |
| 18_desk_9 | 20 | EUR/CHF "near 0.965" intraday not supported. Sources report an intraday low around 0.895 (a JPMorgan note, one source) and a late low around 0.973. FXCM capital figures ($225m negative equity, $300m) not verified. Loss recomputed on 0.895. | 0.965 replaced by "about 0.895, one reported low; venues differ". Loss CHF 3.05m, about 30 times the plan. FXCM figures removed. | https://www.jpmorganchase.com/institute/research/financial-markets/insight-timing-central-bank-announcements (single source for 0.895); recomputed |
| 18_desk_9 | 21 (cloze) | Same 0.965 figure and "roughly 20%" below floor. | Changed to about 0.90, roughly 25% below the old floor. | as card 20 |
| 18_desk_9 | 22 | "Yen slid more than 0.5%" not verified. | Changed to "the yen weakened against the dollar after the decision". | unverified figure removed |
| 18_desk_9 | 24 | "A press estimate put losses at 15-30%" not verified. | Sentence removed. | unverified figure removed |
| 18_desk_9 | 29 | Sterling "fell about 10% overnight to near $1.31" on 27 June. The 10% fall was on 24 June. Sterling was near $1.32 on 27 June (Reuters intraday low $1.3122). Gilt 10y "record low about 0.93%" confirmed. | Text now reads "fallen about 10% against the dollar since the referendum, to near $1.32". | https://www.business-standard.com/amp/article/reuters/sterling-at-lowest-since-1985-gilt-yield-record-low-below-1-percent-116062701156_1.html |

## Checked and confirmed without change

- 18_desk_7: 5, 7 (L = 180, S = −27.5 recomputed), 11 (JTD 26 / 36 recomputed), 12 (notional 83.3m, carry −£250k recomputed), 14 (h* = 0.83), 15, 16–17, 19 (n = −1.84, residual Δ −£2.2k, swap 4.9m, residual vega −£1.8k, all recomputed), 20–21 (cross-gamma £2.0m / £0.6m recomputed), 22 (solve n1 = −64.7, n2 = 47.4 recomputed; H1-only residual −37k), 26–29.
- 18_desk_8: 1 (linear error 0.095, convexity C = 78.5, recomputed), 3 (ACT/ACT 0.67033 vs ACT/365F 0.66849; £1,837 per £100m, recomputed), 5, 8, 10 (forward / central DV01 error recomputed), 11 (25 min / 29.3 s, recomputed), 25 (C++ snippet compiled with g++ -std=c++20 -Wall -Wextra -O2; output matches the card).
- 18_desk_9: 12 (LDI), 13 (BoE purchases 28 Sep to 14 Oct 2022; unwind completed 12 Jan 2023; https://www.bankofengland.co.uk/news/2023/january/boe-completes-unwind-of-recent-financial-stability-gilt-purchases), 19 (CHF 16bn AT1 write-down), 23 (ECB dates), 25 (forward F = 107.39 and repo sensitivity recomputed), 26 (HTM 600m, 120m, 20% recomputed), 27 (£27/day recomputed).

## Unverified items (kept, not checked by search)

- 18_desk_8 card 13: Excel volatile function list (NOW, RAND, OFFSET, INDIRECT; CELL and INFO are volatile only in some cases). Not checked by search.
- 18_desk_8 cards 19 to 21: kdb+ aj, ej, xbar and parted-attribute semantics are from knowledge, not checked against the q reference.
- 18_desk_7 card 10: Basel FRTB liquidity-horizon square-root add-on formula is from knowledge. The example numbers are recomputed.
- 18_desk_9 card 18: 1 UBS share per 22.48 CS shares, and about CHF 3bn to shareholders, not checked.
- 18_desk_9 card 19: UBS CHF 9bn protection beyond the first CHF 5bn not checked.
- 18_desk_9 card 9 to 10: Lehman gross exposure is now only qualitative. Other Lehman figures were confirmed.
- 18_desk_9 card 15: the 5.25% intraday/close print on 17 Sep 2019 not checked.
- 18_desk_9 card 22: BoJ policy-rate range and BoJ ETF/J-REIT ending were not checked.
- 18_desk_9 card 28: the ISDA fallback and fixed spread conversion were described qualitatively and not checked against the protocol.
