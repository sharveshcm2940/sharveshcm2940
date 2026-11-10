"""Render the animated SVG cards in cards/ from data/*.json.
   STATIC=1  -> final frame, no animation (for screenshots)
   SAMPLE=1  -> fake data (to preview before your real data exists)"""
import os, json, html, base64, random, datetime as dt, collections

# ───────────── CONFIG: edit these ─────────────
USER    = os.environ.get("GH_USER", "sharveshcm2940")
NAME    = os.environ.get("DISPLAY_NAME", "Sharvesh")
TAGLINE = "Building things for the web, one commit at a time."
ROLE    = "DEVELOPER  ·  LEARNER  ·  MAKER"
STATUS  = "open to collaborate"
# ──────────────────────────────────────────────
STATIC = os.environ.get("STATIC") == "1"
SAMPLE = os.environ.get("SAMPLE") == "1"

BG1, BG2, INK, MUTED = "#090d1f", "#161c3d", "#eaf0ff", "#8a93b8"
TEAL, VIOLET, AMBER = "#2ee6c5", "#9b7bff", "#ffb454"
LEVELS = ["#1a2142", "#0f5a66", "#12918f", "#19c8b4", "#6bffe0"]
LANG = {"Python": "#3572A5", "JavaScript": "#f1e05a", "TypeScript": "#3178c6", "HTML": "#e34c26",
        "CSS": "#9b7bff", "Java": "#b07219", "C++": "#f34b7d", "C": "#8a93b8", "Jupyter Notebook": "#DA5B0B"}
DISPLAY = "'Righteous','Trebuchet MS',sans-serif"
MONO = "'Space Mono','Courier New',monospace"
esc = html.escape

# ───────────── data ─────────────
def load():
    if SAMPLE:
        random.seed(7); today = dt.date.today(); days = []
        for i in range(371, -1, -1):
            d = today - dt.timedelta(days=i)
            c = 0 if random.random() < .35 else int(random.expovariate(.25))
            days.append({"date": d.isoformat(), "count": c})
        repos = [{"name": n, "desc": s, "lang": l, "stars": random.randint(0, 40), "forks": random.randint(0, 9), "url": "#"}
                 for n, s, l in [("portfolio-site", "Personal website with animated sections and a blog", "TypeScript"),
                                 ("study-notes", "Notes and solved problems from my coursework", "Python"),
                                 ("chat-app", "Realtime chat app using websockets", "JavaScript"),
                                 ("ui-playground", "Experiments with CSS and SVG animation", "CSS")]]
        return {"total": sum(d["count"] for d in days), "days": days}, repos
    c = json.load(open("data/contributions.json")); r = json.load(open("data/repos.json"))
    return c, r

cal, repos = load()
days = cal["days"][-371:]
total = sum(d["count"] for d in days)
repos.sort(key=lambda r: (-r["stars"], -r["forks"]))

def streaks(ds):
    best = cur = 0
    for d in ds:
        cur = cur + 1 if d["count"] else 0; best = max(best, cur)
    now = 0
    for d in reversed(ds):
        if d["count"]: now += 1
        elif d is ds[-1]: continue   # today may not have commits yet
        else: break
    return now, best

cur_streak, best_streak = streaks(days)
active = sum(1 for d in days if d["count"])
busiest = max(days, key=lambda d: d["count"])
bd = dt.date.fromisoformat(busiest["date"])

# ───────────── svg helpers ─────────────
def font(name, file, weight):
    p = f"fonts/{file}"
    if not os.path.exists(p): return ""
    b = base64.b64encode(open(p, "rb").read()).decode()
    return f"@font-face{{font-family:'{name}';font-weight:{weight};src:url(data:font/woff;base64,{b}) format('woff')}}"

FONTS = font("Righteous", "display.woff", 400) + font("Space Mono", "mono-400.woff", 400) + font("Space Mono", "mono-700.woff", 700)

ANIM = """
.rise{animation:rise .8s cubic-bezier(.2,.8,.2,1) both}
.fade{animation:fade .6s ease-out both}
.pop{transform-box:fill-box;transform-origin:center;animation:pop .5s cubic-bezier(.3,1.6,.5,1) both}
.bar{transform-box:fill-box;transform-origin:bottom;animation:grow .8s cubic-bezier(.2,.9,.2,1) both}
.swing{transform-box:fill-box;transform-origin:50% 100%;animation:swing 1s cubic-bezier(.2,.8,.2,1) both}
.ring{transform-box:fill-box;transform-origin:center;animation:ring 3.2s ease-out infinite}
.float{animation:float 6s ease-in-out infinite}
.nudge{animation:nudge 1.6s ease-in-out infinite}
.blink{animation:blink 1.8s ease-in-out infinite}
.sweep{animation:sweep 5s ease-in-out infinite}
.sweepT{animation:sweepT 5s ease-in-out infinite}
.type{transform-box:fill-box;transform-origin:left;animation:type 2s steps(34) both}
@keyframes rise{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:none}}
@keyframes fade{from{opacity:0}to{opacity:1}}
@keyframes pop{0%{opacity:0;transform:scale(0)}70%{transform:scale(1.25)}100%{opacity:1;transform:scale(1)}}
@keyframes grow{from{transform:scaleY(0)}to{transform:scaleY(1)}}
@keyframes swing{0%{opacity:0;transform:translateY(60px) rotate(-8deg)}55%{opacity:1;transform:translateY(-8px) rotate(2deg)}78%{transform:translateY(3px) rotate(-.6deg)}100%{opacity:1;transform:none}}
@keyframes ring{0%{transform:scale(.3);opacity:.8}100%{transform:scale(2);opacity:0}}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-14px)}}
@keyframes nudge{0%,100%{transform:translateX(0)}50%{transform:translateX(6px)}}
@keyframes blink{0%,100%{opacity:1}50%{opacity:.2}}
@keyframes sweep{0%,55%{transform:translateX(-220px)}100%{transform:translateX(760px)}}
@keyframes sweepT{0%,55%{transform:translateX(-140px)}100%{transform:translateX(340px)}}
@keyframes type{from{transform:scaleX(0)}to{transform:scaleX(1)}}
@media (prefers-reduced-motion:reduce){*{animation:none!important}.cf{display:none}}
"""

def svg(w, h, body, defs=""):
    css = FONTS + f".d{{font-family:{DISPLAY}}}.m{{font-family:{MONO}}}" + ("" if STATIC else ANIM)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
            f'<style>{css}</style><defs>{defs}</defs>{body}</svg>')

def D(delay): return "" if STATIC else f' style="animation-delay:{delay:.2f}s"'
def save(name, s):
    os.makedirs("cards", exist_ok=True); open(f"cards/{name}.svg", "w").write(s)

def bg(w, h, rx=20, stroke="#2a3366"):
    return (f'<rect width="{w}" height="{h}" rx="{rx}" fill="url(#bg)" stroke="{stroke}" stroke-width="1.5"/>')
BGDEF = f'<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BG1}"/><stop offset="1" stop-color="{BG2}"/></linearGradient>'

def counter(x, y, size, value, color, t0, cls="d", anchor="start"):
    """Count-up with SMIL <set> frames (CSS can't change text). Final value fades in at the end."""
    N, step = 16, .06
    out = f'<text class="{cls} fade" x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}"{D(t0 + N * step)}>{value:,}</text>'
    if STATIC: return out.replace(' fade"', '"')
    for k in range(N):
        v = round(value * ((k + 1) / (N + 1)) ** 2)
        out += (f'<text class="{cls} cf" x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}" visibility="hidden">'
                f'<set attributeName="visibility" to="visible" begin="{t0 + k * step:.2f}s" dur="{step}s"/>{v:,}</text>')
    return out

# ───────────── 1. hero ─────────────
def hero():
    W, H = 900, 290
    defs = BGDEF + f'''
<pattern id="grid" width="30" height="30" patternUnits="userSpaceOnUse"><path d="M30 0H0V30" fill="none" stroke="#ffffff" stroke-opacity=".05"/></pattern>
<clipPath id="nm"><text class="d" x="44" y="168" font-size="92">{esc(NAME)}</text></clipPath>
<clipPath id="ty"><rect class="type" x="44" y="196" width="640" height="26"{D(1.1)}/></clipPath>
<linearGradient id="sh" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".85"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<linearGradient id="nameg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{TEAL}"/><stop offset="1" stop-color="{VIOLET}"/></linearGradient>'''
    b = bg(W, H, 22) + f'<rect width="{W}" height="{H}" rx="22" fill="url(#grid)"/>'
    b += f'<g class="float"{D(0)}><circle cx="760" cy="80" r="95" fill="{VIOLET}" opacity=".16"/></g>'
    b += f'<g class="float"{D(-2)}><circle cx="840" cy="235" r="60" fill="{TEAL}" opacity=".14"/></g>'
    b += f'<g class="float"{D(-4)}><circle cx="640" cy="40" r="28" fill="{AMBER}" opacity=".22"/></g>'
    b += (f'<g class="fade"{D(.1)}><circle class="blink" cx="52" cy="58" r="5" fill="{TEAL}"/>'
          f'<text class="m" x="68" y="63" font-size="13" fill="{MUTED}" letter-spacing="2">{esc(STATUS.upper())}</text></g>')
    b += f'<g class="rise"{D(.25)}><text class="d" x="44" y="168" font-size="92" fill="url(#nameg)">{esc(NAME)}</text></g>'
    b += f'<g clip-path="url(#nm)"><rect class="sweep" x="0" y="80" width="90" height="110" fill="url(#sh)" transform="skewX(-18)"/></g>'
    b += f'<g clip-path="url(#ty)"><text class="m" x="44" y="214" font-size="19" fill="{INK}">{esc(TAGLINE)}</text></g>'
    b += f'<text class="m rise" x="44" y="258" font-size="12" font-weight="700" fill="{AMBER}" letter-spacing="3"{D(2.2)}>{esc(ROLE)}</text>'
    b += f'<text class="m fade" x="{W-36}" y="{H-24}" font-size="12" fill="{MUTED}" text-anchor="end"{D(2.4)}>github.com/{esc(USER)}</text>'
    save("hero", svg(W, H, b, defs))

# ───────────── 2. contribution graph ─────────────
def graph():
    W, H, P, C = 900, 200, 16, 12.5
    mx = max(d["count"] for d in days) or 1
    def lvl(n): return 0 if n == 0 else min(4, 1 + int(3 * n / mx + .0001))
    first = dt.date.fromisoformat(days[0]["date"]); off = (first.weekday() + 1) % 7
    b = bg(W, H, 22)
    b += f'<text class="d fade" x="30" y="40" font-size="22" fill="{INK}"{D(.2)}>{total:,} <tspan class="m" font-size="13" fill="{MUTED}">contributions in the last year</tspan></text>'
    seen = set()
    for i, d in enumerate(days):
        col, row = divmod(off + i, 7); dd = dt.date.fromisoformat(d["date"])
        x, y = 30 + col * P, 62 + row * P
        if dd.day <= 7 and dd.month not in seen and row == 0 or (i == 0 and False):
            seen.add(dd.month)
            b += f'<text class="m" x="{x}" y="58" font-size="10" fill="{MUTED}">{dd.strftime("%b")}</text>'
        b += f'<rect class="pop" x="{x}" y="{y}" width="{C}" height="{C}" rx="3" fill="{LEVELS[lvl(d["count"])]}"{D(.5 + col * .02)}/>'
    lx = W - 190
    b += f'<text class="m" x="{lx-8}" y="{H-16}" font-size="10" fill="{MUTED}" text-anchor="end">less</text>'
    for k, c in enumerate(LEVELS):
        b += f'<rect x="{lx + k * 18}" y="{H-26}" width="12.5" height="12.5" rx="3" fill="{c}"/>'
    b += f'<text class="m" x="{lx+98}" y="{H-16}" font-size="10" fill="{MUTED}">more</text>'
    save("graph", svg(W, H, b, BGDEF))

# ───────────── 3. monthly bars + stats ─────────────
def activity():
    W, H = 900, 250
    by = collections.OrderedDict()
    for d in days: by[d["date"][:7]] = by.get(d["date"][:7], 0) + d["count"]
    months = list(by.items())[-12:]
    peak = max(v for _, v in months) or 1
    b = bg(W, H, 22) + f'<text class="d" x="30" y="40" font-size="22" fill="{INK}">Monthly rhythm</text>'
    base, maxh = 205, 118
    for i, (m, v) in enumerate(months):
        h = max(4, int(maxh * v / peak)); x = 34 + i * 50; best = v == peak
        col = TEAL if best else "#3b4688"
        b += f'<rect class="bar" x="{x}" y="{base-h}" width="32" height="{h}" rx="6" fill="{col}"{D(1.2 + i * .07)}/>'
        b += f'<text class="m" x="{x+16}" y="{base+20}" font-size="10" fill="{MUTED}" text-anchor="middle">{dt.date.fromisoformat(m + "-01").strftime("%b")}</text>'
        if best:
            b += f'<text class="d pop" x="{x+16}" y="{base-h-10}" font-size="18" fill="{TEAL}" text-anchor="middle"{D(2.3)}>{v:,}</text>'
    stats = [("CURRENT STREAK", f"{cur_streak}d", TEAL), ("LONGEST STREAK", f"{best_streak}d", VIOLET),
             ("ACTIVE DAYS", str(active), AMBER), ("BUSIEST DAY", f"{bd.strftime('%b')} {bd.day}  ·  {busiest['count']}", INK)]
    for i, (lab, val, c) in enumerate(stats):
        y = 74 + i * 42
        b += f'<g class="rise"{D(.5 + i * .15)}><text class="m" x="670" y="{y}" font-size="10" fill="{MUTED}" letter-spacing="2">{lab}</text>'
        b += f'<text class="d" x="670" y="{y+24}" font-size="{26 if i < 3 else 20}" fill="{c}">{esc(val)}</text></g>'
    b += f'<line x1="640" y1="64" x2="640" y2="224" stroke="#2a3366"/>'
    save("activity", svg(W, H, b, BGDEF))

# ───────────── 4. tiles ─────────────
def tile(name, label, color, value, sub, i):
    W, H, t = 300, 220, .6 + i * .35
    defs = (f'<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG1}"/></linearGradient>'
            f'<clipPath id="cl"><rect width="{W}" height="{H}" rx="22"/></clipPath>'
            f'<linearGradient id="sh" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{color}" stop-opacity="0"/><stop offset=".5" stop-color="{color}" stop-opacity=".35"/><stop offset="1" stop-color="{color}" stop-opacity="0"/></linearGradient>')
    b = f'<g class="swing"{D(t)}>' + bg(W, H, 22, color)
    b += f'<rect x="0" y="0" width="{W}" height="6" fill="{color}" clip-path="url(#cl)"/>'
    b += f'<g clip-path="url(#cl)"><rect class="sweepT" x="0" y="0" width="70" height="{H}" fill="url(#sh)" transform="skewX(-18)"{D(t + 1.5)}/></g>'
    b += f'<text class="m" x="26" y="46" font-size="14" font-weight="700" fill="{color}" letter-spacing="5">{label}</text>'
    b += f'<circle class="ring" cx="266" cy="40" r="14" fill="none" stroke="{color}" stroke-width="2"{D(t + .8)}/><circle cx="266" cy="40" r="5" fill="{color}"/>'
    b += counter(26, 135, 82, value, color, t + .5)
    b += f'<text class="m" x="26" y="168" font-size="13" fill="{MUTED}">{esc(sub)}</text>'
    b += f'<text class="m nudge" x="262" y="198" font-size="22" fill="{color}">→</text></g>'
    save(name, svg(W, H, b, defs))

def tiles():
    langs = len({r["lang"] for r in repos if r["lang"]})
    tile("build", "BUILD", TEAL, len(repos), "public repositories", 0)
    tile("ship", "SHIP", VIOLET, sum(r["stars"] for r in repos), "stars earned", 1)
    tile("learn", "LEARN", AMBER, langs, "languages explored", 2)

# ───────────── 5. repo cards ─────────────
def repo_cards(n=4):
    for i, r in enumerate(repos[:n]):
        W, H = 440, 130
        desc = r["desc"] if len(r["desc"]) <= 62 else r["desc"][:59] + "..."
        lc = LANG.get(r["lang"], MUTED)
        b = f'<g class="rise"{D(.3 + i * .2)}>' + bg(W, H, 18)
        b += f'<text class="d" x="24" y="42" font-size="24" fill="{INK}">{esc(r["name"])}</text>'
        b += f'<text class="m" x="24" y="72" font-size="12" fill="{MUTED}">{esc(desc) or "No description yet"}</text>'
        if r["lang"]:
            b += f'<circle cx="31" cy="104" r="6" fill="{lc}"/><text class="m" x="44" y="108" font-size="12" fill="{INK}">{esc(r["lang"])}</text>'
        b += f'<text class="m" x="{W-24}" y="108" font-size="12" fill="{AMBER}" text-anchor="end">{r["stars"]} stars  ·  {r["forks"]} forks</text>'
        b += f'<text class="m nudge" x="{W-26}" y="40" font-size="18" fill="{TEAL}" text-anchor="end">→</text></g>'
        save(f"repo{i+1}", svg(W, H, b, BGDEF))

hero(); graph(); activity(); tiles(); repo_cards()
print("rendered:", ", ".join(sorted(os.listdir("cards"))))
