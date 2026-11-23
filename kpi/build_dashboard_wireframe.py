"""Render the pilot KPI dashboard wireframe (layout for the Power BI build). No pilot data exists yet, so values are blank."""
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
tiles = [("Ticket deflection rate", "Target: 40% or more"), ("First response time (AI, median)", "Target: under 5 s"),
         ("CSAT (4-5 rating)", "Target: 80% or more"), ("Answer accuracy (QA sample)", "Target: 95% or more"),
         ("Agent pickup after handoff", "Target: under 2 min"), ("Privacy incidents", "Target: 0")]
tile_html = "".join(f'<div class="tile"><div class="tt">{t}</div><div class="tv">&mdash;</div><div class="tn">{n}</div></div>' for t, n in tiles)
reasons = ["HT-01 Asked for human", "HT-02 Low confidence", "HT-03 Negative sentiment", "HT-04 Refund exception",
           "HT-05 Fraud / legal / safety", "HT-06 OTP failed", "HT-07 Out of scope"]
reason_html = "".join(f'<div class="bar"><span class="bl">{r}</span><div class="track"></div></div>' for r in reasons)
html = f"""<html><head><style>
body{{margin:0;font-family:'Segoe UI',Arial,sans-serif;background:#f3f2f1;color:#0b0b0b;width:1600px}}
.top{{background:#1F3A5F;color:#fff;padding:16px 28px;display:flex;justify-content:space-between;align-items:center}}
.top h1{{font-size:22px;margin:0}} .top span{{font-size:13px;opacity:.85}}
.filters{{display:flex;gap:10px;padding:14px 28px 0}} .f{{background:#fff;border:1px solid #d0d0d0;border-radius:4px;padding:6px 12px;font-size:13px;color:#52514e}}
.tiles{{display:grid;grid-template-columns:repeat(6,1fr);gap:14px;padding:14px 28px}}
.tile{{background:#fff;border-radius:6px;padding:14px 16px;box-shadow:0 1px 2px rgba(0,0,0,.08)}}
.tt{{font-size:13px;color:#52514e}} .tv{{font-size:30px;font-weight:700;margin:4px 0;color:#c3c2b7}} .tn{{font-size:12px;color:#898781}}
.row{{display:grid;grid-template-columns:1.3fr 1fr;gap:14px;padding:0 28px}}
.card{{background:#fff;border-radius:6px;padding:16px 18px;box-shadow:0 1px 2px rgba(0,0,0,.08);margin-bottom:14px;min-height:260px}}
.card h2{{font-size:15px;margin:0 0 6px}} .sub{{font-size:12px;color:#898781;margin-bottom:12px}}
.ph{{border:2px dashed #c3c2b7;border-radius:6px;height:190px;display:flex;align-items:center;justify-content:center;color:#898781;font-size:13px}}
.bar{{display:flex;align-items:center;gap:10px;margin:8px 0;font-size:13px}} .bl{{width:210px;color:#52514e}}
.track{{flex:1;background:#f0efec;height:16px;border-radius:3px}}
.foot{{padding:0 28px 16px;font-size:12px;color:#898781}}
</style></head><body>
<div class="top"><h1>GenAI Support Assistant &ndash; Pilot KPIs</h1><span>Pilot: web chat, 10% of traffic, 4 weeks</span></div>
<div class="filters"><div class="f">Date range: Pilot to date</div><div class="f">Intent: All</div><div class="f">Channel: AI vs Agent</div></div>
<div class="tiles">{tile_html}</div>
<div class="row"><div class="card"><h2>Deflection rate and CSAT by day</h2><div class="sub">Line chart, one line per KPI on its own small multiple; target shown as a reference line</div><div class="ph">Daily trend &ndash; populated from pilot data</div></div>
<div class="card"><h2>Handoffs by reason</h2><div class="sub">Bar chart, share of AI chats handed off</div>{reason_html}</div></div>
<div class="foot">Wireframe for the Power BI build. Values stay blank until pilot data exists; KPI formulas are in KPI_Definitions.xlsx.</div>
</body></html>"""
tmp = HERE / "_wire.html"; tmp.write_text(html)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1600, "height": 585}, device_scale_factor=1.5)
    pg.goto(f"file://{tmp}"); pg.screenshot(path=str(HERE / "pilot_dashboard_wireframe.png"), full_page=True); b.close()
tmp.unlink()
