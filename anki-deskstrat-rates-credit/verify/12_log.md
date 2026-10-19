# Verify log: cards/12_structured_exotics.json

Checked: 45 cards. Changed: 8. Structure, card types and count unchanged; JSON validated.

Card # is 1-based position in the file.

## Changes

| Card # | Type | What was wrong | Fix | Source / method |
|---|---|---|---|---|
| 4 | basic | Market-practice claim that the flow richens 10y receiver tails stated as fact | Flagged "(approx.; unverified market-practice claim)" | Not verifiable; flagged |
| 16 | basic (AUTOCALL 3/3) | Year-2 call paid 106 instead of the stated 112; year-3 maturity used 106 instead of 118; expected CFs 28.7 and 48.23 were wrong; "yield to expected CFs is exactly 6%" was false (about 8.9% at price 100) | Recomputed expected CFs 36.00 / 30.17 / 53.69, PV at 4% = 110.24 vs 3y bullet 105.55; removed the false yield claim; flagged redemption convention as ambiguous | Recomputed (python) |
| 24 | basic ($1bn vega case) | Follow-up said expiries run 2y to 9y on an 8y swap; call-date swap tenors actually shrink from 8y to 1y | Corrected the tenor description | Reasoning from the 10NC2 call schedule; vega figures ($0.55m/bp, 0.055 pt/bp, $11m scaled) recomputed and correct |
| 31 | basic (PRDC) | Generic coupon formula and sign statements contradicted each other ("short the FX-reverse" and "long the coupon's FX dependence") | Replaced with a common call-spread-capped form, flagged as approximate, and removed the contradictory sign language | Mathfinance newsletter example and ICE SDX help page (https://mathfinance.com/wp-content/uploads/2025/01/Newsletter_Dec-2024.pdf ; https://idd.ice.com/IRHelp/Content/FM/Power_Reverse_Dual_Curre.htm) |
| 32 | basic (YoY floorlet) | RPI-CPIH alignment date stated without a basis | Stated as February 2030, decided Nov 2020, 2022 judicial review dismissed | https://www.hsfkramer.com/notes/pensions/2020-11/no-reform-of-rpi-until-2030 ; https://linklaters.com/knowledge/publications/alerts-newsletters-and-guides/2020/november/26/chancellor-pushes-rpi-reform-out-to-2030 |
| 33 | basic (CPDO) | No historical anchor for ABN AMRO 2006 | Added: first CPDO (ABN AMRO Surf) arranged summer 2006 with S&P AAA; three of ABN AMRO's first 2006 CPDOs later failed and were downgraded to D; 2007-08 timing flagged as unverified per deal | https://www.euromoney.com/article/27bjsstsqxhkmh1ncoger/opinion/inside-investment-obituary-the-cpdo-2006-2008 ; Federal Reserve FEDS 2010-05 (https://www.federalreserve.gov/pubs/feds/2010/201005) |
| 35 | basic (day-1 P&L) | Recognition rule stated loosely as "Level 1 or 2 immediate, Level 3 deferred"; B5.1.2A applies to Level 2 or 3 inputs with unobservable data | Restated per B5.1.2A; added IFRS 7.28 disclosure | Deloitte ASC 820 / IFRS comparison and DNB Q&A summaries (https://dart.deloitte.com/USDART/home/codification/broad-transactions/asc820-10/roadmap-fair-value-measurements-disclosures/appendix-b-comparison-us-gaap-ifrs/b-1-inception-gains-losses). Standard text itself not opened; see unverified list |
| 45 (cloze) | cloze (Formosa) | "Formosa notes are typically zero-coupon callable notes sold to retail" overstated | Described Formosa bonds as Taiwan-sold foreign-issuer bonds; early 30y zero-coupon callables mainly held by life insurers; flagged the five-year call rule and retail access as unverified | https://financeasia.com/article/ubs-joins-formosa-bond-bonanza/397218 ; https://www.theedgemarkets.com/article/cimb-bank-completes-issuance-us313m-notes |

## Checked and confirmed without change

- Callable = bullet minus issuer's Bermudan receiver, consistent across cards 1, 2, 4, 17 and cloze 39.
- Callable coupon derivation (card 17) and the 10NC2 case (card 23): D(10)=0.6703, A10=8.0783, A8=6.1944, forward 4.08%, uplift 39/53/62bp for k=1.0/1.35/1.6.
- Bachelier binary with smile (card 10): 0.8183, 0.8447, 0.8413 and the 2.6-point skew effect.
- Range accrual (cards 9, 26): in-range probabilities, PVs 88.9k/91.4k/91.5k/90.4k, total $362k, sensitivity $4.8k.
- TARN (cards 12, 27): E[coupon] 9.13/11.52/11.96; P(KO) 0.500/0.896/0.991; 0.75^3 = 0.422.
- CMS spread (cards 19, 25): spread vols 119.4/91.2/79.6bp, prices 47.6/36.4/31.8bp, reserve about $1.27m.
- Floorlet (card 28): d=0.5, floorlet 19.8bp, GBP 19.2k.
- CPPI (cards 22, 29, cloze 38): threshold -1/m; -20% gives NAV 92; -30% gives 88 (breach); -25% is exactly the floor.
- Structured note (card 30): A5=4.4677, coupon 1.86%, plain 3.87%, gap 2.01%.
- CPDO leverage numbers (card 33): 10x4.5x1.5% = 67.5% MTM; 2x gives 13.5%.
- Quanto drift (cards 21, cloze 43): mu = r_f - rho*sigma_S*sigma_X under domestic measure.
- Longstaff-Schwartz bias direction (cards 20, cloze 42): in-sample upward, out-of-sample lower bound.
- Copula/Bachelier spread formula (card 18/19): sigma_s^2 = s1^2 + s2^2 - 2 rho s1 s2.
- UK RPI 2-month lag and normal-vol quoting (card 32).

## Remaining unverified items (kept, not changed unless noted)

1. Card 4: the flow claim about richening 10y receiver tails (flagged in the card).
2. Card 16: redemption convention for 106/112/118 in the autocall case is ambiguous; the arithmetic is recomputed on the stated reading (flagged in the card).
3. Card 23: the Bermudan factor k (1.0-1.6) is an assumption; the receiver is struck at the forward rather than the coupon.
4. Cards 5-7 and 9: CMS convexity formula is the standard first-order approximation; not checked against Hagan 2002 text.
5. Card 13 and cloze 42: dual upper bound attribution to Andersen-Broadie is standard but the exact claim is not re-read from the paper.
6. Card 33: CPDO per-deal loss timing 2007-08 and the 2x-leverage counterfactual.
7. Card 34 and card 35: day-2 mark below issue and the deferred-day-1 accounting depend on firm policy; standard text of IFRS 9 B5.1.2A not opened, only secondary summaries.
8. Card 31: PRDC formula is one published example; term sheets vary.
9. Cloze 44 and card 45: Formosa retail access and the five-year non-call rule rest on single trade-press sources; current FSC rules not checked.
10. Card 38 (risk recycling) and the CSO card: qualitative, no numeric claims verified.
