#!/usr/bin/env python3
"""Generate the profile README graphics (light + dark variants).

    pip install fonttools uharfbuzz brotli
    python assets/build.py

Text is converted to outlines because GitHub serves README SVGs as images, which cannot load web fonts.
Typefaces match the website (mazarbeik.github.io/azarbeik): Newsreader, Geist, Geist Mono — all SIL OFL.
They are downloaded once from github.com/google/fonts into ~/.cache/readme-fonts and instanced there.
Animations are CSS inside the SVG, play once (the verdict figure loops slowly) and stop under prefers-reduced-motion.
"""
import urllib.request
from pathlib import Path

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

# ------------------------------------------------------------------ content --

NAME = "Mohammad Mahdi Azarbeik"
KICKER = ["Offline reinforcement learning", "Off-policy evaluation", "Critical care"]
TAGLINE = "Offline reinforcement learning for critical care."
AFFILIATIONS = ["PhD candidate in Computer Science, TU Wien", "Researcher, Medical University of Vienna"]
LINKS = {  # file key -> label (the README wraps each button in its link)
    "website": "Website",
    "scholar": "Google Scholar",
    "orcid": "ORCID",
    "linkedin": "LinkedIn",
    "email": "Email",
    "cv": "CV (PDF)",
}

# ------------------------------------------------------------------- theme --
# Same tokens as the website (assets/css/site.css).

THEMES = {
    "light": dict(paper="#f5f3ee", paper2="#ece9e1", edge="#dad6cc", rule="#c3beb2", ink="#16171a", ink2="#3a3c41",
                  muted="#66676c", accent="#c2410c", accent_text="#b03a0a", wash="#f3e3da"),
    "dark": dict(paper="#101113", paper2="#18191c", edge="#2a2b2f", rule="#3c3d42", ink="#ece9e2", ink2="#c5c2ba",
                 muted="#8e8c86", accent="#ff7a4d", accent_text="#ff8a60", wash="#2a1a14"),
}

# ------------------------------------------------------------------- fonts --

GF = "https://raw.githubusercontent.com/google/fonts/main/ofl/"
SOURCES = {
    "newsreader": "newsreader/Newsreader%5Bopsz,wght%5D.ttf",
    "newsreader_italic": "newsreader/Newsreader-Italic%5Bopsz,wght%5D.ttf",
    "geist": "geist/Geist%5Bwght%5D.ttf",
    "geist_mono": "geistmono/GeistMono%5Bwght%5D.ttf",
}
INSTANCES = {  # name -> (source, axis location)
    "display": ("newsreader", {"opsz": 72, "wght": 400}),
    "italic": ("newsreader_italic", {"opsz": 28, "wght": 400}),
    "sans": ("geist", {"wght": 400}),
    "sans_medium": ("geist", {"wght": 500}),
    "mono": ("geist_mono", {"wght": 400}),
    "mono_medium": ("geist_mono", {"wght": 500}),
}
CACHE = Path.home() / ".cache" / "readme-fonts"


def ntos(v):
    s = f"{v:.1f}"
    return s[:-2] if s.endswith(".0") else s


class Face:
    """HarfBuzz shaping + fontTools outlines -> SVG path data."""

    def __init__(self, path):
        self.hb = hb.Font(hb.Face(hb.Blob.from_file_path(str(path))))
        tt = TTFont(str(path))
        self.gs, self.order, self.upem = tt.getGlyphSet(), tt.getGlyphOrder(), tt["head"].unitsPerEm

    def _shape(self, text, features=None):
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(self.hb, buf, {"kern": True, "liga": True, **(features or {})})
        return buf.glyph_infos, buf.glyph_positions

    def width(self, text, size, tracking=0.0):
        _, pos = self._shape(text)
        return sum(p.x_advance for p in pos) * size / self.upem + tracking * size * (len(pos) - 1)

    def path(self, text, size, x, y, tracking=0.0, anchor="start"):
        infos, pos = self._shape(text)
        scale = size / self.upem
        x -= {"start": 0, "middle": self.width(text, size, tracking) / 2, "end": self.width(text, size, tracking)}[anchor]
        pen = SVGPathPen(self.gs, ntos=ntos)
        cx = 0.0
        for info, p in zip(infos, pos):
            t = (scale, 0, 0, -scale, x + (cx + p.x_offset) * scale, y - p.y_offset * scale)
            self.gs[self.order[info.codepoint]].draw(TransformPen(pen, t))
            cx += p.x_advance + tracking * size / scale
        return pen.getCommands()


def load_fonts():
    CACHE.mkdir(parents=True, exist_ok=True)
    for key, rel in SOURCES.items():
        dst = CACHE / f"{key}.ttf"
        if not dst.exists():
            urllib.request.urlretrieve(GF + rel, dst)
    faces = {}
    for name, (src, loc) in INSTANCES.items():
        dst = CACHE / f"inst-{name}.ttf"
        if not dst.exists():
            instantiateVariableFont(TTFont(str(CACHE / f"{src}.ttf")), loc).save(str(dst))
        faces[name] = Face(dst)
    return faces


def text(face, s, size, x, y, fill, tracking=0.0, anchor="start", extra=""):
    return f'<path fill="{fill}"{extra} d="{face.path(s, size, x, y, tracking, anchor)}"/>'


def svg_open(w, h, title, desc):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" '
            f'aria-labelledby="t d"><title id="t">{title}</title><desc id="d">{desc}</desc>\n')


def card(w, h, c):
    return (f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="10" fill="{c["paper"]}" stroke="{c["edge"]}"/>\n')


# ------------------------------------------------- figure 1 (decision process) --
# Geometry shared with the website's Fig. 1 (index.html), in a 520 x 300 box.

STATES = [(40, 120), (140, 92), (240, 106), (340, 124), (440, 116)]
ACTS = [(90, 104), (190, 100), (290, 118), (390, 118)]
BRANCH = "M40 120 90 78M40 120 90 160M140 92 190 52M140 92 190 140M240 106 290 66M240 106 290 150M340 124 390 84M340 124 390 166"
BRANCH_TIPS = [(90, 78), (90, 160), (190, 52), (290, 66), (290, 150), (390, 84), (390, 166)]
OBS = ("M40 120C60 108 72 104 90 104S120 94 140 92 172 98 190 100 222 104 240 106 272 116 290 118 322 122 340 124 "
       "372 120 390 118 424 116 440 116")
POL = "M140 92C160 104 172 128 190 140S222 166 240 172 272 180 290 182 322 184 340 182 372 176 390 174 422 172 440 172"
POL_NODES = [(190, 140, 3.6, True), (240, 172, 6, False), (290, 182, 3.6, True), (340, 182, 6, False), (390, 174, 3.6, True)]


def figure1(f, c, ox, oy, s):
    """Fig. 1 at offset (ox, oy) and scale s, with a draw-on animation (CSS classes defined by the caller)."""
    g = [f'<g transform="translate({ox} {oy}) scale({s})">']
    g.append(f'<path class="f1-branch" d="{BRANCH}" fill="none" stroke="{c["rule"]}" stroke-dasharray="2 3"/>')
    for x, y in BRANCH_TIPS:
        g.append(f'<circle class="f1-branch" cx="{x}" cy="{y}" r="3" fill="{c["paper"]}" stroke="{c["rule"]}"/>')
    g.append(f'<path d="M40 262H480" stroke="{c["rule"]}"/>')
    for i, (x, _) in enumerate(STATES):
        g.append(f'<path d="M{x} 257v10" stroke="{c["rule"]}"/>')
        g.append(text(f["mono"], "t = 0" if i == 0 else str(i), 15, x, 292, c["muted"], anchor="middle"))
    g.append(f'<path class="f1-obs" pathLength="1" d="{OBS}" fill="none" stroke="{c["ink"]}" stroke-width="2.2" stroke-linecap="round"/>')
    g.append(f'<path class="f1-pol" d="{POL}" fill="none" stroke="{c["accent"]}" stroke-width="2.2" stroke-linecap="round" stroke-dasharray="7 6"/>')
    for i, (x, y) in enumerate(STATES):
        g.append(f'<circle class="f1-node" style="animation-delay:{0.45 + i * 0.3:.2f}s" cx="{x}" cy="{y}" r="8" '
                 f'fill="{c["paper"]}" stroke="{c["ink"]}" stroke-width="2"/>')
    for i, (x, y) in enumerate(ACTS):
        g.append(f'<circle class="f1-node" style="animation-delay:{0.6 + i * 0.3:.2f}s" cx="{x}" cy="{y}" r="4.2" fill="{c["ink"]}"/>')
    for i, (x, y, r, filled) in enumerate(POL_NODES):
        fill = c["accent"] if filled else c["paper"]
        g.append(f'<circle class="f1-pnode" style="animation-delay:{1.7 + i * 0.23:.2f}s" cx="{x}" cy="{y}" r="{r + 0.6}" '
                 f'fill="{fill}" stroke="{c["accent"]}" stroke-width="{0 if filled else 2}"/>')
    g.append(f'<g class="f1-q"><circle cx="440" cy="172" r="11" fill="{c["paper"]}" stroke="{c["accent"]}" stroke-width="2"/>'
             f'{text(f["sans_medium"], "?", 15, 440, 177.5, c["accent_text"], anchor="middle")}'
             f'{value_of_pi(f, c, 440, 210)}</g>')
    g.append("</g>")
    return "\n".join(g)


def value_of_pi(f, c, cx, y):
    """'value of π', centred: Newsreader italic has no Greek, so π comes from Geist, slanted to sit with the italic."""
    words, size = "value of ", 17
    w1 = f["italic"].width(words, size)
    w2 = f["sans"].width("π", size)
    x = cx - (w1 + w2) / 2
    return (text(f["italic"], words, size, x, y, c["accent_text"]) +
            f'<g transform="translate({x + w1:.1f} {y}) skewX(-12) translate({-(x + w1):.1f} {-y})">'
            f'{text(f["sans"], "π", size, x + w1, y, c["accent_text"])}</g>')


FIG1_CSS = """
.f1-obs{stroke-dasharray:1 1;stroke-dashoffset:1;animation:draw 1.6s cubic-bezier(.65,0,.35,1) .5s forwards}
.f1-pol{clip-path:inset(0 100% 0 0);animation:wipe 1.5s cubic-bezier(.65,0,.35,1) 1.5s forwards}
.f1-node,.f1-pnode,.f1-branch,.f1-q{opacity:0;animation:fade .5s cubic-bezier(.16,1,.3,1) forwards}
.f1-branch{animation-delay:1.7s}.f1-q{animation-delay:2.9s}
@keyframes draw{to{stroke-dashoffset:0}}
@keyframes wipe{to{clip-path:inset(0 0 0 0)}}
@keyframes fade{to{opacity:1}}
@media (prefers-reduced-motion:reduce){.f1-obs,.f1-pol,.f1-node,.f1-pnode,.f1-branch,.f1-q{animation:none;opacity:1;stroke-dashoffset:0;clip-path:none}}
"""

# ------------------------------------------------------------------- header --

HW, HH = 1200, 410


def header(f, c):
    out = [svg_open(HW, HH, NAME, f"{TAGLINE} {AFFILIATIONS[0]}; {AFFILIATIONS[1]}. A schematic shows an ICU stay as a "
                                    "sequence of decisions: the path clinicians took, and the counterfactual path of a "
                                    "learned policy whose value can only be estimated off-policy.")]
    out.append(f"<style>{FIG1_CSS}"
               ".rise{opacity:0;animation:rise .9s cubic-bezier(.16,1,.3,1) forwards}"
               "@keyframes rise{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}"
               "@media (prefers-reduced-motion:reduce){.rise{animation:none;opacity:1}}</style>\n")
    out.append(card(HW, HH, c))
    # kicker with accent separators
    x = 56
    parts = []
    for i, word in enumerate(KICKER):
        label = word.upper()
        parts.append(text(f["mono_medium"], label, 12.5, x, 66, c["ink2"], tracking=0.1))
        x += f["mono_medium"].width(label, 12.5, 0.1)
        if i < len(KICKER) - 1:
            parts.append(text(f["mono_medium"], "·", 12.5, x + 11, 66, c["accent"]))
            x += 30
    out.append('<g class="rise">' + "".join(parts) + "</g>")
    # name + affiliation marks
    name_w = f["display"].width(NAME, 76, -0.028)
    out.append(f'<g class="rise" style="animation-delay:.12s">{text(f["display"], NAME, 76, 52, 152, c["ink"], tracking=-0.028)}'
               f'{text(f["mono"], "1,2", 15, 52 + name_w + 10, 112, c["accent_text"])}</g>')
    # tagline
    out.append(f'<g class="rise" style="animation-delay:.28s">{text(f["italic"], TAGLINE, 29, 56, 212, c["ink2"])}</g>')
    # affiliations with hairline
    aff = [f'<path d="M56 268H604" stroke="{c["edge"]}"/>']
    for i, line in enumerate(AFFILIATIONS):
        y = 302 + i * 30
        aff.append(text(f["mono"], str(i + 1), 12, 56, y - 1, c["accent_text"]))
        aff.append(text(f["sans"], line, 17, 76, y, c["ink2"]))
    aff.append(f'<path d="M56 {302 + 30 + 22}H604" stroke="{c["edge"]}"/>')
    out.append('<g class="rise" style="animation-delay:.42s">' + "".join(aff) + "</g>")
    # figure
    out.append(figure1(f, c, 690, 108, 0.84))
    out.append(text(f["mono_medium"], "FIG. 1", 11, 724, 380, c["ink"], tracking=0.1))
    out.append(text(f["sans"], "An ICU stay as a decision process — schematic, not data", 12.5, 776, 380, c["muted"]))
    return "".join(o if o.endswith("\n") else o + "\n" for o in out) + "</svg>\n"


# ------------------------------------------------------- figure 2 (verdict) --

VW, VH = 960, 318
TRACK_X0, TRACK_X1 = 268, 920


def tx(v):
    return TRACK_X0 + v * (TRACK_X1 - TRACK_X0)


def verdict(f, c):
    out = [svg_open(VW, VH, "The estimator changes the verdict",
                    "Qualitative summary of the sepsis study. Tabular Q-learning sits above the clinicians under weighted "
                    "importance sampling but below them under FQE and DICE estimators. A Dueling DQN sits at clinician "
                    "level, with slight improvements, under FQE and DICE; the abstract states its standing only for these. "
                    "Ordinal positions only, not estimates.")]
    out.append("<style>"
               ".flip{animation:flip 7s infinite}"
               "@keyframes flip{0%,22%{transform:translateX(0);animation-timing-function:cubic-bezier(.34,1.18,.5,1)}"
               "36%,86%{transform:translateX(" f"{tx(.2) - tx(.82):.1f}" "px);animation-timing-function:cubic-bezier(.65,0,.35,1)}"
               "100%{transform:translateX(0)}}"
               ".lab-wis{animation:labwis 7s infinite}.lab-fqe{animation:labfqe 7s infinite}"
               "@keyframes labwis{0%,24%,96%,100%{opacity:1}34%,86%{opacity:.35}}"
               "@keyframes labfqe{0%,24%,96%,100%{opacity:.35}34%,86%{opacity:1}}"
               "@media (prefers-reduced-motion:reduce){.flip{animation:none;transform:translateX(" f"{tx(.2) - tx(.82):.1f}" "px)}"
               ".lab-wis,.lab-fqe{animation:none}}"
               "</style>\n")
    out.append(card(VW, VH, c))
    # scale header
    for label, v, anchor in (("BELOW CLINICIANS", 0, "start"), ("ON PAR", .5, "middle"), ("ABOVE CLINICIANS", 1, "end")):
        out.append(text(f["mono_medium"], label, 11, tx(v), 48, c["muted"], tracking=0.09, anchor=anchor))
    out.append(f'<path d="M40 64H{VW - 40}" stroke="{c["edge"]}"/>')
    # reference line (clinicians)
    out.append(f'<path d="M{tx(.5)} 74V250" stroke="{c["ink2"]}" stroke-opacity=".55" stroke-dasharray="4 4"/>')
    out.append(text(f["sans"], "Clinicians — the observed policy", 13, tx(.5), 276, c["muted"], anchor="middle"))

    def row(y, name, sub):
        r = [text(f["sans_medium"], name, 17, 40, y + 5, c["ink"])]
        if sub:
            r.append(text(f["sans"], sub, 13, 40, y + 25, c["muted"]))
        r.append(f'<path d="M{TRACK_X0} {y}H{TRACK_X1}" stroke="{c["rule"]}"/>')
        return r

    # row 1: tabular Q-learning
    y1 = 122
    out += row(y1, "Tabular Q-learning", "AI Clinician-style")
    for v, label, cls in ((.82, "WIS", "lab-wis"), (.2, "FQE · DICE", "lab-fqe")):
        out.append(f'<g class="{cls}"><path d="M{tx(v)} {y1 - 9}V{y1 + 9}" stroke="{c["rule"]}"/>'
                   f'{text(f["mono"], label, 11, tx(v), y1 - 18, c["ink2"], tracking=0.05, anchor="middle")}</g>')
    out.append(f'<circle cx="{tx(.82)}" cy="{y1}" r="7.5" fill="none" stroke="{c["accent"]}" stroke-width="1.5" stroke-dasharray="2.5 2.5" opacity=".7"/>')
    out.append(f'<path d="M{tx(.82) - 16} {y1 + 22}C{tx(.6)} {y1 + 40} {tx(.42)} {y1 + 40} {tx(.2) + 16} {y1 + 22}" fill="none" '
               f'stroke="{c["accent"]}" stroke-width="1.2" stroke-dasharray="3 4" opacity=".55"/>')
    out.append(f'<path d="M{tx(.2) + 16} {y1 + 22}l9 -1.5M{tx(.2) + 16} {y1 + 22}l5.5 7.5" stroke="{c["accent"]}" stroke-width="1.2" opacity=".55" fill="none"/>')
    out.append(f'<g class="flip"><circle cx="{tx(.82)}" cy="{y1}" r="11" fill="{c["wash"]}"/>'
               f'<circle cx="{tx(.82)}" cy="{y1}" r="7" fill="{c["accent"]}"/></g>')
    # row 2: dueling DQN
    y2 = 212
    out += row(y2, "Dueling DQN", None)
    out.append(f'<path d="M{tx(.57)} {y2 - 9}V{y2 + 9}" stroke="{c["rule"]}"/>')
    out.append(text(f["mono"], "FQE · DICE", 11, tx(.57) + 4, y2 - 18, c["ink2"], tracking=0.05, anchor="start"))
    out.append(f'<circle cx="{tx(.57)}" cy="{y2}" r="11" fill="{c["wash"]}"/><circle cx="{tx(.57)}" cy="{y2}" r="7" fill="{c["accent"]}"/>')
    out.append(text(f["mono"], "WIS: not shown", 11, tx(.82), y2 + 24, c["muted"], tracking=0.03, anchor="middle"))
    # footer note
    out.append(text(f["mono_medium"], "FIG. 2", 11, 40, 302, c["ink"], tracking=0.1))
    out.append(text(f["sans"], "Sepsis, MIMIC-IV v3.1 (ICCAI 2025). Ordinal positions only — not estimates.", 12.5, 92, 302, c["muted"]))
    return "".join(o if o.endswith("\n") else o + "\n" for o in out) + "</svg>\n"


# ------------------------------------------------------------------ buttons --

def button(f, c, label):
    size, padx, h = 14.5, 18, 38
    w = round(f["sans_medium"].width(label, size) + 2 * padx)
    return (svg_open(w, h, label, f"Link: {label}") +
            f'<rect x=".75" y=".75" width="{w - 1.5}" height="{h - 1.5}" rx="{(h - 1.5) / 2}" fill="{c["paper"]}" stroke="{c["rule"]}" stroke-width="1.2"/>\n'
            f'{text(f["sans_medium"], label, size, w / 2, 24, c["ink"], anchor="middle")}\n</svg>\n')


# --------------------------------------------------------------------- main --

if __name__ == "__main__":
    fonts = load_fonts()
    out = Path(__file__).resolve().parent
    for old in out.glob("*.svg"):
        old.unlink()
    for theme, colors in THEMES.items():
        (out / f"header-{theme}.svg").write_text(header(fonts, colors))
        (out / f"verdict-{theme}.svg").write_text(verdict(fonts, colors))
        for key, label in LINKS.items():
            (out / f"btn-{key}-{theme}.svg").write_text(button(fonts, colors, label))
    print("Wrote", len(list(out.glob("*.svg"))), "SVGs to", out)
