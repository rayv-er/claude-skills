#!/usr/bin/env python3
"""Strategic Plan KPI Report builder — reuses build_report.py's design system.

Extracts the <style> block (embedded Flama/Plex fonts), STEDDY/SEAT/ROOF
assets, and cover mark from build_report.py so the two reports can never
drift apart visually. Emits strategy_report.html (mid-year edition) and
strategy_onepager.html (single-page scorecard).

Render:
  python3 build_strategy_report.py
  chrome --headless --no-pdf-header-footer --print-to-pdf=out.pdf file://.../strategy_report.html

Data: values from strategy.v_kpi_scorecard + plan mid-year checks as of
2026-07-20. On refresh, update the SC dict and narrative numbers below.
"""

import pathlib
import re

HERE = pathlib.Path(__file__).parent
SRC = (HERE / "build_report.py").read_text()

def _grab(pattern, flags=re.S):
    m = re.search(pattern, SRC, flags)
    if not m:
        raise SystemExit(f"asset extraction failed: {pattern[:40]}")
    return m.group(1)

STYLE = _grab(r"<style>(.*?)</style>")
STEDDY_URI = _grab(r'STEDDY_URI\s*=\s*"([^"]+)"')
SEAT_URI = _grab(r'SEAT_URI\s*=\s*"([^"]+)"')
ROOF_URI = _grab(r'ROOF_URI\s*=\s*"([^"]+)"')
MARK_URI = _grab(r'<img class="mark" src="(data:image/png;base64,[^"]+)"')

STYLE = (STYLE.replace("{STEDDY_URI}", STEDDY_URI)
              .replace("{SEAT_URI}", SEAT_URI)
              .replace("{{", "{").replace("}}", "}"))

DATE_LONG = "FY2026 Mid-Year &middot; 07.20.2026"
RUNHEAD = ("<div class='runhead'><div class='rleft'><img src='" + ROOF_URI + "'/>"
           "<span>The Center for the Arts &middot; Strategic Plan KPI Report</span></div>"
           f"<span>{DATE_LONG}</span></div>")
RUNFOOT = ("<div class='runfoot'><span style='background:#fff;padding:0 6px'>crestedbuttearts.org</span>"
           "<span style='background:#fff;padding:0 6px'>Prepared for the leadership team &middot; Strategic Plan FY26</span></div>")

def page(body, first=False):
    br = "" if first else " style='page-break-before:always'"
    return (f"<table class='pagetbl'{br}><thead><tr><td>{RUNHEAD}</td></tr></thead>"
            f"<tfoot><tr><td>{RUNFOOT}</td></tr></tfoot>"
            f"<tbody><tr><td><div style='min-height:8.85in'>{body}</div></td></tr></tbody></table>")

def sechead(num, title):
    return (f"<div class='sechead'><div><div class='eb'>Section {num}.0</div>"
            f"<div class='tt'>{title}</div></div><div class='bn'>{num}.</div></div>")

def kpi(label, val, delta):
    return (f"<div class='kpi'><div class='k'>{label}</div>"
            f"<div class='val'>{val}</div><div class='d'>{delta}</div></div>")

NAVY, CERISE = "#0A3A82", "#A7182F"
POS = f"color:{NAVY};font-weight:700"
NEG = f"color:{CERISE};font-weight:700"

# ── Cover ─────────────────────────────────────────────────────────────────────
COVER = f"""
<div class="cover">
<div class="rhead"><span>The Center for the Arts &middot; Crested Butte</span><span>{DATE_LONG}</span></div>
<img class="mark" src="{MARK_URI}">
<div class="eyebrow">Strategic Plan</div>
<h1 class="big">Strategic<br>Plan KPI<br>Report</h1>
<hr class="rule">
<div class="meta2"><span>Reporting period &middot; November 1, 2025 &ndash; July 20, 2026 &middot; Mid-Year</span>
<span class="fig">15 KPIs measured &middot; NPS +80</span></div>
<div class="bignum">%</div>
</div>"""

# ── 1.0 Executive Summary ─────────────────────────────────────────────────────
S1 = sechead(1, "Executive Summary") + """
<div class="lede">At mid-year, the plan&rsquo;s <b>audience goals are running well ahead of target</b> &mdash; tickets issued are up <b>95%</b>, online ticket revenue up <b>129%</b>, and guest satisfaction holds at <b>9.3/10</b>. Revenue goals are <b>mixed but explainable</b>: bar sales at +10.2% sit three points shy of the 13% target with Alpenglow season half played, and giving trails a capital-gift-heavy FY25 while running <b>+8% over budget</b> on Development&rsquo;s own basis. The clearest watch area is the <b>donor pipeline</b>: 74 first-time donors against 119 at this point last year &mdash; though 70 of last year&rsquo;s arrived in festival July, which is under way now.</div>

<div class="half"><div>
<b style="color:#0A3A82">On track / ahead</b><ul>
<li><b>Tickets issued 9,434 (+95.1%)</b> and online net ticket revenue <b>$442,505 (+128.7%)</b> against a &ldquo;maintain&rdquo; target &mdash; String Cheese plus a strong winter season.</li>
<li><b>Unique participants 3,168</b> &mdash; the &ge;3,000 annual target met with three months remaining; 70.6% are first-time buyers.</li>
<li><b>Guest NPS 9.3/10 FYTD</b> (target &ge;8); winter averaged 9.4; all-time NPS +80 across 799 responses.</li>
<li><b>Email clicks +28.7%</b> (target +25%); opens +22.0% and closing.</li>
<li><b>Program expenses ~15% below budget YTD</b> (target: 3&ndash;5% reduction) with 41% local / emerging artists (target &ge;20%).</li>
<li><b>CRM implemented March 1</b>; sponsor retention 72%; board giving participation 100%.</li>
</ul></div><div>
<b style="color:#0A3A82">Watch</b><ul>
<li><b>Bar sales $203,248 (+10.2%</b> vs +13% target) &mdash; Alpenglow&rsquo;s first three 2026 nights ran +36% over last year&rsquo;s same window; the gap should close if the season holds.</li>
<li><b>New donors 74 vs 119.</b> Development&rsquo;s seasonal view: 46% of the annual target earned vs 25% at this point last year; July/festival season is historically the largest acquisition month.</li>
<li><b>Donor retention to date 33.4%</b> vs 36.1% last year (target &ge;65% by FYE; year-end and Arts Ball giving still ahead).</li>
</ul>
<b style="color:#A7182F">Behind / needs attention</b><ul>
<li><b>Total giving $1,191,307 (&minus;34.9% YoY)</b> &mdash; the FY25 base included major capital receipts; on the budget basis contributed revenue is +8% over budget YTD. A capital-adjusted YoY is the right FY27 refinement.</li>
<li><b>Business sponsorship dollars &minus;5%</b> vs a +10% target (sponsor count retention 72%).</li>
<li><b>Admin staff retention 77%</b> vs &ge;85% (two involuntary, one voluntary departure); hourly retention strong at 96&ndash;97%.</li>
</ul></div></div>
<div class="note">KPI values computed from the data warehouse (strategy.v_kpi_scorecard) on July 20, 2026; comparisons are same-period FY25 unless noted. Process-milestone statuses quote the departments&rsquo; own mid-year checks in the plan workbook.</div>"""

# ── 2.0 Scorecard ─────────────────────────────────────────────────────────────
def sc_table(rows):
    out = ["<table class='compact'><tr class='hd'><td class='lbl'>KPI</td><td class='n'>FY26 to date</td><td class='n'>FY25 same period</td><td class='n'>Change</td><td class='lbl' style='padding-left:16px'>Plan target</td><td class='lbl'>Read</td></tr>"]
    for kpi_, f26, f25, chg, chg_style, tgt, read in rows:
        st = f" style='{chg_style}'" if chg_style else ""
        out.append(f"<tr><td class='lbl'>{kpi_}</td><td class='n'>{f26}</td><td class='n'>{f25}</td><td class='n'{st}>{chg}</td><td class='v' style='padding-left:16px'>{tgt}</td><td class='v'>{read}</td></tr>")
    out.append("</table>")
    return "".join(out)

S2 = sechead(2, "KPI Scorecard") + """
<div class="lede">All fifteen warehouse-measurable KPIs from the plan&rsquo;s five department tabs, with FY26-to-date actuals against the same period of FY25. Roughly 35 further plan KPIs are process milestones owned by department leads; their mid-year status appears in Section 6.</div>
<div class="tcap">Revenue &middot; Sustainability</div>""" + sc_table([
    ("Total giving (Bloomerang, all transactions)", "$1,191,307", "$1,831,108", "&minus;34.9%", NEG, "+13% YoY", "FY25 base incl. capital gifts; +8% over budget YTD"),
    ("Ticket sales (Humanitix online net)", "$442,505", "$193,492", "+128.7%", POS, "maintain", "String Cheese + winter strength"),
    ("Bar sales (Clover payments)", "$203,248", "$184,397", "+10.2%", "", "+13% YoY", "Alpenglow opened +36%; gap closing"),
    ("Rental events (EventTemple)", "202", "&mdash;", "baseline", "", "revenue +20%", "QBO basis: rental income +21% vs phased budget"),
]) + "<div class='tcap'>Donors &middot; Development</div>" + sc_table([
    ("New donors (first-ever gift)", "74", "119", "&minus;37.8%", NEG, "+5% YoY", "festival July pending; 46% of target earned"),
    ("Donor retention to date", "33.4%", "36.1%", "&minus;2.7 pts", NEG, "&ge;65% by FYE", "year-end + Arts Ball giving ahead"),
    ("Upgrades: small &rarr; mid tier", "2", "&mdash;", "new metric", "", "start tracking", "now tracked"),
    ("Upgrades: mid &rarr; major tier", "3", "&mdash;", "new metric", "", "start tracking", "now tracked"),
]) + "<div class='tcap'>Audience &middot; Marketing + Sales</div>" + sc_table([
    ("Tickets issued (Humanitix)", "9,434", "4,835", "+95.1%", POS, "participation +10%", "far ahead"),
    ("Unique ticket buyers", "3,168", "&mdash;", "met", POS, "&ge;3,000 participants", "met with 3 months left"),
    ("First-time buyers, share of FY26 buyers", "70.6%", "&mdash;", "met", POS, "&ge;5&ndash;10%", "records begin Oct 2023"),
    ("Email opens (Mailchimp)", "193,319", "158,473", "+22.0%", "", "engagement +25%", "close"),
    ("Email clicks (Mailchimp)", "8,907", "6,920", "+28.7%", POS, "engagement +25%", "met"),
    ("Web sessions (GA4)", "326,528", "&mdash;", "baseline", "", "+25% by FYE", "baseline established"),
]) + "<div class='tcap'>Experience &middot; Operations + Programming</div>" + sc_table([
    ("Event NPS (average guest score)", "9.3 / 10", "9.5", "&minus;2.1%", "", "&ge;8/10; NPS 80+", "winter 9.4; all-time NPS +80"),
]) + """
<div class="fine">Definitions: FY = Nov 1&ndash;Oct 31; &ldquo;same period&rdquo; = Nov 1 through today&rsquo;s date one year prior. New donors = constituents whose first-ever recorded gift falls in the window. Retention-to-date = share of FY25 donors with any FY26 gift so far (a partial-year figure that rises through year-end). Tier bands per donor fiscal-year totals: small &lt;$1K, mid $1K&ndash;$5K, major &ge;$5K. First-time floor: online ticketing records begin October 2023. Staff-retention and program-expense KPIs are department-reported pending reliable source data (Gusto history; QBO class detail).</div>"""

# ── 3.0 Revenue ───────────────────────────────────────────────────────────────
S3 = sechead(3, "Revenue &amp; Sustainability") + """
<div class="lede">The Sustainability priority&rsquo;s cash-positive-FY26 goal runs through four measured revenue KPIs. Earned revenue is the standout &mdash; <b>ticket revenue more than doubled</b> &mdash; while bar sales track just under target with the summer&rsquo;s biggest bar season half played. Giving optics are dominated by FY25&rsquo;s capital gifts; on the operating-budget basis the Finance Committee reviews, total revenue is <b>+14% vs budget</b>.</div>
<div class="kpis">""" + \
    kpi("Ticket revenue FYTD", "$442,505", "+128.7% YoY") + \
    kpi("Bar sales FYTD", "$203,248", "+10.2% &middot; target +13%") + \
    kpi("Total giving FYTD", "$1.19M", "+8% vs budget") + \
    kpi("Rental events FY26", "202", "income +21% vs budget") + """
</div>
<div class="tcap">Bar sales by month &mdash; FY26 vs FY25 (Clover payments)</div>
<table class="compact"><tr class="hd"><td class="lbl">Year</td><td class="n">Nov</td><td class="n">Dec</td><td class="n">Jan</td><td class="n">Feb</td><td class="n">Mar</td><td class="n">Apr</td><td class="n">May</td><td class="n">Jun</td><td class="n">Jul TD</td><td class="n">Total</td></tr>
<tr><td class="lbl">FY26</td><td class="n">$7,211</td><td class="n">$14,078</td><td class="n">$24,422</td><td class="n">$27,315</td><td class="n">$28,315</td><td class="n">$3,934</td><td class="n">$6,071</td><td class="n">$66,410</td><td class="n">$25,493</td><td class="n"><b>$203,248</b></td></tr>
<tr class="b"><td class="lbl">FY25</td><td class="n">$8,739</td><td class="n">$23,081</td><td class="n">$14,675</td><td class="n">$28,227</td><td class="n">$30,086</td><td class="n">$4,824</td><td class="n">$4,153</td><td class="n">$33,563</td><td class="n">$37,049</td><td class="n"><b>$184,397</b></td></tr></table>
<div class="note">June +98% YoY on Alpenglow&rsquo;s earlier start and String Cheese; December&rsquo;s FY25 figure included a large private-event run. Alpenglow&rsquo;s first three 2026 nights: $41,073, +36% over the same window in 2025 ($30,121) &mdash; pacing toward a ~$120k+ season vs $99k in 2025. July TD is 20 days vs a full FY25 July of $60,316.</div>
<div class="tcap">Ticket revenue by month &mdash; FY26 (Humanitix online net, order-date basis)</div>
<table class="compact"><tr class="hd"><td class="lbl">&nbsp;</td><td class="n">Nov</td><td class="n">Dec</td><td class="n">Jan</td><td class="n">Feb</td><td class="n">Mar</td><td class="n">Apr</td><td class="n">May</td><td class="n">Jun</td><td class="n">Jul TD</td></tr>
<tr><td class="lbl">FY26 net</td><td class="n">$27,778</td><td class="n">$43,258</td><td class="n">$60,272</td><td class="n">$196,501</td><td class="n">$84,512</td><td class="n">$15,628</td><td class="n">$6,262</td><td class="n">$6,865</td><td class="n">$1,430</td></tr>
<tr><td class="lbl">Orders</td><td class="n">467</td><td class="n">491</td><td class="n">881</td><td class="n">1,212</td><td class="n">715</td><td class="n">227</td><td class="n">182</td><td class="n">190</td><td class="n">56</td></tr></table>
<div class="note">February&rsquo;s $196.5k is the String Cheese on-sale (June shows; revenue recognized at event in the books &mdash; this table is order-date cash pacing, not P&amp;L). The Finance Committee report carries the accrual view: earned revenue $773,905, essentially on budget (+0.4%).</div>
<div class="tcap">Giving &mdash; reconciling the two reads</div>
<table><tr class="hd"><td class="lbl">Lens</td><td class="n">Figure</td><td class="lbl">Basis</td><td class="lbl">Read</td></tr>
<tr><td class="lbl">Plan KPI (this report)</td><td class="n" style=\"""" + NEG + """\">&minus;34.9% YoY</td><td class="v">All Bloomerang transactions, same period</td><td class="v">FY25 base included major capital-campaign receipts</td></tr>
<tr><td class="lbl">Budget basis (Finance Committee)</td><td class="n" style=\"""" + POS + """\">+22% vs budget</td><td class="v">Contributed revenue vs phased budget</td><td class="v">$164,339 ahead of plan; grants + major-donor cultivation ahead</td></tr>
<tr><td class="lbl">Recommended refinement</td><td class="n">FY27 plan</td><td class="v">Capital-adjusted YoY</td><td class="v">exclude capital / one-time gifts so the target measures annual-fund growth</td></tr></table>"""

# ── 4.0 Donors ────────────────────────────────────────────────────────────────
S4 = sechead(4, "Donors &amp; Development") + """
<div class="lede">Development&rsquo;s KPIs read soft on a raw year-over-year basis, but the seasonality matters: <b>new-donor acquisition is concentrated in festival season</b> &mdash; July 2025 alone produced 70 first-time donors, more than every other FY25 month combined. Development&rsquo;s own mid-year check: <b>46% of the annual new-donor target already earned vs 25% at this point last year</b>. Tier-movement tracking, a plan ask, now exists.</div>
<div class="kpis">""" + \
    kpi("New donors FYTD", "74", "FY25 same period: 119") + \
    kpi("Retention to date", "33.4%", "rises through year-end") + \
    kpi("Small &rarr; mid upgrades", "2", "new metric") + \
    kpi("Mid &rarr; major upgrades", "3", "new metric") + """
</div>
<div class="tcap">New donors by month &mdash; the festival effect</div>
<table class="compact"><tr class="hd"><td class="lbl">Year</td><td class="n">Nov</td><td class="n">Dec</td><td class="n">Jan</td><td class="n">Feb</td><td class="n">Mar</td><td class="n">Apr</td><td class="n">May</td><td class="n">Jun</td><td class="n">Jul</td><td class="n">Aug</td><td class="n">Sep</td><td class="n">Oct</td></tr>
<tr><td class="lbl">FY25</td><td class="n">6</td><td class="n">19</td><td class="n">6</td><td class="n">2</td><td class="n">6</td><td class="n">3</td><td class="n">3</td><td class="n">9</td><td class="n"><b>70</b></td><td class="n">19</td><td class="n">2</td><td class="n">2</td></tr>
<tr><td class="lbl">FY26</td><td class="n">4</td><td class="n">40</td><td class="n">3</td><td class="n">1</td><td class="n">3</td><td class="n">0</td><td class="n">10</td><td class="n">3</td><td class="n">10 TD</td><td class="n">&mdash;</td><td class="n">&mdash;</td><td class="n">&mdash;</td></tr></table>
<div class="note">December 2025&rsquo;s 40 new donors reflect the EOY campaign (+215% campaign new donors per Marketing). July 2026 is 10 through the 20th with Wine + Food Festival mid-flight. The +5% annual target requires 125 by October 31 &mdash; a ~51-donor festival-and-fall season, vs 93 in the same FY25 months.</div>
<div class="tcap">Retention pipeline &mdash; where the year-end lift must come from</div>
<table><tr class="hd"><td class="lbl">Prior-year giving tier</td><td class="n">Not yet renewed</td><td class="n">Prior-year giving</td><td class="lbl">Priority (Donor Intelligence, Finance report &sect;6)</td></tr>
<tr><td class="lbl">$10,000+</td><td class="n">28</td><td class="n">$671,498</td><td class="v">personal / ED outreach now</td></tr>
<tr><td class="lbl">$5,000&ndash;$9,999</td><td class="n">26</td><td class="n">$154,534</td><td class="v">personal outreach + event invite</td></tr>
<tr><td class="lbl">$1,000&ndash;$4,999</td><td class="n">90</td><td class="n">$157,770</td><td class="v">targeted appeal / call</td></tr>
<tr><td class="lbl">Under $1,000</td><td class="n">137</td><td class="n">$39,501</td><td class="v">annual appeal</td></tr>
<tr class="b"><td class="lbl">Total re-engagement pipeline</td><td class="n">281</td><td class="n">$1,023,303</td><td class="v">year-end + Arts Ball giving still ahead</td></tr></table>
<h3>Process milestones &mdash; Development mid-year checks</h3><ul>
<li><b>CRM cleanup</b>: additional cleanup initiated pre-summer; still needs help.</li>
<li><b>Monthly fundraising dashboards</b>: draft exists; defining which data is useful &mdash; this report and the Monday scorecard can serve as the backbone.</li>
<li><b>Donor impact stories</b>: Marketing working toward the three-story target.</li>
<li><b>Prospect follow-up within 10 days</b>: protocol not established for winter; being set up with EA support for summer.</li></ul>"""

# ── 5.0 Audience ──────────────────────────────────────────────────────────────
S5 = sechead(5, "Audience &amp; Marketing") + """
<div class="lede">Every audience KPI with a prior-year comparison is <b>at or ahead of target</b>. Participation nearly doubled, the 3,000-participant goal is already met, and email engagement grew faster than the list. The web-traffic and rental-retention KPIs establish baselines this year; the CRM milestone landed March 1.</div>
<div class="kpis">""" + \
    kpi("Tickets issued FYTD", "9,434", "+95.1% &middot; target +10%") + \
    kpi("Unique buyers", "3,168", "target &ge;3,000 met") + \
    kpi("First-time share", "70.6%", "target &ge;5&ndash;10% met") + """
</div><div class="kpis">""" + \
    kpi("Email opens FYTD", "193,319", "+22.0% &middot; target +25%") + \
    kpi("Email clicks FYTD", "8,907", "+28.7% &middot; met") + \
    kpi("Web sessions FYTD", "326,528", "baseline &middot; +25% by FYE") + """
</div>
<div class="tcap">Distribution reach &mdash; email lists (Finance report &sect;7)</div>
<table><tr class="hd"><td class="lbl">List</td><td class="n">Subscribers</td><td class="lbl">Note</td></tr>
<tr><td class="lbl">CB Center for the Arts</td><td class="n">10,659</td><td class="v">flagship list; all lists run above the 25&ndash;28% nonprofit open-rate benchmark</td></tr>
<tr><td class="lbl">Wine + Food Festival</td><td class="n">2,646</td><td class="v">festival season active</td></tr>
<tr><td class="lbl">Donors</td><td class="n">2,076</td><td class="v">donor + festival lists approach 55% opens</td></tr>
<tr><td class="lbl">Mountain Words Festival</td><td class="n">1,266</td><td class="v">&nbsp;</td></tr></table>
<h3>Process milestones &mdash; Marketing mid-year checks</h3><ul>
<li><b>CRM implemented and integrated</b> with the Programming calendar &mdash; completed March 1, 2026.</li>
<li><b>Rental client retention 85%</b> against the 75% target (EventTemple baselines the metric going forward).</li>
<li><b>Guest satisfaction 81.4/100</b> as of March 10 against the &ge;80 target &mdash; aligns with the warehouse&rsquo;s 9.3/10 average.</li>
<li><b>EOY campaign</b>: +63% campaign giving; +215% campaign new donors.</li>
<li><b>Sponsorships</b>: 72% sponsor retention; <span style=\"""" + NEG + """\">dollar value &minus;5%</span> vs the +10% target &mdash; the section&rsquo;s clearest gap.</li>
<li><b>Website redesign / brand adoption</b>: mid-year status TBD in the plan; the web baseline is now measurable.</li></ul>
<div class="fine">Email figures are Mailchimp list activity summed daily across all lists; engagement growth outpacing list growth indicates content, not just list size. Web sessions from GA4 daily traffic; the plan measures the +25% target to December 1, 2026 &mdash; the FY baseline enables that check.</div>"""

# ── 6.0 Experience & Milestones ───────────────────────────────────────────────
S6 = sechead(6, "Experience, Operations &amp; Milestones") + """
<div class="lede">Guest experience holds at an elite level &mdash; <b>9.3/10 average FYTD</b>, no month below 8.9 &mdash; and the operational milestones behind it (debriefs, BEO dashboard, trainings) are moving. Staff retention splits: hourly is excellent at 96&ndash;97%; admin sits at 77% against the 85% target after two managed departures.</div>
<div class="kpis">""" + \
    kpi("Event NPS avg FYTD", "9.3 / 10", "target &ge;8 met") + \
    kpi("All-time NPS", "+80", "799 responses") + \
    kpi("Hourly retention", "96.7%", "target &ge;85% met &middot; dept-reported") + \
    kpi("Admin retention", "77%", "target &ge;85% &middot; dept-reported") + """
</div>
<div class="tcap">Guest score by month (surveys)</div>
<table class="compact"><tr class="hd"><td class="lbl">&nbsp;</td><td class="n">Nov</td><td class="n">Dec</td><td class="n">Jan</td><td class="n">Feb</td><td class="n">Mar</td><td class="n">Apr</td><td class="n">May</td><td class="n">Jun</td></tr>
<tr><td class="lbl">Avg score</td><td class="n">10.0</td><td class="n">9.4</td><td class="n">8.9</td><td class="n">9.5</td><td class="n">9.6</td><td class="n">9.2</td><td class="n">10.0</td><td class="n">8.9</td></tr>
<tr><td class="lbl">Responses</td><td class="n">3</td><td class="n">52</td><td class="n">15</td><td class="n">34</td><td class="n">40</td><td class="n">17</td><td class="n">5</td><td class="n">30</td></tr></table>
<div class="tcap">Process milestones by department &mdash; mid-year status</div>
<table class="compact"><tr class="hd"><td class="lbl">Department</td><td class="lbl">Milestone (plan target)</td><td class="lbl">Mid-year status</td></tr>
<tr><td class="lbl">Programming</td><td class="v">Program expenses &minus;3&ndash;5% FY25&rarr;FY26</td><td class="v"><b style="color:#0A3A82">~15% below budget YTD</b>; per-event P&amp;Ls being implemented</td></tr>
<tr><td class="lbl">Programming</td><td class="v">&ge;20% local / emerging artists</td><td class="v"><b style="color:#0A3A82">41% across winter season</b></td></tr>
<tr><td class="lbl">Programming</td><td class="v">1&ndash;2 new / risk-taking programs; signature categories</td><td class="v">SCI, new gallery shows, ROMP, 6&times;6 delivered; categories established; family programming expanding</td></tr>
<tr><td class="lbl">Prog + Ops</td><td class="v">100% events on BEO dashboard by Q3; &ge;2 trainings</td><td class="v">dashboard in progress with new event manager; 1 training held, more scheduled</td></tr>
<tr><td class="lbl">Operations</td><td class="v">Event / facility budgets within &plusmn;3%</td><td class="v"><b style="color:#0A3A82">under budget on expenses</b>; preventive maintenance on schedule</td></tr>
<tr><td class="lbl">Leadership</td><td class="v">&ge;2 municipal planning processes</td><td class="v"><b style="color:#0A3A82">PROST Plan, Zoning Plan, Community Spaces Strategy</b></td></tr>
<tr><td class="lbl">Leadership</td><td class="v">Board: 100% giving; &ge;2 new local directors</td><td class="v">100% giving; one new local director &mdash; FY27 recruitment focus</td></tr>
<tr><td class="lbl">Leadership</td><td class="v">Financial policies by Q4; &ge;3 major / planned gifts</td><td class="v">policies drafted post-summer; major-donor commitments expected in summer</td></tr>
<tr><td class="lbl">Leadership</td><td class="v">&ge;10 partner meetings; &ge;2 new partnerships</td><td class="v"><b style="color:#0A3A82">8+ partners engaged</b> (PPF, RMBL, KBUT, SOD, Town of CB&hellip;); Sleds &amp; Kegs + RMBL expanded; 2 regional committees</td></tr>
<tr><td class="lbl">Leadership</td><td class="v">Staff wellbeing: satisfaction &ge;4/5; burnout &minus;50%</td><td class="v">EAP being implemented; manager check-ins; survey lands in Q4</td></tr>
<tr><td class="lbl">Creative District</td><td class="v">&ge;2 CD initiatives</td><td class="v"><b style="color:#0A3A82">3 PD workshops, Makers Market, flower-box program</b></td></tr></table>
<div class="foot">Sources: strategy.plan_items (plan workbook, synced daily); strategy.v_kpi_scorecard (warehouse KPIs); surveys.nps_responses; Finance Committee Report 07.20.2026 (&sect;6 Donor Intelligence, &sect;7 Forward Book). Department-reported figures quote the plan&rsquo;s mid-year check column where the warehouse lacks a reliable source. Regenerates on demand; the same scorecard appears in the Monday morning briefing.</div>"""

HTML = ("<!doctype html><html><head><meta charset='utf-8'><style>" + STYLE +
        "</style></head><body>" + COVER +
        page(S1, first=True) + page(S2) + page(S3) + page(S4) + page(S5) + page(S6) +
        "</body></html>")
(HERE / "strategy_report.html").write_text(HTML)
print(f"strategy_report.html written ({len(HTML)//1024}KB)")

# ── One-pager: scorecard summary, no cover ────────────────────────────────────
ONE = sechead(1, "FY26 KPI Scorecard") + """
<div class="lede">Every measurable KPI from the strategic plan, computed live from the Center&rsquo;s data warehouse. FY26 runs November 1, 2025 &ndash; October 31, 2026; comparisons are to the same period of FY25. Sources: Bloomerang, Humanitix, Clover, Mailchimp, guest NPS surveys, GA4, EventTemple.</div>
<div class="kpis">""" + \
    kpi("Total giving FYTD", "$1,191,307", "&minus;34.9% YoY &middot; +8% vs budget") + \
    kpi("Ticket sales FYTD", "$442,505", "+128.7% YoY") + \
    kpi("Bar sales FYTD", "$203,248", "+10.2% &middot; target +13%") + \
    kpi("Event NPS", "9.3 / 10", "target &ge;8 met") + \
    "</div>"
ONE += S2.split("</div>", 1)[1].split("<div class='fine'")[0] if False else ""
# reuse the scorecard tables from S2 (skip its sechead + lede)
ONE += S2[S2.index('<div class="tcap">'):]
ONE_HTML = ("<!doctype html><html><head><meta charset='utf-8'><style>" + STYLE +
            "</style></head><body>" + page(ONE, first=True) + "</body></html>")
(HERE / "strategy_onepager.html").write_text(ONE_HTML)
print(f"strategy_onepager.html written ({len(ONE_HTML)//1024}KB)")
