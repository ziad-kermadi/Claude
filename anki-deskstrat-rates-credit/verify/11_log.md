# Verification log: cards/11_repo_financing.json

Checked: 45 cards (38 basic, 7 cloze). Fixed: 16 cards (indices are 0-based array positions). Card count and types unchanged. JSON validated.

## Cards changed

| Idx | Type | What was wrong | Fix | Source or method |
|---|---|---|---|---|
| 5 | basic | TMPG fails charge inverted: formula was max(0, r_ref - 3%). Charge also said to be high in low-rate regimes in the wrong direction. Example used 4.50% reference. | Charge rate = max(3% - r_ref, 0). Example uses 1.50% reference, giving 1.50% charge and $8,333. Breaks-where and follow-up rewritten. | NY Fed TMPG fails charge documentation (2009 formulation, 3% cap; 2016 and 2018 TMPG revisions); WilmerHale 2009 summary |
| 32 | basic | Same inverted formula. Front used 4.50% reference; back said charge zero at 3% or below. | Front uses 1.50% reference and max(3% less reference, 0). Charge zero at 3% or above. | Same as idx 5 |
| 6 | basic | Euro negative deposit rate start given as 2015. | 2014 (ECB cut to -0.10% effective 11 June 2014). | Banco de Espana, ECB deposit facility history |
| 8 | basic | Reformed SONIA trimmed mean described as "roughly interquartile". | Central 50% of the volume distribution. | BoE SONIA key features; Wikipedia summary of BoE method |
| 11 | basic | Facilities incomplete. STR omitted. CTRF described as a 2022 facility in the verify spec. ILTR date uncertain. | Added STR (announced 4 Aug 2022; 7-day, Bank Rate, Level A, unlimited). CTRF described as 3-month stress liquidity facility, launch date flagged unverified. ILTR says it predates 2022, date flagged unverified. | BoE market notices (STR 4 Aug 2022); BoE ILTR notices (2014 format; 2025 recalibration) |
| 13 | basic | Pre-spike level described as "low 2% range the prior week". | About 2.43% on 16 Sep 2019 (previous business day). 5.25% SOFR and approx. 10% intraday retained as approx. | Sources summarised by search: DWS, OFR, GFMI; 5.25% is the daily SOFR print, 10% is intraday |
| 14 | basic | SRF said to be "announced in 2019, operational 2021". | Fed established the standing repo facility on 28 July 2021; 2019 overnight repo operations preceded it (approx.). | Federal Reserve press release 28 July 2021 |
| 15 | basic | Compliance dates flagged "approximate; verify". | Dates confirmed: cash 31 Dec 2026, repo 30 Jun 2027 (SEC Feb 2025 extension). | SEC extension coverage (Sewkis, Arnold & Porter, The Global Treasurer); no later change found |
| 20 | basic | ROE inconsistent with card 29. Card called 48.5% "ROE" but card 29 uses 54% (accounting, before equity cost). | Separates accounting ROE (54%) from economic return after equity cost (48.5%). | Recomputed |
| 21 | basic | Compounded product stated as about 1.0004044; correct is about 1.000776. Annualised 4.044% was already correct. | Product value corrected. | Recomputed (python) |
| 26 | basic | Excess-carry ROE ignores the 2% haircut funding; not stated. | Added note that the full 100m is treated as earning the spread and the 98m cash financing is not separately costed. Numbers unchanged (75,000; 3.75%; 15.2%). | Recomputed; modelling simplification |
| 28 | basic | Sanity-check explanation wrong: 60bp gap is not the net difference. | Net gap = 75bp minus 17.7bp effective repo spread = 57.3bp, matching $0.573m. | Recomputed |
| 31 | basic | Two steps labelled "Step 4". | Second renumbered Step 5. Numbers unchanged (-19,444; 1,389 per day). | Recomputed |
| 35 | basic | Futures leg "needs no funding" (contradicts margin point). | "needs margin but no principal funding". | Conceptual |
| 36 | basic | NSFR RSF for Level 1 reverse repo with financial counterparty under 6m given as about 0%. Basel standard gives 10%; 0% is a transitional or jurisdictional treatment. | Basel 10% (NSFR standard para. 38), with jurisdictional 0% noted as unverified. | Basel NSFR text as summarised by ICMA ERCC (May 2024) and the NSFR FAQ; EU CRR II transitional rule |
| 41 | cloze | US SLR for G-SIB holding companies given as "5% plus a buffer" (old eSLR). Final rule changed it. | US eSLR buffer = 50% of Method 1 GSIB surcharge on top of 3% minimum. Effective 1 Apr 2026, early adoption 1 Jan 2026. UK 3.25% confirmed. | Fed/FDIC/OCC final eSLR rule, 25 Nov 2025 (Orrick, Mondaq and Forvis summaries); PRA Rulebook leverage ratio |

## Checked and left unchanged (recomputed or verified)

- Card 0: 76,712 interest; repurchase price 50,076,712.
- Card 1: 52.63m market value.
- Card 3: 2/0.10 = 20m; sell 80m.
- Card 4 and 25: 80bp specialness; 6,575 over 30 days; 80,000 per year.
- Card 6: repo price 99,998,611; 1,389 per day; 13,889 for 10 days.
- Card 7: 0.275 per 100 over 90 days.
- Card 16 and 43: 4.00% Act/360 = 4.056% Act/365 (about 4.06%).
- Card 17: forward about 4.286% (about 4.29%).
- Card 18: forward dirty price 100.49.
- Card 19: carry 125,000.
- Card 22: breakeven TRS spread 17.7bp (14.73 + 3.0).
- Card 23: DV01 10,000 per bp per year on 100m.
- Card 24 and 33: 12,575 lending spread revenue.
- Card 27: extra turn cost 205,479; daily carry 13,699; about 15 days.
- Card 29: 2% carry 1.08m, ROE 54%; 10% carry 0.28m, ROE 14%.
- Card 30: 500,000 per year; 41,096 over 30 days.
- Card 39: LCR haircuts 0% (L1) and 15% (L2A), Basel LCR.
- Card 40: 140% of customer debit balances (Rule 15c3-3), confirmed.
- Card 42: 102% domestic and 105% non-domestic margins are the market convention (checked against several lender policies).
- Card 44: reformed SONIA = trimmed mean of unsecured sterling transactions, BoE.
- Card 38: ON RRP at the bottom, SRF at the top of the target range.

## Unverified items (kept, flagged in text)

1. ILTR launch date (card 11). Search shows an ILTR format from 2014 and an earlier one from 2010. The spec's "launched 2022" claim is not supported.
2. CTRF launch date (card 11). Sources conflict: a 2014 BoE notice and a 2020 Covid-era description.
3. Standing Lending Facility penal rate level (card 11). Card says only "penal rate above Bank Rate"; the exact spread not checked.
4. Intraday SOFR peak about 10% on 17 Sep 2019 (card 13). Reported in several sources but not a primary figure.
5. NSFR 0% transitional treatment in the EU and whether the UK, US, Japan and Switzerland made it permanent (card 36). Sources conflict; current national text not checked.
6. TMPG fails-charge text: the 3% cap and formula were checked against the 2009 and 2016 releases. The 2018 trading practice revision was not read in full, so the current reference rate definition is unverified (card 5 and 32).
7. Card 9 (floor system): the statement that the anchor is the reserve remuneration rate rather than Bank Rate was not checked against the current BoE technical rate.
8. Card 2 (CCP names): LCH RepoClear and FICC are named as approximate; not checked against current clearing lists.
9. Card 8 (reformed SONIA): the publication timing (9:00 next business day) and the 2018 start date were confirmed; the observation-period detail was not checked against the key features document in full.
10. Card 12 (SOFR): transaction base and publication timing from memory, not re-checked against NY Fed methodology.
11. Card 15 (SEC): SEC rule adoption date and sponsored-repo description not re-checked; only the compliance dates were confirmed.
12. Card 23 and 26 (repo-spread sensitivities): modelling simplifications, not market data.
