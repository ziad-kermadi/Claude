# Verify log: 09_scenarios_markets_reg (main and deep)

Checked: 52 main cards + 30 deep cards = 82 cards (all read, all arithmetic re-run).
Card counts unchanged; JSON validated after edits.

## Changed cards

| Card (file, index) | What was wrong | Fix | Source / method |
|---|---|---|---|
| main #4 | Follow-up said a protection buyer's CS01 is negative while stating its MTM rises when spreads widen (internally contradictory) | Buyer's spread sensitivity is positive; JTD opposite sign to long bond | Sign convention, reasoning |
| main #12 | Dates marked "approximate" | BoE: announced 28 Sep 2022, ended 14 Oct 2022; gilt sales postponed (resumed 1 Nov) | BoE statement on end of gilt market operations (search results) |
| main #13 | CTD had "lowest implied repo"; CTD has the highest implied repo (cheapest basis) | Corrected | Definition |
| main #32 | CCC weight "over 50%" | B 30%, BB 15%, CCC 50%, default 100% | ActiveViam FRTB DRC configuration docs (secondary); BCBS MAR22 not fetched |
| main #34 | Follow-up asked "why is ES not coherent" and answered "ES is coherent" | Reworded: ES is coherent; 97.5% vs 99% VaR match is approximate | Definition |
| main #35 | "approx." on 24-observation test | 24 obs over 12 months confirmed (Risk.net, Clarus); 4-per-month cap unverified | Search (partial) |
| main #36 | PLA: red/amber consequences incomplete; red = fail, but amber keeps IMA with surcharge | Traffic light spelled out | Zanders summary (secondary); MAR32 not fetched |
| main #40 | EUR 500k MTA stated without caveat | Caveat added: EUR 8bn phase 6 and EUR 50m IM threshold confirmed; MTA unverified | Search (secondary) |
| main #42 | UK Basel 3.1 "approx. 2027" | PS1/26 (Jan 2026): 1 Jan 2027; FRTB IMA moved to 1 Jan 2028. Output floor phase-in unverified | Crisil Integral IQ, A&O Shearman summaries (secondary); PRA PS1/26 not fetched |
| main #45 | 26bp "approx." | 26.161bp (ISDA USD 3M fallback) | Secondary sources (MathWorks, ISDA consultation) |
| main #46 | MiFIR changes not flagged | Regulation (EU) 2024/791 status noted; derivatives transparency final thresholds and DTO scope unverified | Search (partial) |
| main #47 | T+1 date "approx." | 11 Oct 2027 for UK and EU, confirmed by multiple sources; statutory finality not checked | Search (secondary) |
| main #49 | Amber/red bands described loosely | Amber 0.7-0.8 / KS 0.09-0.12 keeps IMA with surcharge; red loses IMA | Zanders summary (secondary) |
| deep #4 | 5-min and 30-min markouts computed from the 4.21% fill price, not the 4.20% trade mid (1bp instead of 2bp, 2bp instead of 3bp); net-edge and "zero" conclusion wrong | Recomputed: 5-min markout -2bp (-80k), net -1bp; 30-min -3bp (-120k), net -2bp (-80k); conclusion: informed flow | Recomputed |
| deep #6 | Correlation scenario formulas stated as verified | Flagged: multipliers 1.25/0.75 confirmed by secondary docs; max/min forms from memory, unverified | Search (partial) |
| deep #8 | Spearman 0.75-type result described as failing; amber is not a loss of IMA | Scenario changed to 0.65 (red); amber note added | Zanders summary |
| deep #19 | Receiver swap given delta +1 (sign convention wrong for a receiver) | Delta -1 for receiver, sign convention flagged; single-trade add-on uses absolute value so numbers unchanged | SA-CCR convention (from memory, to verify) |
| deep #21 | Explained P&L arithmetic: -1,151 + 4,500 + 106,200 + 134 = 109,683, not 109,684; residual 3,317 not 3,316 | Corrected | Recomputed |

## Checked and left unchanged (recomputed or confirmed)

- main #0 (10y swap DV01 ~82k per bp per 100m; annuity identity confirmed: par bond modified duration 8.18), #1, #2, #5, #6, #7, #8, #9, #10, #11, #14-#31, #33, #37-#39, #41, #43, #44, #48, #50, #51 (arithmetic and formulas checked; RRAO 1.0% / 0.1% and ES 97.5% with LH 10/20/40/60/120 consistent with BCBS as recalled).
- deep #0-#3, #5, #7, #9-#18, #20, #22-#29: arithmetic re-run; Avellaneda-Stoikov derivation (deep #14-#15) re-derived, signs and numbers correct; Almgren-Chriss (deep #16) re-derived; square-root law (deep #17) re-derived; SA-CCR SD and EAD (deep #19, #23, #28) recomputed; KVA recomputed by Python = 662,279 (card 662k correct); LVaR (deep #24) recomputed; CVA and FRTB SBM aggregation (deep #5) recomputed (sqrt(20)=4.47, 6.0, 2.0, 17.1, 18).
- ES 97.5% and liquidity horizons 10/20/40/60/120: not directly fetched; consistent with BCBS as known.
- UK RPI aligned with CPIH from 2030: from memory of the Nov 2020 decision; not re-fetched.

## Unverified items (kept; approximate tag where it appears)

1. FRTB MAR21.6 correlation scenario formulas (max(2rho-1, 0.75rho), min(1.25rho, 1)): only the 1.25/0.75 multipliers are confirmed by secondary sources. (deep #6)
2. PLA thresholds: Spearman 0.8/0.7 and KS 0.09/0.12 are from secondary sources (Zanders, ActiveViam), not MAR32 text. (main #36, #49)
3. NMRF: cap of at most 4 observations in any single month is unconfirmed. (main #35)
4. DRC weights: B 30% and CCC 50% confirmed by secondary ActiveViam tables; BCBS MAR22 not fetched.
5. UK Basel 3.1 output floor phase-in schedule and 72.5% applicability: unverified. (main #42)
6. UMR minimum transfer amount EUR 500k: unverified. (main #40)
7. MiFIR review: final derivatives deferral thresholds, deferral lengths and DTO scope unverified. (main #46)
8. SA-CCR interest-rate supervisory factor 0.5%, alpha 1.4 and 5% multiplier floor: from BCBS 279 as recalled; the search did not return the parameter table. (main #37, #38, deep #19, #23, #28)
9. SA-CCR receiver-swap delta sign convention. (deep #19)
10. SIMM calibration (stressed period, 99% quantile, 10-day horizon). (main #39)
11. Reserve/central-bank claim exclusion from leverage ratio ("some jurisdictions", approx.). (main #43)
12. US eSLR measurement convention (quarter-end vs average balance) and the claim that the leverage charge on derivatives is small relative to gross notional. (main #10, #43)
13. UK index-linked gilt lag (3 months; 8 months for older issues). (main #18)
14. T+1 statutory finality for UK and EU (main #47): sources agree on 11 Oct 2027 but the UK statutory instrument was not checked.
15. ES 97.5% and liquidity horizons, RRAO 1.0%/0.1%: consistent with BCBS as recalled, not fetched.
16. Avellaneda-Stoikov and Almgren-Chriss: derivations re-checked internally; no external source fetched.
17. BoE LDI dates: verified (see changes). LIBOR 26.161bp: verified by secondary sources only.
