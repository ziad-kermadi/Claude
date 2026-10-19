import json
M='cards/09_scenarios_markets_reg.json'; D='cards/09_scenarios_markets_reg_deep.json'
m=json.load(open(M,encoding='utf-8')); d=json.load(open(D,encoding='utf-8'))
def rep(card,field,old,new):
    assert old in card[field], (field, old[:60])
    card[field]=card[field].replace(old,new,1)
# ---- main file
rep(m[4],'back',"Why is CS01 for a protection buyer negative? Because the buyer's MTM rises when spreads widen, so under the convention where CS01 is the change in MTM for +1bp, the buyer's sensitivity is negative. Its JTD is the opposite sign of a long-bond position's.",
 "Why is a protection buyer's spread sensitivity positive? Its MTM rises when spreads widen, so the change in MTM for +1bp of spread is positive, the opposite sign to a long bond's spread DV01. Its JTD is also the opposite sign of a long-bond position's.")
rep(m[13],'back',"the old CTD had the lowest implied repo (its basis was cheapest)","the old CTD had the highest implied repo rate (its net basis was cheapest)")
rep(m[12],'back',"ended mid-October 2022) and paused its planned active gilt sales. Dates approximate.","ended 14 October 2022) and postponed its planned active gilt sales (resumed 1 November 2022). Dates verified against BoE statements.")
rep(m[32],'back',"rating-based weights increase steeply from AAA (well under 1%) to CCC (over 50%, approx.), with default at 100%.","rating-based weights increase steeply from AAA (0.5%) through BB (15%) and B (30%) to CCC (50%), with default at 100%.")
rep(m[34],'back',"Expected shortfall at 97.5% on a 10-day base is calibrated to match the tail of 99% VaR in normal data while being more coherent.",
 "Expected shortfall at 97.5% is chosen so that, for normal data, it roughly matches the tail of 99% VaR (approx.), while being coherent.")
rep(m[34],'back',"Why is ES not coherent under all definitions? ES is coherent (subadditive). The issue in FRTB is the use of the stressed period and the backtesting regime, plus the P&L attribution requirement.","Is ES coherent? Yes, it is subadditive, unlike VaR. The stressed-period calibration, the backtesting regime and PLA are separate design decisions in FRTB, not consequences of the risk measure.")
rep(m[35],'back',"roughly 24 real price observations over 12 months, with no more than 4 in any single month (approx.).","at least 24 real price observations over 12 months (confirmed by Risk.net and Clarus), with no more than 4 in any single month (cap unverified).")
rep(m[36],'back',"Failing it means the desk falls back to the standardised approach for that desk.",
 "Traffic light (worst of the two tests): red (Spearman below about 0.7, or KS above about 0.12) means the desk falls back to the standardised approach. Amber (in between) keeps IMA but adds a capital surcharge until remediated. Return to green needs the statistics to pass and 12 months of backtesting.")
rep(m[36],'back',"Statistics (approx. thresholds):","Statistics (approx. thresholds; secondary sources, MAR32 not retrieved):")
rep(m[40],'back',"Check the current rule text before quoting exact figures in a live discussion.",
 "Check the current rule text before quoting exact figures in a live discussion. The EUR 8bn phase-6 scope (Sept 2022) and EUR 50m IM threshold are confirmed by secondary sources; the EUR 500k minimum transfer amount is unverified (approx.).")
rep(m[42],'back',"The timetable has been moved; check the latest PRA publication before quoting dates. The planned start is approximately 2027.",
 "PRA policy statement PS1/26 (Jan 2026) sets 1 January 2027 for Basel 3.1, with the FRTB internal model approach moved to 1 January 2028 (per A&O Shearman summary). The output floor phase-in schedule for the UK is unverified; 72.5% is the Basel standard level.")
rep(m[45],'back',"(USD 3-month LIBOR fallback spread about 26bp, approx.)","(USD 3-month LIBOR fallback spread 26.161bp, per secondary sources)")
rep(m[46],'back',"Verify each against the current rulebook before use.",
 "Verify each against the current rulebook before use. The MiFIR review (Regulation (EU) 2024/791, in force 28 March 2024) is still being implemented through delegated acts, and the derivatives transparency regime was under ESMA consultation in 2025; its final thresholds and DTO scope are unverified here.")
rep(m[47],'back',"11 October 2027 (approx.; check the latest announcements)","11 October 2027 (confirmed by UK Treasury draft legislation and the EU Commission proposal; statutory finality not checked)")
rep(m[49],'back',"Amber and red bands sit below these values. Desks that fall into red for a risk-theoretical P&L test lose IMA eligibility for that desk.",
 "Amber sits between the green and red bands (Spearman 0.7 to 0.8; KS 0.09 to 0.12). Red (Spearman below 0.7 or KS above 0.12) loses IMA eligibility for that desk; amber keeps IMA with a capital surcharge.")
# ---- deep file
rep(d[4],'back',d[4]['back'][d[4]['back'].index('<ul>'):], "<ul><li><b>Edge at trade:</b> +1bp (bought at 4.21% vs 4.20% mid), which is \\(+\\pounds 40\\text{k}\\).</li><li><b>5-minute markout, unhedged:</b> mid 4.20% to 4.22% is +2bp against a long, so \\(-2\\text{bp} = -\\pounds 80\\text{k}\\). Net after markout: 1 - 2 = -1bp, or -\\pounds 40k.</li><li><b>5-minute markout, hedged:</b> the short futures offset the parallel move, so the hedged markout is near zero. The hedged P&amp;L still shows the edge less basis and latency.</li><li><b>30-minute markout, unhedged:</b> mid 4.20% to 4.23% is +3bp, so \\(-3\\text{bp} = -\\pounds 120\\text{k}\\). Net after markout: 1 - 3 = -2bp, or -\\pounds 80k.</li></ul>Reading: the edge is gone within 5 minutes and negative by 30 minutes. This is the signature of informed flow, so tighten the client's quote or cut the size. Use the unhedged markout to judge information and the hedged markout to judge execution quality.<br><br><b>Interviewer follow-up:</b> How do you separate hedging latency from information? Compare markouts at sub-second and few-second horizons (latency) with 5- to 30-minute horizons (information). Latency shows up early and decays; information builds over time.")
rep(d[4],'back',"a markout is the change in the mid after the trade, signed from the dealer's position. The dealer is long, so a rise in yield is a loss.","a markout is the change in the mid after the trade (from the 4.20% trade mid), signed from the dealer's position. The dealer is long, so a rise in yield is a loss.")
rep(d[6],'back',"Answer:</b> the correlation scenarios are (verify exact wording in the MAR21 text before use):","Answer:</b> the correlation scenarios are (MAR21.6; the 1.25 and 0.75 multipliers are confirmed by secondary FRTB docs, the max/min forms are from memory and unverified against the BCBS text):")
rep(d[8],'front',"the Spearman correlation falls below the green threshold of about 0.8.","the Spearman correlation falls to 0.65, below the red threshold of about 0.7.")
rep(d[8],'back',"the desk loses IMA eligibility for capital and reverts to the standardised approach (SA) for that desk until it passes the test again.","the desk loses IMA eligibility for capital and reverts to the standardised approach (SA) for that desk until it passes the test again. A Spearman between 0.7 and 0.8 would instead be amber: IMA kept with a capital surcharge.")
rep(d[19],'back',"\\(\\delta = +1\\) for a long position","\\(\\delta = -1\\) for a receiver (short-rate) trade (sign convention to verify; the single-trade add-on uses the absolute value, so the numbers below are unchanged)")
rep(d[21],'back',"<td><b>109,684</b></td>","<td><b>109,683</b></td>")
rep(d[21],'back',"<td><b>3,316</b></td>","<td><b>3,317</b></td>")
for name,obj in ((M,m),(D,d)):
    json.dump(obj,open(name,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('ok', len(m), len(d))
