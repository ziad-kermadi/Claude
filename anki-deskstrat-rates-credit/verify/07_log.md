# 07 converts and loans: verification log

Files: `cards/07_converts_loans.json` (36 cards), `cards/07_converts_loans_deep.json` (30 cards). All 66 cards checked. Card counts and types unchanged. Both files validated as JSON.

## Cards changed

| File | Index | What was wrong | Fix | Source or method |
|---|---|---|---|---|
| 07_converts_loans.json | 8 | Soft-call window said "20 of the last 30 trading days". The standard convention is 20 of 30 consecutive trading days. | Front now reads "20 of 30 consecutive trading days (a typical US convention)". | LG Display 6-K filings (sec.gov) and XBRL soft-call tags: 130% trigger, 20 of 30 consecutive trading days |
| 07_converts_loans.json | 21 | Said the 1.5-point premium over par is "earned" over the short period. The holder pays 101.5 and is repaid 101 at the soft call, so the loss is 0.5 point. | Rewritten: 0.5-point loss over six months makes yield-to-soft-call the lowest yield. | Recomputed (arithmetic and logic) |
| 07_converts_loans.json | 23 | LMA T+10 standard settlement not confirmed. | Tagged "(approx.; unverified, ...)". LSTA T+7 kept. | LSTA source confirms delayed compensation starts at T+7. LMA T+10 not confirmed by any source found. |
| 07_converts_loans.json | 28 | Moody's WARF factors not confirmed against a primary source. Arithmetic checked: 2,748 to 2,448, fall of 300. | Front tagged "unverified against Moody's CLO methodology". | Search gave no primary table. Values match my recollection of Moody's table, not confirmed. |
| 07_converts_loans.json | 32 | Serta date given only as "Dec 2024". | Changed to "31 Dec 2024". | Fifth Circuit decision dated 31 Dec 2024 (Mondaq, Proskauer, Chapman summaries) |
| 07_converts_loans.json | 34 | Part 26A sanction conditions misstated. "Required majority" was vague, and "at least one class in the money" is not statutory wording. | Rewritten with Condition A (no dissenting member worse off than the relevant alternative) and Condition B (75% in value of a class that would receive payment or has a genuine economic interest under the relevant alternative). | legislation.gov.uk, Companies Act 2006 ss.901F and 901G |
| 07_converts_loans_deep.json | 3 | Sept 2008 short-sale episode cited without a date or scope. GM and Ford episode lacked detail. | Added SEC emergency order of 19 Sept 2008 banning short sales of 799 financial companies. Convert-specific effect of the GM/Ford downgrade tagged approx. | SEC order 19 Sep 2008 (Harvard Law forum, Akin Gump, Kirkland alerts). GM/Ford downgrade May 2005 (IMD case study, Las Vegas Sun, Risk.net). |
| 07_converts_loans_deep.json | 21 | Fulcrum recovery at EV 800 wrong. Senior unsecured (250) and general unsecured (50) rank pari passu, so the pool is 300, not 250. | 20/300 = 6.7%, not 8%. | Recomputed: 800 - 780 = 20; 20/300 = 6.67% |
| 07_converts_loans_deep.json | 23 | Haircut said to "lose 60%" of defaulted principal at 60% recovery. Should be 40% loss. The card's own answer (CDR about 3.0%) and sanity check use 40% loss. | Changed to "lose 40% of the defaulted principal (60% recovery)". Breakeven CDR 3.0% confirmed. | Recomputed in python: breakeven CDR = 2.997% |

## Recomputed and confirmed (no change)

- Card 0 and 1 (conversion price, parity, premium, payback 13.9 years).
- Card 19 and 20 and deep 15 and 19: flat-forward discount margin 387.75bp; floor-binding DM 415.74bp. Confirmed with python.
- Deep 12: TF delta. d1 = 0.433, N(d1) = 0.6675, delta 8.34 shares.
- Deep 13: floor price 951.37, Dm 4.62, dP/ds -0.44 per bp.
- Deep 14: zero-coupon risky price 752.74 vs risk-free 860.71; exact cc spread 268bp (triangle 300bp).
- Deep 16: gamma P&L variance and SD 1,140 (11.4 per bond).
- Deep 24: YTP 6.39% and YTM 3.79%. Confirmed with python.
- Deep 7: base IRR 13.0%; stressed IRR 3.94%.
- Deep 18: case-study P&L (+200 net, bond +33, rebalance to 875).
- Deep 20: CCC haircut; OC 118.3%; cure 5.63.
- Card 11 and deep 1: gamma P&L 9.84 per bond per year and 5,600 for the 100-bond book.
- Card 26 and 27 and 28 and 29 and 30 and 31: CLO and TRS arithmetic.
- Card 22: CAS 26.161bp, added to compounded SOFR, fixed at cessation. Confirmed by secondary source (ISDA fallback table).
- Card 23 (LSTA T+7 delayed compensation start): confirmed.
- Card 30 (EU/US CLO risk retention 5%): confirmed.
- Card 10 (AT1 CoCo triggers 5.125% and 7% CET1): confirmed.
- Card 32 (Serta uptier, not an open market purchase): confirmed.
- Card 35 and deep 21 waterfall: recoveries confirmed.
- Deep 22 (mandatory convertible payoff and decomposition): confirmed.
- Deep 23 breakeven CDR (about 3.0%): confirmed in python with a stated model (quarterly-free annual model, 40% loss, 6.5 base residual).

## Unverified items (kept, tagged or flagged)

1. Moody's WARF factors (B2 2720, Ba3 1766, Caa1 4770), card 28: no primary source retrieved. Tagged.
2. LMA T+10 standard settlement, card 23: no source retrieved. Tagged.
3. Convertible-arb unwind size in May 2005 (GM/Ford), deep 3: sources do not quantify it. Tagged approx.
4. Ayache-Forsyth-Vetzal attribution: not present in either card file. Nothing to fix. The user should confirm whether it belongs in another card or was intended.
5. ISDA CAS 26.161bp, card 22: confirmed only via secondary source (educational page, MathWorks). Primary ISDA document not retrieved.
6. Soft-call convention: confirmed from issuer filings, not from a market standard document.
7. Ranking of CB sensitivities (card 3, credit > rates > vol > delta) is qualitative. Not checked numerically.
8. Deep 23 breakeven CDR depends on the model convention chosen (annual periods, interest on start-of-year performing par, 40% loss). Results are model-dependent.
9. Card 10 "approx." on CoCo levels: Credit Suisse used 7%. Not all AT1s use 7% and 5.125% is common. Left as is.
