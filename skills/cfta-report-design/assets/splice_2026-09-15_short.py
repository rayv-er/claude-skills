#!/usr/bin/env python3
"""Condensed September 2026 edition (Brett 9/9: "too much writing and details"). Same data as splice_2026-09-15.py, each
section cut to its tables, a KPI row, and one line of reading. Writes build_report.py; the long edition is kept as
finance_report_v2_full_2026-09-15.html."""
import re
exec(open("splice_2026-09-15.py").read().split("# ------------------------------------------------------------------ 2. cover")[0])   # SRC, cut, esc, DATA block applied -> NEW
# cover
NEW = NEW.replace('FY2026 Year-to-Date &middot; 08.17.2026', 'FY2026 Year-to-Date &middot; 09.15.2026')
NEW = NEW.replace('Reporting Period &middot; November 1, 2025 &ndash; July 31, 2026 &middot; Accrual Basis', 'Reporting Period &middot; November 1, 2025 &ndash; August 31, 2026 &middot; Accrual Basis')
NEW = NEW.replace('<span>$2.85M revenue &middot; +4% vs budget</span>', '<span>$3.03M revenue &middot; on budget &middot; ten months</span>')
NEW = NEW.replace('"<span>FY2026 Year-to-Date &middot; 08.17.2026</span></div>")', '"<span>FY2026 Year-to-Date &middot; 09.15.2026</span></div>")')
NEW = NEW.replace('<td class="n">Jul 31, 2026</td><td class="n">Jul 31, 2025</td>', '<td class="n">Aug 31, 2026</td><td class="n">Aug 31, 2025</td>')
NEW = NEW.replace('Statement of Financial Position — July 31', 'Statement of Financial Position — August 31')

def k(v):
    s = f"{abs(v):,.0f}"; return f"(${s})" if v < 0 else f"${s}"

AGENDA = '''<div class="sechead"><div><div class="eb">Finance Committee</div><div class="tt">Agenda &amp; Minutes</div></div><div class="bn"></div></div>
<h3>Agenda &mdash; September 21, 2026 &middot; 9:00 am MT &middot; Zoom</h3>
<div style="border:1px solid #d5e0f0; border-radius:6px; background:#fff; padding:6px 12px; margin:4px 0 10px; font-size:9.5px;">
<ol style="margin:4px 0 4px 16px; padding:0;">
<li><b>Welcome</b> &mdash; Dave Ebner: approval of agenda; approval of June and July minutes (carried from August, when the report went out by email in place of a meeting)</li>
<li><b>Financial report</b> through August 31, including revisions to prior months from the year-end clean-up; year-end projection and cash; FY27 draft budget, first pass; FY25 audit status</li>
<li><b>Other updates</b> &mdash; Fidelity account funded by two stock gifts; new Front Row pledge; bar inventory count</li>
<li><b>Fundraising</b> &mdash; fall appeal and Front Row pipeline</li>
<li><b>Other business</b> &mdash; investment policy; Wine + Food expansion ad hoc committee</li>
<li><b>Executive session</b> &middot; <b>Adjournment</b></li>
</ol></div>
<h3>Draft Minutes &mdash; June 15, 2026</h3>
<p class="note"><b>Attendees:</b> Dave, Drew, Margery, Brett; Jillian late. Absent: Bill B, Bill P, Scott, Julie. Called to order 9:07 am, quorum of four. May minutes and the agenda approved.</p>
<p class="note"><b>String Cheese Incident:</b> the biggest performance to date, streamed worldwide, estimated net $25&ndash;30k; the band interested in a three-night return. <b>Financials:</b> ahead of budget and prior year; Alpenglow underwriting &asymp;$170k against $150k; cash $600k+ through the slow season; Front Row behind pace. <b>Staffing:</b> Julia Brazell hired as executive assistant (July 6). <b>Grants:</b> MetRec &asymp;$40k awarded; NEA application in progress. <b>Building:</b> BOZAR capacity approval secured; building-ownership conversation with the Town this fall. <b>Systems:</b> payroll moving to Gusto. Adjourned by motion.</p>
<h3>Draft Minutes &mdash; July 20, 2026</h3>
<p class="note"><b>Attendees:</b> Dave, Scott, Drew, Bill B, Margery (left early), Jillian, Brett; Julie remote. Absent: Bill P. 9:05 to 10:07 am. Minutes deferred to the next meeting.</p>
<p class="note"><b>Financials:</b> new report format debuted; figures through June 30; contributed ahead on early gifts, payroll under on vacancies, programming over on String Cheese; $100k of debt paid down; Front Row completions the main risk. Requests: &plusmn; instead of tilde, larger text, a true cash-flow view, revenue-by-stream margins. <b>Arts Ball:</b> record year over $900k. <b>Wine + Food:</b> effectively sold out, projected at or above budget. <b>Motion by Bill B, seconded by Drew, to open the Fidelity brokerage and interest-bearing accounts; approved unanimously.</b> Sweep renegotiated to &asymp;3.05%. <b>Investment policy</b> draft to governance, then the board. Drew to circulate festival-expansion ideas.</p>
<div class="pb"></div>
'''
NEW = cut(NEW, '<div class="sechead"><div><div class="eb">Finance Committee</div><div class="tt">Agenda', '<div class="sechead"><div><div class="eb">Section 1.0</div>', esc(AGENDA))

EXEC = '''<div class="sechead"><div><div class="eb">Section 1.0</div><div class="tt">Executive Summary</div></div><div class="bn">1.</div></div>
<div class="lede">Net revenue of <b>$223,676</b> for ten months. Revenue of <b>$3.03M</b> is on budget and $244,247 ahead of last year; expenditures of <b>$2.54M</b> are $131,854 (+5.5%) over budget, led by programming, alcohol cost and insurance. Operating income of <b>$283,208</b> is $181,277 behind plan. Since the August report the year-end clean-up restated November through July: net revenue through July now reads <b>$313,916</b>, not $445,117.</div>
<div class="kpis">
<div class="kpi"><div class="k">Revenue YTD</div><div class="val">$3.03M</div><div class="d">+0.3% vs budget &middot; +8.8% YoY</div></div>
<div class="kpi"><div class="k">Operating Income</div><div class="val">$283k</div><div class="d">&minus;39% vs budget</div></div>
<div class="kpi"><div class="k">Net Revenue</div><div class="val">$224k</div><div class="d">($176,899) vs budget</div></div>
<div class="kpi"><div class="k">Cash &amp; Equivalents</div><div class="val">$606k</div><div class="d">incl. $149k Fidelity brokerage</div></div>
</div>
<div class="half">
<div>
<h3>Revisions Since the August 17 Report (Nov&ndash;Jul)</h3>
<div class="compact"><table>
<tr class="hd"><td>Line</td><td class="n">Change</td><td class="lbl2">Driver</td></tr>
<tr><td class="lbl">Cost of sales</td><td class="n">($40,949)</td><td class="lbl2">Alcohol re-based to the 8/31 count</td></tr>
<tr><td class="lbl">Building</td><td class="n">($39,648)</td><td class="lbl2">Insurance and building bills to their months</td></tr>
<tr><td class="lbl">Programming</td><td class="n">($39,989)</td><td class="lbl2">Festival wine out of inventory; event staffing by shift</td></tr>
<tr><td class="lbl">Earned revenue</td><td class="n">($35,268)</td><td class="lbl2">Bar sales net of tax; rental deferrals corrected</td></tr>
<tr><td class="lbl">Contributed revenue</td><td class="n">($18,540)</td><td class="lbl2">Chargebacks and gala recodes</td></tr>
<tr><td class="lbl">Other expense (in-kind netted)</td><td class="n">$36,021</td><td class="lbl2">In-kind entries netted down</td></tr>
<tr><td class="lbl">Other lines</td><td class="n">$7,173</td><td class="lbl2"></td></tr>
<tr class="b"><td class="lbl">Net revenue through July</td><td class="n">($131,200)</td><td class="lbl2">$445,117 &rarr; $313,916</td></tr>
</table></div>
</div>
<div>
<h3>vs. Budget and Prior Year</h3>
<div><b style="color:#0A3A82">Favorable</b><ul>
<li>Contributed revenue <b>+$61,330</b>: grants at 2.5x plan, unrestricted gifts ahead.</li>
<li>Ticket and program income <b>+$115,854</b> on the strongest season on record.</li>
<li>Payroll and administrative on budget.</li></ul></div>
<div><b style="color:#A7182F">Unfavorable</b><ul>
<li>Programming <b>+$85,863</b>; cost of sales <b>+$59,111</b> (alcohol now 38% of bar revenue); building <b>+$41,141</b> (insurance).</li>
<li>Front Row <b>$260k vs $300k</b> phased; bar, hosted bar and rentals <b>$77k behind</b> combined.</li>
<li>vs. FY25: revenue +$244k, expense +$321k; Front Row $130k lower; last year's other income carried a one-time $110,534 adjustment.</li></ul></div>
</div>
</div>
<h3>Cash, Balance Sheet, Updates</h3><ul>
<li>Cash <b>$605,746</b> ($51,886 below last year): operating and sweep $442,140, Fidelity $149,249, bar banks and clearing $14,357. <b>$149,138</b> collected and deferred for fall events. Front Row receivable <b>$1.35M</b>; debt <b>$1.05M</b>, down $100k.</li>
<li><b>Fidelity funded:</b> Valentine/Bolton MSFT $50,750 (Aug 10) and Carol Ann May IWF $99,125 (Aug 20), sold to money market; $816 realized loss.</li>
<li><b>Front Row:</b> Burciaga $100,000 recorded August 26. <b>Bar:</b> physical count August 31 valued alcohol at $32,901; cost of sales rebuilt from it. <b>Audit:</b> Weaver final status at the meeting. <b>Bank reconciliations</b> June to August in progress.</li></ul>
<div class="pb"></div>
'''
NEW = cut(NEW, '<div class="sechead"><div><div class="eb">Section 1.0</div>', '<div class="sechead"><div><div class="eb">Section 2.0</div>', esc(EXEC))

EVENTS = '''<div class="sechead"><div><div class="eb">Section 2.0</div><div class="tt">Summer Signature Events &mdash; Final</div></div><div class="bn">2.</div></div>
<div class="kpis">
<div class="kpi"><div class="k">Combined Raised</div><div class="val">&plusmn;$1.30M</div><div class="d">two signature events</div></div>
<div class="kpi"><div class="k">Arts Ball</div><div class="val">$917k</div><div class="d">+7% vs budget &middot; +13% YoY</div></div>
<div class="kpi"><div class="k">Festival</div><div class="val">$379k</div><div class="d">&minus;6% vs budget and FY25</div></div>
<div class="kpi"><div class="k">2027 Lever</div><div class="val">Sponsorship</div><div class="d">$25k of festival budget never billed</div></div>
</div>
<div class="half">
<div>
<div class="compact"><table>
<tr class="hd"><td>Arts Ball 2026</td><td class="n">Actual</td><td class="n">Budget</td><td class="n">FY25</td></tr>
<tr><td class="lbl">Paddle-raise, auction &amp; gifts</td><td class="n">$777,770</td><td class="n">$762,363</td><td class="n">$729,842</td></tr>
<tr><td class="lbl">Tables &amp; tickets</td><td class="n">$139,422</td><td class="n">$85,000</td><td class="n">$76,818</td></tr>
<tr><td class="lbl">Corporate sponsorship</td><td class="n">$0</td><td class="n">$10,000</td><td class="n">$3,000</td></tr>
<tr class="b"><td class="lbl">Total</td><td class="n">$917,192</td><td class="n">$857,363</td><td class="n">$809,660</td></tr>
</table></div>
</div>
<div>
<div class="compact"><table>
<tr class="hd"><td>Wine + Food 2026</td><td class="n">Actual</td><td class="n">Budget</td><td class="n">FY25</td></tr>
<tr><td class="lbl">Tickets &amp; passes, all channels</td><td class="n">$371,209</td><td class="n">$372,500</td><td class="n">$383,471</td></tr>
<tr><td class="lbl">Vendor fees &amp; sponsorship</td><td class="n">$7,325</td><td class="n">$32,000</td><td class="n">$18,644</td></tr>
<tr class="b"><td class="lbl">Total</td><td class="n">$378,534</td><td class="n">$404,500</td><td class="n">$402,115</td></tr>
</table></div>
</div>
</div>
<p class="note">Both closed. The High Note dinner (Aug 6, $27,900) recognized in August; $15,102 of Ball gifts recoded to Fundraiser Contributions; the ledger now tags $866k of the Ball to Arts Ball records. Two-year Ball trajectory $678k &rarr; $812k &rarr; $917k.</p>
<div class="sechead"><div><div class="eb">Section 3.0</div><div class="tt">Financial Statements</div></div><div class="bn">3.</div></div>
<p class="fine">Accrual basis, ten months, as booked. Prior months revised since August 17 (Section 1.0). Depreciation and the donated lease are booked October 31 in both years, so every bottom line here is before depreciation.</p>
'''
NEW = cut(NEW, '<div class="sechead"><div><div class="eb">Section 2.0</div>', '<div class="stitle">Statement of Activities — Budget vs. Actual', esc(EVENTS))
NEW = NEW.replace('{cfrow("Construction loans, net (FY26: $100k paydown; FY25: $1.0M draw less $950k retirement)","fin")}', '{cfrow("Construction loans, net (FY26: $100k paydown; FY25: $50k net draw)","fin")}')
NEW = NEW.replace('{cfrow("Inventory build &amp; artist advances","inv")}', '{cfrow("Inventory, allowances &amp; other current assets","inv")}')

def cell(v):
    if v == 0: return "&mdash;"
    return f"(${abs(v):,.0f})" if v < 0 else f"${v:,.0f}"
LINEUP = [("<b>The String Cheese Incident (two nights)</b>","Jun 3&ndash;4",151126,17773,-135500,-8129,0),("Kitchen Dwellers (two nights)","Jan 17&ndash;18",35564,13322,-24690,-4488,0),("Alpenphunk Incident (two nights, co-pro)","Jan 31&ndash;Feb 1",43673,11266,-15000,-4396,0),("Hank Azaria + The EZ Street Band","Dec 28",27995,4952,-25742,-2257,0),("Vandelux (Sleds &amp; Kegs)","Mar 7",24265,9711,-12137,-3714,0),("Nutcracker! [Rated CB]","Dec 13",20660,1738,0,-3543,-15859),("Steve Earle, Steddy Theater","Aug 6",16132,2711,-20750,-143,-403),("Beats Antique","Mar 13",14115,4203,-12100,-2655,0),("Ski Patrol (community benefit)","Feb 8",12205,10756,-4000,-6894,-9764),("The Brothers Comatose","Feb 26",10102,2750,-5403,-3826,0),("Bodhi &amp; the Rainforest (three shows)*","Aug 20&ndash;22",9005,846,0,-6651,-352),("Deadhead Ed's End of Season Party","Apr 3",8867,3699,-5000,-2661,0),("Opera Colorado: Pirates of Penzance","Feb 5",6165,745,-600,-753,0),("Mr. Sun Plays Ellington's Nutcracker","Dec 20",5376,955,-3000,-1056,0),("Opera Lollipops*","Aug 1",3883,484,0,-1505,-629)]
lrows = []; T = [0]*6
for n, d, t, pos, fee, st, oth in LINEUP:
    bar = round(pos*0.62); net = t+bar+fee+st+oth; T[0]+=t; T[1]+=bar; T[2]+=fee; T[3]+=st; T[4]+=oth; T[5]+=net
    lrows.append(f'<tr><td class="lbl">{n}</td><td class="n">{d}</td><td class="n">{cell(t)}</td><td class="n">{cell(bar)}</td><td class="n">{cell(fee)}</td><td class="n">{cell(st)}</td><td class="n">{cell(oth)}</td><td class="n">{cell(net)}</td></tr>')
MONTHS = [("Nov",4969,354,7210.78,791.90),("Dec",12900,880,14078.03,2421.73),("Jan",22069,1473,24422.00,4459.37),("Feb",24669,1707,27315.01,4512.81),("Mar",25452,1648,28315.02,5300.09),("Apr",3450,273,3934.03,765.50),("May",5976,433,6070.50,1102.60),("Jun",59713,4749,66409.54,10965.50),("Jul",40468,3041,50989.00,7259.07),("Aug",13435,1863,26277.01,4163.71)]
mrow = lambda i: "".join(f'<td class="n">{m[i]}</td>' for m in MONTHS)
PROG = f'''<div class="pb"></div>
<div class="sechead"><div><div class="eb">Section 4.0</div><div class="tt">Programming &amp; Bar</div></div><div class="bn">4.</div></div>
<div class="kpis">
<div class="kpi"><div class="k">Concert Tickets FY26</div><div class="val">$389k</div><div class="d">16 headline shows &middot; 6,889 attendees</div></div>
<div class="kpi"><div class="k">Lineup Net, Direct</div><div class="val">$70k</div><div class="d">after $29k season hospitality</div></div>
<div class="kpi"><div class="k">Bar Revenue YTD</div><div class="val">$213k</div><div class="d">+ $35k hosted &middot; net of sales tax</div></div>
<div class="kpi"><div class="k">Alcohol Cost</div><div class="val">38%</div><div class="d">of bar revenue, from the 8/31 count</div></div>
</div>
<h3>Per-Event P&amp;L &mdash; Concert Lineup, FY26 Complete</h3>
<div class="compact"><table><tr class="hd"><td>Event</td><td class="n">Date</td><td class="n">Tickets</td><td class="n">Bar (net)</td><td class="n">Perf. fee</td><td class="n">Staffing</td><td class="n">Other</td><td class="n">Est. net</td></tr>
{"".join(lrows)}
<tr class="b"><td class="lbl">Total, event-identifiable costs</td><td class="n"></td><td class="n">{cell(T[0])}</td><td class="n">{cell(T[1])}</td><td class="n">{cell(T[2])}</td><td class="n">{cell(T[3])}</td><td class="n">{cell(T[4])}</td><td class="n">{cell(T[5])}</td></tr>
<tr class="b"><td class="lbl">Net after season hospitality ($28,741)</td><td class="n"></td><td class="n"></td><td class="n"></td><td class="n"></td><td class="n"></td><td class="n"></td><td class="n">{cell(T[5]-28741)}</td></tr></table></div>
<p class="fine">Bar = event-night POS net of alcohol cost at the counted 38% (13% in earlier reports; that alone takes $20k out of the lineup). * Artist settlements not yet booked. On the counted rate the Nov&ndash;Jun concert season nets ($21,554) on direct terms, in line with FY25's ($16,685); revenue grew 39%, pour cost is the fix.</p>
<div class="half">
<div>
<h3>Bar by Month (GL net of tax; Clover POS)</h3>
<div class="compact"><table>
<tr class="hd"><td></td>{"".join(f'<td class="n">{m[0]}</td>' for m in MONTHS)}<td class="n">YTD</td></tr>
<tr><td class="lbl">Revenue</td>{"".join(f'<td class="n">${m[1]//1000}k</td>' for m in MONTHS)}<td class="n">$213k</td></tr>
<tr><td class="lbl">Transactions</td>{"".join(f'<td class="n">{m[2]:,}</td>' for m in MONTHS)}<td class="n">16,421</td></tr>
<tr><td class="lbl">Avg ticket</td>{"".join(f'<td class="n">${m[3]/m[2]:.0f}</td>' for m in MONTHS)}<td class="n">$15.53</td></tr>
</table></div>
<p class="fine">Card tips 16.4% of sales. Alpenglow closed at <b>$99,839 over nine nights vs $99,101 in 2025</b>, flat on a like-for-like basis. NPS season +84 on 73 responses.</p>
</div>
<div>
<h3>Per-Attendee Bar</h3>
<div class="compact"><table>
<tr class="hd"><td>Show type</td><td class="n">$ / attendee</td></tr>
<tr><td class="lbl">Party and jam (Ski Patrol, Alpenphunk, SCI, Vandelux)</td><td class="n">$14&ndash;$19</td></tr>
<tr><td class="lbl">Seated (Azaria, Brothers Comatose, Steve Earle)</td><td class="n">$8&ndash;$9</td></tr>
<tr><td class="lbl">Family (Bodhi, Opera Lollipops)</td><td class="n">$2&ndash;$4</td></tr>
<tr class="b"><td class="lbl">Blended, 14 shows, 6,889 attendees</td><td class="n">$12.10</td></tr>
</table></div>
</div>
</div>
<div class="sechead"><div><div class="eb">Section 5.0</div><div class="tt">Rentals &amp; Forward Book</div></div><div class="bn">5.</div></div>
<div class="kpis">
<div class="kpi"><div class="k">Rental Income YTD</div><div class="val">$115k</div><div class="d">&minus;20% vs budget &middot; &minus;35% YoY</div></div>
<div class="kpi"><div class="k">Deferred for Fall</div><div class="val">$135k</div><div class="d">collected, recognizes at the events</div></div>
<div class="kpi"><div class="k">Signed Sep&ndash;Dec</div><div class="val">$103k</div><div class="d">$80k already collected</div></div>
<div class="kpi"><div class="k">Contracted into FY27</div><div class="val">$97k</div><div class="d">$28k of deposits held</div></div>
</div>
<div class="half">
<div>
<div class="compact"><table>
<tr class="hd"><td>Recognized (QuickBooks)</td><td class="n">FY26 YTD</td><td class="n">Budget</td><td class="n">FY25</td></tr>
<tr><td class="lbl">Facility fees</td><td class="n">$95,464</td><td class="n">$143,900</td><td class="n">$155,889</td></tr>
<tr><td class="lbl">Staffing fees</td><td class="n">$19,393</td><td class="n">n/b</td><td class="n">$19,754</td></tr>
<tr class="b"><td class="lbl">Rental income</td><td class="n">$114,857</td><td class="n">$143,900</td><td class="n">$175,643</td></tr>
<tr><td class="lbl">Hosted bar</td><td class="n">$35,424</td><td class="n">$71,000</td><td class="n">$51,688</td></tr>
<tr class="b"><td class="lbl">Rental-related total</td><td class="n">$150,281</td><td class="n">$214,900</td><td class="n">$227,331</td></tr>
</table></div>
<p class="fine">Top renters: School of Dance $35.6k, McCoy wedding $8.8k, Wild Hare $7.5k, GVH gala $6.0k. The summer months went to the Center's own events; $135k of rental cash is deferred for fall.</p>
</div>
<div>
<div class="compact"><table>
<tr class="hd"><td>Signed, Sep&ndash;Dec 2026</td><td class="n">Date</td><td class="n">Value</td><td class="n">Collected</td></tr>
<tr><td class="lbl">Wedding &mdash; Schreier</td><td class="n">Sep 19</td><td class="n">$33,710</td><td class="n">$33,710</td></tr>
<tr><td class="lbl">Wedding &mdash; Hoffmeister</td><td class="n">Sep 29</td><td class="n">$11,760</td><td class="n">$11,760</td></tr>
<tr><td class="lbl">Wedding &mdash; Steinbach</td><td class="n">Sep 4</td><td class="n">$11,380</td><td class="n">$11,380</td></tr>
<tr><td class="lbl">Gibson welcome party</td><td class="n">Oct 2</td><td class="n">$10,518</td><td class="n">$3,500</td></tr>
<tr><td class="lbl">Petito celebration of life</td><td class="n">Sep 6</td><td class="n">$8,608</td><td class="n">$1,000</td></tr>
<tr><td class="lbl">CB Film Festival</td><td class="n">Sep 24</td><td class="n">$7,672</td><td class="n">$7,672</td></tr>
<tr><td class="lbl">Seven smaller bookings</td><td class="n">Sep&ndash;Dec</td><td class="n">$19,010</td><td class="n">$11,410</td></tr>
<tr class="b"><td class="lbl">Total signed</td><td class="n"></td><td class="n">$102,658</td><td class="n">$80,432</td></tr>
</table></div>
<p class="fine">FY27 contracted: Abele $31,400, Friedman &amp; Abbott $30,850, Lueckemeyer $18,055, Emily &amp; Sam $11,000, four smaller; $97,355 with $27,550 of deposits. &plusmn;$115k of further FY27 proposals active.</p>
</div>
</div>
<div class="pb"></div>
<div class="sechead"><div><div class="eb">Section 6.0</div><div class="tt">Donor Intelligence</div></div><div class="bn">6.</div></div>
<div class="kpis">
<div class="kpi"><div class="k">Donors YTD</div><div class="val">405</div><div class="d">398 last year</div></div>
<div class="kpi"><div class="k">New Donors</div><div class="val">119</div><div class="d">$197,290 first-year giving</div></div>
<div class="kpi"><div class="k">Not Yet Renewed</div><div class="val">225</div><div class="d">&plusmn;$525k prior giving; 18 gave $10k+</div></div>
<div class="kpi"><div class="k">Top-10 Share</div><div class="val">36%</div><div class="d">of CRM cash, vs 31% last year</div></div>
</div>
<div class="compact"><table>
<tr class="hd"><td>Gift band, Nov&ndash;Aug CRM cash</td><td class="n">FY26 donors</td><td class="n">FY26 $</td><td class="n">FY25 donors</td><td class="n">FY25 $</td></tr>
<tr><td class="lbl">$25,000+</td><td class="n">18</td><td class="n">$930,923</td><td class="n">18</td><td class="n">$792,218</td></tr>
<tr><td class="lbl">$10,000 &ndash; $24,999</td><td class="n">42</td><td class="n">$558,261</td><td class="n">42</td><td class="n">$567,426</td></tr>
<tr><td class="lbl">$5,000 &ndash; $9,999</td><td class="n">26</td><td class="n">$152,335</td><td class="n">38</td><td class="n">$229,219</td></tr>
<tr><td class="lbl">$1,000 &ndash; $4,999</td><td class="n">112</td><td class="n">$186,135</td><td class="n">118</td><td class="n">$215,081</td></tr>
<tr><td class="lbl">$250 &ndash; $999</td><td class="n">80</td><td class="n">$35,165</td><td class="n">82</td><td class="n">$39,319</td></tr>
<tr><td class="lbl">Under $250</td><td class="n">127</td><td class="n">$13,077</td><td class="n">100</td><td class="n">$9,386</td></tr>
<tr class="b"><td class="lbl">Total</td><td class="n">405</td><td class="n">$1,875,896</td><td class="n">398</td><td class="n">$1,852,649</td></tr>
</table></div>
<p class="note">Top and bottom grew, the $1k&ndash;$10k middle is soft (138 vs 156 donors) and is the upgrade target. CRM cash is within $49k of the books' contributed revenue plus Front Row, down from a $159k gap last month. The prospect model flags 2,889 Hot or Warm households who have never given; named lists are with Development, not in this report.</p>
'''
NEW = cut(NEW, '<div class="sechead"><div><div class="eb">Section 4.0</div>', '<div class="sechead"><div><div class="eb">Section 8.0</div>', esc(PROG))
# drop the original section 8 (donor) entirely: cut from its sechead to the footer, replacing with sections 7 and 8 (projection, FY27)
SEC = '''<div class="pb"></div>
<div class="sechead"><div><div class="eb">Section 7.0</div><div class="tt">Year-End Projection &amp; Cash</div></div><div class="bn">7.</div></div>
<div class="kpis">
<div class="kpi"><div class="k">FY26 Before Depreciation</div><div class="val">$22,887</div><div class="d">budget $242,426 &middot; FY25 $284,811</div></div>
<div class="kpi"><div class="k">FY26 Full Accrual</div><div class="val">($582,818)</div><div class="d">after $605,705 depreciation and lease</div></div>
<div class="kpi"><div class="k">Cash at October 31</div><div class="val">$496,706</div><div class="d">$605,746 at 8/31 &middot; $455,001 a year ago</div></div>
<div class="kpi"><div class="k">Sept + Oct</div><div class="val">($200,789)</div><div class="d">before depreciation; four payroll runs, 18 fall dates</div></div>
</div>
<div class="compact"><table>
<tr class="hd"><td>Projected year end</td><td class="n">Nov&ndash;Aug actual</td><td class="n">Sept + Oct</td><td class="n">FY26 projected</td><td class="n">FY26 budget</td><td class="n v">vs budget</td><td class="n">FY25</td></tr>
<tr><td class="lbl">Contributed Revenue</td><td class="n">$1,665,362</td><td class="n">$16,718</td><td class="n">$1,682,080</td><td class="n">$1,636,234</td><td class="n v">$45,846</td><td class="n">$1,412,747</td></tr>
<tr><td class="lbl">Earned Revenue</td><td class="n">$1,106,468</td><td class="n">$207,441</td><td class="n">$1,313,909</td><td class="n">$1,208,799</td><td class="n v">$105,110</td><td class="n">$1,141,579</td></tr>
<tr><td class="lbl">Front Row</td><td class="n">$260,000</td><td class="n">$0</td><td class="n">$260,000</td><td class="n">$400,000</td><td class="n v">($140,000)</td><td class="n">$490,000</td></tr>
<tr class="b"><td class="lbl">Total Income</td><td class="n">$3,031,830</td><td class="n">$224,159</td><td class="n">$3,255,989</td><td class="n">$3,245,033</td><td class="n v">$10,956</td><td class="n">$3,044,327</td></tr>
<tr><td class="lbl">Cost of Sales</td><td class="n">$208,031</td><td class="n">$42,238</td><td class="n">$250,269</td><td class="n">$168,660</td><td class="n v">$81,609</td><td class="n">$183,693</td></tr>
<tr><td class="lbl">Administrative, Building, Marketing</td><td class="n">$526,515</td><td class="n">$31,876</td><td class="n">$558,391</td><td class="n">$561,945</td><td class="n v">($3,554)</td><td class="n">$569,417</td></tr>
<tr><td class="lbl">Payroll</td><td class="n">$1,138,348</td><td class="n">$207,013</td><td class="n">$1,345,361</td><td class="n">$1,376,445</td><td class="n v">($31,084)</td><td class="n">$1,286,208</td></tr>
<tr><td class="lbl">Programming</td><td class="n">$875,728</td><td class="n">$89,759</td><td class="n">$965,487</td><td class="n">$818,865</td><td class="n v">$146,622</td><td class="n">$733,359</td></tr>
<tr class="b"><td class="lbl">Operating Surplus/(Deficit)</td><td class="n">$283,208</td><td class="n">($146,727)</td><td class="n">$136,481</td><td class="n">$319,118</td><td class="n v">($182,637)</td><td class="n">$271,650</td></tr>
<tr><td class="lbl">Other revenue less other expense, before depreciation</td><td class="n">($59,532)</td><td class="n">($54,062)</td><td class="n">($113,594)</td><td class="n">($76,692)</td><td class="n v">($36,902)</td><td class="n">$13,161</td></tr>
<tr class="b"><td class="lbl">Net Revenue before Depreciation</td><td class="n">$223,676</td><td class="n">($200,789)</td><td class="n">$22,887</td><td class="n">$242,426</td><td class="n v">($219,539)</td><td class="n">$284,811</td></tr>
<tr><td class="lbl">Depreciation and donated lease (October 31)</td><td class="n">$0</td><td class="n">($605,705)</td><td class="n">($605,705)</td><td class="n">not budgeted</td><td class="n v"></td><td class="n">($605,705)</td></tr>
<tr class="b"><td class="lbl">Change in Net Assets</td><td class="n">$223,676</td><td class="n">($806,494)</td><td class="n">($582,818)</td><td class="n"></td><td class="n v"></td><td class="n">($320,894)</td></tr>
</table></div>
<p class="fine">September and October: bottom-up from the fall calendar, the Event Temple book, the Gusto pay calendar and run rates. In-kind ($195,793 each side) nets to zero in October. <b>Open calls:</b> the $38,211 duplicate Philadelphia Insurance payment is treated as recoverable; a $44,684 year-end adjustments plug stands in for the pledge allowance reset and audit entries; fall event hourly runs $6.5k under the last two Gusto runs; Front Row holds at $260k unless a fall designation lands.</p>
<div class="compact"><table>
<tr class="hd"><td>Bank and brokerage cash at month end</td><td class="n">Nov</td><td class="n">Dec</td><td class="n">Jan</td><td class="n">Feb</td><td class="n">Mar</td><td class="n">Apr</td><td class="n">May</td><td class="n">Jun</td><td class="n">Jul</td><td class="n">Aug</td><td class="n">Sep</td><td class="n">Oct</td></tr>
<tr><td class="lbl">FY26 (Sept and Oct projected)</td><td class="n">$420,380</td><td class="n">$445,831</td><td class="n">$410,323</td><td class="n">$239,943</td><td class="n">$422,606</td><td class="n">$486,289</td><td class="n">$560,833</td><td class="n">$489,972</td><td class="n">$612,778</td><td class="n">$605,746</td><td class="n">$557,101</td><td class="n">$496,706</td></tr>
<tr><td class="lbl">FY27 draft</td><td class="n">$418,779</td><td class="n">$515,226</td><td class="n">$425,077</td><td class="n">$403,475</td><td class="n">$617,085</td><td class="n">$712,742</td><td class="n">$797,659</td><td class="n">$705,421</td><td class="n">$748,028</td><td class="n">$739,936</td><td class="n">$670,597</td><td class="n">$625,949</td></tr>
<tr><td class="lbl">FY25 actual</td><td class="n">$82,988</td><td class="n">$298,351</td><td class="n">$299,687</td><td class="n">$245,709</td><td class="n">$320,315</td><td class="n">$356,028</td><td class="n">$225,268</td><td class="n">$361,509</td><td class="n">$874,325</td><td class="n">$651,828</td><td class="n">$527,980</td><td class="n">$372,286</td></tr>
</table></div>
<p class="fine">August 31 to October 31: $605,746 less the $200,789 operating loss, plus $56,750 of Front Row installments and $100,000 of receivables collected, less $70,000 of deferred revenue recognized, plus $5,000 of accruals = $496,706. Front Row is scheduled member by member: FY26 collections $257,876, FY27 $317,876 (15 current, four due now, three late, five behind at half, two dormant at zero, three new). Debt $1.05M, then $950k after the January payment.</p>

<div class="pb"></div>
<div class="sechead"><div><div class="eb">Section 8.0</div><div class="tt">FY27 Draft Budget</div></div><div class="bn">8.</div></div>
<div class="lede">A first pass seeded from the FY26 projection with the rules the committee set on September 2. Not a recommendation. The one structural move is programming, brought back toward FY25 scale; that sets tickets, bar and event payroll with it. The full draft with schedules comes in October.</div>
<div class="kpis">
<div class="kpi"><div class="k">FY27 Operating</div><div class="val">$226,369</div><div class="d">before $605,705 depreciation and lease</div></div>
<div class="kpi"><div class="k">FY27 Full Accrual</div><div class="val">($379,336)</div><div class="d">FY26 projected ($582,818)</div></div>
<div class="kpi"><div class="k">Revenue</div><div class="val">$3.32M</div><div class="d">FY26 projected $3.47M</div></div>
<div class="kpi"><div class="k">Cash at 10/31/2027</div><div class="val">$625,949</div><div class="d">low point $403,475 in February</div></div>
</div>
<div class="compact"><table>
<tr class="hd"><td>Block</td><td class="n">FY25 actual</td><td class="n">FY26 projected</td><td class="n">FY27 draft</td><td class="n v">FY27 vs FY26</td></tr>
<tr><td class="lbl">4000 Contributed Income</td><td class="n">$1,412,747</td><td class="n">$1,682,080</td><td class="n">$1,588,418</td><td class="n v">($93,661)</td></tr>
<tr><td class="lbl">4100 Earned Income</td><td class="n">$1,141,579</td><td class="n">$1,313,909</td><td class="n">$1,224,071</td><td class="n v">($89,838)</td></tr>
<tr><td class="lbl">4200 Front Row (three pledges)</td><td class="n">$490,000</td><td class="n">$260,000</td><td class="n">$300,000</td><td class="n v">$40,000</td></tr>
<tr><td class="lbl">7000 Other Income (incl. in-kind)</td><td class="n">$319,174</td><td class="n">$210,075</td><td class="n">$204,293</td><td class="n v">($5,782)</td></tr>
<tr class="b"><td class="lbl">Total Revenue</td><td class="n">$3,363,501</td><td class="n">$3,466,064</td><td class="n">$3,316,782</td><td class="n v">($149,282)</td></tr>
<tr><td class="lbl">5000 Cost of Goods Sold</td><td class="n">$183,693</td><td class="n">$250,269</td><td class="n">$259,469</td><td class="n v">$9,200</td></tr>
<tr><td class="lbl">6000 Administrative</td><td class="n">$134,133</td><td class="n">$132,583</td><td class="n">$141,777</td><td class="n v">$9,194</td></tr>
<tr><td class="lbl">6100 Building</td><td class="n">$314,806</td><td class="n">$304,981</td><td class="n">$313,860</td><td class="n v">$8,878</td></tr>
<tr><td class="lbl">6200 Marketing</td><td class="n">$120,478</td><td class="n">$120,827</td><td class="n">$129,748</td><td class="n v">$8,921</td></tr>
<tr><td class="lbl">6300 Payroll</td><td class="n">$1,286,208</td><td class="n">$1,345,361</td><td class="n">$1,291,936</td><td class="n v">($53,425)</td></tr>
<tr><td class="lbl">6400 Programming</td><td class="n">$733,359</td><td class="n">$965,487</td><td class="n">$683,850</td><td class="n v">($281,637)</td></tr>
<tr><td class="lbl">8000 Other Expenditures (incl. depreciation, in-kind, interest)</td><td class="n">$911,718</td><td class="n">$929,374</td><td class="n">$875,479</td><td class="n v">($53,895)</td></tr>
<tr class="b"><td class="lbl">Total Expense</td><td class="n">$3,684,395</td><td class="n">$4,048,882</td><td class="n">$3,696,119</td><td class="n v">($352,764)</td></tr>
<tr class="b"><td class="lbl">Net, full accrual</td><td class="n">($320,894)</td><td class="n">($582,818)</td><td class="n">($379,336)</td><td class="n v">$203,482</td></tr>
<tr class="b"><td class="lbl">Net, operating (before depreciation and lease)</td><td class="n">$284,811</td><td class="n">$22,887</td><td class="n">$226,369</td><td class="n v">$203,482</td></tr>
</table></div>
<div class="half">
<div>
<h3>Set on September 2</h3>
<ul style="font-size:9px;"><li>Depreciation and lease: one entry October 31, $605,705.</li><li>Front Row: FY26 at $260k; FY27 three pledges of $100k.</li><li>In-kind: zero-sum pair at $195,793.</li><li>Capital campaign closed. Tips out of the P&amp;L. Kegs to accrual cost from September.</li></ul>
</div>
<div>
<h3>Still to Decide</h3>
<ul style="font-size:9px;"><li><b>Programming scale:</b> $683,850 seeded against $965,487 this year.</li><li><b>Payroll:</b> $1,291,936 by person; open roles, benefits review and wage step not yet in.</li><li><b>Bar pour cost:</b> 38% assumed to hold; pricing and purchasing could move $30&ndash;50k.</li><li><b>Contributed:</b> Ball at $917k again, grants at FY26 pace, fall appeal.</li><li><b>Rentals and hosted bar:</b> $97k contracted into FY27; hosted bar has undershot two years running.</li></ul>
</div>
</div>
<div class="foot">Prepared September 9, 2026 from QuickBooks Online (accrual basis) after the August close; budget = FY2026 board-approved, phased YTD from the QBO budget object; prior year = FY2025 same period; projection and FY27 draft from the FY27 budget workbook. Not audited.</div>
</body></html>"""'''
NEW = cut(NEW, '<div class="sechead"><div><div class="eb">Section 8.0</div>', '</body></html>"""', esc(SEC).replace('</body></html>"""', '</body></html>"""'))
# the cut above kept the closing triple-quote from SEC; remove the duplicate left in the template
NEW = NEW.replace('</body></html>"""</body></html>"""', '</body></html>"""')
open("build_report.py", "w", encoding="utf-8").write(NEW)
print("wrote condensed build_report.py", len(NEW))
