#!/usr/bin/env python3
"""September 2026 edition, consolidated per Brett 9/9: no signature-events or donor sections; statements on one page;
programming with consolidated concert economics and Alpenglow vs prior years; rentals by bucket, utilization through
August, forward book to fiscal year end plus Nov/Dec; year-end projection one page; FY27 draft one page ("basis", not "seed")."""
import re
exec(open("splice_2026-09-15.py").read().split("# ------------------------------------------------------------------ 2. cover")[0])   # SRC, cut, esc, DATA -> NEW
short = open("splice_2026-09-15_short.py").read()
AGENDA = short.split("AGENDA = '''")[1].split("'''")[0]
EXEC = short.split("EXEC = '''")[1].split("'''")[0]
NEW = NEW.replace('FY2026 Year-to-Date &middot; 08.17.2026', 'FY2026 Year-to-Date &middot; 09.15.2026')
NEW = NEW.replace('Reporting Period &middot; November 1, 2025 &ndash; July 31, 2026 &middot; Accrual Basis', 'Reporting Period &middot; November 1, 2025 &ndash; August 31, 2026 &middot; Accrual Basis')
NEW = NEW.replace('<span>$2.85M revenue &middot; +4% vs budget</span>', '<span>$3.03M revenue &middot; on budget &middot; ten months</span>')
NEW = NEW.replace('"<span>FY2026 Year-to-Date &middot; 08.17.2026</span></div>")', '"<span>FY2026 Year-to-Date &middot; 09.15.2026</span></div>")')
NEW = NEW.replace('<td class="n">Jul 31, 2026</td><td class="n">Jul 31, 2025</td>', '<td class="n">Aug 31, 2026</td><td class="n">Aug 31, 2025</td>')
NEW = NEW.replace('Statement of Financial Position — July 31', 'Statement of Financial Position — August 31')
NEW = NEW.replace('{cfrow("Construction loans, net (FY26: $100k paydown; FY25: $1.0M draw less $950k retirement)","fin")}', '{cfrow("Construction loans, net (FY26: $100k paydown; FY25: $50k net draw)","fin")}')
NEW = NEW.replace('{cfrow("Inventory build &amp; artist advances","inv")}', '{cfrow("Inventory, allowances &amp; other current assets","inv")}')
NEW = cut(NEW, '<div class="sechead"><div><div class="eb">Finance Committee</div><div class="tt">Agenda', '<div class="sechead"><div><div class="eb">Section 1.0</div>', esc(AGENDA))
NEW = cut(NEW, '<div class="sechead"><div><div class="eb">Section 1.0</div>', '<div class="sechead"><div><div class="eb">Section 2.0</div>', esc(EXEC))
STMT_HEAD = '''<div class="sechead"><div><div class="eb">Section 2.0</div><div class="tt">Financial Statements</div></div><div class="bn">2.</div></div>
<p class="fine">Accrual basis, ten months, as booked. Prior months revised since August 17 (Section 1.0). Depreciation and the donated lease are booked October 31 in both years, so every bottom line here is before depreciation.</p>
'''
NEW = cut(NEW, '<div class="sechead"><div><div class="eb">Section 2.0</div>', '<div class="stitle">Statement of Activities — Budget vs. Actual', esc(STMT_HEAD))

def cell(v):
    if v == 0: return "&mdash;"
    return f"(${abs(v):,.0f})" if v < 0 else f"${v:,.0f}"
GROUPS = [("Headline concerts (9 shows)", [(151126,17773,-135500,-8129,0),(35564,13322,-24690,-4488,0),(43673,11266,-15000,-4396,0),(27995,4952,-25742,-2257,0),(24265,9711,-12137,-3714,0),(16132,2711,-20750,-143,-403),(14115,4203,-12100,-2655,0),(10102,2750,-5403,-3826,0),(8867,3699,-5000,-2661,0)]),
          ("Family, classical &amp; theatre (5 shows)*", [(20660,1738,0,-3543,-15859),(6165,745,-600,-753,0),(5376,955,-3000,-1056,0),(9005,846,0,-6651,-352),(3883,484,0,-1505,-629)]),
          ("Community benefit (Ski Patrol)", [(12205,10756,-4000,-6894,-9764)])]
grows = []; T = [0]*6
for name, shows in GROUPS:
    t = sum(s[0] for s in shows); bar = sum(round(s[1]*0.62) for s in shows); fee = sum(s[2] for s in shows); st = sum(s[3] for s in shows); oth = sum(s[4] for s in shows); net = t+bar+fee+st+oth
    for i, v in enumerate((t, bar, fee, st, oth, net)): T[i] += v
    grows.append(f'<tr><td class="lbl">{name}</td><td class="n">{cell(t)}</td><td class="n">{cell(bar)}</td><td class="n">{cell(fee)}</td><td class="n">{cell(st)}</td><td class="n">{cell(oth)}</td><td class="n">{cell(net)}</td></tr>')
AL = [("Jun 15", 9986, 8748, 11044), ("Jun 22", 13308, 10940, 10106), ("Jun 29", 13720, 10342, 11692), ("Jul 6", 7952, 12618, 16249), ("Jul 13", 9596, 13488, 5961), ("Jul 20", 7673, 10246, 17787), ("Jul 27", 16496, 11406, 13960), ("Aug 3", 11686, 11717, 1404), ("Aug 10", 9422, 9595, 9268)]
alrows = "".join(f'<tr><td class="lbl">Night {i+1} ({d} in 2026)</td><td class="n">${a:,}</td><td class="n">${b:,}</td><td class="n">${c:,}</td></tr>' for i, (d, a, b, c) in enumerate(AL))
MONTHS = [("Nov",4969,354,7210.78,791.90),("Dec",12900,880,14078.03,2421.73),("Jan",22069,1473,24422.00,4459.37),("Feb",24669,1707,27315.01,4512.81),("Mar",25452,1648,28315.02,5300.09),("Apr",3450,273,3934.03,765.50),("May",5976,433,6070.50,1102.60),("Jun",59713,4749,66409.54,10965.50),("Jul",40468,3041,50989.00,7259.07),("Aug",13435,1863,26277.01,4163.71)]
PROG = f'''<div class="pb"></div>
<div class="sechead"><div><div class="eb">Section 3.0</div><div class="tt">Programming &amp; Bar</div></div><div class="bn">3.</div></div>
<div class="kpis">
<div class="kpi"><div class="k">Concert Tickets FY26</div><div class="val">$389k</div><div class="d">15 headline shows &middot; 6,889 attendees</div></div>
<div class="kpi"><div class="k">Lineup Net, Direct</div><div class="val">{cell(T[5]-28741).replace("$","$")}</div><div class="d">after $28,741 season hospitality</div></div>
<div class="kpi"><div class="k">Bar Revenue YTD</div><div class="val">$213k</div><div class="d">+ $35k hosted &middot; net of sales tax</div></div>
<div class="kpi"><div class="k">Alcohol Cost</div><div class="val">38%</div><div class="d">of bar revenue, from the 8/31 count</div></div>
</div>
<h3>Concert Economics, FY26 Complete</h3>
<div class="compact"><table><tr class="hd"><td>Group</td><td class="n">Tickets</td><td class="n">Bar (net of alcohol)</td><td class="n">Performer fees</td><td class="n">Show staffing</td><td class="n">Other</td><td class="n">Est. net</td></tr>
{"".join(grows)}
<tr class="b"><td class="lbl">Total, event-identifiable costs</td><td class="n">{cell(T[0])}</td><td class="n">{cell(T[1])}</td><td class="n">{cell(T[2])}</td><td class="n">{cell(T[3])}</td><td class="n">{cell(T[4])}</td><td class="n">{cell(T[5])}</td></tr>
<tr><td class="lbl">Season hospitality (lodging, travel, artist food)</td><td class="n"></td><td class="n"></td><td class="n"></td><td class="n"></td><td class="n"></td><td class="n">($28,741)</td></tr>
<tr class="b"><td class="lbl">Net after hospitality</td><td class="n"></td><td class="n"></td><td class="n"></td><td class="n"></td><td class="n"></td><td class="n">{cell(T[5]-28741)}</td></tr></table></div>
<p class="fine">Headline concerts: String Cheese (two nights), Kitchen Dwellers, Alpenphunk, Azaria, Vandelux, Steve Earle, Beats Antique, Brothers Comatose, Deadhead Ed. Family, classical and theatre: Nutcracker, Pirates of Penzance, Mr. Sun, Bodhi &amp; the Rainforest, Opera Lollipops. Bar = event-night POS net of alcohol cost at the counted 38% (13% in earlier reports). Other = co-production payouts. * Two August artist settlements not yet booked. On the counted rate the Nov&ndash;Jun concert season nets ($21,554) on direct terms against +$24,054 reported in August; direct revenue grew 39% on FY25, pour cost is the fix.</p>
<div class="half">
<div>
<h3>Alpenglow vs. Prior Seasons (bar revenue by night)</h3>
<div class="compact"><table>
<tr class="hd"><td>Night</td><td class="n">2026</td><td class="n">2025</td><td class="n">2024</td></tr>
{alrows}
<tr class="b"><td class="lbl">Season, nine nights</td><td class="n">$99,839</td><td class="n">$99,101</td><td class="n">$97,472</td></tr>
</table></div>
<p class="fine">Clover payments by Denver-time night, all three seasons on the same basis. Flat on 2025; June ran ahead, July behind, August level.</p>
</div>
<div>
<h3>Bar by Month (revenue net of tax; Clover POS)</h3>
<div class="compact"><table>
<tr class="hd"><td>Month</td><td class="n">Revenue</td><td class="n">Transactions</td><td class="n">Avg ticket</td><td class="n">Card tips</td></tr>
{"".join(f'<tr><td class="lbl">{m[0]}</td><td class="n">${m[1]:,}</td><td class="n">{m[2]:,}</td><td class="n">${m[3]/m[2]:.2f}</td><td class="n">{m[4]/m[3]*100:.1f}%</td></tr>' for m in MONTHS)}
<tr class="b"><td class="lbl">Nov&ndash;Aug</td><td class="n">$213,103</td><td class="n">16,421</td><td class="n">$15.53</td><td class="n">16.4%</td></tr>
</table></div>
<p class="fine">Hosted bar at rentals adds $35,424. Party and jam shows run $14&ndash;$19 of bar per attendee, seated shows $8&ndash;$9, family shows under $4.</p>
</div>
</div>
'''
NEW = cut(NEW, '<div class="sechead"><div><div class="eb">Section 4.0</div>', '<div class="sechead"><div><div class="eb">Section 5.0</div>', esc(PROG))

RENT = '''<div class="pb"></div>
<div class="sechead"><div><div class="eb">Section 4.0</div><div class="tt">Rentals &amp; Forward Book</div></div><div class="bn">4.</div></div>
<div class="kpis">
<div class="kpi"><div class="k">Rental Income YTD</div><div class="val">$115k</div><div class="d">&minus;20% vs budget &middot; &minus;35% YoY</div></div>
<div class="kpi"><div class="k">Deferred for Fall</div><div class="val">$135k</div><div class="d">collected, recognizes at the events</div></div>
<div class="kpi"><div class="k">Signed Sep&ndash;Oct</div><div class="val">$99k</div><div class="d">$78k already collected</div></div>
<div class="kpi"><div class="k">Days in Real Use</div><div class="val">291 / 304</div><div class="d">Nov 1 to Aug 31, all 14 rooms</div></div>
</div>
<div class="half">
<div>
<h3>Rental Revenue by Type (Nov&ndash;Aug)</h3>
<div class="compact"><table>
<tr class="hd"><td>Type</td><td class="n">FY26 YTD</td><td class="n">Share</td></tr>
<tr><td class="lbl">Dance and studio programs (School of Dance, Wild Hare, life drawing)</td><td class="n">$43,792</td><td class="n">38%</td></tr>
<tr><td class="lbl">Nonprofit galas and community events (GVH gala, KBUT, CFGV, Wildflower, PPF, Trailhead)</td><td class="n">$28,708</td><td class="n">25%</td></tr>
<tr><td class="lbl">Weddings and rehearsal dinners (McCoy, Cornish, Georgitsis)</td><td class="n">$19,422</td><td class="n">17%</td></tr>
<tr><td class="lbl">Private parties and room rentals</td><td class="n">$6,836</td><td class="n">6%</td></tr>
<tr><td class="lbl">Memorials and celebrations of life</td><td class="n">$5,648</td><td class="n">5%</td></tr>
<tr><td class="lbl">Not yet tagged to a renter</td><td class="n">$10,452</td><td class="n">9%</td></tr>
<tr class="b"><td class="lbl">Rental income</td><td class="n">$114,857</td><td class="n">100%</td></tr>
<tr><td class="lbl">Hosted bar at rentals (base, before gratuity and tax)</td><td class="n">$35,424</td><td class="n"></td></tr>
<tr class="b"><td class="lbl">Rental-related revenue</td><td class="n">$150,281</td><td class="n"></td></tr>
</table></div>
<p class="fine">Budget YTD $143,900 rental and $71,000 hosted bar; FY25 same period $175,643 and $51,688. The summer months went to the Center's own events; the fall weddings sit in deferred revenue until they happen.</p>
<h3>Forward Book to Fiscal Year End (Event Temple, signed)</h3>
<div class="compact"><table>
<tr class="hd"><td>Booking</td><td class="n">Date</td><td class="n">Value</td><td class="n">Collected</td></tr>
<tr><td class="lbl">Wedding &mdash; Schreier</td><td class="n">Sep 19</td><td class="n">$33,710</td><td class="n">$33,710</td></tr>
<tr><td class="lbl">Wedding &mdash; Hoffmeister</td><td class="n">Sep 29</td><td class="n">$11,760</td><td class="n">$11,760</td></tr>
<tr><td class="lbl">Wedding &mdash; Steinbach</td><td class="n">Sep 4</td><td class="n">$11,380</td><td class="n">$11,380</td></tr>
<tr><td class="lbl">Gibson welcome party</td><td class="n">Oct 2</td><td class="n">$10,518</td><td class="n">$3,500</td></tr>
<tr><td class="lbl">Petito celebration of life</td><td class="n">Sep 6</td><td class="n">$8,608</td><td class="n">$1,000</td></tr>
<tr><td class="lbl">CB Film Festival</td><td class="n">Sep 24</td><td class="n">$7,672</td><td class="n">$7,672</td></tr>
<tr><td class="lbl">COSA networking and film</td><td class="n">Oct 5</td><td class="n">$6,500</td><td class="n">$2,000</td></tr>
<tr><td class="lbl">Steinberger celebration of life</td><td class="n">Sep 20</td><td class="n">$3,620</td><td class="n">$3,620</td></tr>
<tr><td class="lbl">Five smaller bookings (conference, classes, retreat, screening)</td><td class="n">Sep&ndash;Oct</td><td class="n">$4,890</td><td class="n">$3,040</td></tr>
<tr class="b"><td class="lbl">Signed, Sep 1 &ndash; Oct 31</td><td class="n"></td><td class="n">$98,658</td><td class="n">$77,682</td></tr>
<tr class="hd2"><td colspan="4">November and December 2026</td></tr>
<tr><td class="lbl">Girl Winter Film Tour screening</td><td class="n">Dec 4</td><td class="n">$3,500</td><td class="n">$2,250</td></tr>
<tr><td class="lbl">Mountain Express winter training</td><td class="n">Nov 23</td><td class="n">$500</td><td class="n">$500</td></tr>
<tr><td class="lbl">Town holiday party (Nov 20) and Matchstick third screening (Dec 19)</td><td class="n"></td><td class="n">not yet priced</td><td class="n"></td></tr>
</table></div>
<p class="fine">Four tentative bookings worth &plusmn;$33k are not counted. Contracts already signed for later in FY27 total $97,355 with $27,550 of deposits held, led by three 2027 weddings.</p>
</div>
<div>
<h3>Building Utilization, Nov 1 &ndash; Aug 31 (all 14 room calendars)</h3>
<div class="kpis" style="margin:4px 0;">
<div class="kpi"><div class="k">Days in Real Use</div><div class="val">291 / 304</div><div class="d">96%</div></div>
<div class="kpi"><div class="k">Studio Sessions</div><div class="val">719</div><div class="d">SOD, Wild Hare and rehearsals</div></div>
</div>
<div class="kpis" style="margin:4px 0;">
<div class="kpi"><div class="k">Real Events &amp; Rentals</div><div class="val">554</div><div class="d">183 distinct event days</div></div>
<div class="kpi"><div class="k">Excluded as Non-Events</div><div class="val">497</div><div class="d">meetings, backstage holds, setup</div></div>
</div>
<div class="compact"><table>
<tr class="hd"><td>Real events &amp; rentals by type</td><td class="n">Bookings</td><td class="n">Event days</td></tr>
<tr><td class="lbl">Room rentals, classes &amp; workshops</td><td class="n">156</td><td class="n">94</td></tr>
<tr><td class="lbl">Concerts &amp; performances</td><td class="n">117</td><td class="n">52</td></tr>
<tr><td class="lbl">Community &amp; private events</td><td class="n">87</td><td class="n">36</td></tr>
<tr><td class="lbl">Literary &amp; culinary</td><td class="n">47</td><td class="n">15</td></tr>
<tr><td class="lbl">Weddings &amp; receptions</td><td class="n">34</td><td class="n">12</td></tr>
<tr><td class="lbl">Gallery &amp; art openings</td><td class="n">19</td><td class="n">17</td></tr>
<tr><td class="lbl">School &amp; youth</td><td class="n">19</td><td class="n">6</td></tr>
<tr><td class="lbl">Film screenings</td><td class="n">9</td><td class="n">6</td></tr>
<tr><td class="lbl">Memorials &amp; celebrations of life</td><td class="n">8</td><td class="n">5</td></tr>
<tr><td class="lbl">Other (gala setup and breakdown, auditions, site visits)</td><td class="n">58</td><td class="n">40</td></tr>
<tr class="b"><td class="lbl">Total</td><td class="n">554</td><td class="n">183</td></tr>
</table></div>
<p class="fine">Real activity only: 112 conference-room meetings, 222 green-room and dressing-room holds, 64 theater changes and setup blocks, and 99 holds and internal blocks are excluded. Studio blocks hold several classes each. June figures on the same rules: 232 of 242 days, 578 studio sessions, 369 events on 137 days.</p>
</div>
</div>
'''
# replace from the short-edition Section 5 marker through Section 8 (donor) start: in NEW the original long sections 5..8 still exist; cut 5.0 .. 8.0 then 8.0 .. footer
NEW = cut(NEW, '<div class="sechead"><div><div class="eb">Section 5.0</div>', '<div class="sechead"><div><div class="eb">Section 8.0</div>', esc(RENT))
SEC = short.split("SEC = '''")[1].split("'''")[0]
SEC = SEC.replace('<div class="eb">Section 7.0</div><div class="tt">Year-End Projection &amp; Cash</div></div><div class="bn">7.</div>', '<div class="eb">Section 5.0</div><div class="tt">Year-End Projection &amp; Cash</div></div><div class="bn">5.</div>')
SEC = SEC.replace('<div class="eb">Section 8.0</div><div class="tt">FY27 Draft Budget</div></div><div class="bn">8.</div>', '<div class="eb">Section 6.0</div><div class="tt">FY27 Draft Budget</div></div><div class="bn">6.</div>')
SEC = SEC.replace("A first pass seeded from the FY26 projection with the rules the committee set on September 2.", "A first pass. The basis for every line is the FY26 projection with the rules the committee set on September 2.")
SEC = SEC.replace("<b>Programming scale:</b> $683,850 seeded against $965,487 this year.", "<b>Programming scale:</b> $683,850 on the current basis against $965,487 this year.")
SEC = SEC.replace("<b>Payroll:</b> $1,291,936 by person;", "<b>Payroll:</b> $1,291,936 by person on the current roster;")
SEC = SEC.replace("<tr class=\"hd\"><td>Block</td><td class=\"n\">FY25 actual</td><td class=\"n\">FY26 projected</td><td class=\"n\">FY27 draft</td><td class=\"n v\">FY27 vs FY26</td></tr>", "<tr class=\"hd\"><td>Block</td><td class=\"n\">FY25 actual</td><td class=\"n\">FY26 projected</td><td class=\"n\">FY27 draft (basis)</td><td class=\"n v\">FY27 vs FY26</td></tr>")
assert "seed" not in SEC.lower(), [m.start() for m in re.finditer("seed", SEC.lower())]
NEW = cut(NEW, '<div class="sechead"><div><div class="eb">Section 8.0</div>', '</body></html>"""', esc(SEC))
NEW = NEW.replace('</body></html>"""</body></html>"""', '</body></html>"""')
open("build_report.py", "w", encoding="utf-8").write(NEW)
print("wrote v3 build_report.py", len(NEW), "| concert groups", T)
