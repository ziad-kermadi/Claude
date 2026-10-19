# Verification log: 04_inflation.json and 04_inflation_deep.json

Checked: 42 cards (04_inflation.json) + 30 cards (04_inflation_deep.json) = 72. Changed: 13.

## Changes

| Index | File | What was wrong | Fix | Source |
|---|---|---|---|---|
| 9 | 04_inflation.json | Reform month given only as 2030 | Cloze now "February 2030"; back adds no-compensation decision and 1 Sep 2022 High Court dismissal | Nov 2020 govt/UKSA response (https://www.ipe.com/rpi-reform-to-go-ahead-in-2030-without-compensation/10049223.article); judgment date (https://www.burges-salmon.com/articles/102hwth/the-end-of-rpi-as-we-know-it, https://dalriadatrustees.co.uk/?p=27817) |
| 15 | 04_inflation.json | Generic 3m lag used for a UK RPI ZC swap | Lag set to 2m (UK RPI swap lag); B(0,9.83)=8.52; index correction -0.51bp, K about -0.05bp (was -0.76bp / -0.08bp) | UK RPI swap lag: https://www.dmo.gov.uk/media/1953/igcalc.pdf and forum/practitioner summary; recomputed in python3 |
| 18 | 04_inflation.json | Pillar equation mixed raw I(0) with deseasonalised I^SA | Uses I^SA(0) on the left and right | Internal consistency with card 41 (I^SA = I exp(-s)); recomputed |
| 23 | 04_inflation.json | Gap of 0.40 is 12.6 SD, not 12 | "about 12.6" | Recomputed: 0.397/(0.01*sqrt(10)) = 12.56 |
| 27 | 04_inflation.json | Said unhedged scheme is short 5% caps; LPI liability is long the 5% caplet, so hedge is short 5% caps | Sign corrected | Payoff identity min(max(x,0),5%) = max(x,0) - max(x-5%,0), verified |
| 34 | 04_inflation.json | 13.5 x 0.0001 = 0.135%, not 0.14% | "0.135%" | Recomputed |
| 36 | 04_inflation.json | Same sign error as card 27 | Front and back now say the hedge is short the 5% caplet | As card 27 |
| 2 (deep) | 04_inflation_deep.json | Pay/receive ambiguous for wedge legs | Clarified as fixed legs of wedge swaps; post-2030 leg gains if post-2030 forward falls | Convention clarification |
| 3 (deep) | 04_inflation_deep.json | Said RPI-linked gilt holders are being compensated. Wrong: the 2020 decision gave no compensation | Front and back rewritten: no compensation; JR dismissed 1 Sep 2022, no appeal | https://www.ipe.com/rpi-reform-to-go-ahead-in-2030-without-compensation/10049223.article; https://dalriadatrustees.co.uk/?p=27817 |
| 4 (deep) | 04_inflation_deep.json | Make-whole discounted twice (PV loss is already time-0) | Removed extra DF; states no payment under 2020 decision | Internal derivation check |
| 12 (deep) | 04_inflation_deep.json | Generic 3m lag for UK ZCIIS | 2m UK RPI lag; B(0,9.83)=8.52; -0.51bp index, -0.05bp on K | As card 15 |
| 23 (deep) | 04_inflation_deep.json | New par 3.109% was wrong; (1.003 x 1.357)^(1/10)-1 = 3.131% (dK = 3.09bp, correct) | 3.131% | Recomputed |
| 28 (deep) | 04_inflation_deep.json | 3m lag; B and lag-cost sanity figure | 2m lag; B=8.52; index -0.51bp; par -0.05bp; lag cost about 50bp (was 75bp) | As card 15 |

## Verified, no change
- Cards 0, 1: 8m lag with daily interpolation pre-2005; 3m lag without interpolation post-2005.
- Card 2, 3, 4, 5, 6, 7, 8, 10, 11, 12-14, 16, 17, 19-22, 24-26, 28-33, 35, 37-41: formulas and arithmetic checked; no errors found.
- Deep cards 0, 1, 5-11, 13-22, 24, 25, 26, 27, 29: numbers recomputed in python3 (for example, 1.031^10=1.3570; caplet 19.19bp; F=3.05 gives 20.73bp; delta 0.2993; seasonal carry +5,162 vs -21,088).

## Unverified items
- 8m-lag and 3m-lag history: the DMO description is in search snippets only. Not checked against a primary page.
- TIPS: 3-month lag, daily interpolation and par principal floor (cards 21-23) are stated from memory and not web-checked in this pass.
- BTP€i lag and floor: no reliable source found. No card in these two files covers BTP€i. OATi and OAT€i are not used in these two files either. AFT pages confirm OAT€i 3m lag and par floor.
- Card 23 uses a normal vol of 1% and a Bachelier value of "effectively zero". This is a hypothetical assumption, not a market quote.
- Card 26 (JY vs SABR delta consistency) is qualitative. Not verified against a source.
- Card 31 (specialness rule of thumb) is approximate.
- Litigation date: the spec's known list says 2023-24. Sources say the High Court dismissed the JR on 1 Sep 2022 and no appeal was pursued. Card text now uses 2022.
