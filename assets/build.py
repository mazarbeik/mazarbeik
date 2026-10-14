#!/usr/bin/env python3
"""Regenerate the profile README graphics, in light and dark variants.

    pip install fonttools uharfbuzz
    python assets/build.py

Edit the content below and rerun. The graphics follow the website (mazarbeik.github.io/azarbeik): an ivory page and
wine panels around a burgundy accent, set in the same typefaces (Newsreader, Geist and Geist Mono; all SIL OFL), which
are downloaded once from github.com/google/fonts into ~/.cache/readme-fonts. Text is converted to outlines because
GitHub serves README SVGs as images, and images can't load web fonts.
"""
import math
import re
import urllib.request
from pathlib import Path
from xml.sax.saxutils import escape

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

# ---------------------------------------------------------------- content ---

NAME = ("Mohammad", "Mahdi", "Azarbeik")  # the middle name is set in italic, as on the website
EYEBROW = ["PhD candidate, TU Wien", "Researcher, Medical University of Vienna"]
PLACE = "Vienna, Austria"
STATEMENT = ("Machine learning for decisions under", "uncertainty")  # the last word is emphasised
INTERESTS = ["Offline reinforcement learning", "Off-policy evaluation", "Clinical decision support",
             "Large language models", "State estimation"]

FIELDS = [  # the website's research canvas, laid out along one time axis instead of morphing on scroll
    dict(title="Sensing & estimation", caption="Many noisy measurements, one estimate",
         where="M.Sc. · Sharif University of Technology", tint="f_sense"),
    dict(title="Learning systems", caption="One state, many possible decisions",
         where="PhD · TU Wien", tint="f_learn"),
    dict(title="Clinical decision support", caption="Vital signs, decided step by step",
         where="Medical University of Vienna", tint="f_clin"),
]

PROJECTS = ["sepsis", "rrt", "halluc", "motion", "wear"]  # one schematic per project card, drawn below

LINKS = {  # file key: (label, icon)
    "website": ("Website", "out"),
    "scholar": ("Google Scholar", "out"),
    "orcid": ("ORCID", "out"),
    "linkedin": ("LinkedIn", "out"),
    "email": ("Email", "arrow"),
    "cv": ("CV", "down"),
}

# ---------------------------------------------------------------- theme -----
# The website's tokens (assets/css/site.css). PAGE is the ivory page (the "cellar" by night), WINE the panel surface.
# A (colour, opacity) pair stands for the site's rgb(... / a) values.

PAGE = {
    "light": dict(bg="#f6f1ea", bg2="#eee6db", ink="#221418", ink2="#4b3a3e", muted="#6e5c63", rule="#e2d6c8",
                  rule2="#cbbbab", accent="#7c1d34", accent_text="#7c1d34", wash=("#7c1d34", .07),
                  aura=[("#7c1d34", .2), ("#d6969b", .3), ("#b09c8a", .28)]),
    "dark": dict(bg="#130c0f", bg2="#1c1317", ink="#f3e9e0", ink2="#d3c3ba", muted="#a6938c", rule="#2a1e23",
                 rule2="#46353b", accent="#c4495f", accent_text="#eba3ad", wash=("#c4495f", .13),
                 aura=[("#961e3c", .42), ("#d68291", .13), ("#8c6e5f", .14)]),
}
WINE = {
    "light": dict(bg="#4b1323", ink="#f8ece3", ink2="#ead3ca", muted="#cfaaa8", rule2="#7d3c4f", accent="#f0b3a5",
                  accent_text="#f4c3b7", glow=("#f0a096", .14), shade=("#14040a", .38),
                  f_sense="#d6bfa9", f_learn="#e79aa6", f_clin="#f6d2c4"),
    "dark": dict(bg="#2b0f18", ink="#f6eadf", ink2="#dec6bd", muted="#bb9b98", rule2="#5e2f3d", accent="#e47f90",
                 accent_text="#f2b4bc", glow=("#f0a096", .14), shade=("#14040a", .38),
                 f_sense="#d6bfa9", f_learn="#e79aa6", f_clin="#f6d2c4"),
}

EASE_OUT, EASE_IO, SPRING = "cubic-bezier(.16,1,.3,1)", "cubic-bezier(.76,0,.24,1)", "cubic-bezier(.34,1.4,.64,1)"

# ---------------------------------------------------------------- fonts -----

GF = "https://raw.githubusercontent.com/google/fonts/main/ofl/"
SOURCES = {
    "newsreader": "newsreader/Newsreader%5Bopsz,wght%5D.ttf",
    "newsreader_italic": "newsreader/Newsreader-Italic%5Bopsz,wght%5D.ttf",
    "geist": "geist/Geist%5Bwght%5D.ttf",
    "geist_mono": "geistmono/GeistMono%5Bwght%5D.ttf",
}
INSTANCES = {  # name: (source, axis location)
    "display": ("newsreader", {"opsz": 72, "wght": 400}),
    "display_italic": ("newsreader_italic", {"opsz": 72, "wght": 400}),
    "serif": ("newsreader", {"opsz": 28, "wght": 400}),
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
    """HarfBuzz shaping and fontTools outlines, to SVG path data. Tracking is in em, like CSS letter-spacing."""

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
        if not text:
            return 0.0
        _, pos = self._shape(text)
        return sum(p.x_advance for p in pos) * size / self.upem + tracking * size * (len(pos) - 1)

    def path(self, text, size, x, y, tracking=0.0, anchor="start"):
        if not text:
            return ""
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
        dst = CACHE / f"inst-{src}-{'-'.join(f'{k}{v}' for k, v in loc.items())}.ttf"
        if not dst.exists():
            instantiateVariableFont(TTFont(str(CACHE / f"{src}.ttf")), loc).save(str(dst))
        faces[name] = Face(dst)
    return faces


# ---------------------------------------------------------------- helpers ---

def paint(attr, colour):
    """fill="…" or stroke="…", with an opacity when the token is a (colour, opacity) pair."""
    if isinstance(colour, tuple):
        return f'{attr}="{colour[0]}" {attr}-opacity="{colour[1]}"'
    return f'{attr}="{colour}"'


def text(face, s, size, x, y, colour, tracking=0.0, anchor="start", extra=""):
    return f'<path {paint("fill", colour)}{extra} d="{face.path(s, size, x, y, tracking, anchor)}"/>'


def label(f, s, size, x, y, colour, anchor="start", tracking=0.11):
    """The website's .label: Geist Mono 500, uppercase, tracked."""
    return text(f["mono_medium"], s.upper(), size, x, y, colour, tracking, anchor)


def wrap(face, s, size, max_w, tracking=0.0):
    lines, cur = [], ""
    for word in s.split():
        trial = f"{cur} {word}".strip()
        if cur and face.width(trial, size, tracking) > max_w:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    return lines + [cur]


def line(pts):
    return "M" + "L".join(f"{ntos(x)} {ntos(y)}" for x, y in pts)


def simplify(pts, tol=0.12):
    """Ramer–Douglas–Peucker: drop the points that lie within tol px of the line through their neighbours."""
    if len(pts) < 3:
        return pts
    (ax, ay), (bx, by) = pts[0], pts[-1]
    dx, dy = bx - ax, by - ay
    norm = math.hypot(dx, dy) or 1
    i, dmax = 0, 0.0
    for k in range(1, len(pts) - 1):
        d = abs(dy * (pts[k][0] - ax) - dx * (pts[k][1] - ay)) / norm
        if d > dmax:
            i, dmax = k, d
    if dmax <= tol:
        return [pts[0], pts[-1]]
    return simplify(pts[: i + 1], tol)[:-1] + simplify(pts[i:], tol)


def svg_open(w, h, title, desc):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" '
            f'aria-labelledby="t d"><title id="t">{escape(title)}</title><desc id="d">{escape(desc)}</desc>\n')


def radial(gid, colour):
    """radial-gradient(closest-side, colour, transparent)"""
    hexc, a = colour
    return (f'<radialGradient id="{gid}"><stop offset="0" stop-color="{hexc}" stop-opacity="{a}"/>'
            f'<stop offset="1" stop-color="{hexc}" stop-opacity="0"/></radialGradient>')


def mark(c, x, y, s):
    """The ring, bar and dot of the website's brand mark (30 × 13 units), at (x, y) and scale s."""
    return (f'<g transform="translate({x} {y}) scale({s})" fill="none" stroke="{c["ink"]}" stroke-width="1.3">'
            f'<circle cx="5" cy="6.5" r="3.85"/><path d="M8.6 6.5h14.6"/>'
            f'<circle cx="26.05" cy="6.5" r="3.4" fill="{c["accent_text"]}" stroke="none"/></g>')


# ---------------------------------------------------------------- header ----
# The website's intro: the roles and the place, the name over two lines (the second indented and ending in the
# brand's dot), the statement beside it and the research interests underneath. Each line of the name rises out of its
# mask, the dot lands last, and the emphasis is underlined once everything has settled.

HW, PAD = 1200, 56
NAME_SIZE = 112


def statement(f, c, x, y, size, lh, max_w):
    """The statement, wrapped, with its last word in italic accent and underlined (the website's .hero__statement em)."""
    lines = wrap(f["serif"], f"{STATEMENT[0]} {STATEMENT[1]}.", size, max_w, -0.01)
    out = []
    for i, ln in enumerate(lines):
        if i == len(lines) - 1:
            lead = ln[: -len(STATEMENT[1]) - 1]
            out.append(text(f["serif"], lead, size, x, y, c["ink"], -0.01))
            ex = x + f["serif"].width(lead, size, -0.01)
            ew = f["italic"].width(STATEMENT[1], size, -0.01)
            out.append(text(f["italic"], STATEMENT[1], size, ex, y, c["accent_text"], -0.01))
            out.append(text(f["serif"], ".", size, ex + ew + 1, y, c["ink"]))
            out.append(f'<rect class="under" x="{ex:.1f}" y="{y + 5:.1f}" width="{ew:.1f}" height="1.5" fill="{c["accent"]}"/>')
        else:
            out.append(text(f["serif"], ln, size, x, y, c["ink"], -0.01))
        y += lh
    return out, len(lines)


def header(f, c):
    name_tr, mid_tr = -0.038, -0.045
    top = 64                                    # baseline of the roles
    y1 = top + 50 + 0.7 * NAME_SIZE             # baselines of the two name lines (line-height .86, as on the site)
    y2 = y1 + 0.86 * NAME_SIZE
    x0 = PAD - 0.03 * NAME_SIZE                 # optical margin for the M
    first = f"{NAME[0]} "
    x_mid = x0 + f["display"].width(first, NAME_SIZE, name_tr)
    x_last = x0 + 0.23 * (HW - 2 * PAD)
    w_last = f["display"].width(NAME[2], NAME_SIZE, name_tr)
    dot_r = 0.065 * NAME_SIZE
    dot_x = x_last + w_last + 0.06 * NAME_SIZE + dot_r
    sx = dot_x + dot_r + 56                     # the statement, bottom-aligned with the second line
    st_size, st_lh = 27, 34
    n_st = len(wrap(f["serif"], f"{STATEMENT[0]} {STATEMENT[1]}.", st_size, HW - PAD - sx, -0.01))
    ty = y2 + 0.28 * NAME_SIZE + 22             # the interests row
    hh = round(ty + 44)

    out = [svg_open(HW, hh, " ".join(NAME),
                    f"{'; '.join(EYEBROW)}. {PLACE}. {STATEMENT[0]} {STATEMENT[1]}. "
                    f"Research interests: {', '.join(INTERESTS)}.")]
    out.append(f"""<style>
.roll{{animation:roll .9s {SPRING} both}}
@keyframes roll{{from{{transform:translateY(108%)}}}}
.rise{{animation:rise 1.1s {EASE_OUT} both}}
@keyframes rise{{from{{opacity:0;transform:translateY(14px)}}}}
.land{{transform-box:fill-box;transform-origin:50% 100%;animation:land .8s {SPRING} 1.05s both}}
@keyframes land{{from{{opacity:0;transform:translateY(.6em)}}}}
.under{{transform-box:fill-box;transform-origin:0 50%;animation:under 1.2s {EASE_OUT} 1.5s both}}
@keyframes under{{from{{transform:scaleX(0)}}}}
@media (prefers-reduced-motion:reduce){{.roll,.rise,.land,.under{{animation:none}}}}
</style>
<defs>{radial("a1", c["aura"][0])}{radial("a2", c["aura"][1])}{radial("a3", c["aura"][2])}
<clipPath id="card"><rect x=".5" y=".5" width="{HW - 1}" height="{hh - 1}" rx="14"/></clipPath>
<clipPath id="l1"><rect x="0" y="{y1 - 1.0 * NAME_SIZE:.1f}" width="{HW}" height="{1.26 * NAME_SIZE:.1f}"/></clipPath>
<clipPath id="l2"><rect x="0" y="{y2 - 1.0 * NAME_SIZE:.1f}" width="{HW}" height="{1.26 * NAME_SIZE:.1f}"/></clipPath>
</defs>
<g clip-path="url(#card)"><rect width="{HW}" height="{hh}" fill="{c['bg']}"/>
<circle cx="1030" cy="0" r="420" fill="url(#a1)"/><circle cx="640" cy="{hh}" r="300" fill="url(#a2)"/><circle cx="20" cy="{hh}" r="340" fill="url(#a3)"/></g>
<rect x=".5" y=".5" width="{HW - 1}" height="{hh - 1}" rx="14" fill="none" stroke="{c['rule']}"/>
""")
    # the brand mark, then the two roles separated by an accent dot; the place on the right
    eb = [mark(c, PAD, top - 13, 1.4)]
    x = PAD + 42 + 22
    for i, s in enumerate(EYEBROW):
        eb.append(label(f, s, 12, x, top, c["ink2"], tracking=0.12))
        x += f["mono_medium"].width(s.upper(), 12, 0.12)
        if i < len(EYEBROW) - 1:
            eb.append(f'<circle cx="{x + 13:.1f}" cy="{top - 4.5}" r="2.5" fill="{c["accent"]}"/>')
            x += 26
    eb.append(text(f["mono"], PLACE, 13, HW - PAD, top, c["muted"], anchor="end"))
    eb.append(f'<path d="M{PAD} {top + 22}H{HW - PAD}" stroke="{c["rule2"]}"/>')
    out.append('<g class="rise">' + "".join(eb) + "</g>\n")
    # the name
    out.append(f'<g clip-path="url(#l1)"><g class="roll" style="animation-delay:.12s">'
               f'{text(f["display"], first, NAME_SIZE, x0, y1, c["ink"], name_tr)}'
               f'{text(f["display_italic"], NAME[1], NAME_SIZE, x_mid, y1, c["accent_text"], mid_tr)}</g></g>\n')
    out.append(f'<g clip-path="url(#l2)"><g class="roll" style="animation-delay:.3s">'
               f'{text(f["display"], NAME[2], NAME_SIZE, x_last, y2, c["ink"], name_tr)}</g></g>\n')
    out.append(f'<circle class="land" cx="{dot_x:.1f}" cy="{y2 - dot_r - 0.02 * NAME_SIZE:.1f}" r="{dot_r:.1f}" fill="{c["accent"]}"/>\n')
    # the statement
    st, _ = statement(f, c, sx, y2 - (n_st - 1) * st_lh, st_size, st_lh, HW - PAD - sx)
    out.append('<g class="rise" style="animation-delay:.55s">' + "".join(st) + "</g>\n")
    # the research interests: one run, separated by accent dots (the website's .hero__topics)
    row = [f'<path d="M{PAD} {ty - 34}H{HW - PAD}" stroke="{c["rule2"]}"/>',
           label(f, "Research interests", 11.5, PAD, ty, c["muted"])]
    x = PAD + f["mono_medium"].width("RESEARCH INTERESTS", 11.5, 0.11) + 32
    size = 15.5  # as large as the row allows
    while x + sum(f["sans_medium"].width(i, size, -0.005) for i in INTERESTS) + 22 * (len(INTERESTS) - 1) > HW - PAD:
        size -= 0.25
    for i, item in enumerate(INTERESTS):
        row.append(text(f["sans_medium"], item, size, x, ty, c["ink"], -0.005))
        x += f["sans_medium"].width(item, size, -0.005)
        if i < len(INTERESTS) - 1:
            row.append(f'<circle cx="{x + 11:.1f}" cy="{ty - 5}" r="2" fill="{c["accent_text"]}"/>')
            x += 22
    out.append('<g class="rise" style="animation-delay:.7s">' + "".join(row) + "</g>\n")
    return "".join(out) + "</svg>\n"


# ---------------------------------------------------------------- fields ----
# One signal line through the three fields, on a wine panel. Sensing: noisy measurements around one estimate, whose
# uncertainty band narrows. Learning: from that state the line branches into possible decisions and the band fans
# out; the accent branch is the chosen policy. Clinical: a vital-sign trace, with treatment decisions at regular steps.

FW = 960
TAU = math.tau
SPREAD = [-0.95, -0.55, -0.18, 0.2, 0.58, 0.92]  # the website's branch offsets; branch 1 is the policy
POLICY = 1


def smooth(a, b, v):
    t = min(1, max(0, (v - a) / (b - a)))
    return t * t * (3 - 2 * t)


def ecg(p):
    g = lambda mu, s: math.exp(-((p - mu) ** 2) / (2 * s * s))
    return 0.1 * g(0.14, 0.025) - 0.09 * g(0.235, 0.008) + g(0.26, 0.011) - 0.24 * g(0.285, 0.01) + 0.2 * g(0.5, 0.04)


class Rand:
    """The website canvas's Park–Miller generator (seed 3), so the measurements scatter the same way."""

    def __init__(self, seed=3):
        self.seed = seed

    def __call__(self):
        self.seed = (self.seed * 16807) % 2147483647
        return self.seed / 2147483647

    def gauss(self):
        u = v = 0
        while u == 0:
            u = self()
        while v == 0:
            v = self()
        return max(-2.2, min(2.2, math.sqrt(-2 * math.log(u)) * math.cos(TAU * v)))


def fields(f, c):
    x0, x1 = 40, FW - 40
    seg = (x1 - x0) / 3
    top, bot, axis = 50, 206, 236
    X = lambda i, u: x0 + seg * (i + u)
    Y = lambda v: top + (bot - top) * v

    A = lambda u: 0.47 + 0.2 * math.sin(TAU * 0.9 * u + 0.6) + 0.05 * math.sin(TAU * 2.6 * u + 2.1)
    sig_a = lambda u: 0.26 * (1 - u) ** 1.5 + 0.035
    a_end, c0 = A(1), 0.52
    fan = lambda u: 1 - (1 - smooth(0, 1, u) ** 0.9) ** 2
    pol = lambda u: a_end + (c0 - a_end) * smooth(0, 1, u) - 0.06 * math.sin(math.pi * u)
    B = lambda u, j: pol(u) + (SPREAD[j] - SPREAD[POLICY]) * 0.24 * fan(u) + 0.02 * math.sin(TAU * (u * 2.2 + j * 0.37)) * fan(u)
    C = lambda u: c0 - 0.36 * ecg((u * 3) % 1)

    us = [i / 119 for i in range(120)]
    uc = [i / 899 for i in range(900)]
    out = []

    # bands: the shape of each field's uncertainty
    band_a = [(X(0, u), Y(A(u) - sig_a(u))) for u in us] + [(X(0, u), Y(A(u) + sig_a(u))) for u in reversed(us)]
    lo = lambda u: min(B(u, j) for j in range(len(SPREAD))) - 0.03
    hi = lambda u: max(B(u, j) for j in range(len(SPREAD))) + 0.03
    band_b = [(X(1, u), Y(lo(u))) for u in us] + [(X(1, u), Y(hi(u))) for u in reversed(us)]
    band_c = simplify([(X(2, u), Y(C(u) - 0.024)) for u in uc]) + simplify([(X(2, u), Y(C(u) + 0.024)) for u in reversed(uc)])

    main = simplify([(X(0, u), Y(A(u))) for u in us] + [(X(1, u), Y(pol(u))) for u in us[1:]] +
                    [(X(2, u), Y(C(u))) for u in uc[1:]])

    rnd = Rand()
    dots = []
    for k in range(30):
        u = (k + 0.5) / 30 + (rnd() - 0.5) * 0.01
        dots.append((u, rnd.gauss()))

    accent_band = paint("fill", (c["accent"], 0.14))
    out.append(f'<g class="fade" style="animation-delay:.2s"><path {accent_band} d="{line(band_a)}Z"/></g>')
    out.append(f'<g class="fade" style="animation-delay:1.5s"><path {accent_band} d="{line(band_b)}Z"/></g>')
    out.append(f'<g class="fade" style="animation-delay:2.6s"><path {accent_band} d="{line(band_c)}Z"/></g>\n')
    # the time axis, and where one field hands over to the next
    out.append(f'<path d="M{x0} {axis}H{x1}" stroke="{c["rule2"]}"/>')
    for i in (1, 2):
        out.append(f'<path d="M{X(i, 0):.1f} {top - 22}V{axis + 6}" stroke="{c["rule2"]}" stroke-dasharray="2 4"/>')
    out.append(text(f["mono"], "t", 13, x1, axis + 20, c["muted"], anchor="end"))
    # learning: the possible decisions branch off from the estimate
    br = []
    for j in range(len(SPREAD)):
        if j == POLICY:
            continue
        br.append(f'<path d="{line([(X(1, u), Y(B(u, j))) for u in us])}" fill="none" stroke="{c["ink"]}" '
                  f'stroke-opacity=".42" stroke-width="1.1"/>')
        for k in range(1, 5):
            u = k / 4
            br.append(f'<circle cx="{X(1, u):.1f}" cy="{Y(B(u, j)):.1f}" r="{3 if k == 4 else 1.8}" fill="{c["ink"]}" fill-opacity=".42"/>')
    out.append('<g class="fade" style="animation-delay:1.4s">' + "".join(br) + "</g>\n")
    # sensing: the measurements
    ms = [f'<circle cx="{X(0, u):.1f}" cy="{Y(A(u) + n * sig_a(u) * 0.85):.1f}" r="2" fill="{c["ink"]}" fill-opacity=".75"/>'
          for u, n in dots]
    out.append('<g class="fade">' + "".join(ms) + "</g>\n")
    # the line itself: estimate, chosen policy, vital sign
    out.append(f'<path class="draw" pathLength="1" d="{line(main)}" fill="none" stroke="{c["accent"]}" stroke-width="2.2" '
               f'stroke-linejoin="round" stroke-linecap="round"/>\n')
    # the estimate becomes the state the decisions start from; the policy's steps
    pts = [f'<circle cx="{X(1, 0):.1f}" cy="{Y(a_end):.1f}" r="10" fill="none" stroke="{c["accent"]}"/>',
           f'<circle cx="{X(1, 0):.1f}" cy="{Y(a_end):.1f}" r="5" fill="{c["accent"]}"/>']
    for k in range(1, 5):
        u = k / 4
        pts.append(f'<circle cx="{X(1, u):.1f}" cy="{Y(pol(u)):.1f}" r="{4.5 if k == 4 else 2.6}" fill="{c["accent"]}"/>')
    out.append('<g class="fade" style="animation-delay:1.3s">' + "".join(pts) + "</g>\n")
    # clinical: a decision at each step, marked on the time axis
    sq = []
    for i in range(3):
        u = (i + 0.8) / 3
        px, py = X(2, u), Y(C(u))
        sq.append(f'<path d="M{px:.1f} {axis - 5}V{axis + 5}" stroke="{c["muted"]}"/>')
        sq.append(f'<rect x="{px - 3:.1f}" y="{py - 3:.1f}" width="6" height="6" fill="{c["accent"]}"/>')
    sq.append(label(f, "decision", 10.5, X(2, 0.8 / 3) + 7, axis + 20, c["muted"]))
    out.append('<g class="fade" style="animation-delay:2.9s">' + "".join(sq) + "</g>\n")

    # captions, one column per field
    bottom = 0
    for i, d in enumerate(FIELDS):
        tx = X(i, 0) + (0 if i == 0 else 18)
        w = seg - 24
        y = axis + 62
        cap = [f'<circle cx="{tx + 4.5:.1f}" cy="{y - 4.5}" r="4.5" fill="{c[d["tint"]]}"/>',
               label(f, f"{i + 1:02d}", 12, tx + 17, y, c["accent_text"])]
        y += 38
        for ln in wrap(f["serif"], d["title"], 25, w, -0.015):
            cap.append(text(f["serif"], ln, 25, tx, y, c["ink"], -0.015))
            y += 32
        y += 2
        for ln in wrap(f["italic"], d["caption"], 17, w):
            cap.append(text(f["italic"], ln, 17, tx, y, c["ink2"]))
            y += 24
        y += 14
        for ln in wrap(f["mono_medium"], d["where"].upper(), 11, w, 0.11):
            cap.append(label(f, ln, 11, tx, y, c["muted"]))
            y += 18
        bottom = max(bottom, y)
        out.append("".join(cap) + "\n")
    fh = round(bottom + 18)
    head = f"""<style>
.draw{{stroke-dasharray:1;stroke-dashoffset:0;animation:draw 3.4s {EASE_IO} .3s both}}
@keyframes draw{{from{{stroke-dashoffset:1}}}}
.fade{{animation:fade .9s {EASE_OUT} both}}
@keyframes fade{{from{{opacity:0}}}}
@media (prefers-reduced-motion:reduce){{.draw,.fade{{animation:none}}}}
</style>
<defs>{radial("glow", c["glow"])}{radial("shade", c["shade"])}
<clipPath id="panel"><rect width="{FW}" height="{fh}" rx="18"/></clipPath></defs>
<g clip-path="url(#panel)"><rect width="{FW}" height="{fh}" fill="{c['bg']}"/>
<ellipse cx="{FW * 0.88}" cy="0" rx="{FW * 0.7}" ry="330" fill="url(#glow)"/><ellipse cx="0" cy="{fh}" rx="{FW * 0.6}" ry="300" fill="url(#shade)"/></g>
"""
    title = "Research: one signal line through three fields"
    desc = "; ".join(f"{d['title']}, {d['caption'].lower()} ({d['where']})" for d in FIELDS) + "."
    return svg_open(FW, fh, title, desc) + head + "".join(out) + "</svg>\n"


# ---------------------------------------------------------------- projects --
# The website's project schematics (assets/js/glyphs.js), drawn in their resting state on a plate. All share a
# 320 × 200 drawing area; the labels are larger than on the website because the README shows the plates smaller.

PW, PH = 352, 242  # 16:11, like the website's plates
G_TEXT = 11.5


def g_styles(c):
    return dict(
        faint=f'fill="none" stroke="{c["rule2"]}"',
        grid=f'fill="{c["rule2"]}"',
        ink=f'fill="none" stroke="{c["ink"]}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"',
        acc=f'fill="none" stroke="{c["accent"]}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"',
        node=f'fill="{c["bg"]}" stroke="{c["ink"]}" stroke-width="1.5"',
        anode=f'fill="{c["accent"]}"',
        wash=paint("fill", c["wash"]),
        bar=f'fill="{c["ink"]}" fill-opacity=".16"',
        flag=f'fill="{c["accent"]}"',
    )


def restyle(style, **over):
    """A style's attributes with some replaced (stroke_width=1.3 sets stroke-width), so none is written twice."""
    attrs = dict(re.findall(r'([\w-]+)="([^"]*)"', style))
    attrs.update({k.replace("_", "-"): v for k, v in over.items()})
    return " ".join(f'{k}="{v}"' for k, v in attrs.items())


def g_text(f, c, s, x, y, anchor="start", accent=False):
    return label(f, s, G_TEXT, x, y, c["accent_text"] if accent else c["muted"], anchor, 0.08)


def r1(n):
    return round(n * 10) / 10


def glyph_sepsis(f, c, s):
    """The path clinicians took through a grid of patient states, and the one a learned policy would take."""
    grid = "".join(f'<circle cx="{40 + i * 40}" cy="{52 + r * 34}" r="1.4"/>' for i in range(7) for r in range(4))
    obs = [(40, 120), (80, 103), (120, 118), (160, 104), (200, 132), (240, 114), (280, 128)]
    pol = [(120, 118), (160, 84), (200, 64), (240, 76), (280, 54)]
    return "".join([
        f'<g {s["grid"]}>{grid}</g>', f'<path {s["ink"]} d="{line(obs)}"/>',
        *(f'<circle {s["node"]} cx="{x}" cy="{y}" r="4.2"/>' for x, y in obs),
        f'<path {s["acc"]} d="{line(pol)}"/>',
        *(f'<circle {s["anode"]} cx="{x}" cy="{y}" r="3.6"/>' for x, y in pol[1:-1]),
        f'<circle {s["acc"]} cx="280" cy="54" r="9"/>', g_text(f, c, "?", 280, 58, "middle", True),
        g_text(f, c, "Clinicians · observed", 40, 176), g_text(f, c, "Learned policy", 128, 38, accent=True)])


def glyph_rrt(f, c, s):
    """A marker rising over 4-hour steps, and the question of when to start."""
    X0, X1 = 34, 286
    Y = lambda x: 146 - 92 * ((x - X0) / (X1 - X0)) ** 1.75
    pts = [(X0 + (X1 - X0) * i / 40, Y(X0 + (X1 - X0) * i / 40)) for i in range(41)]
    ticks = [X0 + k * (X1 - X0) / 6 for k in range(7)]
    sx = ticks[3]
    return "".join([
        f'<path {s["faint"]} d="M{X0} 164H{X1}"/>', f'<path {s["faint"]} d="{"".join(f"M{r1(x)} 160v8" for x in ticks)}"/>',
        g_text(f, c, "0 h", X0, 186, "middle"), g_text(f, c, "12 h", r1(ticks[3]), 186, "middle"),
        g_text(f, c, "24 h", X1, 186, "middle"),
        f'<path {s["ink"]} d="{line(pts)}"/>',
        *(f'<circle {s["node"]} cx="{r1(x)}" cy="{r1(Y(x))}" r="3"/>' for x in ticks),
        f'<path {s["acc"]} d="M{r1(sx)} 30V160" stroke-dasharray="3 4"/>', g_text(f, c, "Start?", r1(sx), 22, "middle", True),
        f'<circle {s["wash"]} cx="{r1(sx)}" cy="{r1(Y(sx))}" r="13"/>', f'<circle {s["anode"]} cx="{r1(sx)}" cy="{r1(Y(sx))}" r="5"/>',
        g_text(f, c, "Kidney function", X1, 42, "end")])


def glyph_halluc(f, c, s):
    """Lines of generated text, scanned; two spans get flagged."""
    rows = [[38, 22, 46, 30, 54, 28], [26, 50, 34, 40, 22, 44], [44, 30, 24, 52, 36, 40], [30, 40, 58, 26, 34, 32], [48, 26, 36, 44]]
    flags = {(1, 2), (3, 2)}
    bars, marks = [], []
    for r, row in enumerate(rows):
        x, y = 34, 46 + r * 26
        for i, w in enumerate(row):
            if x + w > 290:
                break
            if (r, i) in flags:
                bars.append(f'<rect {s["flag"]} x="{x}" y="{y}" width="{w}" height="10" rx="5"/>')
                q = w / 8
                marks.append(f'<path {restyle(s["acc"], stroke_width=1.3)} d="M{x} {y + 17}q{ntos(q)} 4 {ntos(2 * q)} 0t{ntos(2 * q)} 0t{ntos(2 * q)} 0t{ntos(2 * q)} 0"/>')
            else:
                bars.append(f'<rect {s["bar"]} x="{x}" y="{y}" width="{w}" height="10" rx="5"/>')
            x += w + 8
    return "".join([f'<rect {s["wash"]} x="22" y="34" width="34" height="136" rx="8"/>',
                    f'<path {restyle(s["acc"], stroke_width=1)} d="M39 30V174"/>', *bars, *marks,
                    g_text(f, c, "Model output", 34, 22), g_text(f, c, "2 spans flagged", 290, 22, "end", True)])


def glyph_motion(f, c, s):
    """An arm with two inertial sensors, and the wrist path the filter estimates, with its uncertainty."""
    S, E, W = (92, 52), (124, 108), (186, 124)

    def sensor(a, b):
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        ang = math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
        return (f'<rect {restyle(s["acc"], fill=c["bg2"])} x="-7" y="-5" width="14" height="10" rx="2" '
                f'transform="translate({r1(mx)} {r1(my)}) rotate({r1(ang)})"/>')

    ells = [(214, 140, 9, 5, 20), (262, 120, 12, 6, -40), (236, 74, 14, 8, 30), (226, 108, 8, 5, 70)]
    return "".join([
        f'<path {s["faint"]} d="M{S[0]} {S[1]}L84 160" stroke-dasharray="2 4"/>', f'<circle {s["faint"]} cx="72" cy="28" r="14"/>',
        f'<path {restyle(s["ink"], stroke_width=2.2)} d="{line([S, E, W])}"/>', sensor(S, E), sensor(E, W),
        *(f'<circle {s["node"]} cx="{x}" cy="{y}" r="4.6"/>' for x, y in (S, E, W)),
        f'<path {s["acc"]} d="M186 124C222 150 268 142 272 110S236 60 216 76 212 120 250 130"/>',
        *(f'<ellipse {restyle(s["acc"], stroke_width=1)} cx="{x}" cy="{y}" rx="{a}" ry="{b}" transform="rotate({rot} {x} {y})"/>'
          for x, y, a, b, rot in ells),
        g_text(f, c, "IMU + SLAM", 34, 188), g_text(f, c, "Estimated wrist path", 290, 188, "end", True)])


def glyph_wear(f, c, s):
    """A wrist-worn sensor streaming a pulse waveform into a network."""
    def beat(x):
        return " ".join(f"L{x + dx} {y}" for dx, y in ((18, 100), (24, 96), (30, 100), (36, 100), (40, 104), (45, 76),
                                                      (50, 112), (55, 100), (66, 100), (72, 94), (78, 100), (80, 100)))
    wave = "M100 100 " + " ".join(beat(100 + k * 80) for k in range(4))
    arcs = "".join(f'<path {restyle(s["acc"], stroke_width=1.4, stroke_opacity=.8)} d="M{206 + r * 0.5} {100 - r}A{r} {r} 0 0 1 {206 + r * 0.5} {100 + r}"/>'
                   for r in (14, 24, 34))
    ends = [(276, 58), (292, 104), (268, 150)]
    return "".join([
        f'<defs><clipPath id="screen"><rect x="112" y="70" width="76" height="60" rx="13"/></clipPath></defs>',
        f'<path {s["faint"]} d="M124 64L128 22M176 64L172 22M124 136L128 178M176 136L172 178"/>',
        f'<rect {s["ink"]} x="104" y="62" width="92" height="76" rx="20"/>',
        f'<g clip-path="url(#screen)"><path {restyle(s["acc"], stroke_width=1.6)} d="{wave}"/></g>', arcs,
        f'<path {s["faint"]} d="M252 100L276 58M252 100L292 104M252 100L268 150"/>', f'<circle {s["node"]} cx="252" cy="100" r="4"/>',
        *(f'<circle {s["anode"]} cx="{x}" cy="{y}" r="5.5"/><circle {s["node"]} cx="{x}" cy="{y}" r="3"/>' for x, y in ends),
        g_text(f, c, "On-body sensor", 104, 192), g_text(f, c, "Network", 300, 34, "end", True)])


GLYPHS = {
    "sepsis": (glyph_sepsis, "Sepsis treatment: the path clinicians took through a grid of patient states, and the one a learned policy would take."),
    "rrt": (glyph_rrt, "Renal replacement therapy: a marker of kidney function over 24 hours in 4-hour steps, and the question of when to start."),
    "halluc": (glyph_halluc, "Hallucination detection: lines of generated text are scanned and two spans are flagged."),
    "motion": (glyph_motion, "Inertial motion capture: an arm with two inertial sensors, and the estimated wrist path with uncertainty ellipses."),
    "wear": (glyph_wear, "Wearables: a wrist-worn sensor streams a pulse waveform into a network."),
}


def plate(f, c, name):
    draw, desc = GLYPHS[name]
    return (svg_open(PW, PH, "Schematic", desc) +
            f'<rect x=".5" y=".5" width="{PW - 1}" height="{PH - 1}" rx="16" fill="{c["bg"]}" stroke="{c["rule"]}"/>\n'
            f'<g transform="translate({(PW - 320) / 2} {(PH - 200) / 2 - 4})">{draw(f, c, g_styles(c))}</g>\n'
            f'{label(f, "Schematic", 10, PW - 16, PH - 13, c["muted"], "end", 0.1)}\n</svg>\n')


# ---------------------------------------------------------------- buttons ---
# The website's pills: a hairline capsule, the label, and the link's icon (out, arrow for e-mail, down for the CV).

ICONS = {
    "out": "M3.5 8.5 8.5 3.5M4 3.5h4.5V8",
    "arrow": "M2 6h8M6.5 2.5 10 6 6.5 9.5",
    "down": "M6 1.5v7M2.75 5.5 6 8.75 9.25 5.5M2 10.75h8",
}


def button(f, c, label_text, icon):
    size, padx, h, gap, isz = 14, 16, 38, 8, 11
    tw = f["sans_medium"].width(label_text, size, -0.005)
    w = round(padx + tw + gap + isz + padx)
    ix, iy = padx + tw + gap, (h - isz) / 2
    return (svg_open(w, h, label_text, f"Link: {label_text}") +
            f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="{(h - 1) / 2}" fill="{c["bg"]}" stroke="{c["rule2"]}"/>\n'
            f'{text(f["sans_medium"], label_text, size, padx, 24, c["ink"], -0.005)}\n'
            f'<path transform="translate({ix:.1f} {iy:.1f}) scale({isz / 12:.4f})" d="{ICONS[icon]}" fill="none" stroke="{c["ink"]}" '
            f'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>\n</svg>\n')


# ---------------------------------------------------------------- main ------

if __name__ == "__main__":
    fonts = load_fonts()
    out = Path(__file__).resolve().parent
    for old in out.glob("*.svg"):
        old.unlink()
    for theme in ("light", "dark"):
        page, wine = PAGE[theme], WINE[theme]
        (out / f"header-{theme}.svg").write_text(header(fonts, page))
        (out / f"fields-{theme}.svg").write_text(fields(fonts, wine))
        for name in PROJECTS:
            (out / f"project-{name}-{theme}.svg").write_text(plate(fonts, page, name))
        for key, (label_text, icon) in LINKS.items():
            (out / f"btn-{key}-{theme}.svg").write_text(button(fonts, page, label_text, icon))
    print("Wrote", len(list(out.glob("*.svg"))), "SVGs to", out)
