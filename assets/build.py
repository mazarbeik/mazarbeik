#!/usr/bin/env python3
"""Regenerate the profile README graphics.

    pip install fonttools uharfbuzz
    python assets/build.py

Edit PROJECTS or LINKS below, then rerun. Text is converted to outlines
because GitHub serves README SVGs as images, and images can't load web fonts.
Fonts (Instrument Serif, Instrument Sans, IBM Plex Mono; all OFL) are
downloaded once into ~/.cache/readme-fonts.
"""
import urllib.request
from pathlib import Path

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

# ---------------------------------------------------------------- content ---

NAME = "Mohammad Mahdi Azarbeik"
TAGLINE = "Offline reinforcement learning for critical care"

PROJECTS = [  # ordered by how direct the reward signal is
    dict(domain="Sepsis", decision="IV fluid and vasopressor dosing",
         status="Published 2026", done=True, tint="rose"),
    dict(domain="Renal replacement therapy", decision="When to initiate RRT",
         status="Published 2025", done=True, tint="blue"),
    dict(domain="Tacrolimus", decision="Dose selection",
         status="In progress", done=False, tint="sage"),
]
AXIS_LEFT, AXIS_RIGHT = "Patient outcome", "Drug concentration"
AXIS_CAPTION = "The reward signal becomes progressively more direct"

LINKS = {"scholar": "Google Scholar", "linkedin": "LinkedIn", "email": "Email"}

# ---------------------------------------------------------------- theme -----

THEMES = {
    "light": dict(paper="#FFFCFB", edge="#EFCFCB", minor="#F9E7E4", major="#EDBAB4",
                  ink="#16202E", muted="#6A5D5B", pen="#D0433A",
                  rose="#FCEEEB", blue="#EDF2F8", sage="#F0F3EA"),
    "dark": dict(paper="#0F1721", edge="#2B2328", minor="#1E1C24", major="#3A2830",
                 ink="#E6EBF1", muted="#9A8F92", pen="#F2766B",
                 rose="#2A1C21", blue="#172230", sage="#1D2419"),
}

# ---------------------------------------------------------------- fonts -----

GF = "https://raw.githubusercontent.com/google/fonts/main/ofl/"
FONT_SOURCES = {
    "serif": "instrumentserif/InstrumentSerif-Regular.ttf",
    "italic": "instrumentserif/InstrumentSerif-Italic.ttf",
    "mono": "ibmplexmono/IBMPlexMono-Regular.ttf",
    "sans_vf": "instrumentsans/InstrumentSans%5Bwdth,wght%5D.ttf",
}
CACHE = Path.home() / ".cache" / "readme-fonts"


def ntos(v):
    s = f"{v:.1f}"
    return s[:-2] if s.endswith(".0") else s


class Face:
    def __init__(self, path):
        self.hb = hb.Font(hb.Face(hb.Blob.from_file_path(str(path))))
        tt = TTFont(str(path))
        self.gs, self.order, self.upem = tt.getGlyphSet(), tt.getGlyphOrder(), tt["head"].unitsPerEm

    def _shape(self, text):
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(self.hb, buf, {"kern": True, "liga": True})
        return buf.glyph_infos, buf.glyph_positions

    def width(self, text, size, tracking=0.0):
        _, pos = self._shape(text)
        return sum(p.x_advance for p in pos) * size / self.upem + tracking * size * (len(pos) - 1)

    def path(self, text, size, x, y, tracking=0.0, anchor="start"):
        infos, pos = self._shape(text)
        scale = size / self.upem
        w = self.width(text, size, tracking)
        x -= {"start": 0, "middle": w / 2, "end": w}[anchor]
        pen = SVGPathPen(self.gs, ntos=ntos)
        cx = 0.0
        for info, p in zip(infos, pos):
            t = (scale, 0, 0, -scale, x + (cx + p.x_offset) * scale, y - p.y_offset * scale)
            self.gs[self.order[info.codepoint]].draw(TransformPen(pen, t))
            cx += p.x_advance + tracking * size / scale
        return pen.getCommands()


def load_fonts():
    CACHE.mkdir(parents=True, exist_ok=True)
    for key, rel in FONT_SOURCES.items():
        dst = CACHE / f"{key}.ttf"
        if not dst.exists():
            urllib.request.urlretrieve(GF + rel, dst)
    for key, wght in (("sans", 400), ("sans_medium", 500)):
        dst = CACHE / f"{key}.ttf"
        if not dst.exists():
            vf = TTFont(str(CACHE / "sans_vf.ttf"))
            instantiateVariableFont(vf, {"wght": wght, "wdth": 100}).save(str(dst))
    return {k: Face(CACHE / f"{k}.ttf") for k in ("serif", "italic", "mono", "sans", "sans_medium")}


def wrap(face, text, size, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if cur and face.width(trial, size) > max_w:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    return lines + [cur]


def svg_open(w, h, title, desc):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-labelledby="t d"><title id="t">{title}</title><desc id="d">{desc}</desc>\n')


# ---------------------------------------------------------------- header ----

HW, HH, BASE = 1200, 300, 240
MINOR, MAJOR = 6, 30  # 1 mm and 5 mm squares


def ecg_trace():
    """Lead II rhythm strip at 25 mm/s and 10 mm/mV, ~60 bpm, after a 1 mV calibration pulse."""
    y = BASE
    d = [f"M36 {y}", "H60", f"V{y - 60}", "H90", f"V{y}"]
    x0 = 126
    for rr, amp in zip([150, 146, 153, 148, 151, 147, 152], [66, 64, 67, 65, 66, 63, 66]):
        if x0 + 90 > HW - 36:
            break
        d += [f"H{x0}",
              f"C{x0 + 4} {y - 5.5} {x0 + 11} {y - 5.5} {x0 + 15} {y}",       # P
              f"H{x0 + 24}",
              f"L{x0 + 27} {y + 4}", f"L{x0 + 31} {y - amp}",                  # Q, R
              f"L{x0 + 35} {y + 12}", f"L{x0 + 38} {y}",                       # S, J
              f"H{x0 + 52}",
              f"C{x0 + 60} {y - 2} {x0 + 64} {y - 18} {x0 + 70} {y - 17}",     # T
              f"C{x0 + 75} {y - 16} {x0 + 77} {y} {x0 + 82} {y}"]
        x0 += rr
    return " ".join(d + [f"H{HW - 36}"])


def header(f, c):
    trace = ecg_trace()
    sweep = dict(dur="2.8s", begin=".35s", spline=".45 0 .55 1")
    return svg_open(HW, HH, NAME, f"{TAGLINE}. An electrocardiogram rhythm strip is drawn across the banner.") + f"""<style>
.trace{{fill:none;stroke:{c['ink']};stroke-width:2.2;stroke-linejoin:round;stroke-linecap:round;stroke-dasharray:1;stroke-dashoffset:0;animation:sweep {sweep['dur']} cubic-bezier({sweep['spline'].replace(' ', ',')}) {sweep['begin']} both}}
@keyframes sweep{{from{{stroke-dashoffset:1}}to{{stroke-dashoffset:0}}}}
@media (prefers-reduced-motion:reduce){{.trace{{animation:none}}.pen{{display:none}}}}
</style>
<defs>
<pattern id="minor" width="{MINOR}" height="{MINOR}" patternUnits="userSpaceOnUse"><path d="M{MINOR} 0H0V{MINOR}" fill="none" stroke="{c['minor']}"/></pattern>
<pattern id="major" width="{MAJOR}" height="{MAJOR}" patternUnits="userSpaceOnUse"><rect width="{MAJOR}" height="{MAJOR}" fill="url(#minor)"/><path d="M{MAJOR} 0H0V{MAJOR}" fill="none" stroke="{c['major']}"/></pattern>
<clipPath id="card"><rect x=".5" y=".5" width="{HW - 1}" height="{HH - 1}" rx="8"/></clipPath>
</defs>
<g clip-path="url(#card)"><rect width="{HW}" height="{HH}" fill="{c['paper']}"/><rect width="{HW}" height="{HH}" fill="url(#major)"/></g>
<rect x=".5" y=".5" width="{HW - 1}" height="{HH - 1}" rx="8" fill="none" stroke="{c['edge']}"/>
<path fill="{c['ink']}" d="{f['serif'].path(NAME, 66, 60, 96, tracking=-0.005)}"/>
<path fill="{c['ink']}" fill-opacity=".78" d="{f['italic'].path(TAGLINE, 30, 62, 138)}"/>
<path fill="{c['muted']}" d="{f['mono'].path('II', 13, 36, 178)}"/>
<path fill="{c['muted']}" d="{f['mono'].path('25 mm/s   10 mm/mV', 13, HW - 36, 282, anchor='end')}"/>
<path class="trace" pathLength="1" d="{trace}"/>
<g class="pen" opacity="0"><circle r="9" fill="{c['pen']}" fill-opacity=".2"/><circle r="3.6" fill="{c['pen']}"/>
<animateMotion dur="{sweep['dur']}" begin="{sweep['begin']}" fill="freeze" calcMode="spline" keyPoints="0;1" keyTimes="0;1" keySplines="{sweep['spline']}" path="{trace}"/>
<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.03;.9;1" dur="{sweep['dur']}" begin="{sweep['begin']}" fill="freeze"/></g>
</svg>
"""


# ---------------------------------------------------------------- research --

RW, RH = 960, 276
CARD_Y, CARD_H, GAP, PAD = 8, 176, 16, 24


def research(f, c):
    cw = (RW - 2 * GAP) / 3
    desc = "; ".join(f"{p['domain']}: {p['decision']} ({p['status'].lower()})" for p in PROJECTS)
    out = [svg_open(RW, RH, "Dissertation: three clinical domains, one offline RL pipeline",
                    f"{desc}. {AXIS_CAPTION}, from {AXIS_LEFT.lower()} to {AXIS_RIGHT.lower()}.")]
    out.append(f'<defs><linearGradient id="axis" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{RW}" y2="0"><stop offset="0" stop-color="{c["ink"]}" stop-opacity=".18"/>'
               f'<stop offset="1" stop-color="{c["ink"]}"/></linearGradient></defs>\n')
    axis_y = CARD_Y + CARD_H + 38
    dots = []
    for i, p in enumerate(PROJECTS):
        x, y = i * (cw + GAP), CARD_Y
        dash = "" if p["done"] else ' stroke-dasharray="5 4"'
        out.append(f'<rect x="{x + .75:.1f}" y="{y + .75}" width="{cw - 1.5:.1f}" height="{CARD_H - 1.5}" rx="8" '
                   f'fill="{c[p["tint"]]}" stroke="{c["ink"]}" stroke-opacity=".5" stroke-width="1.25"{dash}/>\n')
        # status: filled dot when published, open dashed ring while in progress
        sx, sy = x + PAD, y + 34
        if p["done"]:
            out.append(f'<circle cx="{sx + 4:.1f}" cy="{sy - 4}" r="4" fill="{c["ink"]}" fill-opacity=".7"/>\n')
        else:
            out.append(f'<circle cx="{sx + 4:.1f}" cy="{sy - 4}" r="3.5" fill="none" stroke="{c["ink"]}" stroke-opacity=".7" stroke-width="1.2" stroke-dasharray="2 1.6"/>\n')
        out.append(f'<path fill="{c["muted"]}" d="{f["mono"].path(p["status"], 13, sx + 16, sy)}"/>\n')
        for j, line in enumerate(wrap(f["serif"], p["domain"], 34, cw - 2 * PAD)):
            out.append(f'<path fill="{c["ink"]}" d="{f["serif"].path(line, 34, x + PAD, y + 84 + j * 34)}"/>\n')
        for j, line in enumerate(wrap(f["sans"], p["decision"], 16, cw - 2 * PAD)):
            out.append(f'<path fill="{c["ink"]}" fill-opacity=".72" d="{f["sans"].path(line, 16, x + PAD, y + 148 + j * 21)}"/>\n')
        dots.append(f'<path d="M{x + cw / 2:.1f} {y + CARD_H + 6}V{axis_y - 8}" stroke="{c["ink"]}" stroke-opacity=".3" stroke-dasharray="2 3"/>\n')
        dots.append(f'<circle cx="{x + cw / 2:.1f}" cy="{axis_y}" r="4" fill="{c["paper"]}" stroke="{c["ink"]}" stroke-width="1.5"/>\n')
    out.append(f'<path d="M1 {axis_y}H{RW - 10}" stroke="url(#axis)" stroke-width="1.5"/>'
                   f'<path d="M{RW - 12} {axis_y - 5}L{RW - 1} {axis_y}L{RW - 12} {axis_y + 5}Z" fill="{c["ink"]}"/>\n')
    out += dots
    ly = axis_y + 34
    out.append(f'<path fill="{c["muted"]}" d="{f["sans"].path(AXIS_LEFT, 14, 0, ly)}"/>\n')
    out.append(f'<path fill="{c["muted"]}" d="{f["sans"].path(AXIS_RIGHT, 14, RW, ly, anchor="end")}"/>\n')
    out.append(f'<path fill="{c["ink"]}" d="{f["italic"].path(AXIS_CAPTION, 20, RW / 2, ly + 1, anchor="middle")}"/>\n')
    return "".join(out) + "</svg>\n"


# ---------------------------------------------------------------- buttons ---

def button(f, c, label):
    size, padx, h = 15, 20, 40
    w = round(f["sans_medium"].width(label, size) + 2 * padx)
    return (svg_open(w, h, label, f"Link to {label}") +
            f'<rect x=".75" y=".75" width="{w - 1.5}" height="{h - 1.5}" rx="8" fill="{c["paper"]}" stroke="{c["major"]}" stroke-width="1.5"/>\n'
            f'<path fill="{c["ink"]}" d="{f["sans_medium"].path(label, size, w / 2, 25.5, anchor="middle")}"/>\n</svg>\n')


# ---------------------------------------------------------------- main ------

if __name__ == "__main__":
    fonts = load_fonts()
    out = Path(__file__).resolve().parent
    for theme, colors in THEMES.items():
        (out / f"header-{theme}.svg").write_text(header(fonts, colors))
        (out / f"research-{theme}.svg").write_text(research(fonts, colors))
        for key, label in LINKS.items():
            (out / f"btn-{key}-{theme}.svg").write_text(button(fonts, colors, label))
    print("Wrote", len(list(out.glob("*.svg"))), "SVGs to", out)
