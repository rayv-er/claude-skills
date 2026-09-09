#!/usr/bin/env python3
"""Refresh build_report.py for the September 2026 edition (FY26 through August 31, ten months).
Reads build_report_2026-08-17.py (the August edition), replaces the data dicts and every narrative section, writes
build_report.py. Numbers: live QBO TrialBalance pulls 2026-09-09 (cfta/data scripts/budget/data/board_dicts_2026-08-31.json),
QBO budget object "FY26 - Consolidated" months Nov..Aug (board_budget_2026-08-31.json), warehouse pulls 2026-09-09."""
import re, json
SRC = open("build_report_2026-08-17.py", encoding="utf-8").read()

def cut(text, start_marker, end_marker, replacement, occurrence=1):
    i = -1
    for _ in range(occurrence): i = text.find(start_marker, i + 1)
    assert i >= 0, start_marker[:60]
    j = text.find(end_marker, i + len(start_marker)); assert j >= 0, end_marker[:60]
    return text[:i] + replacement + text[j:]

def esc(s):  # the HTML lives inside an f-string: double any literal braces
    return s.replace("{", "{{").replace("}", "}}")

# ------------------------------------------------------------------ 1. data dicts
DATA = '''# ---------------------------------------------------------------------------
# FY26 YTD - REPORTING PERIOD: NOVEMBER 1, 2025 - AUGUST 31, 2026 (10 months)
# Refreshed 2026-09-09 from live QBO TrialBalance reports (start_date/end_date honoured; the BalanceSheet
# report ignores end_date, so every as-of figure comes from the TrialBalance).
#
#   A   actuals    TrialBalance 2025-11-01..2026-08-31, accrual, P&L rows
#   B   budget     Budget "FY26 - Consolidated" (QBO object, mirror qbo.budgets), months Nov..Aug summed.
#                  The object carries NO depreciation and NO tips lines; two unnumbered Marketing "Creative"
#                  lines fold into Marketing. Processing Fees = 5010 + the unnumbered Stripe fees line.
#   P   prior yr   TrialBalance 2024-11-01..2025-08-31, accrual, as booked (no W+FF restatement: both years
#                  now hold a full festival)
#   BS  balance sheet 2026-08-31    BSP  balance sheet 2025-08-31
#   CF  indirect cash flow from balance sheets at FY start and cutoff; both columns reconcile to the movement in
#       total bank accounts (incl. Stripe Clearing and the Fidelity brokerage) with a $0.00 gap.
#
# PRIOR-MONTH REVISIONS: Nov..Jul figures moved since the 08.17 edition (net revenue through July 445,116.68 ->
# 313,916.35). The bridge is in REV below and printed in Section 1.
# ---------------------------------------------------------------------------
A = {"contrib":1665362.20,"earned":1106468.05,"frontrow":260000.00,"totrev":3031830.25,
 "proc":31420.86,"prod":176609.94,"cogs":208030.80,"gross":2823799.45,
 "admin":110528.47,"building":304866.24,"marketing":111121.03,"payroll":1138347.67,"programming":875727.93,"totexp":2540591.34,
 "netop":283208.11,"othrev":28780.93,"othexp":88312.95,"interest":64535.00,"netrev":223676.09}
B = {"contrib":1604032.0,"earned":1118110.0,"frontrow":300000.0,"totrev":3022142.0,
 "proc":40000.0,"prod":108920.0,"cogs":148920.0,"gross":2873222.0,
 "admin":112913.0,"building":263725.0,"marketing":107103.0,"payroll":1135131.0,"programming":789865.0,"totexp":2408737.0,
 "netop":464485.0,"othrev":83528.0,"othexp":147438.0,"interest":68910.0,"netrev":400575.0}
P = {"contrib":1395229.69,"earned":1002353.84,"frontrow":390000.00,"totrev":2787583.53,
 "proc":36016.93,"prod":111482.80,"cogs":147499.73,"gross":2640083.80,
 "admin":112679.31,"building":268721.60,"marketing":103815.43,"payroll":1046523.28,"programming":687966.76,"totexp":2219706.38,
 "netop":420377.42,"othrev":187107.84,"othexp":143019.25,"interest":65596.86,"netrev":464466.01}
# July as reported 08.17 (AJ0) vs July as the books read now (AJ1): the revision bridge
AJ0 = {"contrib":1652036.74,"earned":1037499.63,"frontrow":160000.00,"cogs":137299.61,"admin":98383.70,"building":239907.99,"marketing":107399.67,"payroll":996741.04,"programming":729698.99,"othrev":21961.03,"othexp":116949.72,"netrev":445116.68}
AJ1 = {"contrib":1633496.71,"earned":1002232.16,"frontrow":160000.00,"cogs":178248.43,"admin":99248.68,"building":279555.68,"marketing":103486.68,"payroll":997507.66,"programming":769688.26,"othrev":26852.07,"othexp":80928.93,"netrev":313916.35}
# BS other_cl = Total Current Liabilities, so the sfp formula
# (other_cl - deferred_ticket - deferred_rental - ap) yields the payroll/deposits/tax residual.
BS = {"op_cash":599948.94,"stripe":5796.57,"cash_tot":605745.51,
 "ar_frontrow":1347376.05,"ar_operating":280276.77,"ar_other":86465.92,"ar_tot":1714118.74,
 "other_ca":64795.86,"tot_ca":2384660.11,"fixed":16792434.09,"donated_lease":1970921.00,"tot_assets":21148015.20,
 "ap":30849.57,"deferred_ticket":14201.00,"deferred_rental":134937.32,"other_cl":242725.72,"loans":1050000.00,"tot_liab":1292725.72,
 "restricted":2325224.00,"unrestricted":17306389.39,"net_rev":223676.09,"tot_eq":19855289.48,"fidelity":149249.14}
BSP = {"tot_assets":21691400.44,"tot_liab":1274426.94,"tot_eq":20416973.50,
 "cash_tot":657631.45,"ar_tot":1573383.32,"ar_frontrow":1506441.59,"ar_oo":66941.73,"other_ca":91326.02,"tot_ca":2322340.79,
 "fixed":17352568.65,"donated_lease":2016491.00,
 "ap":15535.54,"deferred_ticket":0.0,"deferred_rental":64461.36,"other_cl_net":44430.04,"loans":1150000.0,
 "restricted":2325224.0,"unrestricted":17627283.49,"net_rev":464466.01}

# Cash flows, indirect method, derived from balance sheets at FY start and cutoff.
# FY26: 2025-10-31 -> 2026-08-31 ; FY25: 2024-10-31 -> 2025-08-31. Gap to bank movement: $0.00 both columns.
CF = {
 "ni":(223676.09, 464466.01), "ar":(-100389.34, -12924.27), "defr":(112721.59, 3861.36),
 "inv":(-6974.50, 10721.20), "wc":(21710.86, -5489.27), "op":(250744.70, 460635.03),
 "invest":(0.00, -26772.29), "fin":(-100000.00, 50000.00), "net":(150744.70, 483862.74),
 "cash_end":(605745.51, 657631.45)}
'''
NEW = cut(SRC, "# ---------------------------------------------------------------------------\n# FY26 YTD - REPORTING PERIOD", "def cfrow(", DATA)

# statement headers: August 31 / prior August 31
NEW = NEW.replace('<td class="n">Jul 31, 2026</td><td class="n">Jul 31, 2025</td>', '<td class="n">Aug 31, 2026</td><td class="n">Aug 31, 2025</td>')
NEW = NEW.replace('Statement of Financial Position — July 31', 'Statement of Financial Position — August 31')

# ------------------------------------------------------------------ 2. cover
NEW = NEW.replace('FY2026 Year-to-Date &middot; 08.17.2026', 'FY2026 Year-to-Date &middot; 09.15.2026')
NEW = NEW.replace('Reporting Period &middot; November 1, 2025 &ndash; July 31, 2026 &middot; Accrual Basis', 'Reporting Period &middot; November 1, 2025 &ndash; August 31, 2026 &middot; Accrual Basis')
NEW = NEW.replace('<span>$2.85M revenue &middot; +4% vs budget</span>', '<span>$3.03M revenue &middot; on budget &middot; ten months</span>')
NEW = NEW.replace('"<span>FY2026 Year-to-Date &middot; 08.17.2026</span></div>")', '"<span>FY2026 Year-to-Date &middot; 09.15.2026</span></div>")')

# ------------------------------------------------------------------ 3. agenda and minutes
AGENDA = '''<div class="sechead"><div><div class="eb">Finance Committee</div><div class="tt">Agenda &amp; Minutes</div></div><div class="bn"></div></div>

<h3>Agenda &mdash; September 21, 2026 &middot; 9:00 am MT &middot; Zoom</h3>
<div style="border:1px solid #d5e0f0; border-radius:6px; background:#fff; padding:6px 12px; margin:4px 0 10px; font-size:9.5px;">
<ol style="margin:4px 0 4px 16px; padding:0;">
<li><b>Welcome</b> &mdash; Dave Ebner
<ol type="a" style="margin:1px 0 1px 16px;"><li>Approval of meeting agenda</li><li>Approval of June and July meeting minutes (carried from August)</li></ol></li>
<li><b>Finance Committee</b>
<ol type="a" style="margin:1px 0 1px 16px;"><li>Review FY26 to date financial report &mdash; through August 31, ten months, including the revisions to prior months from the year-end clean-up</li><li>FY26 year-end projection and cash through October 31 (Section 9.0)</li><li>FY27 draft budget, first pass (Section 10.0)</li><li>FY25 audit (Weaver) &mdash; status of the final report</li></ol></li>
<li><b>Other Updates</b> &mdash; Fidelity account funded by two stock gifts; new Front Row pledge recorded; bar inventory count and cost rebuild; bank reconciliations</li>
<li><b>Fundraising</b> &mdash; fall appeal and Front Row pipeline</li>
<li><b>Other Business</b> &mdash; investment policy (governance); Wine + Food expansion ad hoc committee</li>
<li><b>Executive Session</b></li>
<li><b>Adjournment</b></li>
</ol></div>
<p class="note"><b>August.</b> No committee meeting was held in August; the August 17 report was circulated to the committee by email in its place. This report also goes to the board for its September 15 meeting.</p>
'''
NEW = cut(NEW, '<div class="sechead"><div><div class="eb">Finance Committee</div><div class="tt">Agenda', '<h3>Draft Minutes &mdash; Finance Committee Meeting, June 15, 2026</h3>', esc(AGENDA))

# ------------------------------------------------------------------ 4. executive summary
def k(v): 
    s = f"{abs(v):,.0f}"; return f"(${s})" if v < 0 else f"${s}"
rev_b = 3031830.25 - 3022142; exp_b = 2540591.34 - 2408737; netop_b = 283208.11 - 464485; net_b = 223676.09 - 400575
rev_p = 3031830.25 - 2787583.53; exp_p = 2540591.34 - 2219706.38; netop_p = 283208.11 - 420377.42; net_p = 223676.09 - 464466.01
REVROWS = [("Contributed revenue","contrib"),("Earned revenue","earned"),("Front Row","frontrow"),("Cost of sales","cogs"),("Administrative","admin"),("Building","building"),("Marketing","marketing"),("Payroll","payroll"),("Programming","programming"),("Other revenue (net)","othrev"),("Other expenses","othexp"),("Total net revenue","netrev")]
AJ0 = {"contrib":1652036.74,"earned":1037499.63,"frontrow":160000.00,"cogs":137299.61,"admin":98383.70,"building":239907.99,"marketing":107399.67,"payroll":996741.04,"programming":729698.99,"othrev":21961.03,"othexp":116949.72,"netrev":445116.68}
AJ1 = {"contrib":1633496.71,"earned":1002232.16,"frontrow":160000.00,"cogs":178248.43,"admin":99248.68,"building":279555.68,"marketing":103486.68,"payroll":997507.66,"programming":769688.26,"othrev":26852.07,"othexp":80928.93,"netrev":313916.35}
why = {"contrib":"W+FF chargebacks and gala recodes","earned":"bar sales now net of 9.4% sales tax; rental and hosted-bar deferrals corrected","cogs":"alcohol cost re-based to the 8/31 physical count and cost rebuild","building":"insurance and building bills posted to their service months","programming":"festival wine moved from inventory to programming; event staffing attributed by shift","othrev":"in-kind entries netted down","othexp":"in-kind entries netted down; no depreciation booked","payroll":"","admin":"","marketing":"","frontrow":"","netrev":"net effect on the ten-month result through July"}
rows = []
for lab, key in REVROWS:
    d = AJ1[key] - AJ0[key]; cls = ' class="b"' if key == "netrev" else ""
    rows.append(f'<tr{cls}><td class="lbl">{lab}</td><td class="n">{k(AJ0[key])}</td><td class="n">{k(AJ1[key])}</td><td class="n v">{k(d)}</td><td class="lbl2" style="padding-left:10px">{why[key]}</td></tr>')
REVTABLE = "\n".join(rows)
EXEC = f'''<div class="sechead"><div><div class="eb">Section 1.0</div><div class="tt">Executive Summary</div></div><div class="bn">1.</div></div>
<div class="lede">Net revenue of <b>$223,676</b> for the first ten months. Revenue of <b>$3.03M</b> is <b>on budget</b> ({k(rev_b)}, +0.3%) and <b>{k(rev_p)} ahead of the prior year</b>; expenditures of <b>$2.54M</b> are <b>{k(exp_b)} (+5.5%) over</b> the year-to-date budget. Operating income of <b>$283,208</b> stands <b>{k(abs(netop_b))} (&minus;39%) behind plan</b>, and the ten-month result is <b>{k(abs(net_b))} behind</b> the budgeted $400,575. Two things changed the picture since the August report: <b>August itself carried the post-season cost base against a quiet revenue month</b>, and <b>the year-end clean-up restated November through July</b> (bridge below).</div>

<div class="kpis">
<div class="kpi"><div class="k">Total Revenue YTD</div><div class="val">$3.03M</div><div class="d">+0.3% vs budget &middot; +8.8% YoY</div></div>
<div class="kpi"><div class="k">Operating Income</div><div class="val">$283k</div><div class="d">&minus;39% vs budget</div></div>
<div class="kpi"><div class="k">Net Revenue</div><div class="val">$224k</div><div class="d">{k(net_b)} vs budget</div></div>
<div class="kpi"><div class="k">Cash &amp; Equivalents</div><div class="val">$606k</div><div class="d">incl. $149k Fidelity brokerage</div></div>
</div>

<h3>Revisions to Prior Months Since the August 17 Report</h3>
<p class="note">The books through July now read <b>$313,916</b> of net revenue, not the <b>$445,117</b> reported on August 17. The year-end clean-up re-based alcohol cost of sales to the August 31 physical count, moved festival wine out of inventory, booked bar sales net of sales tax, corrected rental and hosted-bar deferrals, and netted down in-kind entries. None of it is new spending; it is timing and classification landing in the right months before the audit.</p>
<div class="compact"><table>
<tr class="hd"><td>Line (Nov&ndash;Jul)</td><td class="n">As reported 8/17</td><td class="n">As restated</td><td class="n v">Change</td><td class="lbl2">Driver</td></tr>
{REVTABLE}
</table></div>

<h3>Year to Date &mdash; vs. Budget</h3>
<div><b>Total revenue of $3.03M is {k(rev_b)} (+0.3%) ahead of budget; expenditures of $2.54M are {k(exp_b)} (+5.5%) over budget, carrying operating income to $283,208 against a plan of $464,485.</b></div>
<div><b style="color:#0A3A82">Favorable</b><ul>
<li>Contributed revenue <b>$61,330 (+3.8%) ahead of budget</b> &mdash; grants at 2.5x plan and unrestricted gifts well ahead; the Ball held its budget.</li>
<li>Ticket and program income <b>$115,854 (+19%) ahead</b> of its line &mdash; the strongest presenting season on record, which is also what drove programming expense.</li>
<li>Payroll <b>$3,217 (+0.3%)</b> &mdash; on budget through the busiest quarter; administrative <b>$2,385 (&minus;2%) under</b>.</li></ul></div>
<div><b style="color:#A7182F">Unfavorable / Watch</b><ul>
<li>Programming <b>+$85,863 (+11%)</b> &mdash; a larger season; net of the ticket beat the two lines are $30k behind plan.</li>
<li>Cost of sales <b>+$59,111 (+40%)</b> &mdash; alcohol cost re-based to the physical count; alcohol cost now runs 38% of bar revenue, a review of routing and pour cost is under way.</li>
<li>Building <b>+$41,141 (+16%)</b> &mdash; property insurance premiums.</li>
<li>Earned revenue <b>$11,642 (&minus;1%) behind</b> overall: bar and hosted bar <b>$48,097 behind</b> (bar sales now booked net of the 9.4% sales tax) and rentals <b>$29,043 behind</b>, offset by tickets.</li>
<li>Front Row <b>$40,000 (&minus;13%) behind</b> the phased target &mdash; $260k against $300k after the $100k Burciaga pledge recorded August 26.</li>
<li>Other revenue <b>$54,747 (&minus;66%) below budget</b> &mdash; the budget's in-kind gross-up is not booked; it offsets in other expenses, which are $59,125 under.</li></ul></div>

<h3>Year to Date &mdash; vs. Prior Year</h3>
<div><b>Net revenue of $223,676 is {k(abs(net_p))} behind the prior year.</b> Front Row is $130,000 lower and last year's other revenue carried a one-time $110,534 receivables adjustment; together $241k of the gap. Underneath, revenue grew {k(rev_p)} (+8.8%) and operating expense grew {k(exp_p)} (+14.5%). Both years contain a full festival, so no prior-year restatement is applied.</div>
<div><b style="color:#0A3A82">Favorable</b><ul>
<li>Revenue <b>+{k(rev_p)} (+8.8%)</b> &mdash; contributed <b>+$270,133 (+19.4%)</b>, earned <b>+$104,114 (+10.4%)</b>.</li></ul></div>
<div><b style="color:#A7182F">Unfavorable</b><ul>
<li>Front Row <b>$260,000 vs $390,000</b> &mdash; a $130,000 timing line; two more designations are in conversation for the fall.</li>
<li>Expenditures <b>+{k(exp_p)} (+14.5%)</b> &mdash; programming +$187,761, payroll +$91,824, cost of sales +$60,531, building +$36,145; operating income {k(abs(netop_p))} (&minus;33%) behind.</li></ul></div>

<h3>Cash &amp; Balance Sheet</h3><ul>
<li>Cash and equivalents of <b>$605,746</b>, <b>$51,886 below</b> the same date last year, and now in three places: <b>$442,140</b> in the operating and sweep accounts, <b>$149,249</b> in the Fidelity brokerage (two stock gifts, liquidated to money market), and <b>$14,357</b> in bar banks, petty cash and processor funds in transit. Last year included the one-time $110k Employee Retention Credit and a $50k net loan draw where this year repaid $100k.</li>
<li><b>$149,138</b> already collected and sitting in deferred revenue for future events and rentals: <b>$134,937</b> for fall weddings and rentals, <b>$14,201</b> for fall shows. Cash in hand, not yet in the P&amp;L.</li>
<li>Front Row pledges receivable <b>$1,347,376</b>; Event Temple contract receivable <b>$75,041</b>; operating receivables <b>$280,277</b> (gala pledge invoices collecting through fall).</li>
<li>Long-term debt <b>$1,050,000</b>, down <b>$100,000</b> year over year; YTD interest $64,535 drives the below-operating-line figure.</li></ul>

<h3>Year-End Outlook</h3>
<div class="lede">Two months remain. On the current projection FY26 closes at <b>$22,887 before depreciation</b> and <b>($582,818)</b> after the $605,705 of depreciation and donated lease booked October 31, against a budget that assumed $242,426 before depreciation. Bank and brokerage cash is projected at <b>$496,706 on October 31</b>, up from $455,001 a year earlier, with $1.05M of debt and $1.35M of Front Row pledges receivable. The first pass of the FY27 budget lands at <b>$226,369 operating</b> and <b>($379,336)</b> full accrual, the swing being a programming line brought back toward FY25 scale. Sections 9.0 and 10.0 carry the detail and the open calls.</div>
<h3>Other Updates</h3><ul>
<li><b>Fidelity brokerage funded.</b> Two stock gifts pledged at the Arts Ball arrived and were sold to money market: 100 MSFT (Valentine and Bolton) for $50,750 on August 10 and 812 IWF (Carol Ann May) for $99,125 on August 20, with $816 of realized loss between pledge and sale. Balance at August 31 <b>$149,249</b>, earning the SPAXX money-market rate.</li>
<li><b>New Front Row pledge recorded.</b> The Burciaga designation of <b>$100,000</b> was booked and invoiced on August 26 and is in these statements; Front Row now stands at $260,000 for the year.</li>
<li><b>Bar inventory counted and costed.</b> A full physical count on August 31 valued alcohol on hand at <b>$32,901</b>. Alcohol cost of sales for the year was rebuilt from purchases less that count and spread across the ten months by bar sales, which is the largest single revision above. Pour cost now reads 38% of bar and hosted-bar revenue; purchase routing and the July wine buys are under review.</li>
<li><b>FY25 audit (Weaver).</b> Draft V1 was reviewed at the August report; final report status to be confirmed at the meeting.</li>
<li><b>Bank reconciliations</b> for June through August are in progress; duplicate and stale entries found in the uncleared list have been removed, and the remaining items are matching work.</li>
<li><b>FY27 budget.</b> The draft workbook is under construction on the FY26 structure; first pass to the committee in October.</li></ul>

<div class="pb"></div>
'''
NEW = cut(NEW, '<div class="sechead"><div><div class="eb">Section 1.0</div>', '<div class="sechead"><div><div class="eb">Section 2.0</div>', esc(EXEC))

# ------------------------------------------------------------------ 5. signature events (final)
EVENTS = '''<div class="sechead"><div><div class="eb">Section 2.0</div><div class="tt">Summer Signature Events &mdash; Final</div></div><div class="bn">2.</div></div>
<div class="lede">The <b>Arts Ball</b> (July 9) and the <b>Wine + Food Festival</b> (mid-July, with the High Note dinner on August 6) are closed. Together they raised roughly <b>$1.30 million</b>. August added the High Note dinner, the last vendor fees, and a round of gift recodes; the figures below are actuals as booked at August 31.</div>
<div class="kpis">
<div class="kpi"><div class="k">Combined Raised</div><div class="val">&plusmn;$1.30M</div><div class="d">two signature events</div></div>
<div class="kpi"><div class="k">Arts Ball</div><div class="val">$917k</div><div class="d">record, +13% YoY</div></div>
<div class="kpi"><div class="k">Festival</div><div class="val">$379k</div><div class="d">ticket, pass &amp; vendor</div></div>
<div class="kpi"><div class="k">2027 Lever</div><div class="val">Sponsorship</div><div class="d">clearest path to growth</div></div>
</div>

<div style="border:1px solid #d5e0f0; border-radius:6px; background:#fff; padding:5px 10px; margin:5px 0; font-size:9px;">
<b style="color:#0A3A82;">Arts Ball 2026 &mdash; a Record Year &nbsp;&middot;&nbsp; $917,192 at the July close (+7% vs budget, +13% vs FY25; +35% over two years)</b>
<div class="compact"><table style="margin-top:4px;">
<tr class="hd"><td>Arts Ball &mdash; all revenue streams</td><td class="n">FY26 Actual</td><td class="n">Budget</td><td class="n v">vs Budget</td><td class="n">FY25</td><td class="n v">YoY</td></tr>
<tr><td class="lbl">Fundraiser income &mdash; paddle-raise, auction &amp; gifts</td><td class="n">$777,770</td><td class="n">$762,363</td><td class="n v">+2%</td><td class="n">$729,842</td><td class="n v">+7%</td></tr>
<tr><td class="lbl">Tables &amp; tickets (ticketing platform, net)</td><td class="n">$139,422</td><td class="n">$85,000</td><td class="n v">+64%</td><td class="n">$76,818</td><td class="n v">+82%</td></tr>
<tr><td class="lbl">Corporate sponsorship</td><td class="n">$0</td><td class="n">$10,000</td><td class="n v">($10,000)</td><td class="n">$3,000</td><td class="n v">&mdash;</td></tr>
<tr class="b"><td class="lbl">Total Arts Ball</td><td class="n">$917,192</td><td class="n">$857,363</td><td class="n v">+7%</td><td class="n">$809,660</td><td class="n v">+13%</td></tr>
</table></div>
<p class="note">Final at the July close. August work was housekeeping: <b>$15,102</b> of gifts recoded into Fundraiser Contributions (CFGV and two donor-advised gifts), and the customer clean-up now tags <b>$865,521</b> of Ball revenue to Arts Ball records in the ledger, up from $420k last month. Growth was led by the <b>paddle raise and major gifts</b>, with tables and tickets up <b>82% year over year</b>. Two-year trajectory: <b>$678k &rarr; $812k &rarr; $917k</b>.</p></div>

<div style="border:1px solid #d5e0f0; border-radius:6px; background:#fff; padding:5px 10px; margin:5px 0; font-size:9px;">
<b style="color:#0A3A82;">Wine + Food Festival 2026 &mdash; Closed, Just Under Last Year &nbsp;&middot;&nbsp; $378,534 booked</b>
<div class="compact"><table style="margin-top:4px;">
<tr class="hd"><td>W+FF revenue stream</td><td class="n">FY26 Actual</td><td class="n">Budget</td><td class="n">FY25 Full</td><td class="n v">vs FY25</td></tr>
<tr><td class="lbl">Ticket &amp; pass sales &mdash; e-commerce shop (completed orders)</td><td class="n">$331,964</td><td class="n"></td><td class="n"></td><td class="n v"></td></tr>
<tr><td class="lbl">Ticket &amp; pass sales &mdash; direct &amp; check</td><td class="n">$39,245</td><td class="n"></td><td class="n"></td><td class="n v"></td></tr>
<tr class="b"><td class="lbl">Total ticket &amp; pass, all channels</td><td class="n">$371,209</td><td class="n">$372,500</td><td class="n">$383,471</td><td class="n v">&minus;3%</td></tr>
<tr><td class="lbl">Vendor fees &amp; sponsorship (final)</td><td class="n">$7,325</td><td class="n">$32,000</td><td class="n">$18,644</td><td class="n v">&minus;61%</td></tr>
<tr class="b"><td class="lbl">Total festival</td><td class="n">$378,534</td><td class="n">$404,500</td><td class="n">$402,115</td><td class="n v">&minus;6%</td></tr>
</table></div>
<p class="note">Ticket and pass revenue landed <b>within 0.3% of the $372,500 budget</b> and 3% below FY25, the high-water mark. The <b>High Note dinner with Steve Earle</b> (Aug 6) closed the festival: its <b>$27,900</b> of tickets, deferred at July 31, is recognized in August. <b>$876</b> of card chargebacks came back in August. <b>Vendor fees and sponsorship finished at $7,325</b> against a $32,000 budget after the last two vendor invoices (Woody Creek $400, Tahoe Kitchen $1,200) &mdash; the festival's one clear miss, and the clearest lever for 2027.</p></div>

<div style="display:flex; gap:16px; margin:5px 0;">
<div style="flex:1;">
<div class="tcap">What Guests &amp; Staff Said</div>
<ul style="margin-top:3px;">
<li><b>The Ball&rsquo;s room and cadence.</b> Intimate and well-paced &mdash; &ldquo;not too loud,&rdquo; &ldquo;it felt intimate,&rdquo; an auction that &ldquo;didn&rsquo;t go on forever.&rdquo; The video and remarks drew unusually strong praise; beautiful decor, great food, dancing afterward.</li>
<li><b>The Festival experience.</b> The Tour de Fork dinners drew some of the strongest response in the festival&rsquo;s history &mdash; food, wine, right-sized, indoors, with name tags and assigned seating. Steve Earle at the High Note: &ldquo;so much better than we expected.&rdquo;</li>
<li><b>Cultivation.</b> Multiple guests volunteered their intent to deepen support &mdash; two of the Ball&rsquo;s pledges have since arrived as stock gifts.</li>
</ul>
</div>
<div style="flex:1;">
<div class="tcap">What to Improve</div>
<ul style="margin-top:3px;">
<li><b>Auction energy.</b> The auctioneer could bring more energy and open the paddle raise higher.</li>
<li><b>Guest flow.</b> Guests gravitated to the atrium; the lounge and bar were underused. A longer cocktail hour and clearer wayfinding would help.</li>
<li><b>Sponsorship.</b> Vendor and sponsor billing needs an owner and a calendar; $25k of budgeted festival revenue was never asked for.</li>
</ul>
<div class="tcap" style="margin-top:5px;">The Bigger Picture</div>
<p class="note" style="margin-top:2px;"><b>Arts Ball = the growth story</b> (+35% over two years, a maturing donor base); <b>Festival = the stability story</b> (a strong earned-revenue event on infrastructure the Center controls). <b>Growing event and festival sponsorship is the clearest lever to lift 2027 revenue.</b></p>
</div>
</div>
<div style="border-left:4px solid #0A3A82; background:#f2f6fb; padding:5px 11px; margin:4px 0; font-style:italic; font-size:8.5px;">
&ldquo;Best of the galas we have been to.&rdquo; &middot; &ldquo;The best party the Center for the Arts has given.&rdquo; &middot; &ldquo;A first-class experience &mdash; bravo.&rdquo;<span style="font-style:normal; color:#555;">&nbsp; &mdash; guests, Arts Ball &amp; Wine + Food Festival 2026</span></div>
<p class="fine">Event revenue above is drawn from source systems (e-commerce shop, ticketing platform, event records) reconciled to the July close. The ledger's own event tags now cover $865,521 of the Ball and $302,747 of the festival; the balance sits in untagged card-deposit lines and the 50/50 festival split.</p>

<div class="pb"></div>
'''
NEW = cut(NEW, '<div class="sechead"><div><div class="eb">Section 2.0</div>', '<div class="sechead"><div><div class="eb">Section 3.0</div>', esc(EVENTS))

# ------------------------------------------------------------------ 6. statements note
NEW = NEW.replace('<p class="fine">Accrual basis. <b>No prior-year restatement this month.</b> June&rsquo;s report moved $308,921 of FY25 W+FF ticket revenue out of the Nov&ndash;Jun comparative because FY26&rsquo;s festival was still post-period. At nine months both years contain a full festival &mdash; FY25 recognized as sold in spring 2025, FY26 at the July 2026 event &mdash; so the columns are directly comparable as booked.</p>',
 '<p class="fine">Accrual basis, ten months. <b>No prior-year restatement.</b> Both years contain a full festival, so the columns compare as booked. <b>Prior months are revised</b> since the August 17 report (bridge in Section 1.0). Depreciation and the donated-lease amortization are booked once a year at October 31 in both years, and the FY26 budget object carries none, so every bottom line here is before depreciation; FY25 booked $560,135 plus $45,570 at year end.</p>')
NEW = NEW.replace('{cfrow("Construction loans, net (FY26: $100k paydown; FY25: $1.0M draw less $950k retirement)","fin")}', '{cfrow("Construction loans, net (FY26: $100k paydown; FY25: $50k net draw)","fin")}')
NEW = NEW.replace('{cfrow("Inventory build &amp; artist advances","inv")}', '{cfrow("Inventory, allowances &amp; other current assets","inv")}')

# ------------------------------------------------------------------ 7. programming
def bar62(pos): return round(pos * 0.62)
LINEUP = [  # name, date, tickets, bar POS, fee, staffing, other
 ("<b>The String Cheese Incident (two nights)</b>","Jun 3&ndash;4",151126,17773,-135500,-8129,0),
 ("Kitchen Dwellers (two nights)","Jan 17&ndash;18",35564,13322,-24690,-4488,0),
 ("Alpenphunk Incident (two nights, co-pro)","Jan 31&ndash;Feb 1",43673,11266,-15000,-4396,0),
 ("Hank Azaria + The EZ Street Band","Dec 28",27995,4952,-25742,-2257,0),
 ("Vandelux (Sleds &amp; Kegs)","Mar 7",24265,9711,-12137,-3714,0),
 ("Nutcracker! [Rated CB]","Dec 13",20660,1738,0,-3543,-15859),
 ("Steve Earle &mdash; Steddy Theater (paired with the High Note dinner, Section 2.0)","Aug 6",16132,2711,-20750,-143,-403),
 ("Beats Antique","Mar 13",14115,4203,-12100,-2655,0),
 ("Ski Patrol <span style='color:#0A3A82;'>(community benefit)</span>","Feb 8",12205,10756,-4000,-6894,-9764),
 ("The Brothers Comatose","Feb 26",10102,2750,-5403,-3826,0),
 ("Bodhi &amp; the Rainforest (three shows; artist settlement not yet booked)","Aug 20&ndash;22",9005,846,0,-6651,-352),
 ("Deadhead Ed's End of Season Party","Apr 3",8867,3699,-5000,-2661,0),
 ("Opera Colorado: Pirates of Penzance","Feb 5",6165,745,-600,-753,0),
 ("Mr. Sun Plays Ellington's Nutcracker","Dec 20",5376,955,-3000,-1056,0),
 ("Opera Lollipops (artist fee not yet booked)","Aug 1",3883,484,0,-1505,-629),
]
def cell(v, neg_dash=True):
    if v == 0: return "&mdash;"
    return f"(${abs(v):,.0f})" if v < 0 else f"${v:,.0f}"
lrows = []; T = [0,0,0,0,0,0]
for n, d, t, pos, fee, st, oth in LINEUP:
    bar = bar62(pos); net = t + bar + fee + st + oth
    T[0]+=t; T[1]+=bar; T[2]+=fee; T[3]+=st; T[4]+=oth; T[5]+=net
    bold = n.startswith("<b>")
    lrows.append(f'<tr><td class="lbl">{n}</td><td class="n">{d}</td><td class="n">{cell(t)}</td><td class="n">{cell(bar)}</td><td class="n">{cell(fee)}</td><td class="n">{cell(st)}</td><td class="n">{cell(oth)}</td><td class="n">{"<b>" if bold else ""}{cell(net)}{"</b>" if bold else ""}</td></tr>')
LTABLE = "\n".join(lrows); hosp = -28741
PROG = f'''<div class="sechead"><div><div class="eb">Section 4.0</div><div class="tt">Programming</div></div><div class="bn">4.</div></div>
<div class="lede">The FY26 ticketed lineup &mdash; complete through August 31 &mdash; delivered <b>$389k of ticket revenue</b> across 16 headline shows and 6,889 attendees. On the re-based alcohol cost the concert lineup nets <b>{cell(T[5])}</b> before season-wide hospitality and <b>{cell(T[5]+hosp)}</b> after it. <b>August was the closing month</b>: Steve Earle in the Steddy (paired with the festival's High Note dinner), <b>Bodhi &amp; the Rainforest</b>, a new all-local children's musical that sold 453 tickets over three shows, Opera Lollipops, two Beth Zink painting workshops, and the Mountain Words Writers' Retreat.</div>

<div style="border:1px solid #d5e0f0; border-radius:6px; background:#fff; padding:5px 10px; margin:5px 0; font-size:9px;">
<b style="color:#0A3A82;">Alpenglow &mdash; the Free Series, Season Complete</b>
<div class="compact"><table style="margin-top:4px;">
<tr class="hd"><td>Free series &mdash; bar revenue by night</td><td class="n">2026</td><td class="n">2025</td><td class="n v">YoY</td></tr>
<tr><td class="lbl">Alpenglow &mdash; two August Mondays (Aug 3 Hand Turkey $11,686; Aug 10 Chantil &amp; The Dukes of Art $9,422)</td><td class="n">$21,108</td><td class="n">$21,312</td><td class="n v">&minus;1%</td></tr>
<tr class="b"><td class="lbl">Alpenglow full season &mdash; nine nights</td><td class="n">$99,839</td><td class="n">$99,101</td><td class="n v">+1%</td></tr>
</table></div>
<p class="fine">A flat season against a record 2025 on a like-for-like basis (both years Clover payments, Denver-time nights). Last month's +7% used order totals, which ran higher on two June nights; the payments basis is used from here on. Summer Classics closed with Cowboy Songs (Aug 4) and Junwen Liang (Aug 11); August artist payments $2,500.</p></div>

<h3>Per-Event P&amp;L — Concert Lineup (FY26, complete)</h3>
<div class="compact"><table><tr class="hd"><td>Event</td><td class="n">Date</td><td class="n">Tickets</td><td class="n">Bar (net est.)</td><td class="n">Perf. Fee</td><td class="n">Staffing</td><td class="n">Other</td><td class="n">Est. Net</td></tr>
{LTABLE}
<tr class="b"><td class="lbl"><b>Total — concert lineup (event-identifiable costs)</b></td><td class="n"></td><td class="n">{cell(T[0])}</td><td class="n">{cell(T[1])}</td><td class="n">{cell(T[2])}</td><td class="n">{cell(T[3])}</td><td class="n">{cell(T[4])}</td><td class="n"><b>{cell(T[5])}</b></td></tr>
<tr><td class="lbl">Hospitality — lodging, travel &amp; artist food (booked season-wide)</td><td class="n"></td><td class="n"></td><td class="n"></td><td class="n"></td><td class="n"></td><td class="n"></td><td class="n">({"$"}{abs(hosp):,.0f})</td></tr>
<tr class="b"><td class="lbl"><b>Net after hospitality</b></td><td class="n"></td><td class="n"></td><td class="n"></td><td class="n"></td><td class="n"></td><td class="n"></td><td class="n"><b>{cell(T[5]+hosp)}</b></td></tr></table></div>
<p class="fine">Per-event rows carry the costs identifiable to each event in the books &mdash; presenter fees, show staffing, co-production payouts. <b>Bar = event-night POS net of alcohol cost at the re-based FY26 rate of 38%</b> (last month used an estimated 13%; that change alone takes $20k out of the lineup's net). Steve Earle's $20,750 fee covers the theater set; the dinner it was paired with is in Section 2.0. Bodhi &amp; the Rainforest and Opera Lollipops show staffing and marketing only; artist settlements were not yet booked at August 31. <b>Other</b> = co-production partner payouts (Nutcracker SOD 75%, Ski Patrol 80%) and miscellaneous per-event costs.</p>
<h3>Programming Economics — FY24 to FY26 (Nov&ndash;Jun window, identical footing)</h3>
<div class="compact"><table>
<tr class="hd"><td>Concert &amp; series direct P&amp;L</td><td class="n">FY24</td><td class="n">FY25</td><td class="n">FY26</td></tr>
<tr><td class="lbl">Gross ticket sales — concerts &amp; series</td><td class="n">$256,888</td><td class="n">$239,230</td><td class="n">$360,113</td></tr>
<tr><td class="lbl">Less: co-production partner splits</td><td class="n">($30,286)</td><td class="n">($33,346)</td><td class="n">($31,446)</td></tr>
<tr><td class="lbl">Net ticket sales</td><td class="n">$226,601</td><td class="n">$205,884</td><td class="n">$328,667</td></tr>
<tr><td class="lbl">Bar sales — programming nights</td><td class="n">$141,584</td><td class="n">$157,798</td><td class="n">$184,259</td></tr>
<tr class="b"><td class="lbl">Direct revenue</td><td class="n">$368,185</td><td class="n">$363,682</td><td class="n">$512,926</td></tr>
<tr><td class="lbl">Performer / presenter fees</td><td class="n">($215,507)</td><td class="n">($222,498)</td><td class="n">($317,476)</td></tr>
<tr><td class="lbl">Show labor — event, tech, bar, set-up</td><td class="n">($92,653)</td><td class="n">($82,628)</td><td class="n">($118,245)</td></tr>
<tr><td class="lbl">Hospitality — lodging, travel, food</td><td class="n">($30,674)</td><td class="n">($37,032)</td><td class="n">($28,741)</td></tr>
<tr><td class="lbl">Alcohol cost of sales (FY26 re-based to the 8/31 count)</td><td class="n">($27,098)</td><td class="n">($38,209)</td><td class="n">($70,018)</td></tr>
<tr class="b"><td class="lbl">Total direct cost</td><td class="n">($365,932)</td><td class="n">($380,367)</td><td class="n">($534,480)</td></tr>
<tr class="b"><td class="lbl">Net direct contribution</td><td class="n">$2,253</td><td class="n">($16,685)</td><td class="n">($21,554)</td></tr>
<tr><td class="lbl"><b>Margin on direct revenue</b></td><td class="n">0.6%</td><td class="n">(4.6%)</td><td class="n"><b>(4.2%)</b></td></tr>
<tr><td class="lbl">Artist share of direct cost</td><td class="n">59%</td><td class="n">58%</td><td class="n"><b>59%</b></td></tr>
<tr><td class="lbl">Largest single artist commitment</td><td class="n">$27,425</td><td class="n">&mdash;</td><td class="n">$75,500</td></tr>
<tr><td class="lbl">Beckwith donated lodging (in-kind, no cash)</td><td class="n">&mdash;</td><td class="n">$30,000</td><td class="n">$15,000</td></tr>
</table></div>
<p class="fine"><b>The re-based alcohol cost changes the three-year read.</b> Last month FY26 showed +$24k on 13% alcohol cost; at the counted 38% the same season is ($22k), in line with FY25's ($17k) rather than above it. Direct revenue still grew 39%, and the artist share of direct cost held at 59%; the pour cost, not the booking, is what to fix.</p>
<p class="fine">Basis: concert and series only, excluding festivals and the Arts Ball, on identical Nov&ndash;Jun footing all three years; FY24 ticket revenue rebuilt from the monthly Humanitix earnings reports; co-production splits identified by event and deducted in every year; gallery staffing excluded throughout. FY24 and FY25 alcohol cost stand as previously reported. Full methodology on file.</p>
<p class="fine">Co-production payouts, netted into Est. Net &mdash; FY26: School of Dance / Nutcracker $16k (75%), Ski Patrol $10k (80%, community benefit), Rocky Horror $2k; Alpenphunk carries an estimated $15k (two nights). Arts Ball and W+FF are reported in Section 2.0. Mountain Words (May festival plus the August Writers' Retreat: $3,550 of tickets against $22,633 of retreat cost) is within YTD.</p>
<p class="fine">Grants: $61.5k YTD vs $24.9k same FY25 period (+147%; 2.5x all of FY25), nearly all restricted to programs. A defined foundation and government pipeline is the clearest opportunity to grow contributed revenue in FY27.</p>
<div class="pb"></div>
'''
NEW = cut(NEW, '<div class="sechead"><div><div class="eb">Section 4.0</div>', '<div class="sechead"><div><div class="eb">Section 5.0</div>', esc(PROG))

# ------------------------------------------------------------------ 8. bar
MONTHS = [("November",4969,354,7210.78,791.90),("December",12900,880,14078.03,2421.73),("January",22069,1473,24422.00,4459.37),("February",24669,1707,27315.01,4512.81),("March",25452,1648,28315.02,5300.09),("April",3450,273,3934.03,765.50),("May",5976,433,6070.50,1102.60),("June",59713,4749,66409.54,10965.50),("July",40468,3041,50989.00,7259.07),("August",13435,1863,26277.01,4163.71)]
tot_rev = sum(m[1] for m in MONTHS); tot_n = sum(m[2] for m in MONTHS); tot_pos = sum(m[3] for m in MONTHS); tot_tip = sum(m[4] for m in MONTHS)
mrows = "\n".join(f'<tr><td class="lbl">{n}</td><td class="n">${r:,}</td><td class="n">{r/tot_rev*100:.0f}%</td><td class="n">{c:,}</td><td class="n">${s/c:,.2f}</td><td class="n">{t/s*100:.1f}%</td></tr>' for n,r,c,s,t in MONTHS)
AL26 = [("Mon Jun 15",9986),("Mon Jun 22",13308),("Mon Jun 29",13720),("Mon Jul 6",7952),("Mon Jul 13",9596),("Mon Jul 20",7673),("Mon Jul 27",16496),("Mon Aug 3",11686),("Mon Aug 10",9422)]
AL25 = [8748,10940,10342,12618,13488,10246,11406,11717,9595]
arows = "\n".join(f'<tr><td class="lbl">2026 &middot; {d}</td><td class="n">${v:,}</td><td class="n">${p:,}</td></tr>' for (d,v),p in zip(AL26,AL25))
MIX = [("Beer (incl. reusable cups)",5187,38588),("Wine",1011,19999),("Liquor / Cocktails",1603,19131),("Other / Custom",1086,13501),("Non-Alcoholic",894,7247),("Hard Seltzer / Cider",512,4757)]
mixt = sum(m[2] for m in MIX)
mixrows = "\n".join(f'<tr><td class="lbl">{n}</td><td class="n">{u:,}</td><td class="n">{r/mixt*100:.1f}%</td></tr>' for n,u,r in MIX)
BAR = f'''<div class="sechead"><div><div class="eb">Section 5.0</div><div class="tt">Bar &amp; Concessions</div></div><div class="bn">5.</div></div>

<p class="note">Bar revenue is a direct function of concert attendance, so it is tracked here alongside programming. Self-serve bar revenue for the ten months is <b>$213,103</b> (plus <b>$35,424</b> of hosted-bar revenue at rentals), now booked <b>net of the 9.4% sales tax</b>; last month's table was gross, so the months below read lower than the same months in August. <b>Alcohol cost of sales, rebuilt from the August 31 physical count, is $94,577, 38% of bar and hosted revenue</b>, against the 13% estimate carried in earlier reports. Point-of-sale detail (Clover) spans the full season &mdash; <b>16,421 bar transactions</b> from November through August; August contributed 1,863 on the final Alpenglow Mondays and the August shows.</p>
<div class="kpis">
<div class="kpi"><div class="k">Bar Gross Margin</div><div class="val">62%</div><div class="d">rev vs counted alcohol cost</div></div>
<div class="kpi"><div class="k">Avg Bar Ticket</div><div class="val">${tot_pos/tot_n:,.2f}</div><div class="d">per sale, Nov&ndash;Aug</div></div>
<div class="kpi"><div class="k">Card Tip Rate</div><div class="val">{tot_tip/tot_pos*100:.1f}%</div><div class="d">card tips on POS sales</div></div>
<div class="kpi"><div class="k">Rev per $1 Bar Labor</div><div class="val">$8.31</div><div class="d">bar wages by shift (broader basis than last month)</div></div>
</div>

<div style="display:flex; gap:20px;">
<div style="flex:1.1">
<p class="tcap">Per-attendee bar — all major concerts (Nov–Aug)</p>
<div class="compact"><table>
<tr class="hd"><td>Event</td><td class="n">Att.</td><td class="n">Bar (POS)</td><td class="n">$ / Att.</td></tr>
<tr><td class="lbl">Ski Patrol: Attitude Adjustment Party</td><td class="n">566</td><td class="n">$10,756</td><td class="n">$19.00</td></tr>
<tr><td class="lbl">Alpenphunk (two nights)</td><td class="n">798</td><td class="n">$11,266</td><td class="n">$14.12</td></tr>
<tr><td class="lbl">Britney's Circus</td><td class="n">309</td><td class="n">$4,569</td><td class="n">$14.79</td></tr>
<tr><td class="lbl">String Cheese Incident (two nights)</td><td class="n">1,245</td><td class="n">$17,773</td><td class="n">$14.28</td></tr>
<tr><td class="lbl">Vandelux</td><td class="n">702</td><td class="n">$9,711</td><td class="n">$13.83</td></tr>
<tr><td class="lbl">Kitchen Dwellers (two nights)</td><td class="n">1,045</td><td class="n">$13,322</td><td class="n">$12.75</td></tr>
<tr><td class="lbl">Beats Antique</td><td class="n">402</td><td class="n">$4,203</td><td class="n">$10.46</td></tr>
<tr><td class="lbl">Hank Azaria + EZ Street Band</td><td class="n">570</td><td class="n">$4,952</td><td class="n">$8.69</td></tr>
<tr><td class="lbl">The Brothers Comatose</td><td class="n">331</td><td class="n">$2,750</td><td class="n">$8.31</td></tr>
<tr><td class="lbl">Steve Earle (Steddy, Aug 6)</td><td class="n">334</td><td class="n">$2,711</td><td class="n">$8.12</td></tr>
<tr><td class="lbl">Opera Lollipops (Aug 1)</td><td class="n">134</td><td class="n">$484</td><td class="n">$3.61</td></tr>
<tr><td class="lbl">Bodhi &amp; the Rainforest (three shows, family)</td><td class="n">453</td><td class="n">$846</td><td class="n">$1.87</td></tr>
<tr class="b"><td class="lbl">Blended — 14 shows</td><td class="n">6,889</td><td class="n">$83,343</td><td class="n">$12.10</td></tr>
</table></div>
</div>
<div style="flex:0.9">
<p class="tcap">Product mix (July + August, % of bar revenue)</p>
<table>
<tr class="hd"><td>Category</td><td class="n">Units</td><td class="n">% Rev</td></tr>
{mixrows}
</table>
<p class="fine">Item-level POS, categorized by item name; ${mixt:,.0f} of line items over the two months.</p>
</div>
</div>
<p class="note"><b>Genre drives the bar:</b> party and jam shows run $14&ndash;$19/attendee vs $8&ndash;$10 for seated shows and under $4 for family shows &mdash; book the mix, staff accordingly. Beer + cocktails &asymp;56% of summer sales, wine a fifth.</p>
<p class="note">Revenue = GL 4110.11 net of sales tax; operations = Clover POS (successful payments, Denver-time months). Tip rate = card tips on POS sales. Margin vs counted alcohol cost; labor = bar wages attributed by shift (6330.11, $29,914).</p>

<div style="display:flex; gap:20px; margin-top:8px;">
<div style="flex:1.5">
<p class="tcap">Bar by month — full year (revenue GL 4110.11 net of tax; operations Clover POS)</p>
<table>
<tr class="hd"><td>Month</td><td class="n">Bar Rev</td><td class="n">% YTD</td><td class="n">POS Sales</td><td class="n">Avg Ticket</td><td class="n">Card Tip %</td></tr>
{mrows}
<tr class="b"><td class="lbl">Total YTD (Nov&ndash;Aug)</td><td class="n">${tot_rev:,}</td><td class="n">100%</td><td class="n">{tot_n:,}</td><td class="n">${tot_pos/tot_n:,.2f}</td><td class="n">{tot_tip/tot_pos*100:.1f}%</td></tr>
</table>
<p class="note">Three phases: the winter run (Dec&ndash;Mar, 40%), the June launch (28%) and the festival month (19%); August closed the season at 6%. July still holds the highest average ticket of the year at $16.77. Card tips run 14&ndash;20%; April&ndash;May is the shoulder.</p>
</div>
<div style="flex:1">
<p class="tcap">Alpenglow free concert series &mdash; 2026 vs 2025, full seasons</p>
<table>
<tr class="hd"><td>Alpenglow night</td><td class="n">2026</td><td class="n">2025 (same week)</td></tr>
{arows}
<tr class="b"><td class="lbl">Full season (nine nights)</td><td class="n">$99,839</td><td class="n">$99,101</td></tr>
</table>
<p class="note">Nine nights each year, <b>$99,839 vs $99,101 (+1%)</b>. June ran ahead (+23% on the first three nights), July fell behind (&minus;13% on four), and August closed level. Jul 27 (Clay Street Unit) was the biggest night of the season at $16,496. Both years on Clover payments, Denver-time nights.</p>
</div>
</div>

<h3>Audience Feedback — NPS (season to date: responses received May 1 &ndash; Sep 9)</h3>
<div class="kpis">
<div class="kpi"><div class="k">NPS — Season</div><div class="val">+84</div><div class="d">73 responses; SCI run through August</div></div>
<div class="kpi"><div class="k">Promoters</div><div class="val">64 of 73</div><div class="d">3 detractors</div></div>
<div class="kpi"><div class="k">Avg Score</div><div class="val">9.4</div><div class="d">latest batch 9.8, zero detractors</div></div>
<div class="kpi"><div class="k">All-Time NPS</div><div class="val">+80</div><div class="d">837 responses</div></div>
</div>
<div style="display:flex;gap:20px">
<div style="flex:1">
<p class="tcap">What guests loved</p>
<p class="note"><b>Bodhi &amp; the Rainforest</b> owns the latest batch: &ldquo;the setting, the set, the children, the story &mdash; all so heartwarming,&rdquo; &ldquo;the community coming together to support the arts,&rdquo; and thanks for &ldquo;more affordable events these past couple years.&rdquo; Earlier in the season: intimacy and artist quality, the staff, the venue, the sound.</p>
</div>
<div style="flex:1">
<p class="tcap">What they&rsquo;d improve</p>
<p class="note">Children's ticket pricing for a family show; floor lighting to find seats; parking, with a request to bring the RTA bus to the door; earlier in the season, bar lines at doors and GA sightlines at full houses.</p>
</div>
</div>
<p class="fine">Source: post-event survey (surveys.nps_responses), anonymized verbatims; May n=5, June n=30, July&ndash;August n=38. Surveys follow each event.</p>

<div class="pb"></div>
'''
NEW = cut(NEW, '<div class="sechead"><div><div class="eb">Section 5.0</div>', '<div class="sechead"><div><div class="eb">Section 6.0</div>', esc(BAR))

# ------------------------------------------------------------------ 9. rentals
RENT_EV = [("School of Dance (studio + event rentals, Move the Butte)",35602),("McCoy Wedding",8822),("Wild Hare (studio)",7495),("Gunnison Valley Health Foundation gala (Aug 7)",6000),("Public Policy Forum sessions",5600),("Georgitsis rehearsal dinner (Jul 23)",5300),("Cornish Wedding",5300),("KBUT",5000),("Pete Basile Memorial",4148),("Crested Butte Wildflower Festival",2800),("Community Foundation of the Gunnison Valley",2763),("Bruce Eckel",2206),("Trailhead Children's Museum",1900),("Town of Crested Butte",1367),("Smaller rentals (27 renters, rooms and celebrations of life)",0),("Rentals overhead / not event-tagged",10452)]
known = sum(v for _, v in RENT_EV); RENT_EV[-2] = (RENT_EV[-2][0], round(114857 - known))
rrows = "\n".join(f'<tr><td class="lbl">{n}</td><td class="n">${v:,}</td></tr>' for n, v in RENT_EV)
RENT = f'''<div class="sechead"><div><div class="eb">Section 6.0</div><div class="tt">Rentals</div></div><div class="bn">6.</div></div>
<div class="lede">Rental income of <b>$114,857</b> is <b>&minus;20% vs the phased budget and &minus;35% YoY</b>. Two things sit behind it: the summer calendar went to the Center's own events, and <b>$134,937 of rental cash is already collected and deferred</b> for fall weddings and events not yet held. The signed September to December book is <b>$102,658</b>, of which <b>$80,432</b> is in hand.</div>

<div class="kpis">
<div class="kpi"><div class="k">Rental Income YTD</div><div class="val">$114,857</div><div class="d">&minus;20% vs budget &middot; &minus;35% YoY</div></div>
<div class="kpi"><div class="k">Deferred for Fall</div><div class="val">$134,937</div><div class="d">collected, recognizes at the events</div></div>
<div class="kpi"><div class="k">Signed Sep&ndash;Dec Book</div><div class="val">$102,658</div><div class="d">$80,432 already collected</div></div>
<div class="kpi"><div class="k">Contracted into FY27</div><div class="val">$97,355</div><div class="d">$27,550 of deposits held</div></div>
</div>

<h3>Recognized Rental Revenue (QuickBooks)</h3>
<table>
<tr class="hd"><td>Line</td><td class="n">FY26 YTD</td><td class="n">Budget YTD</td><td class="n v">Var $</td><td class="n">Prior YTD</td><td class="n v">YoY $</td><td class="n v">YoY %</td></tr>
<tr><td class="lbl">Facility Fees</td><td class="n">$95,464</td><td class="n">$143,900</td><td class="n v">($48,436)</td><td class="n">$155,889</td><td class="n v">($60,425)</td><td class="n v">-39%</td></tr>
<tr><td class="lbl">Staffing Fees</td><td class="n">$19,393</td><td class="n">n/b</td><td class="n v"></td><td class="n">$19,754</td><td class="n v">($361)</td><td class="n v">-2%</td></tr>
<tr class="b"><td class="lbl">Total Rental Income</td><td class="n">$114,857</td><td class="n">$143,900</td><td class="n v">($29,043)</td><td class="n">$175,643</td><td class="n v">($60,786)</td><td class="n v">-35%</td></tr>
<tr><td class="lbl">Hosted Bar (sales + service fee)</td><td class="n">$35,424</td><td class="n">$71,000</td><td class="n v">($35,576)</td><td class="n">$51,688</td><td class="n v">($16,264)</td><td class="n v">-31%</td></tr>
<tr class="b"><td class="lbl">Total Rental-Related Revenue</td><td class="n">$150,281</td><td class="n">$214,900</td><td class="n v">($64,619)</td><td class="n">$227,331</td><td class="n v">($77,050)</td><td class="n v">-34%</td></tr>
</table>
<p class="fine">Budget carries all rental income on the Facility line, so line-level variance is mix. The $15,215 posted at the 4150 parent last month has been recoded to its sub-lines. Hosted bar is booked at the contract base, before gratuity and tax, and August added $11,205 on the GVH gala and the rehearsal dinner.</p>

<h3>Rental Revenue by Event — Actual (Nov&ndash;Aug)</h3>
<div class="compact"><table>
<tr class="hd"><td>Event / renter</td><td class="n">Actual Revenue</td></tr>
{rrows}
<tr class="b"><td class="lbl">Total Rental Income</td><td class="n">$114,857</td></tr>
</table></div>
<p class="fine">Budgeted in aggregate, not per event. Every rental line now carries a renter; the untagged share fell from roughly half to 9% with the August customer clean-up.</p>
<h3>Building Utilization — All 14 Room Calendars (Nov 1 &ndash; Jun 30), Real Activity Only</h3>
<div class="kpis">
<div class="kpi"><div class="k">Days in Real Use</div><div class="val">231 / 242</div><div class="d">95% &mdash; events, rentals &amp; classes</div></div>
<div class="kpi"><div class="k">Studio Sessions</div><div class="val">570+</div><div class="d">SOD + Wild Hare; multiple classes per block</div></div>
<div class="kpi"><div class="k">Real Events &amp; Rentals</div><div class="val">445</div><div class="d">171 distinct event days</div></div>
<div class="kpi"><div class="k">Excluded as Non-Events</div><div class="val">306</div><div class="d">internal mtgs, backstage, theater changes</div></div>
</div>
<p class="note">Counts reflect <b>real activity only</b>: excluded are 84 conference-room internal meetings, 140 backstage green/dressing-room holds, 74 theater-change and setup blocks, and 8 internal-titled bookings. Studio blocks each contain multiple classes, so the true class count exceeds 570. <b>The July and August calendar detail lands with the October report as a full-season view.</b></p>
<h3>Real Events &amp; Rentals by Type (Nov&ndash;Jun)</h3>
<div class="compact"><table>
<tr class="hd"><td>Type</td><td class="n">Bookings</td><td class="n">Event Days</td></tr>
<tr><td class="lbl">School, Youth &amp; Dance (SOD, Wild Hare performances)</td><td class="n">153</td><td class="n">87</td></tr>
<tr><td class="lbl">Room rentals (studios, meetings, workshops)</td><td class="n">60</td><td class="n">42</td></tr>
<tr><td class="lbl">Concerts &amp; performances</td><td class="n">59</td><td class="n">28</td></tr>
<tr><td class="lbl">Community events (rentals &amp; one-offs)</td><td class="n">40</td><td class="n">22</td></tr>
<tr><td class="lbl">Literary (Mountain Words &amp; author events)</td><td class="n">26</td><td class="n">5</td></tr>
<tr><td class="lbl">Weddings &amp; receptions</td><td class="n">19</td><td class="n">6</td></tr>
<tr><td class="lbl">Gallery &amp; art openings</td><td class="n">15</td><td class="n">12</td></tr>
<tr><td class="lbl">Film screenings</td><td class="n">8</td><td class="n">5</td></tr>
<tr><td class="lbl">Memorials &amp; celebrations of life</td><td class="n">7</td><td class="n">5</td></tr>
<tr><td class="lbl">Other</td><td class="n">58</td><td class="n">42</td></tr>
<tr class="b"><td class="lbl">Total Real Events &amp; Rentals</td><td class="n">445</td><td class="n">171</td></tr>
</table></div>

<div class="pb"></div>
'''
NEW = cut(NEW, '<div class="sechead"><div><div class="eb">Section 6.0</div>', '<div class="sechead"><div><div class="eb">Section 7.0</div>', esc(RENT))

# ------------------------------------------------------------------ 10. forward book
FWD = [("Wedding &mdash; Schreier","Sep 19","Final invoice",33710,33710),("Wedding &mdash; Hoffmeister","Sep 29","Deposit 1",11760,11760),("Wedding &mdash; Steinbach","Sep 4","Deposit 1",11380,11380),("Gibson Welcome Party","Oct 2","Deposit 1",10518,3500),("Celebration of Life &mdash; Petito","Sep 6","Final invoice",8608,1000),("CB Film Festival 2026","Sep 24","Deposit 1",7672,7672),("COSA Networking &amp; Film Screening","Oct 5","Deposit 2",6500,2000),("Celebration of Life &mdash; Steinberger","Sep 20","Deposit 2",3620,3620),("Film Screening &mdash; Girl Winter Film Tour","Dec 4","Deposit 1",3500,2250),("Platform Partners Conference","Sep 21","Final invoice",2440,2440),("Matchstick Productions film screening","Oct 3","Deposit 2",1000,0),("Zeeco corporate retreat (room)","Oct 7","Deposit 2",850,0),("Smaller signed bookings (3 rooms, training)","Sep&ndash;Nov","Sent",1100,1100)]
ft = sum(x[3] for x in FWD); fc = sum(x[4] for x in FWD)
frows = "\n".join(f'<tr><td class="lbl">{n}</td><td class="n">{d}</td><td class="n">{s}</td><td class="n">${v:,}</td><td class="n">${c:,}</td></tr>' for n,d,s,v,c in FWD)
FY27 = [("Wedding &mdash; Abele","Aug 6, 2027","Wedding",31400,6000),("Wedding &mdash; Friedman &amp; Abbott","Aug 14, 2027","Wedding",30850,8500),("Wedding &mdash; Lueckemeyer / Irby","Oct 1, 2027","Wedding",18055,4750),("Wedding &mdash; Emily &amp; Sam","Apr 3, 2027","Wedding",11000,3500),("Film Screening &mdash; Girl Winter Film Tour","Dec 4, 2026","Private",3500,2250),("Alpenglow Stage &mdash; Oh Be Joyful Church Service","Jul 4, 2027","Community",1350,1350),("Wildflowers Photography Workshop","Oct 3, 2027","Room",700,700),("Mountain Express Winter Training","Nov 23, 2026","Room",500,500)]
f27t = sum(x[3] for x in FY27); f27d = sum(x[4] for x in FY27)
f27rows = "\n".join(f'<tr><td class="lbl">{n}</td><td class="n">{d}</td><td class="n">{t}</td><td class="n">${v:,}</td><td class="n">${c:,}</td></tr>' for n,d,t,v,c in FY27)
FWDS = f'''<div class="sechead"><div><div class="eb">Section 7.0</div><div class="tt">Forward Book</div></div><div class="bn">7.</div></div>
<h3>Forward Rental Pipeline (EventTemple) — September through December 2026</h3>
<table>
<tr class="hd"><td>Signed booking (definite)</td><td class="n">Date</td><td class="n">Stage</td><td class="n">Contract Value</td><td class="n">Collected</td></tr>
{frows}
<tr class="b"><td class="lbl">Total signed, Sep 1 &ndash; Dec 31 2026</td><td class="n"></td><td class="n"></td><td class="n">${ft:,}</td><td class="n">${fc:,}</td></tr>
</table>
<p class="note">Signed-and-priced only, as of August 31; internal Center events (Mary Roach, Fall Folk, Creede Repertory, Makers Market, KPop Dance Party) excluded. <b>Weddings = 55% of the signed book</b>, and 78% of the book is already collected. Four tentative bookings worth &plusmn;$33k (Jackson &amp; Jess, HOA night, Hillenbrand, CBAC) are not counted.</p>
<p class="note">EventTemple values at invoicing; QuickBooks is the authoritative rental figure, ET is pipeline and volume. Steinbach (Sep 4) and Petito (Sep 6) have since taken place and recognize in September.</p>

<h3>Contracted into FY27 — Signed Bookings Beyond November 1, 2026 (EventTemple)</h3>
<table>
<tr class="hd"><td>Booking</td><td class="n">Date</td><td class="n">Type</td><td class="n">Contract Value</td><td class="n">Deposits Held</td></tr>
{f27rows}
<tr class="b"><td class="lbl">Total contracted (priced)</td><td class="n"></td><td class="n"></td><td class="n">${f27t:,}</td><td class="n">${f27d:,}</td></tr>
</table>
<p class="note"><b>Weddings book a year out</b>: the Friedman &amp; Abbott wedding (Aug 2027) signed in August with an $8,500 deposit. &plusmn;$115k of further FY27 proposals are active (seven weddings and dinners, two conferences). Calendar anchors: Mountain Words (May 20&ndash;23), Alpenglow opens Jun 14, Arts Ball hold Jul 8, W+FF hold Jul 11&ndash;17; Prism holds include <b>String Cheese Dec 17&ndash;20</b>.</p>
<div class="lede">With the summer season closed, the back two months of the fiscal year rest on the fall rental book, the fall concert presales, and year-end giving. A meaningful base is already committed or collected.</div>
<h3>Revenue Already Committed for Future Periods</h3>
<div class="kpis">
<div class="kpi"><div class="k">Deferred Revenue (collected)</div><div class="val">$149,138</div><div class="d">rentals $134,937 + tickets $14,201</div></div>
<div class="kpi"><div class="k">Fall Shows Presold</div><div class="val">$14,201</div><div class="d">Humanitix funds held at 8/31</div></div>
<div class="kpi"><div class="k">Sep&ndash;Oct Rental Book</div><div class="val">$98,658</div><div class="d">signed, vs $49,420 of budget left</div></div>
<div class="kpi"><div class="k">Front Row in Conversation</div><div class="val">2</div><div class="d">designations discussed for fall</div></div></div>

<h3>FY26 Rental Outlook vs Budget</h3>
<div class="compact"><table>
<tr class="hd"><td>Rental-related revenue (4150 + hosted bar)</td><td class="n">Amount</td><td class="n">Budget</td><td class="n v">Var</td></tr>
<tr><td class="lbl">Recognized Nov 1 &ndash; Aug 31</td><td class="n">$150,281</td><td class="n">$214,900</td><td class="n v">($64,619)</td></tr>
<tr><td class="lbl">Remaining FY26 budget (Sep&ndash;Oct: facility $36,000 + hosted bar $13,420)</td><td class="n"></td><td class="n">$49,420</td><td class="n v"></td></tr>
<tr><td class="lbl">Signed Sep&ndash;Oct book, contract value (of which $77,082 collected)</td><td class="n">$98,658</td><td class="n"></td><td class="n v"></td></tr>
<tr class="b"><td class="lbl">Full-year FY26 budget</td><td class="n"></td><td class="n">$264,320</td><td class="n v"></td></tr>
</table></div>
<p class="fine">Read: the signed September to October book is twice the rental budget left for the year, so facility income closes the gap on plan only partly &mdash; the full-year line will land near $215k against $264k budgeted, because the summer months went to the Center's own events. <b>Hosted bar is the weak line</b>: $35.4k against an $84.4k full-year budget. Contract values include service components billed with events.</p>
<div class="pb"></div>
'''
NEW = cut(NEW, '<div class="sechead"><div><div class="eb">Section 7.0</div>', '<div class="sechead"><div><div class="eb">Section 8.0</div>', esc(FWDS))

# ------------------------------------------------------------------ 11. donor intelligence
DON = '''<div class="sechead"><div><div class="eb">Section 8.0</div><div class="tt">Donor Intelligence</div></div><div class="bn">8.</div></div>
<div class="lede">Ten months in, the donor base is <b>broader and more concentrated at once</b>. <b>119 new donors</b> have given for the first time this year with <b>$197,290</b> of first-year giving; total donors are up to <b>405</b> (398 last year); and the unrenewed pipeline is down to <b>225 donors / &plusmn;$525k</b>. The top ten now carry <b>36%</b> of CRM cash (31% last year) as the Ball's major gifts and stock transfers landed. The remaining re-engagement window is the fall appeal and year-end.</div>

<div class="kpis">
<div class="kpi"><div class="k">New Donors (FY26 YTD)</div><div class="val">119</div><div class="d">$197,290 first-year giving</div></div>
<div class="kpi"><div class="k">Not Yet Renewed</div><div class="val">225</div><div class="d">&plusmn;$525k prior giving</div></div>
<div class="kpi"><div class="k">New Prospects (Hot/Warm)</div><div class="val">2,889</div><div class="d">scored, never given</div></div>
<div class="kpi"><div class="k">Upgrade Tier</div><div class="val">165</div><div class="d">current donors, 39 at top capacity</div></div>
</div>
<div class="kpis">
<div class="kpi"><div class="k">Donors YTD</div><div class="val">405</div><div class="d">+2% vs 398 last year</div></div>
<div class="kpi"><div class="k">Retention to Date</div><div class="val">43%</div><div class="d">173 of 398 FY25 donors; rises through year-end</div></div>
<div class="kpi"><div class="k">Median Gift</div><div class="val">$759</div><div class="d">vs $1,000 last year</div></div>
<div class="kpi"><div class="k">Top-10 Share</div><div class="val">36%</div><div class="d">of CRM cash, vs 31% last year</div></div>
</div>

<h3>Donor Base Health — Giving Pyramid (Nov&ndash;Aug, CRM cash received)</h3>
<table>
<tr class="hd"><td>Gift band (per-donor total)</td><td class="n">FY26 Donors</td><td class="n">FY26 $</td><td class="n">FY25 Donors</td><td class="n">FY25 $</td><td class="n">Read</td></tr>
<tr><td class="lbl">$25,000+</td><td class="n">18</td><td class="n">$930,923</td><td class="n">18</td><td class="n">$792,218</td><td class="n">Ball major gifts and stock now in</td></tr>
<tr><td class="lbl">$10,000 &ndash; $24,999</td><td class="n">42</td><td class="n">$558,261</td><td class="n">42</td><td class="n">$567,426</td><td class="n">core held</td></tr>
<tr><td class="lbl">$5,000 &ndash; $9,999</td><td class="n">26</td><td class="n">$152,335</td><td class="n">38</td><td class="n">$229,219</td><td class="n">soft &mdash; upgrade focus</td></tr>
<tr><td class="lbl">$1,000 &ndash; $4,999</td><td class="n">112</td><td class="n">$186,135</td><td class="n">118</td><td class="n">$215,081</td><td class="n">soft &mdash; upgrade focus</td></tr>
<tr><td class="lbl">$250 &ndash; $999</td><td class="n">80</td><td class="n">$35,165</td><td class="n">82</td><td class="n">$39,319</td><td class="n">steady</td></tr>
<tr><td class="lbl">Under $250</td><td class="n">127</td><td class="n">$13,077</td><td class="n">100</td><td class="n">$9,386</td><td class="n"><b>base broadening +27%</b></td></tr>
<tr class="b"><td class="lbl">Total</td><td class="n">405</td><td class="n">$1,875,896</td><td class="n">398</td><td class="n">$1,852,649</td><td class="n"></td></tr>
</table>
<p class="note"><b>Top and bottom grew, the middle is soft:</b> the $25k+ band is up $139k on the same 18 donors, entry-level donors are up 27%, and the $1k&ndash;$10k middle (138 vs 156) remains the upgrade target. CRM cash is now within <b>$49k (2.6%)</b> of the books' $1,925,362 of contributed revenue plus Front Row, down from a $159k gap last month as the Ball entry backlog cleared.</p>
<p class="note"><b>Counts are floors.</b> Basis: Bloomerang payments (donations, pledge and recurring payments; pledge commitments excluded) through 8/31, both years on the same window. Presentation-only; no records changed.</p>

<h3>Retention — Donors Who Gave Last Year, Not Yet This Year</h3>
<table>
<tr class="hd"><td>Prior-Year Giving Tier</td><td class="n">Donors</td><td class="n">Prior-Year $</td><td class="lbl2">Priority</td></tr>
<tr><td class="lbl">$10,000+</td><td class="n">18</td><td class="n">$277,477</td><td class="lbl2" style="padding-left:12px">Personal / ED outreach now</td></tr>
<tr><td class="lbl">$5,000 &ndash; $9,999</td><td class="n">15</td><td class="n">$91,569</td><td class="lbl2" style="padding-left:12px">Personal outreach + event invite</td></tr>
<tr><td class="lbl">$1,000 &ndash; $4,999</td><td class="n">73</td><td class="n">$121,836</td><td class="lbl2" style="padding-left:12px">Targeted appeal / call</td></tr>
<tr><td class="lbl">Under $1,000</td><td class="n">119</td><td class="n">$34,111</td><td class="lbl2" style="padding-left:12px">Annual appeal</td></tr>
<tr class="b"><td class="lbl">Total re-engagement pipeline</td><td class="n">225</td><td class="n">$524,993</td><td class="lbl2"></td></tr>
</table>
<p class="note">A re-engagement worklist, not attrition &mdash; twelve more prior-year donors renewed in August; year-end giving is still ahead. The <b>18 lapsed $10k+ donors</b> are unchanged since July and remain the priority; named list available to Development.</p>

<h3>New Potential Donors — Prospect Model (~23,000 scored across giving, events, email, property &amp; public records)</h3>
<table>
<tr class="hd"><td>Signal (among never-given prospects)</td><td class="n">Count</td><td class="lbl2">Why it matters</td></tr>
<tr><td class="lbl">Own property valued $2M+</td><td class="n">224</td><td class="lbl2" style="padding-left:12px">Wealth capacity</td></tr>
<tr><td class="lbl">Documented public / political giving</td><td class="n">411</td><td class="lbl2" style="padding-left:12px">Demonstrated charitable behavior</td></tr>
<tr><td class="lbl">Give to peer arts / cultural orgs</td><td class="n">118</td><td class="lbl2" style="padding-left:12px">Proven local philanthropy</td></tr>
<tr><td class="lbl">Business owners</td><td class="n">750</td><td class="lbl2" style="padding-left:12px">Corporate sponsorship angle</td></tr>
<tr><td class="lbl"><b>Upgrade tier (current donors, capacity above giving)</b></td><td class="n">165</td><td class="lbl2" style="padding-left:12px">Ask for more, warm relationship</td></tr>
</table>
<p class="note">The model ranks every constituent on capacity + engagement across Bloomerang giving, Humanitix attendance, Mailchimp engagement, Gunnison County property records, and state/federal public-giving data. It flags <b>2,889 Hot or Warm prospects who have never given</b> (1,315 Hot). The fall appeal is the natural moment for the property-owning and peer-org segments above. Ranked, named cultivation lists can be pulled for the Development team as a separate working document.</p>
<p class="fine">Prospect figures are for internal cultivation planning and draw on wealth-screening and public-records data; they do not reconcile to QuickBooks contributed revenue and should not be cited as financial figures. Individual names and capacity detail are held in the Development working file, not this report.</p>


<div class="pb"></div>
<div class="sechead"><div><div class="eb">Section 9.0</div><div class="tt">Year-End Projection</div></div><div class="bn">9.</div></div>
<div class="lede">Ten months are booked. September and October are built bottom-up from the fall calendar (18 programming dates), the Event Temple book (definite bookings at 100%, tentative at 50%), the Gusto pay calendar (four runs), and run rates for the steady lines, with depreciation, the donated lease and the in-kind valuation booked in October as in FY25. The result is a year that <b>breaks even before depreciation</b> after a record summer, because the post-season cost base outruns a quiet fall.</div>
<div class="kpis">
<div class="kpi"><div class="k">FY26 Before Depreciation</div><div class="val">$22,887</div><div class="d">budget $242,426 &middot; FY25 $284,811</div></div>
<div class="kpi"><div class="k">FY26 Full Accrual</div><div class="val">($582,818)</div><div class="d">after $605,705 depreciation and lease</div></div>
<div class="kpi"><div class="k">Cash at October 31</div><div class="val">$496,706</div><div class="d">from $605,746 at 8/31 &middot; $455,001 a year ago</div></div>
<div class="kpi"><div class="k">Sept + Oct Net</div><div class="val">($200,789)</div><div class="d">before depreciation; $224k income, $371k spend</div></div>
</div>
<div class="stitle">Statement of Activities &mdash; Projected Year End</div>
<div class="compact"><table>
<tr class="hd"><td>Income</td><td class="n">Nov&ndash;Aug actual</td><td class="n">Sept + Oct</td><td class="n">FY26 projected</td><td class="n">FY26 budget</td><td class="n v">vs budget</td><td class="n">FY25 actual</td></tr>
<tr><td class="lbl">Contributed Revenue</td><td class="n">$1,665,362</td><td class="n">$16,718</td><td class="n">$1,682,080</td><td class="n">$1,636,234</td><td class="n v">$45,846</td><td class="n">$1,412,747</td></tr>
<tr><td class="lbl">Earned Revenue</td><td class="n">$1,106,468</td><td class="n">$207,441</td><td class="n">$1,313,909</td><td class="n">$1,208,799</td><td class="n v">$105,110</td><td class="n">$1,141,579</td></tr>
<tr><td class="lbl">Front Row</td><td class="n">$260,000</td><td class="n">$0</td><td class="n">$260,000</td><td class="n">$400,000</td><td class="n v">($140,000)</td><td class="n">$490,000</td></tr>
<tr class="b"><td class="lbl">Total Income</td><td class="n">$3,031,830</td><td class="n">$224,159</td><td class="n">$3,255,989</td><td class="n">$3,245,033</td><td class="n v">$10,956</td><td class="n">$3,044,327</td></tr>
<tr><td class="lbl">Cost of Sales</td><td class="n">$208,031</td><td class="n">$42,238</td><td class="n">$250,269</td><td class="n">$168,660</td><td class="n v">$81,609</td><td class="n">$183,693</td></tr>
<tr class="b"><td class="lbl">Gross Surplus</td><td class="n">$2,823,799</td><td class="n">$181,921</td><td class="n">$3,005,720</td><td class="n">$3,076,373</td><td class="n v">($70,653)</td><td class="n">$2,860,634</td></tr>
<tr class="hd2"><td colspan="7">Expenses</td></tr>
<tr><td class="lbl">Administrative</td><td class="n">$110,528</td><td class="n">$22,055</td><td class="n">$132,583</td><td class="n">$132,337</td><td class="n v">$246</td><td class="n">$134,133</td></tr>
<tr><td class="lbl">Building</td><td class="n">$304,866</td><td class="n">$115</td><td class="n">$304,981</td><td class="n">$305,823</td><td class="n v">($842)</td><td class="n">$314,806</td></tr>
<tr><td class="lbl">Marketing</td><td class="n">$111,121</td><td class="n">$9,706</td><td class="n">$120,827</td><td class="n">$123,785</td><td class="n v">($2,958)</td><td class="n">$120,478</td></tr>
<tr><td class="lbl">Payroll</td><td class="n">$1,138,348</td><td class="n">$207,013</td><td class="n">$1,345,361</td><td class="n">$1,376,445</td><td class="n v">($31,084)</td><td class="n">$1,286,208</td></tr>
<tr><td class="lbl">Programming</td><td class="n">$875,728</td><td class="n">$89,759</td><td class="n">$965,487</td><td class="n">$818,865</td><td class="n v">$146,622</td><td class="n">$733,359</td></tr>
<tr class="b"><td class="lbl">Total Expenses</td><td class="n">$2,540,591</td><td class="n">$328,648</td><td class="n">$2,869,239</td><td class="n">$2,757,255</td><td class="n v">$111,984</td><td class="n">$2,588,984</td></tr>
<tr class="b"><td class="lbl">Operating Surplus/(Deficit)</td><td class="n">$283,208</td><td class="n">($146,727)</td><td class="n">$136,481</td><td class="n">$319,118</td><td class="n v">($182,637)</td><td class="n">$271,650</td></tr>
<tr><td class="lbl">Other Revenue (net, incl. in-kind valuation)</td><td class="n">$28,781</td><td class="n">$181,294</td><td class="n">$210,075</td><td class="n">$213,793</td><td class="n v">($3,718)</td><td class="n">$319,174</td></tr>
<tr><td class="lbl">Other Expenses before depreciation (interest, in-kind, adjustments)</td><td class="n">$88,313</td><td class="n">$235,356</td><td class="n">$323,669</td><td class="n">$290,485</td><td class="n v">$33,184</td><td class="n">$306,013</td></tr>
<tr class="b"><td class="lbl">Net Revenue before Depreciation</td><td class="n">$223,676</td><td class="n">($200,789)</td><td class="n">$22,887</td><td class="n">$242,426</td><td class="n v">($219,539)</td><td class="n">$284,811</td></tr>
<tr><td class="lbl">Depreciation and donated lease (October 31)</td><td class="n">$0</td><td class="n">$605,705</td><td class="n">$605,705</td><td class="n">not budgeted</td><td class="n v"></td><td class="n">$605,705</td></tr>
<tr class="b"><td class="lbl">Total Net Revenue / Change in Net Assets</td><td class="n">$223,676</td><td class="n">($806,494)</td><td class="n">($582,818)</td><td class="n">$242,426</td><td class="n v"></td><td class="n">($320,894)</td></tr>
</table></div>
<p class="fine">Budget = the QBO "FY26 - Consolidated" object, full year; it carries no depreciation line, so the comparison stops at net revenue before depreciation. FY25 shown as booked. The in-kind valuation ($195,793 each side) sits in other revenue and other expense in October and nets to zero.</p>

<div class="half">
<div>
<div class="stitle">What September and October Carry</div>
<div class="compact"><table>
<tr class="hd"><td>Piece</td><td class="n">Amount</td><td class="lbl2">Basis</td></tr>
<tr><td class="lbl">Payroll, four runs</td><td class="n">$207,013</td><td class="lbl2">Salaried $24,960 a run, steady hourly, event hourly from the event table</td></tr>
<tr><td class="lbl">Programming, 18 dates</td><td class="n">$89,759</td><td class="lbl2">Presenter fees $35,683, production rentals $26,548, consulting and materials</td></tr>
<tr><td class="lbl">Fall tickets</td><td class="n">$85,814</td><td class="lbl2">$8,823 presold; Firebird, LVDY, Creede Rep, Rocky Horror, Ditchwalkers, Halloween</td></tr>
<tr><td class="lbl">Event Temple rentals and hosted bar</td><td class="n">$79,820</td><td class="lbl2">Contracted: Schreier, Steinbach, Hoffmeister, Film Festival, Gibson, four celebrations</td></tr>
<tr><td class="lbl">Cash bar and alcohol cost</td><td class="n">$17,873 / ($22,770)</td><td class="lbl2">FY25 fall pattern; alcohol at the counted 38% rate</td></tr>
<tr><td class="lbl">Contributed revenue</td><td class="n">$16,718</td><td class="lbl2">FY25 fall pattern; year-end giving lands in FY27</td></tr>
<tr><td class="lbl">Year-end adjustments</td><td class="n">($44,684)</td><td class="lbl2">Midpoint of FY24 and FY25; the real entries are an open call</td></tr>
<tr><td class="lbl">Insurance true-up</td><td class="n">$52,231</td><td class="lbl2">Prepaid at 10/31 $12,460, finance charge $1,560, and the $38,211 duplicate PHLY payment treated as recoverable</td></tr>
</table></div>
</div>
<div>
<div class="stitle">Open Calls That Move the Number</div>
<ul style="font-size:9px;">
<li><b>Philadelphia Insurance $38,211</b> paid June 23 on top of the AFCO plan. Projected as a receivable; if no refund, the year is $38k worse.</li>
<li><b>Year-end adjustments $44,684 plug.</b> Pledge allowance reset (today a $31,895 net debit), gala receivable write-offs, audit entries.</li>
<li><b>Fall event hourly</b> at $28,702 from the event table against $35,210 in the last two Gusto runs.</li>
<li><b>Front Row.</b> $260,000 holds unless a fall designation lands; two are in conversation.</li>
<li><b>Fall lineup</b> complete? Vinotok carries no dollars; artist settlements for two August shows are not yet booked.</li>
</ul>
</div>
</div>

<div class="stitle">Cash Through Year End and Into FY27</div>
<div class="compact"><table>
<tr class="hd"><td>Bank and brokerage cash at month end</td><td class="n">Nov</td><td class="n">Dec</td><td class="n">Jan</td><td class="n">Feb</td><td class="n">Mar</td><td class="n">Apr</td><td class="n">May</td><td class="n">Jun</td><td class="n">Jul</td><td class="n">Aug</td><td class="n">Sep</td><td class="n">Oct</td></tr>
<tr><td class="lbl">FY26 (Nov&ndash;Aug booked; Sept and Oct projected)</td><td class="n">$420,380</td><td class="n">$445,831</td><td class="n">$410,323</td><td class="n">$239,943</td><td class="n">$422,606</td><td class="n">$486,289</td><td class="n">$560,833</td><td class="n">$489,972</td><td class="n">$612,778</td><td class="n">$605,746</td><td class="n">$557,101</td><td class="n">$496,706</td></tr>
<tr><td class="lbl">FY27 draft</td><td class="n">$418,779</td><td class="n">$515,226</td><td class="n">$425,077</td><td class="n">$403,475</td><td class="n">$617,085</td><td class="n">$712,742</td><td class="n">$797,659</td><td class="n">$705,421</td><td class="n">$748,028</td><td class="n">$739,936</td><td class="n">$670,597</td><td class="n">$625,949</td></tr>
<tr><td class="lbl">FY25 actual</td><td class="n">$82,988</td><td class="n">$298,351</td><td class="n">$299,687</td><td class="n">$245,709</td><td class="n">$320,315</td><td class="n">$356,028</td><td class="n">$225,268</td><td class="n">$361,509</td><td class="n">$874,325</td><td class="n">$651,828</td><td class="n">$527,980</td><td class="n">$372,286</td></tr>
</table></div>
<p class="note"><b>August 31 to October 31:</b> $605,746 less the $200,789 operating loss for the two months, plus $56,750 of Front Row installments (Bailey, Clark, Liebl, Stroh and half of three late payers), plus $100,000 of receivables collected (Humanitix, the Event Temple invoices due in September, the gala pledges still open), less $70,000 of deferred revenue recognized as the fall weddings and shows happen, plus $5,000 of year-end accruals = <b>$496,706</b>. The low point of FY26 was February at $239,943; the FY27 draft bottoms at $403,475 in February and ends at $625,949 after the January principal payment. Every month of FY26 through August reconciles to the books.</p>
<p class="fine">Front Row cash is now scheduled member by member from the payment history in both receivable accounts: 15 members current, four due this September or October, three late, five behind on their FY26 installment (counted at half), two dormant (counted at zero), three new pledges. FY26 collections project to $257,876 and FY27 to $317,876 including $30,000 on three planned new pledges; the earlier on-schedule figure was $348,500.</p>

<div class="pb"></div>
<div class="sechead"><div><div class="eb">Section 10.0</div><div class="tt">FY27 Draft Budget</div></div><div class="bn">10.</div></div>
<div class="lede">A first pass, not a recommendation. It seeds each account from the FY26 projection with the build rules the committee has already set: depreciation and the donated lease booked in October, in-kind kept as a zero-sum pair, Front Row planned at three pledges of $100,000, the capital campaign at zero, bar revenue net of sales tax with alcohol cost at the counted rate, and tips out of the P&amp;L. The one structural move is programming, which the seed brings back toward FY25 scale. The full draft with the programming, rental, payroll and pledge schedules comes to the October meeting.</div>
<div class="kpis">
<div class="kpi"><div class="k">FY27 Operating</div><div class="val">$226,369</div><div class="d">before $605,705 depreciation and lease</div></div>
<div class="kpi"><div class="k">FY27 Full Accrual</div><div class="val">($379,336)</div><div class="d">FY26 projected ($582,818)</div></div>
<div class="kpi"><div class="k">Revenue</div><div class="val">$3.32M</div><div class="d">FY26 projected $3.47M</div></div>
<div class="kpi"><div class="k">Cash at 10/31/2027</div><div class="val">$625,949</div><div class="d">low point $403,475 in February</div></div>
</div>
<div class="stitle">FY27 Draft by Block</div>
<div class="compact"><table>
<tr class="hd"><td>Block</td><td class="n">FY24 actual</td><td class="n">FY25 actual</td><td class="n">FY26 projected</td><td class="n">FY27 draft</td><td class="n v">FY27 vs FY26</td><td class="lbl2">Seed rule</td></tr>
<tr><td class="lbl">4000 Contributed Income</td><td class="n">$1,566,670</td><td class="n">$1,412,747</td><td class="n">$1,682,080</td><td class="n">$1,588,418</td><td class="n v">($93,661)</td><td class="lbl2">FY26 less one-time gifts; Ball at FY26; grants at the FY26 run rate</td></tr>
<tr><td class="lbl">4100 Earned Income</td><td class="n">$1,126,609</td><td class="n">$1,141,579</td><td class="n">$1,313,909</td><td class="n">$1,224,071</td><td class="n v">($89,838)</td><td class="lbl2">Tickets follow the programming seed; rentals from the Event Temple book and FY27 contracts; bar net of tax</td></tr>
<tr><td class="lbl">4200 Front Row</td><td class="n">$385,000</td><td class="n">$490,000</td><td class="n">$260,000</td><td class="n">$300,000</td><td class="n v">$40,000</td><td class="lbl2">Decision 2: three pledges of $100,000</td></tr>
<tr><td class="lbl">7000 Other Income</td><td class="n">$228,608</td><td class="n">$319,174</td><td class="n">$210,075</td><td class="n">$204,293</td><td class="n v">($5,782)</td><td class="lbl2">In-kind $195,793 (zero-sum), interest income</td></tr>
<tr class="b"><td class="lbl">Total Revenue</td><td class="n">$3,306,887</td><td class="n">$3,363,501</td><td class="n">$3,466,064</td><td class="n">$3,316,782</td><td class="n v">($149,282)</td><td class="lbl2"></td></tr>
<tr><td class="lbl">5000 Cost of Goods Sold</td><td class="n">$133,302</td><td class="n">$183,693</td><td class="n">$250,269</td><td class="n">$259,469</td><td class="n v">$9,200</td><td class="lbl2">Alcohol at 38% of bar and hosted revenue; auction lots and merchandise at FY26</td></tr>
<tr><td class="lbl">6000 Administrative</td><td class="n">$179,914</td><td class="n">$134,133</td><td class="n">$132,583</td><td class="n">$141,777</td><td class="n v">$9,194</td><td class="lbl2">FY26 projected plus inflation on services</td></tr>
<tr><td class="lbl">6100 Building</td><td class="n">$293,229</td><td class="n">$314,806</td><td class="n">$304,981</td><td class="n">$313,860</td><td class="n v">$8,878</td><td class="lbl2">Insurance at the renewed premium; utilities at FY26</td></tr>
<tr><td class="lbl">6200 Marketing</td><td class="n">$115,719</td><td class="n">$120,478</td><td class="n">$120,827</td><td class="n">$129,748</td><td class="n v">$8,921</td><td class="lbl2">FY26 projected with the four unnumbered accounts folded in</td></tr>
<tr><td class="lbl">6300 Payroll</td><td class="n">$1,404,857</td><td class="n">$1,286,208</td><td class="n">$1,345,361</td><td class="n">$1,291,936</td><td class="n v">($53,425)</td><td class="lbl2">Payroll Schedule by person; event hourly follows the programming seed; tips out</td></tr>
<tr><td class="lbl">6400 Programming</td><td class="n">$823,382</td><td class="n">$733,359</td><td class="n">$965,487</td><td class="n">$683,850</td><td class="n v">($281,637)</td><td class="lbl2">Programming Schedule: FY26 series at FY26 cost less the one-off headliner; the largest call in the draft</td></tr>
<tr><td class="lbl">8000 Other Expenditures</td><td class="n">$765,364</td><td class="n">$911,718</td><td class="n">$929,374</td><td class="n">$875,479</td><td class="n v">($53,895)</td><td class="lbl2">Depreciation $560,135 and lease $45,570 in October; interest $69,567; in-kind; no adjustments plug</td></tr>
<tr class="b"><td class="lbl">Total Expense</td><td class="n">$3,715,768</td><td class="n">$3,684,395</td><td class="n">$4,048,882</td><td class="n">$3,696,119</td><td class="n v">($352,764)</td><td class="lbl2"></td></tr>
<tr class="b"><td class="lbl">Net, full accrual</td><td class="n">($408,881)</td><td class="n">($320,894)</td><td class="n">($582,818)</td><td class="n">($379,336)</td><td class="n v">$203,482</td><td class="lbl2"></td></tr>
<tr><td class="lbl">of which depreciation and donated lease</td><td class="n">($605,705)</td><td class="n">($605,705)</td><td class="n">($605,705)</td><td class="n">($605,705)</td><td class="n v"></td><td class="lbl2"></td></tr>
<tr class="b"><td class="lbl">Net, operating (before depreciation and lease)</td><td class="n">$196,824</td><td class="n">$284,811</td><td class="n">$22,887</td><td class="n">$226,369</td><td class="n v">$203,482</td><td class="lbl2"></td></tr>
</table></div>
<p class="fine">FY24 and FY25 are the trial balances at fiscal year end; FY26 projected and FY27 draft are the live workbook (FY27 - Budget - CFTA - Draft), which the committee can comment on cell by cell.</p>
<div class="half">
<div>
<div class="stitle">Decisions Already Taken (9/2)</div>
<ul style="font-size:9px;">
<li><b>Depreciation and donated lease:</b> one entry on October 31, FY26 and FY27, at the FY25 amount until the schedule is updated.</li>
<li><b>Front Row:</b> FY26 holds at $260,000; FY27 plans three pledges of $100,000.</li>
<li><b>In-kind:</b> stays in Other Revenue and Other Expenditures as a zero-sum pair at the FY25 valuation.</li>
<li><b>Capital campaign:</b> closed; zero in FY27.</li>
<li><b>Event Temple gratuity:</b> billed after the event, recognized in the event month; no budget line under the net tips model.</li>
<li><b>Kegs:</b> draft beer moves to accrual cost of goods on pours from September.</li>
</ul>
</div>
<div>
<div class="stitle">Calls the Draft Still Needs</div>
<ul style="font-size:9px;">
<li><b>Programming scale.</b> The seed budgets $683,850 against $965,487 this year. Which of the FY26 season repeats, and at what fee level, sets tickets, bar, event payroll and the bottom line.</li>
<li><b>Payroll.</b> $1,291,936 seeded by person; open roles, the benefits review and the wage step for FY27 are not yet in it.</li>
<li><b>Bar pour cost.</b> 38% is what the count says; the draft assumes it holds. Pricing and purchasing changes would move $30k to $50k.</li>
<li><b>Contributed.</b> The Ball at $917k again, grants at the FY26 pace, and the fall appeal: the seed is $1.59M against $1.68M this year.</li>
<li><b>Rentals and hosted bar.</b> $97k already contracted into FY27; the hosted bar line has undershot two years running.</li>
</ul>
</div>
</div>

<div class="foot">Prepared September 9, 2026 from QuickBooks Online (accrual basis) after the August close; budget = FY2026 board-approved, phased YTD from the QBO budget object; prior year = FY2025 same period. Not audited.</div>
'''
NEW = cut(NEW, '<div class="sechead"><div><div class="eb">Section 8.0</div>', '</body></html>"""', esc(DON))
open("build_report.py", "w", encoding="utf-8").write(NEW)
print("wrote build_report.py", len(NEW), "chars; lineup total net", T, "hosp", hosp)
