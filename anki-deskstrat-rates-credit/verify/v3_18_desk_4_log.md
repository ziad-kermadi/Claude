# Verification log: 18_desk_4.json and 18_desk_5.json

Cards checked: 60 (30 + 30). Cards changed: 11. Numbers recomputed in python3 unless a source is given.

| File | Card index | Issue | Fix | Source or "recomputed" |
|---|---|---|---|---|
| 18_desk_4.json | 1 (RFQ_WIN 2/4) | Winner's-curse maths used the 4-dealer maximum (1.029σ, 0.51bp, 25% win rate) although the RFQ has five dealers including us. | Five-dealer maximum: E[max of 5] ≈ 1.163σ = 0.58bp; win frequency 20%. Monte Carlo (400k draws): 1.160σ, 20.1%. | recomputed |
| 18_desk_4.json | 2 (RFQ_WIN 3/4) | P&L chain built on the old 0.51bp curse. | Net edge 0.42bp; gross £16.7k per win; £11.7k after £5k hedge; week ≈ £1.76m (0.29bp per unit DV01 traded). Tightening to 0.5bp gives −0.08bp, about −£3.3k per win before hedging. | recomputed |
| 18_desk_4.json | 4 (hit-curve derivation) | Follow-up claimed a larger s raises the optimal hit ratio. It lowers it. | Added the check: s = 0.3 gives h* = 1.33, p* = 0.638; s = 0.4 gives h* = 1.41, p* = 0.558. Text now says "lowers the optimal hit ratio and widens the optimal spread". | recomputed (grid search) |
| 18_desk_4.json | 9 (MARK 2/3) | "Tier C keeps the most per unit of spread" is wrong. Tier A keeps 70% of its spread, tier C 67%; C has the largest absolute realised spread (0.8bp). | Rewrote the sentence with both measures. | recomputed |
| 18_desk_4.json | 16 (07:15 scenario) | Short gilt position was described as hurt by a move up in yield. A short DV01 gains when yields rise, so the implied +2bp move is a gain of about £800k. Hedge reasoning was reversed. | Step 5 and follow-up rewritten: do not hedge a gain unless at the limit or the release could reverse the move. | recomputed (sign of DV01) |
| 18_desk_5.json | 6 (DEFAULT 3/4) | "Long the bonds and short CDS" is ambiguous and reads as a doubled credit position, not a hedge. | Changed to "long protection (you have bought CDS)". | n/a (wording) |
| 18_desk_5.json | 7 (DEFAULT 4/4) | Purchase price of 28 is outside the 22 bid / 26 offer market on the card. | Bought at the 26 offer: (35/26)^(1/2) − 1 = 16.0% p.a. (was 11.8% at 28). Exit cost £200k unchanged. | recomputed |
| 18_desk_5.json | 9 (ETF case study) | "0.4 cents per 100 of value" is wrong by a factor of 10. A 0.40% premium is 0.40 points per 100, or 40p per £100. | Corrected. | recomputed |
| 18_desk_5.json | 21 (FUNDING 1/3) | Annual carry £3.6m is on a 360-day basis. Over a 365-day year it is £3.65m. | Stated both bases. | recomputed |
| 18_desk_5.json | 23 (FUNDING 3/3) | The question "what would the desk pay to keep the special" was not answered. | Added: 9 extra special days are worth 10m × 0.80% × 9/360 = £2,000, the most the desk would pay. | recomputed |
| 18_desk_5.json | 24 (credit P&L explain) | Sign error. Selling protection is long spread risk and gains when spreads widen, so a 3bp widening on £90k/bp is +£270k, not −£270k. The stated actual P&L of −£450k did not reconcile to the stated £180k residual. | Actual P&L set to +£90k. Explain +£270k, residual 90 − 270 = −£180k, which matches the card's residual. | recomputed |

Checked, no change needed:
- 18_desk_4: cards 0, 3, 5, 6, 7, 8, 10–15, 17–29. The gilt, futures (CTD DV01 £94.1, 1,764 contracts), tick and cloze numbers were recomputed and agree.
- 18_desk_5: cards 0–5, 8, 10–20, 22, 25–29. Index hedge £80m and beta-0.8 hedge £64m, the NIC figures, the TRACE caps, and the ETF breakeven 0.181% were recomputed and agree.
- Source checks: the TRACE 15-minute reporting window and the dissemination caps (5MM+ for IG above $5m, 1MM+ for non-IG above $1m) match FINRA's TRACE reporting-timeframes page. The Long Gilt tick of 0.01 (£10 per contract) matches third-party contract profiles.

HTML and format checks: JSON valid; 30 cards per file; each card has exactly one lvl_* tag and 2 to 7 tags; no bare "<" or "&"; no markdown; MathJax uses \( \) and \[ \].

## Unverified or still doubtful

- 18_desk_4 card 23 (UK/EU trading obligation): the scope principle is stated correctly, but the current UK class list was not checked against the FCA source. The card already says to check it with compliance.
- 18_desk_4 card 16: "stale marks are the commonest source of morning P&L surprises" is a practitioner claim, not sourced.
- 18_desk_4 card 22 (last look): regulatory detail is kept generic on purpose; no specific rule text was checked.
- 18_desk_5 cards 16 and 20: FINRA caps and window verified. A block-dissemination pilot is mentioned as "to be checked" and was not verified either way. The card already flags this.
- 18_desk_5 card 4: "a bankruptcy filing is a credit event, decided by the Determinations Committee" follows the ISDA 2014 framework as I understand it. The primary ISDA text was not fetched.
- 18_desk_5 card 9: the premium and costs are illustrative inputs, not market data.
- 18_desk_5 card 26: "open interest shows net buying or selling pressure" is a simplification of the auction imbalance.
- The Long Gilt tick of £10 rests on third-party contract profiles, not the ICE specification.

**Orchestrator correction (Opus review):** the verifier's change to 18_desk_5 card 24 was itself wrong — a protection seller is long credit and *loses* when spreads widen. Restored: explain −£270k, actual −£450k, residual −£180k.
