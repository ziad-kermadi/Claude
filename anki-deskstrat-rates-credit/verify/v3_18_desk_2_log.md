# v3 verification log: 18_desk_2.json and 18_desk_3.json

Covers cards/18_desk_2.json (30 cards) and cards/18_desk_3.json (30 cards). Card indices are 0-based.
Format and tags checked: all cards have exactly one lvl_* tag, 2-7 tags, no markdown, no bare ampersands, MathJax in \( \) and \[ \]. Card counts and types unchanged.

## Changes

| file | card index | issue | fix | source URL or "recomputed" |
|---|---|---|---|---|
| 18_desk_2.json | 13 (cloze, SR 11-7) | Definition said "incorrect or misused models"; SR 11-7 refers to incorrect or misused model outputs and reports | Cloze now reads "{{c3::incorrect or misused model outputs and reports}}" | https://www.federalreserve.gov/supervisionreg/srletters/sr1107.htm (search summaries confirm the three elements; full letter text not retrieved) |
| 18_desk_2.json | 17 (derivation, AVA) | Units mismatch: sigma was "in price units" but the worked example uses sigma = 0.3 bp of rate and DV01 = 85,000 per bp, and the formula was z·sigma·E with E undefined in units | Front now defines sigma in bp of rate and E as DV01 (price per bp); back writes the exit value and adjustment as z·sigma·E, with sigma·E in price units; removed the "Computed in python." meta note | recomputed: 1.2816 × 0.3 × 85,000 = 32,680 (32,679.6) |
| 18_desk_2.json | 23 (case study, AVA aggregation) | Invented sanity threshold ("if above 2%, check double counting") with no basis | Replaced with a qualitative check ("if the adjustment is large relative to fair value") | no figure needed; 1.75m / 450.0m = 0.39% recomputed |
| 18_desk_3.json | 21 (derivation, compression DV01/PV) | Condition for the S'A term to sum exactly omitted the notional condition sum(N_i) = N_r | Added "when the residual notional equals the net notional, sum_i N_i = N_r" | derivation check (algebra), no external source |
| 18_desk_3.json | 26 (amendment, PV impact) | 0.5 bp x 8.376 x 100m = 41,882, card said about 41,900; direction of the impact was not stated | Value set to 41,880; stated magnitude and that the sign depends on payer or receiver | recomputed: 0.00005 x 8.3764 x 100m = 41,882 (A10 at 3.50% semi-annual recomputed as 8.3764) |

## Checked and confirmed (no change)

| file | card index | check | result | source URL or "recomputed" |
|---|---|---|---|---|
| 18_desk_2.json | 14 (cloze, PRA SS1/23) | effective date 17 May 2024; five principles (identification/classification, governance, development/implementation/use, independent validation, mitigants) | confirmed | https://www.bankofengland.co.uk/prudential-regulation/publication/2023/may/model-risk-management-principles-for-banks-ss |
| 18_desk_2.json | 28 (cloze, nine AVA categories) | list and order: market price uncertainty, close-out costs, model risk, unearned credit spreads, investing and funding costs, concentrated positions, future administrative costs, early termination, operational risk | consistent with RTS 2016/101 structure (Arts 9 to 17, nine categories); see unverified list | https://www.legislation.gov.uk/eur/2016/101/contents (contents listing via search) |
| 18_desk_2.json | 0 to 3 (IPV chain) | 0.9 x 60,000 = 54,000; 0.4 x 250,000 = 100,000; sign logic | confirmed | recomputed |
| 18_desk_2.json | 8 to 10 (remark chain) | -180,000 x 2 = -360,000 | confirmed | recomputed |
| 18_desk_2.json | 11 (month-end bond) | (62.4 - 61.1)/100 x 10m = 130,000 | confirmed | recomputed |
| 18_desk_2.json | 15 (model reserve) | 98.7 - 97.9 = 0.8 | confirmed | recomputed |
| 18_desk_2.json | 18 (close-out AVA) | 85,000 x 0.25 = 21,250; x4 size gives 85,000 | confirmed | recomputed |
| 18_desk_2.json | 19 (5y5y IPV) | 0.7 x 300,000 = 210,000 | confirmed | recomputed |
| 18_desk_2.json | 22 (IPV case study) | 36,000; -80,000; 54,000; net 10,000; gross 170,000; breach at 10y10y only | confirmed | recomputed |
| 18_desk_2.json | 23 (AVA aggregation) | 0.9 + 0.35 + 0.5 = 1.75m; 1.75/450 = 0.39% | confirmed | recomputed |
| 18_desk_2.json | 24 (stale bond) | 8 x 8,500 = 68,000 loss; 3 x 8,500 = 25,500 reserve | confirmed | recomputed |
| 18_desk_2.json | 29 (IFRS 9 B5.1.2A cloze) | paragraph reference and the factor test | consistent with IFRS 9 B5.1.2A as known; not re-fetched | (from knowledge; see unverified) |
| 18_desk_3.json | 0 to 3 (booking flip chain) | DV01 209,411; residual 2 x 209,400 x 5 = 2.09m; wrong-hedge unwind | confirmed | recomputed |
| 18_desk_3.json | 5 and 6 (CCP basis) | A10 at 3.00% semi-annual = 8.584; DV01 171,686; 0.3 bp = 51,506 | confirmed | recomputed |
| 18_desk_3.json | 8 and 9 (SOFR fixing) | 100m x 0.0004 x 3/360 = 333; 500m x 0.0004 x 7/360 = 3,889 | confirmed | recomputed |
| 18_desk_3.json | 11 (static data) | 3m x 3% x 365/360 - 3m = 41,667 per year; ten years about 0.42m; two-day lag 500 | confirmed | recomputed |
| 18_desk_3.json | 13 (CSA cloze) | 3.2m - 1m = 2.2m >= 0.5m MTA, call; 1.3m - 1m = 0.3m < 0.5m, no call | confirmed | recomputed |
| 18_desk_3.json | 14 (cloze, OIS spot start) | USD and EUR T+2; SONIA T+0 | SONIA T+0 supported by CFTC made-available-to-trade table; see unverified | https://www.cftc.gov/PressRoom/PressReleases/8745-23 |
| 18_desk_3.json | 15 (CSA dispute) | 24m x 4% x 2/360 = 5,333 | confirmed | recomputed |
| 18_desk_3.json | 20 (compression case) | A2, A5, A10 at 3% annual = 1.9135, 4.5797, 8.5302; 5y DV01 per bp 9,159; aggregate 31,960; gross 310m to 70m | confirmed | recomputed |
| 18_desk_3.json | 22 (back-dated trade) | (3.20% - 3.24%) x 4.5797 x 100m = -183,188; DV01 45,797 | confirmed | recomputed |
| 18_desk_3.json | 23 (novation) | (3.00% - 2.80%) x 4.5797 x 100m = 915,941 | confirmed | recomputed |
| 18_desk_3.json | 25 (UK EMIR and MiFIR) | UK EMIR reporting by T+1 (working day after); MiFIR scope for bilateral OTC swap | T+1 supported by secondary sources; MiFIR scope kept with "check current rules" wording | https://www.confluence.com/?p=1697 ; https://www.bankofengland.co.uk/financial-stability/trade-repository-data/uk-emir-reporting-qas |
| 18_desk_3.json | 12 (identifiers cloze), 28 and 29 (lifecycle and VM cloze) | LEI, UTI, UPI roles; VM settlement in cash | confirmed | from knowledge of EMIR and MiFIR reporting fields |

## Unverified items (kept, not changed)

1. UK EMIR T+1 deadline (18_desk_3 card 25). The primary text (UK EMIR Article 9) could not be retrieved: legislation.gov.uk and eur-lex.europa.eu were not reachable from this session. T+1 is supported only by secondary sources and the Bank of England Q&A.
2. SONIA OIS spot start at T+0 (18_desk_3 card 14). Supported by one CFTC table (2023); no ISDA or dealer convention document was retrieved.
3. AVA category titles (18_desk_2 card 28). The nine names and order are consistent with RTS 2016/101 Articles 9 to 17, but the titles of Articles 12, 13 and 15 were not checked individually against the text.
4. CRR Article 105 and Article 34 references and the EBA RTS 90% confidence wording (18_desk_2 card 16). Stated from knowledge; not re-fetched.
5. IFRS 9 B5.1.2A wording (18_desk_2 cards 6 and 29). Stated from knowledge; not re-fetched from IFRS Foundation.
6. MiFIR scope for a bilateral OTC swap (18_desk_3 card 25). Written as "generally not" with a check-the-rules instruction; no specific rule text retrieved.
7. Illustrative figures that are not market facts and are labelled as such in the cards: 0.5 vol bp band, 0.5 bp IPV tolerance, 4% carry rate, 0.3 bp basis, the 85,000 DV01 used in the AVA derivation.
