#!/usr/bin/env python3
"""Development Report builder — giving performance x pipeline x strategic plan.

Blends the Finance Committee report's contributed-revenue results and Donor
Intelligence section (pyramid, retention pipeline, prospect model) with the
strategic plan's Development goals, KPIs, and mid-year checks. Same
design-system extraction pattern as the other sibling builders. Aggregates
only — no donor names or individual wealth detail in this report.

Render:
  python3 build_development_report.py
  chrome --headless --no-pdf-header-footer --print-to-pdf=out.pdf file://.../development_report.html

Data as of 2026-07-20: finance figures from the 07.20.2026 Finance Committee
report (QBO accrual; CRM pyramid Nov-Jun), warehouse KPIs through 07.20
(strategy.v_kpi_scorecard), plan status from strategy.plan_items.
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
.aligntbl td.pad{padding-left:14px}
"""
STYLE = (STYLE.replace("{STEDDY_URI}", STEDDY_URI)
              .replace("{SEAT_URI}", SEAT_URI)
              .replace("{{", "{").replace("}}", "}")) + EXTRA_CSS

DATE_LONG = "FY2026 Mid-Year &middot; 07.20.2026"
RUNHEAD = ("<div class='runhead'><div class='rleft'><img src='" + ROOF_URI + "'/>"
           "<span>The Center for the Arts &middot; Development Report</span></div>"
           f"<span>{DATE_LONG}</span></div>")
RUNFOOT = ("<div class='runfoot'><span style='background:#fff;padding:0 6px'>crestedbuttearts.org</span>"
           "<span style='background:#fff;padding:0 6px'>Prepared for the leadership team &middot; Development &middot; FY26</span></div>")

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
<div class="eyebrow">Development &middot; Finance &times; Strategic Plan</div>
<h1 class="big">Development<br>Report</h1>
<hr class="rule">
<div class="meta2"><span>Reporting period &middot; November 1, 2025 &ndash; July 20, 2026 &middot; Mid-Year</span>
<span class="fig">+22% vs budget &middot; 274 donors &middot; 2,833 prospects</span></div>
<div class="bignum">D</div>
</div>"""

# ── 1.0 Executive Summary ─────────────────────────────────────────────────────
S1 = sechead(1, "Executive Summary") + """
<div class="lede">Development&rsquo;s year splits cleanly into <b>what&rsquo;s working and what&rsquo;s waiting</b>. Working: contributed revenue is <b>$164k (+22%) ahead of budget</b>, the donor base is broadening &mdash; <b>274 donors year-to-date, +14%</b>, with entry-level giving up 74% and the EOY campaign delivering +215% campaign new donors &mdash; and Front Row runs 50% ahead of its phased target. Waiting: the year-over-year optics trail a capital-gift-heavy FY25, <b>281 prior-year donors representing ~$1.0M have not yet renewed</b>, and the middle of the pyramid ($1K&ndash;$10K) is soft. The seasonal shape matters everywhere: festival July has historically been the biggest acquisition month, year-end and the Arts Ball carry renewal &mdash; both are still ahead.</div>

<div class="half"><div>
<b style="color:#0A3A82">Working</b><ul>
<li><b>Contributed revenue +22% vs budget</b> ($898,195 vs $733,856) &mdash; grants and major-donor cultivation ahead of plan.</li>
<li><b>Front Row $150,000</b> against a $100k phased target (+50%); fall renewals ahead; pledges receivable $1.4M.</li>
<li><b>Base broadening</b>: 274 donors (+14%); under-$250 donors up 74% by count; median gift $500.</li>
<li><b>EOY campaign</b>: +63% campaign giving, +215% campaign new donors (40 in December alone).</li>
<li><b>Concentration easing</b>: top-10 households = 43% of CRM cash, down from 46%.</li>
<li><b>Tier-movement tracking now exists</b> (a plan ask): 2 small&rarr;mid and 3 mid&rarr;major upgrades so far.</li>
</ul></div><div>
<b style="color:#0A3A82">Waiting on the season</b><ul>
<li><b>New donors 74 vs 119</b> at this point last year &mdash; but 46% of the annual target is already earned vs 25% last year, and July 2025 alone brought 70 (festival mid-flight now).</li>
<li><b>281 not-yet-renewed donors, ~$1.0M prior giving</b> &mdash; a re-engagement worklist, not attrition; year-end and Ball giving were still ahead at the same point last year.</li>
<li><b>Retention-to-date 33.4%</b> vs 36.1% last year (donors-basis; rises through year-end toward the &ge;65% target).</li>
</ul>
<b style="color:#A7182F">Needs attention</b><ul>
<li><b>Middle softness</b>: $1K&ndash;$10K bands are down in both count and dollars &mdash; the named upgrade focus.</li>
<li><b>Planned gifts</b>: zero of the &ge;3 major/planned-gift commitments so far; expected in summer per Leadership&rsquo;s check.</li>
<li><b>Business sponsorship dollars &minus;5%</b> vs +10% target (72% sponsor count retention) &mdash; shared with Marketing.</li>
</ul></div></div>
<div class="note">Financial figures from the 07.20.2026 Finance Committee report (QBO accrual; CRM pyramid Nov&ndash;Jun); warehouse KPIs through July 20 (the finance report&rsquo;s 64 new donors + 10 in July = 74 here). Aggregates only; named cultivation lists live in Development&rsquo;s working documents.</div>"""

# ── 2.0 Giving Performance ────────────────────────────────────────────────────
S2 = sechead(2, "Giving Performance") + """
<div class="lede">Three lenses on the same year: <b>ahead of budget, behind a capital-inflated prior year, broadening at the base</b>. The pyramid tells the structural story &mdash; growth at the entry bands, softness in the middle, and top-band variance that is mostly Front Row installment timing.</div>
<div class="kpis">""" + \
    kpi("Contributed revenue", "$898,195", "+22% vs budget ($164k ahead)") + \
    kpi("Front Row YTD", "$150,000", "+50% vs $100k phased target") + \
    kpi("Donors YTD", "274", "+14% vs 241 last year") + \
    kpi("Median gift", "$500", "vs $1,000 last year &mdash; base effect") + """
</div>
<div class="tcap">Donor base health &mdash; giving pyramid (Nov&ndash;Jun, CRM cash received)</div>
<table><tr class="hd"><td class="lbl">Gift band (per-donor total)</td><td class="n">FY26 donors</td><td class="n">FY26 $</td><td class="n">FY25 donors</td><td class="n">FY25 $</td><td class="lbl" style="padding-left:14px">Read</td></tr>
<tr><td class="lbl">$25,000+</td><td class="n">12</td><td class="n">$505,841</td><td class="n">14</td><td class="n">$772,307</td><td class="v" style="padding-left:14px">Front Row payment timing</td></tr>
<tr><td class="lbl">$10,000 &ndash; $24,999</td><td class="n">27</td><td class="n">$327,720</td><td class="n">26</td><td class="n">$347,401</td><td class="v" style="padding-left:14px">stable core</td></tr>
<tr><td class="lbl">$5,000 &ndash; $9,999</td><td class="n">15</td><td class="n">$89,620</td><td class="n">22</td><td class="n">$138,988</td><td class="v" style="padding-left:14px">soft &mdash; upgrade focus</td></tr>
<tr><td class="lbl">$1,000 &ndash; $4,999</td><td class="n">62</td><td class="n">$112,202</td><td class="n">78</td><td class="n">$164,166</td><td class="v" style="padding-left:14px">soft &mdash; upgrade focus</td></tr>
<tr><td class="lbl">$250 &ndash; $999</td><td class="n">59</td><td class="n">$23,831</td><td class="n">44</td><td class="n">$20,090</td><td class="v" style="padding-left:14px">growing</td></tr>
<tr><td class="lbl">Under $250</td><td class="n">99</td><td class="n">$9,767</td><td class="n">57</td><td class="n">$6,262</td><td class="v" style="padding-left:14px"><b style="color:#0A3A82">base broadening +74%</b></td></tr>
<tr class="b"><td class="lbl">Total</td><td class="n">274</td><td class="n">$1,068,981</td><td class="n">241</td><td class="n">$1,449,213</td><td class="v" style="padding-left:14px">counts are floors &mdash; see CRM bridge, &sect;4</td></tr></table>
<div class="tcap">Reconciling the three reads on giving</div>
<table class="aligntbl"><tr class="hd"><td class="lbl" style="width:190px">Lens</td><td class="n" style="width:110px">Figure</td><td class="lbl pad">Basis &amp; read</td></tr>
<tr><td class="lbl">Budget basis (Finance Committee)</td><td class="n" style=\"""" + POS + """\">+22% vs budget</td><td class="v pad">contributed revenue vs phased budget &mdash; the operating measure; grants and cultivation ahead of plan</td></tr>
<tr><td class="lbl">Plan KPI (warehouse, all transactions)</td><td class="n" style=\"""" + NEG + """\">&minus;34.9% YoY</td><td class="v pad">FY25 base included major capital receipts; not a like-for-like annual-fund comparison</td></tr>
<tr><td class="lbl">Recommended FY27 refinement</td><td class="n">capital-adjusted YoY</td><td class="v pad">exclude capital / one-time gifts from the KPI base so the +13% target measures annual-fund growth</td></tr></table>
<div class="fine">Pyramid per the finance report&rsquo;s Donor Intelligence section (CRM cash received, Nov&ndash;Jun). Books show ~$1,196k of donor cash vs $1,068,981 in the CRM &mdash; a ~$127k entry backlog; presentation-only, no records changed.</div>"""

# ── 3.0 Donor Pipeline ────────────────────────────────────────────────────────
S3 = sechead(3, "Donor Pipeline") + """
<div class="lede">Acquisition and renewal both run on the Center&rsquo;s seasonal clock. New donors arrive with the festivals and the EOY campaign; renewal concentrates at year-end and the Arts Ball. Mid-year numbers must be read against that shape &mdash; and against it, the pipeline is <b>on pace, with the middle bands the deliberate work</b>.</div>
<div class="kpis">""" + \
    kpi("New donors FYTD", "74", "FY25 same period: 119") + \
    kpi("Target progress", "46%", "of annual target vs 25% last year") + \
    kpi("Retention to date", "33.4%", "donors-basis &middot; rises to year-end") + \
    kpi("Tier upgrades", "2 + 3", "small&rarr;mid + mid&rarr;major &middot; new metric") + """
</div>
<div class="tcap">New donors by month &mdash; the festival effect</div>
<table class="compact"><tr class="hd"><td class="lbl">Year</td><td class="n">Nov</td><td class="n">Dec</td><td class="n">Jan</td><td class="n">Feb</td><td class="n">Mar</td><td class="n">Apr</td><td class="n">May</td><td class="n">Jun</td><td class="n">Jul</td><td class="n">Aug</td><td class="n">Sep</td><td class="n">Oct</td></tr>
<tr><td class="lbl">FY25</td><td class="n">6</td><td class="n">19</td><td class="n">6</td><td class="n">2</td><td class="n">6</td><td class="n">3</td><td class="n">3</td><td class="n">9</td><td class="n"><b>70</b></td><td class="n">19</td><td class="n">2</td><td class="n">2</td></tr>
<tr><td class="lbl">FY26</td><td class="n">4</td><td class="n"><b>40</b></td><td class="n">3</td><td class="n">1</td><td class="n">3</td><td class="n">0</td><td class="n">10</td><td class="n">3</td><td class="n">10 TD</td><td class="n">&mdash;</td><td class="n">&mdash;</td><td class="n">&mdash;</td></tr></table>
<div class="note">Two acquisition engines, one per year-half: December&rsquo;s 40 came from the EOY campaign (+215% campaign new donors); July&rsquo;s historical surge comes from festival giving &mdash; W+FF is mid-flight now. The +5% annual target needs 125 by October 31: a ~51-donor festival-and-fall season vs 93 in the same FY25 months.</div>
<div class="tcap">Renewal &mdash; donors who gave last year, not yet this year</div>
<table><tr class="hd"><td class="lbl">Prior-year giving tier</td><td class="n">Donors</td><td class="n">Prior-year giving</td><td class="lbl" style="padding-left:14px">Priority</td></tr>
<tr><td class="lbl">$10,000+</td><td class="n">28</td><td class="n">$671,498</td><td class="v" style="padding-left:14px"><b style="color:#0A3A82">personal / ED outreach now</b> &mdash; named list available</td></tr>
<tr><td class="lbl">$5,000 &ndash; $9,999</td><td class="n">26</td><td class="n">$154,534</td><td class="v" style="padding-left:14px">personal outreach + event invite</td></tr>
<tr><td class="lbl">$1,000 &ndash; $4,999</td><td class="n">90</td><td class="n">$157,770</td><td class="v" style="padding-left:14px">targeted appeal / call &mdash; the soft-middle band</td></tr>
<tr><td class="lbl">Under $1,000</td><td class="n">137</td><td class="n">$39,501</td><td class="v" style="padding-left:14px">annual appeal</td></tr>
<tr class="b"><td class="lbl">Total re-engagement pipeline</td><td class="n">281</td><td class="n">$1,023,303</td><td class="v" style="padding-left:14px">a worklist, not attrition &mdash; year-end + Ball ahead</td></tr></table>
<div class="fine">Retention-to-date = share of FY25 donors with any FY26 gift so far (33.4% vs 36.1% at the same point last year); the full-year plan target is &ge;65%. Tier bands per donor fiscal-year totals: small &lt;$1K, mid $1K&ndash;$5K, major &ge;$5K.</div>"""

# ── 4.0 Prospect Intelligence ─────────────────────────────────────────────────
S4 = sechead(4, "Prospect Intelligence") + """
<div class="lede">The cross-system prospect model &mdash; giving, event attendance, email engagement, property records, and public giving data across ~22,700 scored constituents &mdash; surfaces a deep bench: <b>2,833 hot/warm prospects who have never given</b>, plus 142 current donors flagged as top upgrade candidates. Festival season is the natural cultivation moment for the property-owning and peer-arts segments.</div>
<div class="kpis">""" + \
    kpi("Hot / warm prospects", "2,833", "scored, never given") + \
    kpi("Upgrade candidates", "142", "current donors, top capacity") + \
    kpi("Constituents scored", "~22,700", "5 data families") + \
    kpi("Top-10 share of CRM cash", "43%", "down from 46% &mdash; healthier") + """
</div>
<div class="tcap">Capacity &amp; affinity signals among never-given prospects</div>
<table class="aligntbl"><tr class="hd"><td class="lbl" style="width:270px">Signal</td><td class="n" style="width:70px">Count</td><td class="lbl pad">Why it matters</td></tr>
<tr><td class="lbl">Own Gunnison County property valued $2M+</td><td class="n">228</td><td class="v pad">wealth capacity, locally rooted</td></tr>
<tr><td class="lbl">Documented public / political giving</td><td class="n">358</td><td class="v pad">demonstrated charitable behavior</td></tr>
<tr><td class="lbl">Give to peer arts / cultural organizations</td><td class="n">109</td><td class="v pad">proven local arts philanthropy &mdash; warmest cohort</td></tr>
<tr><td class="lbl">Business owners</td><td class="n">597</td><td class="v pad">corporate sponsorship angle &mdash; also the fix-lane for sponsorship dollars (&minus;5%)</td></tr>
<tr><td class="lbl">Upgrade candidates (current donors)</td><td class="n">142</td><td class="v pad">ask for more within a warm relationship &mdash; feeds the soft middle bands</td></tr></table>
<div class="tcap">Working the bench &mdash; how the model meets the plan</div>
<table class="aligntbl"><tr class="hd"><td class="lbl" style="width:220px">Plan objective</td><td class="lbl pad">Model-backed play</td></tr>
<tr><td class="lbl">Broaden and diversify the donor base</td><td class="v pad">festival-season cultivation of the 109 peer-arts and 228 property-segment prospects; ranked, named lists can be pulled on demand for the team</td></tr>
<tr><td class="lbl">Improve retention $5K-and-below (+5%)</td><td class="v pad">the 90-donor $1&ndash;5K lapsed band plus 142 upgrade candidates are the exact target population</td></tr>
<tr><td class="lbl">10-business-day prospect follow-up</td><td class="v pad">summer protocol (EA-supported) pairs with event-attendee lists from priority events &mdash; measurable once the protocol logs first-touch dates</td></tr></table>
<div class="fine">Prospect figures are for internal cultivation planning; they draw on wealth-screening and public-records data and do not reconcile to QuickBooks contributed revenue. Individual names and capacity detail stay in Development&rsquo;s working files, not this report.</div>"""

# ── 5.0 Plan Alignment & Systems ──────────────────────────────────────────────
S5 = sechead(5, "Plan Alignment &amp; Systems") + """
<div class="lede">Development&rsquo;s three plan rows, scored at mid-year, plus the systems milestones &mdash; where the fundraising-dashboard ask is now concretely answerable: this report, the Monday scorecard, and the warehouse KPI view are the delivery mechanism.</div>
<div class="tcap">Plan goals &rarr; KPIs &rarr; mid-year status</div>
<table class="compact aligntbl"><tr class="hd"><td class="lbl" style="width:180px">Department goal</td><td class="lbl">Plan KPIs</td><td class="lbl pad">Mid-year status</td></tr>
<tr><td class="lbl">Increase contributed revenue &amp; long-term resilience</td><td class="v">Contributed &uarr;&ge;13%; new donors &uarr;&ge;5%; retention &le;$5K +5%; track tier movement</td><td class="v pad"><b style="color:#0A3A82">+22% vs budget</b>; new donors 46% of target (vs 25% last year); retention measured at 33.4% to date; <b style="color:#0A3A82">tier tracking now live</b> (2 + 3 upgrades)</td></tr>
<tr><td class="lbl">Enhance fundraising systems &amp; internal communication</td><td class="v">CRM cleanup by Q1; monthly dashboards from Q2; shared donor-engagement calendar</td><td class="v pad">additional CRM cleanup initiated pre-summer (needs help); dashboard draft existed &mdash; <b style="color:#0A3A82">this report + Monday scorecard now fill the role</b>; calendar adoption in progress</td></tr>
<tr><td class="lbl">Collaborate across departments on impact storytelling</td><td class="v">3 donor impact stories by Q4; 100% priority-event prospects followed up within 10 business days</td><td class="v pad">Marketing working the three-story target; follow-up protocol being established for summer with EA support (was not in place for winter)</td></tr></table>
<div class="tcap">Where the two lenses meet</div>
<table class="aligntbl"><tr class="hd"><td class="lbl" style="width:190px">Plan intent</td><td class="lbl">Financial evidence</td><td class="lbl pad">Read</td></tr>
<tr><td class="lbl">Grow contributed revenue 13%</td><td class="v">+22% vs budget; &minus;34.9% vs a capital-heavy FY25</td><td class="v pad">on the operating measure, <b style="color:#0A3A82">ahead</b>; fix the KPI base for FY27</td></tr>
<tr><td class="lbl">Broaden the base</td><td class="v">274 donors +14%; entry band +74%; top-10 share 43% (from 46%)</td><td class="v pad"><b style="color:#0A3A82">structurally healthier</b> even in a lighter dollar year</td></tr>
<tr><td class="lbl">Diversify beyond majors</td><td class="v">middle bands ($1K&ndash;$10K) down in count and dollars</td><td class="v pad">the deliberate work: 90 lapsed mid-band donors + 142 upgrade candidates</td></tr>
<tr><td class="lbl">Long-term resilience</td><td class="v">Front Row pledges receivable $1.4M; zero planned gifts booked</td><td class="v pad">capital secured; the planned-giving lane (&ge;3 commitments) is summer&rsquo;s open item</td></tr></table>
<div class="foot">Sources: Finance Committee Report 07.20.2026 (&sect;1 Executive Summary, &sect;6 Donor Intelligence); strategy.plan_items mid-year checks; strategy.v_kpi_scorecard and bloomerang via the data warehouse, 07.20.2026. Donor data presented in aggregate only. Not audited.</div>"""

HTML = ("<!doctype html><html><head><meta charset='utf-8'><style>" + STYLE +
        "</style></head><body>" + COVER +
        page(S1, first=True) + page(S2) + page(S3) + page(S4) + page(S5) +
        "</body></html>")
(HERE / "development_report.html").write_text(HTML)
print(f"development_report.html written ({len(HTML)//1024}KB)")
