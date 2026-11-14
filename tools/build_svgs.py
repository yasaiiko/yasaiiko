"""Generates the hand-made SVGs of the profile README (hero, stack, project cards), dark and light.

    python tools/build_svgs.py
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

THEMES = {
    "dark": dict(bg="#0b0f17", panel="#0f1621", border="#1e2a3a", text="#e6edf3", muted="#8b98a5",
                 faint="#1a2433", cyan="#22d3ee", amber="#fbbf24", green="#34d399", violet="#a78bfa",
                 rose="#fb7185"),
    "light": dict(bg="#ffffff", panel="#f6f8fa", border="#d0d7de", text="#1f2328", muted="#59636e",
                  faint="#e6ebf1", cyan="#0891b2", amber="#b45309", green="#047857", violet="#6d28d9",
                  rose="#be123c"),
}
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans',Helvetica,Arial,sans-serif"


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def dot_grid(w, h, color, step=22):
    return (f'<pattern id="g" width="{step}" height="{step}" patternUnits="userSpaceOnUse">'
            f'<circle cx="1.5" cy="1.5" r="1.1" fill="{color}"/></pattern>'
            f'<rect width="{w}" height="{h}" fill="url(#g)"/>')


def right_panel(t):
    """Agentic harness (hub + skills, plugins, MCP...) feeding a live bootstrap distribution."""
    import math, random
    cx, cy, R = 628, 172, 94
    sats = [("MCP", "servers", "cyan"), ("SKILLS", "packaged", "violet"), ("PLUGINS", "hooks", "violet"),
            ("PIPELINES", "automated", "green"), ("DATA", "lakehouse", "amber"), ("EVALS", "tests", "rose")]
    out = [f'<text x="514" y="40" style="font:10px {MONO};letter-spacing:2px" fill="{t["muted"]}">AGENTIC HARNESS  ·  STATISTICAL RIGOR</text>',
           f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{t["border"]}" stroke-dasharray="3 6" class="orbit"/>',
           f'<circle cx="{cx}" cy="{cy}" r="{R - 34}" fill="none" stroke="{t["border"]}" stroke-opacity=".6"/>']
    for i, (lab, sub, col) in enumerate(sats):
        ang = math.radians(-90 + i * 60)
        x, y = cx + R * math.cos(ang), cy + R * math.sin(ang)
        c = t[col]
        out.append(f'<path id="s{i}" d="M{cx},{cy} L{x:.1f},{y:.1f}" stroke="{t["border"]}" stroke-width="1.4"/>')
        dur = 2.2 + (i % 3) * 0.4
        out.append(f'<circle r="2.8" fill="{c}"><animateMotion dur="{dur}s" begin="{i * .3:.1f}s" repeatCount="indefinite" '
                   f'keyPoints="0;1;0" keyTimes="0;.5;1" calcMode="linear"><mpath href="#s{i}"/></animateMotion></circle>')
        out.append(f'<g class="node" style="animation-delay:{.3 + i * .2:.1f}s">'
                   f'<rect x="{x - 37:.1f}" y="{y - 14:.1f}" width="74" height="28" rx="14" fill="{t["panel"]}" stroke="{c}" stroke-opacity=".75"/>'
                   f'<text x="{x:.1f}" y="{y - 1:.1f}" class="nl" fill="{c}">{lab}</text>'
                   f'<text x="{x:.1f}" y="{y + 9:.1f}" class="ns">{sub}</text></g>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="38" fill="{t["cyan"]}" opacity=".10" class="breathe"/>'
               f'<circle cx="{cx}" cy="{cy}" r="30" fill="{t["panel"]}" stroke="url(#hl)" stroke-width="2"/>'
               f'<text x="{cx}" y="{cy - 1}" class="nl" fill="{t["text"]}" style="font-size:12px">AGENT</text>'
               f'<text x="{cx}" y="{cy + 11}" class="ns">harness</text>')

    # stats panel: histogram re-sampled like a bootstrap, density curve, 95% CI band
    px, py, pw, ph = 762, 58, 216, 240
    out.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="12" fill="{t["panel"]}" stroke="{t["border"]}"/>'
               f'<text x="{px + 14}" y="{py + 22}" style="font:700 10px {MONO};letter-spacing:1.4px" fill="{t["cyan"]}">BOOTSTRAP · B=10k</text>'
               f'<text x="{px + pw - 14}" y="{py + 22}" style="font:10px {MONO};text-anchor:end" fill="{t["muted"]}">live</text>'
               f'<circle cx="{px + pw - 44}" cy="{py + 18.5}" r="3" fill="{t["green"]}" class="pulse"/>')
    n, bx, base, bw, top = 15, px + 16, py + 168, (pw - 32) / 15, 110
    rnd = random.Random(7)
    dens = [math.exp(-((i - 7) / 3.1) ** 2 / 2) for i in range(n)]
    lo, hi = 3, 11
    out.append(f'<rect x="{bx + lo * bw:.1f}" y="{py + 40}" width="{(hi - lo + 1) * bw:.1f}" height="{base - py - 40}" fill="{t["violet"]}" opacity=".10"/>')
    for i in range(n):
        hs = [max(4, top * dens[i] * (0.82 + 0.36 * rnd.random())) for _ in range(4)]
        hs.append(hs[0])
        col = t["violet"] if lo <= i <= hi else t["muted"]
        vals_h = ";".join(f"{h:.1f}" for h in hs)
        vals_y = ";".join(f"{base - h:.1f}" for h in hs)
        out.append(f'<rect x="{bx + i * bw + 1.5:.1f}" y="{base - hs[0]:.1f}" width="{bw - 3:.1f}" height="{hs[0]:.1f}" rx="2" fill="{col}" fill-opacity=".75">'
                   f'<animate attributeName="height" values="{vals_h}" dur="6s" repeatCount="indefinite"/>'
                   f'<animate attributeName="y" values="{vals_y}" dur="6s" repeatCount="indefinite"/></rect>')
    pts = []
    for k in range(61):
        u = k / 60 * (n - 1)
        pts.append(f"{bx + (u + .5) * bw:.1f},{base - top * 1.02 * math.exp(-((u - 7) / 3.1) ** 2 / 2):.1f}")
    out.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{t["cyan"]}" stroke-width="2" class="ln"/>')
    mxl = bx + 7.5 * bw
    out.append(f'<line x1="{mxl:.1f}" x2="{mxl:.1f}" y1="{py + 40}" y2="{base}" stroke="{t["amber"]}" stroke-dasharray="3 3"/>'
               f'<line x1="{bx}" x2="{px + pw - 16}" y1="{base}" y2="{base}" stroke="{t["border"]}"/>'
               f'<text x="{px + 14}" y="{base + 24}" style="font:12px {MONO}" fill="{t["text"]}">beta <tspan fill="{t["amber"]}" font-weight="700">0.40</tspan>'
               f'<tspan fill="{t["muted"]}">  CI95 </tspan>[0.26, 0.55]</text>'
               f'<text x="{px + 14}" y="{base + 44}" style="font:10.5px {MONO}" fill="{t["muted"]}">walk-forward · pre-registered</text>'
               f'<text x="{px + 14}" y="{base + 60}" style="font:10.5px {MONO}" fill="{t["muted"]}">no lookahead · <tspan fill="{t["green"]}">✓</tspan></text>')
    out.append(f'<text x="514" y="318" style="font:10px {MONO}" fill="{t["muted"]}"><tspan fill="{t["violet"]}">●</tspan> skills · plugins · mcp   '
               f'<tspan fill="{t["green"]}">●</tspan> self-running pipelines</text>')
    return "".join(out)


# --------------------------------------------------------------------------------------- hero
def hero(t):
    W, H = 1000, 340
    right = right_panel(t)

    lines = [
        ("$", " whoami"),
        (">", " statistics · data science · agentic genai · mcp"),
        ("$", " run --from raw --to insight --guard rigor"),
    ]
    typed = []
    y0 = 236
    for i, (p, cmd) in enumerate(lines):
        y = y0 + i * 24
        w = len(p + cmd) * 8.6 + 6
        begin = 0.6 + i * 1.6
        typed.append(
            f'<clipPath id="c{i}"><rect x="56" y="{y - 15}" height="22" width="0">'
            f'<animate attributeName="width" from="0" to="{w:.0f}" begin="{begin}s" dur="1.2s" fill="freeze" '
            f'calcMode="discrete" keyTimes="{";".join(f"{k / 20:.2f}" for k in range(21))}" '
            f'values="{";".join(f"{w * k / 20:.0f}" for k in range(21))}"/></rect></clipPath>'
            f'<text x="56" y="{y}" class="term" clip-path="url(#c{i})">'
            f'<tspan fill="{t["green"] if p == "$" else t["cyan"]}">{p}</tspan>'
            f'<tspan fill="{t["text"] if p == "$" else t["muted"]}">{esc(cmd)}</tspan></text>')
    cursor_x = 56 + len(lines[-1][0] + lines[-1][1]) * 8.45 + 4
    typed.append(f'<rect x="{cursor_x:.0f}" y="{y0 + 2 * 24 - 13}" width="9" height="16" fill="{t["cyan"]}" class="cur"/>')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Víctor Carrión, Senior Data Engineer">
<style>
.edge{{fill:none;stroke:{t["border"]};stroke-width:1.6}}
.nl{{font:700 11px {MONO};text-anchor:middle;letter-spacing:.5px}}
.ns{{font:9px {MONO};fill:{t["muted"]};text-anchor:middle}}
.node{{opacity:0;animation:pop .6s ease-out forwards}}
@keyframes pop{{from{{opacity:0;transform:translateY(6px)}}to{{opacity:1;transform:none}}}}
.term{{font:14px {MONO}}}
.cur{{animation:blink 1s steps(1) infinite}}
@keyframes blink{{50%{{opacity:0}}}}
.fade{{opacity:0;animation:fadein .8s ease-out forwards}}
@keyframes fadein{{to{{opacity:1}}}}
.pulse{{animation:pulse 2s ease-in-out infinite}}
@keyframes pulse{{50%{{opacity:.35}}}}
.orbit{{transform-origin:628px 172px;animation:spin 40s linear infinite}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
.breathe{{transform-origin:628px 172px;animation:br 3s ease-in-out infinite}}
@keyframes br{{50%{{transform:scale(1.18);opacity:.04}}}}
.ln{{stroke-dasharray:600;stroke-dashoffset:600;animation:draw 2.5s ease-out .8s forwards}}
@keyframes draw{{to{{stroke-dashoffset:0}}}}
</style>
<defs>
<linearGradient id="hl" x1="0" x2="1"><stop offset="0" stop-color="{t["cyan"]}"/><stop offset=".55" stop-color="{t["violet"]}"/><stop offset="1" stop-color="{t["amber"]}"/></linearGradient>
<radialGradient id="glow" cx=".78" cy=".5" r=".5"><stop offset="0" stop-color="{t["cyan"]}" stop-opacity=".10"/><stop offset="1" stop-color="{t["cyan"]}" stop-opacity="0"/></radialGradient>
<clipPath id="card"><rect width="{W}" height="{H}" rx="16"/></clipPath>
</defs>
<g clip-path="url(#card)">
<rect width="{W}" height="{H}" fill="{t["bg"]}"/>
{dot_grid(W, H, t["faint"])}
<rect width="{W}" height="{H}" fill="url(#glow)"/>
<rect width="{W}" height="3" fill="url(#hl)"/>
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" fill="none" stroke="{t["border"]}"/>

<g class="fade">
<circle cx="62" cy="58" r="4" fill="{t["green"]}" class="pulse"/>
<text x="74" y="62" style="font:12px {MONO}" fill="{t["muted"]}">online · Data Engineering @ <tspan fill="{t["text"]}" font-weight="700">dsm-firmenich</tspan></text>
<text x="54" y="122" style="font:800 50px {SANS};letter-spacing:-1.5px" fill="{t["text"]}">Víctor Carrión</text>
<text x="56" y="160" style="font:600 21px {SANS}" fill="url(#hl)">Senior Data Engineer</text>
<text x="56" y="190" style="font:14px {SANS}" fill="{t["muted"]}">Pipeline automation · Data analysis · Forward development</text>
<text x="56" y="209" style="font:14px {SANS}" fill="{t["muted"]}">powered by frontier LLMs and machine learning.</text>
</g>
{"".join(typed)}

{right}
</svg>'''


# --------------------------------------------------------------------------------------- stack
STACK = [
    ("DATA PLATFORM", "cyan", ["SQL", "Python", "PySpark", "Databricks", "Delta Lake", "Unity Catalog"]),
    ("SAP & ENTERPRISE", "amber", ["SAP MDG", "SAP Migration", "Data Quality", "Master Data", "ETL / ELT", "Orchestration"]),
    ("ML · LLM", "violet", ["Frontier LLMs", "LLM Agents", "Machine Learning", "Walk-forward", "Bootstrap CIs", "pandas"]),
    ("PRODUCT & WEB", "green", ["TypeScript", "Node.js", "Next.js", "Supabase", "Cloudflare", "SQLite"]),
]


def stack(t):
    W, H = 1000, 236
    colw = (W - 48) / 4
    out = []
    for c, (title, col, items) in enumerate(STACK):
        x = 24 + c * colw
        out.append(f'<g class="col" style="animation-delay:{c * .15:.2f}s">')
        out.append(f'<rect x="{x + 6}" y="22" width="{colw - 12}" height="{H - 44}" rx="12" fill="{t["panel"]}" stroke="{t["border"]}"/>')
        out.append(f'<rect x="{x + 22}" y="40" width="18" height="3" rx="1.5" fill="{t[col]}"/>')
        out.append(f'<text x="{x + 22}" y="62" style="font:700 11px {MONO};letter-spacing:1.6px" fill="{t[col]}">{esc(title)}</text>')
        for i, it in enumerate(items):
            y = 86 + i * 22
            out.append(f'<text x="{x + 22}" y="{y}" style="font:13px {MONO}" fill="{t["text"]}">'
                       f'<tspan fill="{t["muted"]}">›</tspan> {esc(it)}</text>')
        out.append('</g>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Tech stack">
<style>.col{{opacity:0;animation:in .7s ease-out forwards}}@keyframes in{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:none}}}}</style>
{"".join(out)}
</svg>'''


# --------------------------------------------------------------------------------------- project cards
PROJECTS = {
    "sedecim": dict(
        tag="RESEARCH · QUANT", col="violet", lang=("Python", "#3572A5"),
        title="sedecim",
        desc=["Prediction markets + an LLM decision model", "vs the dYdX BTC perpetual, net of costs."],
        stats=[("~6,000", "pre-registered configs"), ("12", "research lanes"), ("696", "tests passing")],
        spark=[3, 4, 3, 5, 4, 6, 5, 5, 4, 5, 4, 4, 5, 4, 5]),
    "vigil": dict(
        tag="RESEARCH · DATA CAPTURE", col="cyan", lang=("JavaScript", "#f1e05a"),
        title="vigil",
        desc=["Walk-forward tests for betting markets:", "24/7 odds capture, tamper-proof track record."],
        stats=[("24/7", "WS + REST capture"), ("SHA-256", "hash-chained log"), ("BTC", "OpenTimestamps")],
        spark=[2, 3, 5, 4, 6, 7, 5, 6, 8, 7, 6, 7, 9, 8, 7]),
    "spain-odds": dict(
        tag="DATA PRODUCT · API", col="amber", lang=("Python", "#3572A5"),
        title="spain-odds-api",
        desc=["14 Spanish bookmakers vs Pinnacle no-vig odds:", "+EV value bets, surebets, CLV, Telegram alerts."],
        stats=[("14", "bookmakers .es"), ("≤30 min", "refresh"), ("+EV", "de-vigged")],
        spark=[5, 4, 6, 5, 7, 6, 8, 6, 7, 9, 8, 7, 9, 10, 9]),
    "vetto": dict(
        tag="SAAS · usevetto.com", col="green", lang=("TypeScript", "#3178c6"),
        title="Vetto",
        desc=["Blocks disposable, dead-domain and bot signups.", "Supabase hook · better-auth · Next.js · audit."],
        stats=[("4", "open-source repos"), ("500k+", "domains audited"), ("fail-open", "by design")],
        spark=[1, 2, 2, 3, 4, 4, 5, 6, 6, 7, 8, 8, 9, 10, 11]),
}


def card(t, p):
    W, H = 480, 236
    col = t[p["col"]]
    sx, sy, sw, sh = 330, 34, 124, 34
    pts = p["spark"]
    mx = max(pts)
    xy = [(sx + i * sw / (len(pts) - 1), sy + sh - v / mx * sh) for i, v in enumerate(pts)]
    poly = " ".join(f"{x:.1f},{y:.1f}" for x, y in xy)
    area = f"M{sx},{sy + sh} L" + " L".join(f"{x:.1f},{y:.1f}" for x, y in xy) + f" L{sx + sw},{sy + sh} Z"
    stats = []
    for i, (v, l) in enumerate(p["stats"]):
        x = 24 + i * 148
        stats.append(f'<text x="{x}" y="188" style="font:700 18px {MONO}" fill="{t["text"]}">{esc(v)}</text>'
                     f'<text x="{x}" y="206" style="font:11px {SANS}" fill="{t["muted"]}">{esc(l)}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{esc(p["title"])}">
<style>
.ln{{stroke-dasharray:400;stroke-dashoffset:400;animation:draw 2.2s ease-out .3s forwards}}
@keyframes draw{{to{{stroke-dashoffset:0}}}}
.ar{{opacity:0;animation:f 1s ease-out 1.6s forwards}}@keyframes f{{to{{opacity:.18}}}}
.pulse{{animation:p 2s ease-in-out infinite}}@keyframes p{{50%{{opacity:.3}}}}
</style>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="14" fill="{t["bg"]}" stroke="{t["border"]}"/>
<rect x="24" y="0" width="56" height="3" rx="1.5" fill="{col}"/>
<text x="24" y="40" style="font:700 10px {MONO};letter-spacing:1.6px" fill="{col}">{esc(p["tag"])}</text>
<text x="24" y="76" style="font:800 26px {SANS};letter-spacing:-.5px" fill="{t["text"]}">{esc(p["title"])}</text>
<text x="24" y="106" style="font:13.5px {SANS}" fill="{t["muted"]}">{esc(p["desc"][0])}</text>
<text x="24" y="125" style="font:13.5px {SANS}" fill="{t["muted"]}">{esc(p["desc"][1])}</text>
<path d="{area}" fill="{col}" class="ar"/>
<polyline points="{poly}" fill="none" stroke="{col}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round" class="ln"/>
<circle cx="{xy[-1][0]:.1f}" cy="{xy[-1][1]:.1f}" r="3.5" fill="{col}" class="pulse"/>
<line x1="24" x2="{W - 24}" y1="152" y2="152" stroke="{t["border"]}"/>
{"".join(stats)}
<circle cx="{W - 112}" cy="83" r="5" fill="{p["lang"][1]}"/>
<text x="{W - 102}" y="87" style="font:12px {SANS}" fill="{t["muted"]}">{p["lang"][0]}</text>
</svg>'''


for name, t in THEMES.items():
    (OUT / f"hero-{name}.svg").write_text(hero(t), encoding="utf-8")
    (OUT / f"stack-{name}.svg").write_text(stack(t), encoding="utf-8")
    for key, p in PROJECTS.items():
        (OUT / f"card-{key}-{name}.svg").write_text(card(t, p), encoding="utf-8")
print("written to", OUT)
