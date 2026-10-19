# Verification log: cards/02_swaps_curves__v3.json

Cards checked: 20. Cards changed: 11 (plus one cloze reworded). Card count and types unchanged. Each card has exactly one lvl_* tag. JSON validated.

| Card | Issue | Fix | Source or method |
|---|---|---|---|
| 4 | Step 4 described the switch option value loosely | Reworded as the gap to the single-currency factor for the cheapest expected rate | Logic |
| 5 | Front assumed EUR always cheaper while the ATM option used forward 0 (inconsistent) | Front now assumes forward spread zero so the option is ATM | Internal consistency |
| 6 | EURIBOR Level 1 threshold said "raised from 20m in 2021" (direction wrong) | "reduced from 20m in the 2021 review" | EMMI methodology page; 2021 EURIBOR methodology review outcome (https://www.emmi-benchmarks.eu/benchmarks/euribor/methodology/) |
| 6 | 2024 enhancement: phase-in date 31 May 2024, "Level 2.3*" label, transparency figures 63%/13% not confirmed | Removed; states Level 2.3 reformulated, Level 3 discontinued, phased in during 2024 | EMMI reforms page (partial read); search summary |
| 7 | Cloze said threshold "raised" from 20m | Reworded to "reduced from 20 million in 2021" | As card 6 |
| 8 | "missed on all three channels" clause not verified | Removed the clause; fallback to previous TARGET2 day if not published by 09:00 CET kept | ECB EUR STR Q&A and overview (https://www.ecb.europa.eu/stats/financial_markets_and_interest_rates/euro_short-term_rate/html/eurostr_qa.en.html) |
| 11 | Step 1 derivative expression was algebraically muddled | Replaced by d_t/tau * prod_{i!=t}(1+r_i d_i) = (d_t/tau)(1+tau R)/(1+r_t d_t) | Recomputed |
| 13 | "-0.016%" difference vs true 3.75% wrong; implied 1m rate 3.5626% is 18.7bp below | Corrected to about 18.7bp; PV error about -15,500 | Recomputed (python: 3.5626%, PV -15,461) |
| 17 | Bias growth "0.8bp per quarter" | "0.8 to 0.9bp per quarter" | Recomputed increments 0.81, 0.87, 0.94 |
| 18 | SR1 "to four decimal places" not confirmed | Cloze reduced to verified content (arithmetic average; daily compounding; $25/bp) | CME One-Month SOFR contract specs (https://cmegroup.com/trading/interest-rates/stir/one-month-sofr_contract_specifications.html) |

Recomputed and confirmed without change: card 1 (148.7005, 148.6085, diff 0.092); card 3 (98.2143m, 1.7857m, 2.00m, -49,107); card 4 (e^-0.20, e^-0.12); card 5 (0.001995, ~199,500); card 9 (annuity 4.7391 under annual compounding, PV01 47,391, PV 20bp 947,820; compounding effect 0.73bp); card 10 (1,388.89; 1.61bp); card 11 (1.61bp, 0.55bp); card 12 (DF 0.990099, 0.980903, 0.964032); card 13 (implied fwd 3.5573%); card 14 (p=0.5, -20,625 per unit p, -206 per pp); card 15 (1.0111%, 1.0162%, 0.51bp); card 16 (4.875bp, 3.9512%); card 17 (futures rates, convexity 4.88/5.69/6.56/7.50bp, forwards); card 19 (no numbers).

Card 0 and card 2 (JPY basis): sign convention and capital arithmetic checked (500m x 0.25% = 1.25m; 1.5m to 3.0m capital cost, labelled approximate). Not sourced to a primary document. Card 3 MtM mechanics not sourced to a primary document.

## Unverified items
- Card 0/2: the JPY basis level (-25bp) and the leverage-ratio figures are illustrative; no market source checked.
- Card 6: current EURIBOR Level 1 share and final phase-in state not confirmed; EMMI pages returned conflicting descriptions (two-level vs three-level) in search.
- Card 8: the republication threshold of 2bp and 09:00 CET confirmed from ECB Q&A/overview text via search summary; not read in full from the primary page.
- Card 18: the SR3 $25 per bp is standard but not re-read from the CME page in this pass.
- Card 9: the card assumes annual compounding for the discount; this convention is stated on the card.
- Card 17: the convexity formula 1/2 sigma^2 T1 T2 is the standard approximation; not checked against the Hull-White source.
