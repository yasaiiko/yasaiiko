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


# --------------------------------------------------------------------------------------- hero
def hero(t):
    W, H = 1000, 340
    nodes = [  # x, y, label, sub, colour
        (560, 92, "SAP MDG", "source", t["amber"]),
        (560, 172, "APIs · Odds", "source", t["amber"]),
        (560, 252, "Events", "source", t["amber"]),
        (712, 172, "BRONZE", "ingest", t["muted"]),
        (812, 112, "SILVER", "clean", t["cyan"]),
        (812, 232, "GOLD", "model", t["green"]),
        (928, 172, "LLM", "decide", t["violet"]),
    ]
    edges = [(0, 3), (1, 3), (2, 3), (3, 4), (3, 5), (4, 6), (5, 6), (4, 5)]

    def path(a, b):
        x1, y1 = nodes[a][0] + 46, nodes[a][1]
        x2, y2 = nodes[b][0] - 46, nodes[b][1]
        if nodes[a][0] == nodes[b][0]:  # vertical (silver -> gold)
            x1 = x2 = nodes[a][0]
            y1, y2 = nodes[a][1] + 18, nodes[b][1] - 18
            return f"M{x1},{y1} L{x2},{y2}"
        mx = (x1 + x2) / 2
        return f"M{x1},{y1} C{mx},{y1} {mx},{y2} {x2},{y2}"

    e_svg, p_svg = [], []
    for i, (a, b) in enumerate(edges):
        d = path(a, b)
        e_svg.append(f'<path id="e{i}" d="{d}" class="edge"/>')
        col = nodes[b][4]
        for k in range(2):
            p_svg.append(
                f'<circle r="3" fill="{col}"><animateMotion dur="{2.4 + (i % 3) * 0.5}s" '
                f'begin="{k * 1.2 + i * 0.17:.2f}s" repeatCount="indefinite"><mpath href="#e{i}"/>'
                f'</animateMotion><animate attributeName="opacity" values="0;1;1;0" dur="{2.4 + (i % 3) * 0.5}s" '
                f'begin="{k * 1.2 + i * 0.17:.2f}s" repeatCount="indefinite"/></circle>')
    n_svg = []
    for i, (x, y, label, sub, col) in enumerate(nodes):
        n_svg.append(
            f'<g class="node" style="animation-delay:{i * 0.35:.2f}s">'
            f'<rect x="{x - 46}" y="{y - 18}" width="92" height="36" rx="8" fill="{t["panel"]}" stroke="{col}" stroke-opacity=".7"/>'
            f'<text x="{x}" y="{y - 1}" class="nl" fill="{col}">{esc(label)}</text>'
            f'<text x="{x}" y="{y + 11}" class="ns">{sub}</text></g>')

    lines = [
        ("$", " whoami"),
        (">", " senior data engineer · pipelines · ml · frontier llms"),
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

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Victor Carrión, Senior Data Engineer">
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
<text x="54" y="122" style="font:800 50px {SANS};letter-spacing:-1.5px" fill="{t["text"]}">Victor Carrión</text>
<text x="56" y="160" style="font:600 21px {SANS}" fill="url(#hl)">Senior Data Engineer</text>
<text x="56" y="190" style="font:14px {SANS}" fill="{t["muted"]}">Pipeline automation · Data analysis · Forward development</text>
<text x="56" y="209" style="font:14px {SANS}" fill="{t["muted"]}">powered by frontier LLMs and machine learning.</text>
</g>
{"".join(typed)}

<text x="514" y="42" style="font:10px {MONO};letter-spacing:2px" fill="{t["muted"]}">LIVE PIPELINE · MEDALLION → LLM</text>
{"".join(e_svg)}
{"".join(p_svg)}
{"".join(n_svg)}
<text x="514" y="312" style="font:10px {MONO}" fill="{t["muted"]}"><tspan fill="{t["green"]}">●</tspan> tests <tspan fill="{t["text"]}">696 ✓</tspan>   <tspan fill="{t["cyan"]}">●</tspan> dq checks <tspan fill="{t["text"]}">pass</tspan>   <tspan fill="{t["violet"]}">●</tspan> lookahead <tspan fill="{t["text"]}">0</tspan></text>
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
