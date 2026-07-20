#!/usr/bin/env python3
"""Programming Report builder — season economics x strategic plan, one document.

Blends the Finance Committee report's programming/bar economics (per-event
P&L, consolidated YoY direct contribution) with the strategic plan's
Programming goals, KPIs, and mid-year checks. Reuses build_report.py's
design system via the same extraction pattern as build_strategy_report.py.

Render:
  python3 build_programming_report.py
  chrome --headless --no-pdf-header-footer --print-to-pdf=out.pdf file://.../programming_report.html

Data as of 2026-07-20: finance figures from the 07.20.2026 Finance Committee
report (QBO accrual + Clover POS), plan status from strategy.plan_items,
audience KPIs from strategy.v_kpi_scorecard, presales from humanitix.
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
EXTRA_CSS = """
.aligntbl td{vertical-align:top;padding:4.5px 12px 4.5px 0;border-bottom:.5px solid #d5e0f0;line-height:1.4}
.aligntbl tr.hd td{border-bottom:1.5px solid #000;padding-bottom:3px}
"""
STYLE = (STYLE.replace("{STEDDY_URI}", STEDDY_URI)
              .replace("{SEAT_URI}", SEAT_URI)
              .replace("{{", "{").replace("}}", "}")) + EXTRA_CSS

DATE_LONG = "FY2026 Mid-Year &middot; 07.20.2026"
RUNHEAD = ("<div class='runhead'><div class='rleft'><img src='" + ROOF_URI + "'/>"
           "<span>The Center for the Arts &middot; Programming Report</span></div>"
           f"<span>{DATE_LONG}</span></div>")
RUNFOOT = ("<div class='runfoot'><span style='background:#fff;padding:0 6px'>crestedbuttearts.org</span>"
           "<span style='background:#fff;padding:0 6px'>Prepared for the leadership team &middot; Programming &middot; FY26</span></div>")

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

COVER = f"""
<div class="cover">
<div class="rhead"><span>The Center for the Arts &middot; Crested Butte</span><span>{DATE_LONG}</span></div>
<img class="mark" src="{MARK_URI}">
<div class="eyebrow">Programming &middot; Finance &times; Strategic Plan</div>
<h1 class="big">Programming<br>Report</h1>
<hr class="rule">
<div class="meta2"><span>Reporting period &middot; November 1, 2025 &ndash; July 20, 2026 &middot; Mid-Year</span>
<span class="fig">$143K est. net &middot; 13 shows &middot; NPS 9.3</span></div>
<div class="bignum">P</div>
</div>"""

# ── 1.0 Executive Summary ─────────────────────────────────────────────────────
S1 = sechead(1, "Executive Summary") + """
<div class="lede">Programming is delivering on <b>both halves of its plan mandate</b>. Financially: the concert season produced a <b>$70k year-over-year swing in direct economics</b> &mdash; last year&rsquo;s ($17k) direct loss is this year&rsquo;s <b>$53k contribution</b> &mdash; on ticket income +$121k, bar +$26k against flat staffing, and an alcohol margin improved from 76% to 87%. Program expenses run <b>~15% below budget</b> against a 3&ndash;5% reduction target. Strategically: <b>41% of winter-season events featured local or emerging artists</b> (target &ge;20%), guest NPS holds at <b>9.3/10</b>, new and risk-taking programs shipped (String Cheese, new gallery shows, ROMP, 6&times;6), and signature-event categories are established. The season&rsquo;s standout is the <b>String Cheese Incident</b>: a touring slot budgeted at roughly $10k became two sold-out nights delivering $151k.</div>

<div class="half"><div>
<b style="color:#0A3A82">Delivering</b><ul>
<li><b>Net direct contribution $52,931</b> vs ($17,330) last year &mdash; a $70,261 swing (&sect;2).</li>
<li><b>Concert ticket revenue $360,113 (+51%)</b> across 13 headline shows; 5,968 attendance.</li>
<li><b>Program expenses ~15% under budget YTD</b>; per-event P&amp;Ls being implemented by the CBO.</li>
<li><b>41% local / emerging artists</b> across winter (target &ge;20%).</li>
<li><b>Audience KPIs</b>: 9,434 tickets issued (+95%), 3,168 unique buyers (&ge;3,000 target met), 70.6% first-time.</li>
<li><b>Guest NPS 9.3/10 FYTD</b>; winter averaged 9.4; no month below 8.9.</li>
</ul></div><div>
<b style="color:#0A3A82">Watch</b><ul>
<li><b>BEO dashboard</b> &mdash; 100%-of-events target lands Q3; in progress with the new event manager.</li>
<li><b>Alcohol cost discipline</b> is the margin story (87%); the reusable-cup program and buying practices need to hold through festival season.</li>
<li><b>Family programming</b> is the one signature category not yet delivered; ambassador program in build for summer/fall.</li>
<li><b>Participation definitions</b> &mdash; two plan KPIs carry &ldquo;what did we mean here?&rdquo; mid-year notes (first-timer scope, neighborhood nights); worth resolving before Q4 scoring.</li>
</ul>
<b style="color:#A7182F">Risk</b><ul>
<li><b>SCI concentration</b>: one event drove the earned-revenue beat. The favorable variance is real but non-recurring &mdash; FY27 budgeting should treat it as upside, not base.</li>
</ul></div></div>
<div class="note">Financial figures from the 07.20.2026 Finance Committee report (QBO accrual; Clover POS); plan status from the strategic plan workbook&rsquo;s mid-year checks; audience KPIs from the data warehouse scorecard. Comparisons are same-period FY25.</div>"""

# ── 2.0 Season Economics ──────────────────────────────────────────────────────
S2 = sechead(2, "Season Economics") + """
<div class="lede">Per-event basis: bar = event-night POS net of estimated alcohol COGS (~13%); Humanitix net box office; door/cash excluded. Rentals like KBUT flow through rental revenue; Arts Ball and W+FF land after 6/30.</div>
<div class="kpis">""" + \
    kpi("Concert ticket revenue", "$360,113", "+51% vs FY25 ($239,230)") + \
    kpi("Headline attendance", "5,968", "across 11 major shows") + \
    kpi("Est. net &mdash; 13 shows", "$143,024", "tickets + bar &minus; fees &amp; staffing") + \
    kpi("Net direct contribution", "$52,931", "vs ($17,330) FY25 &mdash; $70k swing") + """
</div>
<div class="tcap">Per-event P&amp;L &mdash; concert lineup (Nov&ndash;Jun)</div>
<table class="compact"><tr class="hd"><td class="lbl">Event</td><td class="n">Date</td><td class="n">Tickets</td><td class="n">Bar (net est.)</td><td class="n">Perf. fee</td><td class="n">Staffing</td><td class="n">Est. net</td></tr>
<tr><td class="lbl"><b>The String Cheese Incident (two nights)</b></td><td class="n">Jun 3&ndash;4</td><td class="n">$151,126</td><td class="n">$15,463</td><td class="n">($135,500)</td><td class="n">($8,129)</td><td class="n"><b>$22,960</b></td></tr>
<tr><td class="lbl">Kitchen Dwellers (two nights)</td><td class="n">Jan 17&ndash;18</td><td class="n">$35,564</td><td class="n">$11,590</td><td class="n">($24,690)</td><td class="n">($4,488)</td><td class="n">$17,976</td></tr>
<tr><td class="lbl">Alpenphunk &mdash; JGB / Grateful Dead Celebration</td><td class="n">Feb 1</td><td class="n">$28,290</td><td class="n">$7,455</td><td class="n">($1,000)</td><td class="n">($2,289)</td><td class="n">$32,456</td></tr>
<tr><td class="lbl">Hank Azaria + The EZ Street Band</td><td class="n">Dec 28</td><td class="n">$27,995</td><td class="n">$4,308</td><td class="n">($25,742)</td><td class="n">($2,257)</td><td class="n">$4,304</td></tr>
<tr><td class="lbl">Vandelux (Sleds &amp; Kegs)</td><td class="n">Mar 7</td><td class="n">$24,265</td><td class="n">$8,449</td><td class="n">($12,137)</td><td class="n">($3,714)</td><td class="n">$16,863</td></tr>
<tr><td class="lbl">Nutcracker! [Rated CB]</td><td class="n">Dec 13</td><td class="n">$20,660</td><td class="n">$1,512</td><td class="n">co-pro</td><td class="n">($3,543)</td><td class="n">$18,629</td></tr>
<tr><td class="lbl">Alpenphunk &mdash; Soulive</td><td class="n">Jan 31</td><td class="n">$15,383</td><td class="n">$2,346</td><td class="n">&mdash;</td><td class="n">($2,107)</td><td class="n">$15,622</td></tr>
<tr><td class="lbl">Beats Antique</td><td class="n">Mar 13</td><td class="n">$14,115</td><td class="n">$3,657</td><td class="n">($12,100)</td><td class="n">($2,655)</td><td class="n">$3,017</td></tr>
<tr><td class="lbl">Ski Patrol: Attitude Adjustment Party</td><td class="n">Feb 8</td><td class="n">$12,205</td><td class="n">$9,358</td><td class="n">($12,000)</td><td class="n">($6,894)</td><td class="n">$2,669</td></tr>
<tr><td class="lbl">The Brothers Comatose</td><td class="n">Feb 26</td><td class="n">$10,102</td><td class="n">$2,393</td><td class="n">($5,403)</td><td class="n">($3,826)</td><td class="n">$3,266</td></tr>
<tr><td class="lbl">Deadhead Ed&rsquo;s End of Season Party</td><td class="n">Apr 3</td><td class="n">$8,867</td><td class="n">$3,218</td><td class="n">($5,000)</td><td class="n">($9,434)</td><td class="n">($2,349)</td></tr>
<tr><td class="lbl">Opera Colorado: Pirates of Penzance</td><td class="n">Feb 5</td><td class="n">$6,165</td><td class="n">$648</td><td class="n">($600)</td><td class="n">($753)</td><td class="n">$5,460</td></tr>
<tr><td class="lbl">Mr. Sun Plays Ellington&rsquo;s Nutcracker</td><td class="n">Dec 20</td><td class="n">$5,376</td><td class="n">$831</td><td class="n">($3,000)</td><td class="n">($1,056)</td><td class="n">$2,151</td></tr>
<tr class="b"><td class="lbl">Total &mdash; concert lineup</td><td class="n">&nbsp;</td><td class="n">$360,113</td><td class="n">$71,228</td><td class="n">($237,172)</td><td class="n">($51,145)</td><td class="n">$143,024</td></tr></table>
<div class="tcap">Concert &amp; series economics &mdash; consolidated year-over-year (Nov&ndash;Jun)</div>
<table><tr class="hd"><td class="lbl">Direct programming P&amp;L</td><td class="n">FY26 YTD</td><td class="n">FY25 YTD</td><td class="n">Change</td></tr>
<tr><td class="lbl">Net ticket sales &mdash; concerts &amp; series</td><td class="n">$360,113</td><td class="n">$239,230</td><td class="n" style=\"""" + POS + """\">+$120,883</td></tr>
<tr><td class="lbl">Bar sales &mdash; all programming nights</td><td class="n">$184,259</td><td class="n">$157,798</td><td class="n" style=\"""" + POS + """\">+$26,461</td></tr>
<tr class="b"><td class="lbl">Direct revenue</td><td class="n">$544,372</td><td class="n">$397,028</td><td class="n">+$147,344</td></tr>
<tr><td class="lbl">Performer / presenter fees</td><td class="n">($317,476)</td><td class="n">($222,498)</td><td class="n">($94,978)</td></tr>
<tr><td class="lbl">Variable hourly staffing</td><td class="n">($149,555)</td><td class="n">($153,651)</td><td class="n" style=\"""" + POS + """\">+$4,096</td></tr>
<tr class="b"><td class="lbl">Direct contribution before alcohol cost</td><td class="n">$77,341</td><td class="n">$20,879</td><td class="n">+$56,462</td></tr>
<tr><td class="lbl">Alcohol cost of sales</td><td class="n">($24,410)</td><td class="n">($38,209)</td><td class="n" style=\"""" + POS + """\">+$13,799</td></tr>
<tr class="b"><td class="lbl">Net direct contribution</td><td class="n">$52,931</td><td class="n">($17,330)</td><td class="n">+$70,261</td></tr></table>
<div class="note">Alcohol margin improved from 76% to 87% (better buying + the reusable-cup program) &mdash; turning last year&rsquo;s ($17k) direct loss into a $53k contribution. Staffing led by Event ($46.7k) and Tech ($46.0k); the July&ndash;October festivals still carry the year. Merchandise excluded; FY25 tickets = GL ticket income excluding festivals for comparability.</div>"""

# ── 3.0 Audience & Experience ─────────────────────────────────────────────────
S3 = sechead(3, "Audience &amp; Experience") + """
<div class="lede">The plan&rsquo;s audience goals &mdash; participation, first-time attendance, satisfaction &mdash; are all at or ahead of target, and the bar data shows <b>genre drives per-attendee spend</b>: party and jam shows run $14&ndash;$19/attendee against $8&ndash;$10 for seated and family shows, which should inform booking mix and staffing.</div>
<div class="kpis">""" + \
    kpi("Tickets issued FYTD", "9,434", "+95.1% &middot; target +10%") + \
    kpi("Unique buyers", "3,168", "&ge;3,000 target met") + \
    kpi("First-time share", "70.6%", "target &ge;5&ndash;10% met") + \
    kpi("Event NPS FYTD", "9.3 / 10", "target &ge;8 &middot; all-time +80") + """
</div>
<div class="half"><div>
<div class="tcap">Per-attendee bar &mdash; major concerts</div>
<table class="compact"><tr class="hd"><td class="lbl">Event</td><td class="n">Att.</td><td class="n">Bar POS</td><td class="n">$ / att.</td></tr>
<tr><td class="lbl">Ski Patrol: Attitude Adjustment</td><td class="n">566</td><td class="n">$10,756</td><td class="n">$19.00</td></tr>
<tr><td class="lbl">Alpenphunk &mdash; JGB</td><td class="n">515</td><td class="n">$8,569</td><td class="n">$16.64</td></tr>
<tr><td class="lbl">Britney&rsquo;s Circus</td><td class="n">309</td><td class="n">$4,569</td><td class="n">$14.79</td></tr>
<tr><td class="lbl">String Cheese &mdash; N1</td><td class="n">617</td><td class="n">$9,036</td><td class="n">$14.65</td></tr>
<tr><td class="lbl">String Cheese &mdash; N2</td><td class="n">628</td><td class="n">$8,737</td><td class="n">$13.91</td></tr>
<tr><td class="lbl">Vandelux</td><td class="n">702</td><td class="n">$9,711</td><td class="n">$13.83</td></tr>
<tr><td class="lbl">Kitchen Dwellers (2 nights)</td><td class="n">1,045</td><td class="n">$13,322</td><td class="n">$12.75</td></tr>
<tr><td class="lbl">Beats Antique</td><td class="n">402</td><td class="n">$4,203</td><td class="n">$10.46</td></tr>
<tr><td class="lbl">Hank Azaria + EZ Street Band</td><td class="n">570</td><td class="n">$4,952</td><td class="n">$8.69</td></tr>
<tr><td class="lbl">The Brothers Comatose</td><td class="n">331</td><td class="n">$2,750</td><td class="n">$8.31</td></tr>
<tr class="b"><td class="lbl">Blended &mdash; 11 shows</td><td class="n">5,968</td><td class="n">$79,302</td><td class="n">$13.29</td></tr></table>
</div><div>
<div class="tcap">Guest score by month (surveys)</div>
<table class="compact"><tr class="hd"><td class="lbl">&nbsp;</td><td class="n">Nov</td><td class="n">Dec</td><td class="n">Jan</td><td class="n">Feb</td><td class="n">Mar</td><td class="n">Apr</td><td class="n">May</td><td class="n">Jun</td></tr>
<tr><td class="lbl">Avg</td><td class="n">10.0</td><td class="n">9.4</td><td class="n">8.9</td><td class="n">9.5</td><td class="n">9.6</td><td class="n">9.2</td><td class="n">10.0</td><td class="n">8.9</td></tr>
<tr><td class="lbl">n</td><td class="n">3</td><td class="n">52</td><td class="n">15</td><td class="n">34</td><td class="n">40</td><td class="n">17</td><td class="n">5</td><td class="n">30</td></tr></table>
<div class="tcap">What guests said (May&ndash;Jun surveys)</div>
<div class="note"><b>Loved:</b> staff, repeatedly (&ldquo;the funnest, nicest, best people ever&rdquo;), the venue itself, the sound, the downstairs bar.<br>
<b>Improve:</b> real food at big shows; smoke-free enforcement inside; night-one balcony / reserved-seat crowd control; drink pricing and a local discount ask. One 0-score tied to an unexpected charge &mdash; worth a service recovery.</div>
<div class="fine">Attendance basis: Humanitix check-ins + door estimates; per-attendee bar = event-night POS. First-time floor: online records begin Oct 2023. Survey source: surveys.nps_responses, anonymized verbatims.</div>
</div></div>"""

# ── 4.0 Strategic Plan Alignment ──────────────────────────────────────────────
S4 = sechead(4, "Strategic Plan Alignment") + """
<div class="lede">Programming&rsquo;s five plan rows, scored at mid-year. Where a KPI is warehouse-measurable the figure is computed; process milestones quote the department&rsquo;s own mid-year check.</div>
<div class="tcap">Plan goals &rarr; KPIs &rarr; mid-year status</div>
<table class="compact aligntbl"><tr class="hd"><td class="lbl" style="width:180px">Department goal</td><td class="lbl">Plan KPIs</td><td class="lbl">Mid-year status</td></tr>
<tr><td class="lbl">Deliver Center-produced programming at net-zero cost</td><td class="v">&ge;3&ndash;5% reduction in program-related expenses FY25&rarr;FY26; quarterly reports on time</td><td class="v"><b style="color:#0A3A82">~15% below budget YTD</b>; net direct contribution +$53k vs ($17k); moving to bi-annual reviews aligned to seasons; per-event P&amp;Ls being implemented</td></tr>
<tr><td class="lbl">Strengthen programming operations &amp; team capacity</td><td class="v">100% of events on BEO dashboard by Q3; &ge;2 team trainings; debrief survey by Q3</td><td class="v">dashboard in progress with new event manager; 1 training held, more scheduled pre-summer; debrief prototype in consistent use</td></tr>
<tr><td class="lbl">Deliver diverse, high-quality, bold programming</td><td class="v">1&ndash;2 new / risk-taking programs; audience score &ge;8/10; &ge;20% local or emerging artists</td><td class="v"><b style="color:#0A3A82">SCI + new gallery shows delivered; NPS 9.3 FYTD (winter 9.4); 41% local/emerging</b></td></tr>
<tr><td class="lbl">Build lasting audiences &amp; community tradition</td><td class="v">Signature Event categories; 1&ndash;2 programs per category + 1&ndash;2 community exhibitions; &ge;1 new engagement initiative with Marketing</td><td class="v">categories established; ROMP and 6&times;6 executed; family programming the remaining gap; ambassador program in build; teacher/PTA pricing offered</td></tr>
<tr><td class="lbl">Expand community access &amp; participation</td><td class="v">&ge;2 Creative District initiatives; &ge;3,000 unique participants; &ge;5&ndash;10% first-time attendees</td><td class="v"><b style="color:#0A3A82">CD: 3 PD workshops, Makers Market, flower-box program; 3,168 unique buyers; 70.6% first-time</b> &mdash; scope questions on the last two KPIs noted for Q4 (&ldquo;what did we mean here?&rdquo;)</td></tr></table>
<div class="tcap">Where the two lenses meet</div>
<table class="aligntbl"><tr class="hd"><td class="lbl" style="width:160px">Plan intent</td><td class="lbl">Financial evidence</td><td class="lbl">Read</td></tr>
<tr><td class="lbl">Net-zero Center-produced programming</td><td class="v">Net direct contribution $52,931 (from ($17,330))</td><td class="v"><b style="color:#0A3A82">exceeded</b> &mdash; programming is now accretive before overhead</td></tr>
<tr><td class="lbl">Bold booking within discipline</td><td class="v">SCI: ~$10k budget slot &rarr; $151k tickets, $23k net</td><td class="v">risk-taking paid; treat as non-recurring upside in FY27 budget</td></tr>
<tr><td class="lbl">Genre mix as a revenue lever</td><td class="v">$19 vs $8 per-attendee bar by genre</td><td class="v">booking mix and bar staffing should price this in explicitly</td></tr>
<tr><td class="lbl">Expense discipline</td><td class="v">Program expenses ~15% under budget; staffing flat on +51% ticket volume</td><td class="v">target beaten 3&ndash;5x; protect through festival season</td></tr></table>"""

# ── 5.0 Forward Book ──────────────────────────────────────────────────────────
S5 = sechead(5, "Forward Book") + """
<div class="lede">The back half of the fiscal year is already earning: <b>$288,419 of future-event revenue is collected</b> and held in deferred revenue, the Wine + Food Festival (mid-July) and Arts Ball (July 9) land immediately after this reporting period, and fall on-sales are open with <b>Steve Earle at $15.6k presold</b>.</div>
<div class="kpis">""" + \
    kpi("Deferred revenue collected", "$288,419", "tickets + rentals, future events") + \
    kpi("Steve Earle &middot; Aug 7", "$15,579", "87 orders presold") + \
    kpi("Alpenglow season pace", "+36%", "first 3 nights vs 2025 &middot; ~$120k+ track") + \
    kpi("W+FF (post-period)", "~$387k", "projected full festival &middot; Grand Tasting sold out") + """
</div>
<div class="tcap">On-sale &mdash; presales by event (Humanitix, net through 07.20)</div>
<table class="compact"><tr class="hd"><td class="lbl">Event</td><td class="n">Date</td><td class="n">Presold net</td><td class="n">Orders</td></tr>
<tr><td class="lbl">Steve Earle</td><td class="n">Aug 7</td><td class="n">$15,579</td><td class="n">87</td></tr>
<tr><td class="lbl">2026 Mountain Words Writer&rsquo;s Retreat</td><td class="n">Aug 21</td><td class="n">$700</td><td class="n">2</td></tr>
<tr><td class="lbl">Opera Lollipops</td><td class="n">Aug 2</td><td class="n">$445</td><td class="n">5</td></tr>
<tr><td class="lbl">Beth Zink painting workshops (two)</td><td class="n">Aug 17 / 19</td><td class="n">$780</td><td class="n">4</td></tr>
<tr><td class="lbl">Bodhi &amp; the Rainforest</td><td class="n">Aug 21</td><td class="n">$225</td><td class="n">3</td></tr>
<tr><td class="lbl">Cookbook Club (Aug + Oct)</td><td class="n">Aug 21 / Oct 23</td><td class="n">$175</td><td class="n">4</td></tr>
<tr><td class="lbl">Off the Page: Mary Roach</td><td class="n">Sep 11</td><td class="n">$110</td><td class="n">2</td></tr></table>
<div class="tcap">Season anchors ahead</div>
<table class="aligntbl"><tr class="hd"><td class="lbl" style="width:170px">Anchor</td><td class="n" style="width:80px">Dates</td><td class="lbl" style="padding-left:14px">Status</td></tr>
<tr><td class="lbl">Wine + Food Festival 2026</td><td class="n">Jul 11&ndash;17</td><td class="v" style="padding-left:14px">just played &mdash; Grand Tasting sold out 7/18 (665 tickets; VIP oversold its 150 cap at 162); actuals land in the August report</td></tr>
<tr><td class="lbl">Alpenglow free concert series</td><td class="n">Mondays thru Aug</td><td class="v" style="padding-left:14px">pacing +36% over 2025&rsquo;s same window; bar-funded, night-of attribution in the warehouse</td></tr>
<tr><td class="lbl">Steve Earle &mdash; MAD residency window</td><td class="n">Jul 23&ndash;Aug 1</td><td class="v" style="padding-left:14px">confirmed holds (Prism); ticketed show Aug 7</td></tr>
<tr><td class="lbl">String Cheese Incident return</td><td class="n">Dec 17&ndash;20</td><td class="v" style="padding-left:14px">Prism holds placed &mdash; the FY27 version of this year&rsquo;s standout</td></tr>
<tr><td class="lbl">Mountain Words Festival 2027</td><td class="n">May 20&ndash;23</td><td class="v" style="padding-left:14px">calendar anchored; retreat presales already open</td></tr></table>
<div class="note">Presales are order-date cash, recognized at event per the deferral model (2100.11). The July&ndash;October festival stretch is the year&rsquo;s revenue weight; a meaningful base is committed or collected before this report&rsquo;s period even closed.</div>
<div class="foot">Sources: Finance Committee Report 07.20.2026 (&sect;3 Programming, &sect;4 Bar, &sect;7 Forward Book); strategy.plan_items mid-year checks; strategy.v_kpi_scorecard; humanitix presales and prism holds via the data warehouse, 07.20.2026. Not audited.</div>"""

HTML = ("<!doctype html><html><head><meta charset='utf-8'><style>" + STYLE +
        "</style></head><body>" + COVER +
        page(S1, first=True) + page(S2) + page(S3) + page(S4) + page(S5) +
        "</body></html>")
(HERE / "programming_report.html").write_text(HTML)
print(f"programming_report.html written ({len(HTML)//1024}KB)")
