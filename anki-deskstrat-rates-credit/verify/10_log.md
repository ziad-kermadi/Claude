# Verification log: cards/10_xva_funding.json

Checked: 45 cards. Fixed: 4 cards (7, 10, 29, plus tag-only edits on 32 and 33). Card count unchanged (45).

## Changes

| Index | File | What was wrong | Fix | Source or method |
|---|---|---|---|---|
| 7 | cards/10_xva_funding.json | Regulatory MPoR floor stated as "extended to about 20 business days ... for disputes". Disputes do not set a flat 20. | Floor is 10 business days; 20 for large (>5,000 trades, approx.) or illiquid / hard-to-replace OTC netting sets; repeated disputes (more than two over the preceding two quarters lasting longer than the MPoR) require at least double the applicable floor for the next two quarters. | Web search summary of Basel IMM MPoR rules (BCBS framework CRE chapters; search result text, not read in full). Repeat-dispute rule and 5,000-trade threshold: the 5,000 figure is from memory and marked approx. Check against the CRE text. |
| 10 | cards/10_xva_funding.json | FCA = -0.01 x 1.5 x 4.6431 = -0.069646, printed as -0.0697 (rounding error). | -0.0696. Net FVA -0.0557, FBA 0.0139 and symmetric -0.0464 unchanged. | Recomputed in python3. |
| 29 | cards/10_xva_funding.json | Cloze said the 20-day MPoR applies to disputes. Same error as card 7. | Cloze now: 10 business days; c2 = 20 business days for large or illiquid netting sets; c3 = at least double the applicable floor after repeated disputes. | Same as card 7. |
| 32 | cards/10_xva_funding.json | Claim that most large dealers adopted FVA in the early 2010s not sourced. | Tagged "(approx.; unverified)". No new figure added. | Not verified. |
| 33 | cards/10_xva_funding.json | Claim that SA-CVA requires supervisory approval not confirmed by search. | Tagged "(approx.; unverified)". | Search did not confirm; BCBS CRE 60 (CVA chapter) and d507 are the places to check. |

## Verified without change (numbers recomputed in python3)

- Cards 2, 4, 6, 10, 17, 20, 23, 24, 25, 40, 43, 44: all worked numbers reproduce the card values, apart from the card 10 rounding fixed above. Card 43 ratio 0.525 matches the hand calculation.
- Card 0 to 3 (CVA/DVA closeout chain), 8 to 9 (FVA), 22 (Burgard-Kjaer PDE sign convention): formulas checked for consistency. For the PDE, the V_C, V_B and funding-term signs were checked against the card's own steps and the standard Feynman-Kac form (zero-coupon bond test).
- Card 23 Brownian bridge: derivation and e^-2 check correct.
- Card 27 and cloze 39: EEPE, running-maximum effective EE and alpha = 1.4 are the standard Basel IMM conventions. Not separately checked against the CRE text.

## Unverified items (kept, not changed unless noted)

1. Hull-White (2012) and Burgard-Kjaer (2011) positions on FVA (card 11, card 22 "where it breaks"). Described at a high level; not checked against the papers.
2. Card 13: MVA "comparable to or larger than CVA for long-dated trades" (approx. already in card).
3. Card 26: AAD cost multiple "a few times" forward cost (approx. already in card).
4. Card 28: subadditivity of PFE for elliptical exposures (true for VaR with alpha >= 0.5; not checked against a source).
5. Card 32: JPMorgan 2014 FVA charge (~$1.5bn) is a known item but does not appear in any card, so it was not added.
6. Card 33: SA-CVA supervisory approval (tagged).
7. Card 7 and cloze 29: 5,000-trade threshold for the 20-day floor (approx.; from memory).
8. Card 30: GBP CSA rate = SONIA (approx.; standard market convention).
9. Card 13 "SIMM" and card 14 regression approach: conventions, not factual figures; not checked.
