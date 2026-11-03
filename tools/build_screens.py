"""Generates Figma-importable SVG screens into design/ (wireframes, mockups, mockups-dark).

Visual language: iOS 26 (inset grouped lists, large-title navigation, floating tab bar, sheets).
Text is start-anchored using real Inter metrics, so it lands in the same place in Figma.
Each run checks every text for overflow, overlap and WCAG contrast, and every tappable layer
(btn-, satir-, sekme-, geri) for a 44 x 44 pt minimum.
"""
from pathlib import Path
from xml.sax.saxutils import escape

from fontTools.ttLib import TTFont

from illustrations import NAME_TO_DISH, TINT, dish_svg, hero_garnish

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE / "design"
FONTS = BASE / "tools" / "fonts"
W, H = 360, 800
M = 16                 # side margin
GX, GW = 16, 328       # inset grouped list
RADIUS = 20
ROW = 52               # pantry rows: room for a 36 pt ingredient painting
TAB_Y = 717            # floating tab bar: 21 pt from the bottom edge

LIGHT = {
    "bg": "#F7EBDD", "surface": "#FFFAF3", "text": "#2B1D14", "text2": "#6B5646",
    "sep": "#E8D7C2", "accent": "#B3401E", "on_accent": "#FFFFFF", "fill": "#EFDFCB",
    "thumb": "#FFFFFF", "glass": "#FFFAF3", "glass_line": "#E8D7C2", "tabsel": "#F7EBDD",
    "photo": "#F2E3CF", "dim": "#BFAE9C", "gray3": "#C9B6A1", "control": "#6B5646",
    "red": "#C4281C", "on_red": "#FFFFFF", "red_text": "#B3261A", "switch_off": "#E8D7C2",
    "sheet": "#F7EBDD", "sheet_cell": "#FFFAF3",
    "herb": "#3B6E35", "tag_red": "#FAE4DB", "tag_green": "#E0ECD6", "tag_yellow": "#F7E6B5",
    "tag_text_y": "#7A5200", "rule": "#EADBC6", "ink": "#2B1D14", "tape": "#E9C46A",
    "cam": "#000000", "preview": "#1C1C1E", "cam_text": "#FFFFFF", "cam_glass": "#3A3A3C", "on_paint": "#000000",
}
DARK = {
    "bg": "#1B1511", "surface": "#2A211B", "text": "#F7EBDD", "text2": "#C8B6A3",
    "sep": "#3E332A", "accent": "#FF8A65", "on_accent": "#1B1511", "fill": "#3A2F27",
    "thumb": "#5C4D41", "glass": "#2A211B", "glass_line": "#3E332A", "tabsel": "#3A2F27",
    "photo": "#3A2F27", "dim": "#000000", "gray3": "#5A4C40", "control": "#C8B6A3",
    "red": "#E9152D", "on_red": "#FFFFFF", "red_text": "#FF6F61", "switch_off": "#3E332A",
    "sheet": "#2A211B", "sheet_cell": "#3A2F27",
    "herb": "#9CCB8C", "tag_red": "#4A271D", "tag_green": "#263821", "tag_yellow": "#40341A",
    "tag_text_y": "#EBC66A", "rule": "#251D17", "ink": "#F7EBDD", "tape": "#8C6A2B",
    "cam": "#000000", "preview": "#1C1C1E", "cam_text": "#FFFFFF", "cam_glass": "#3A3A3C", "on_paint": "#000000",
}
WIRE = {
    "bg": "#F2F2F2", "surface": "#FFFFFF", "text": "#1A1A1A", "text2": "#5E5E5E",
    "sep": "#C8C8C8", "accent": "#3A3A3A", "on_accent": "#FFFFFF", "fill": "#E2E2E2",
    "thumb": "#FFFFFF", "glass": "#FFFFFF", "glass_line": "#D0D0D0", "tabsel": "#EDEDED",
    "photo": "#DADADA", "dim": "#C8C8C8", "gray3": "#B0B0B0", "control": "#5E5E5E",
    "red": "#3A3A3A", "on_red": "#FFFFFF", "red_text": "#3A3A3A", "switch_off": "#DADADA",
    "sheet": "#F2F2F2", "sheet_cell": "#FFFFFF",
    "herb": "#3A3A3A", "tag_red": "#E2E2E2", "tag_green": "#E2E2E2", "tag_yellow": "#E2E2E2",
    "tag_text_y": "#3A3A3A", "rule": "#F2F2F2", "ink": "#1A1A1A", "tape": "#CCCCCC",
    "cam": "#222222", "preview": "#444444", "cam_text": "#FFFFFF", "cam_glass": "#555555", "on_paint": "#1A1A1A",
}
MOCK = LIGHT  # kept for older imports

# Hand-painted gouache illustrations (design/cizimler/web), embedded into the mockups.
import base64
def _uri(f):
    mime = "image/png" if f.suffix == ".png" else "image/jpeg"
    return f"data:{mime};base64," + base64.b64encode(f.read_bytes()).decode()


WEB = ROOT / "cizimler" / "web"
PAINTED = {f.stem: _uri(f) for f in WEB.glob("*.jpg")}
# m- ingredients, s- scenes (cream, framed), d- small doodles, k- cover vignettes (transparent PNG)
for prefix, folder in (("m", "malzeme"), ("s", "sahne"), ("d", "sus"), ("k", "kapak")):
    PAINTED.update({f"{prefix}-{f.stem}": _uri(f) for f in sorted((WEB / folder).glob("*.*"))})
SCENE_DOODLES = {"buyutec": ("biber", "maydanoz"), "tencere": ("defne", "karabiber"),
                 "defter": ("kasik", "dereotu"), "sepet": ("limon", "sarimsak")}
import itertools
CLIP_IDS = itertools.count(1)   # unique across all files, so screens can share one HTML page
# pantry / list names -> ingredient painting
INGREDIENT = {"Yoğurt": "yogurt", "Domates": "domates", "Yumurta": "yumurta", "Patates": "patates",
              "Soğan": "sogan", "Peynir": "peynir", "Maydanoz": "maydanoz", "Biber": "biber",
              "Tereyağı": "tereyagi", "Salatalık": "salatalik", "Ekmek": "ekmek", "Süt": "sut"}
# state / expiry label -> tag colours (background, text)
TAGS = {"Yarın": ("tag_red", "accent"), "Var": ("tag_green", "herb"), "Azaldı": ("tag_yellow", "tag_text_y")}

WEIGHTS = {400: "Regular", 500: "Medium", 600: "SemiBold", 700: "Bold"}
METRICS = {}
for weight, name in WEIGHTS.items():
    font = TTFont(FONTS / f"Inter-{name}.ttf", lazy=True)
    METRICS[weight] = (font.getBestCmap(), font["hmtx"].metrics, font["head"].unitsPerEm)


# notebook handwriting fonts (OFL): Patrick Hand for text, Caveat Bold for titles and emphasis
for family, file in (("Patrick Hand", "PatrickHand-Regular"), ("Caveat", "Caveat-Bold")):
    font = TTFont(FONTS / f"{file}.ttf", lazy=True)
    METRICS[family] = (font.getBestCmap(), font["hmtx"].metrics, font["head"].unitsPerEm)


def wobble_rect(x, y, w, h, r, seed):
    """Rounded rectangle drawn with a slightly unsteady hand."""
    rng = random.Random(seed)
    j = lambda: rng.uniform(-0.9, 0.9)
    r = min(r, h / 2, w / 2)
    pts = [f"M{x + r:.1f} {y + j():.1f}", f"L{x + w * 0.5:.1f} {y + j():.1f}", f"L{x + w - r:.1f} {y + j():.1f}",
           f"Q{x + w + j():.1f} {y + j():.1f} {x + w + j():.1f} {y + r:.1f}",
           f"L{x + w + j():.1f} {y + h * 0.5:.1f}", f"L{x + w + j():.1f} {y + h - r:.1f}",
           f"Q{x + w + j():.1f} {y + h + j():.1f} {x + w - r:.1f} {y + h + j():.1f}",
           f"L{x + w * 0.5:.1f} {y + h + j():.1f}", f"L{x + r:.1f} {y + h + j():.1f}",
           f"Q{x + j():.1f} {y + h + j():.1f} {x + j():.1f} {y + h - r:.1f}",
           f"L{x + j():.1f} {y + h * 0.5:.1f}", f"L{x + j():.1f} {y + r:.1f}",
           f"Q{x + j():.1f} {y + j():.1f} {x + r:.1f} {y + j():.1f}Z"]
    return " ".join(pts)


def wobble_circle(cx, cy, r, seed):
    rng = random.Random(seed)
    n = 10
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        rr = r + rng.uniform(-0.6, 0.6)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    mids = [((pts[i][0] + pts[(i + 1) % n][0]) / 2, (pts[i][1] + pts[(i + 1) % n][1]) / 2) for i in range(n)]
    d = f"M{mids[-1][0]:.1f} {mids[-1][1]:.1f}"
    for i in range(n):
        d += f" Q{pts[i][0]:.1f} {pts[i][1]:.1f} {mids[i][0]:.1f} {mids[i][1]:.1f}"
    return d + "Z"


import math
import random


def text_width(s, size, weight, family="Inter"):
    cmap, hmtx, upem = METRICS[weight if family == "Inter" else family]
    return sum(hmtx[cmap[ord(ch)]][0] for ch in s) * size / upem


def luminance(hex_color):
    channels = [int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    r, g, b = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    hi, lo = sorted((luminance(a), luminance(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


# SF Symbols-style icons, drawn around (0, 0) in a ~22 pt box. Keys are SF Symbols names.
ICONS = {
    "house.fill": [("f", "M-9 -1 L0 -9 L9 -1 V9 H3 V3 H-3 V9 H-9 Z")],
    "bookmark": [("s", "M-6 -9 H6 V10 L0 5 L-6 10 Z")],
    "bookmark.fill": [("f", "M-6 -9 H6 V10 L0 5 L-6 10 Z")],
    "list.bullet": [("s", "M-3 -6 H9 M-3 0 H9 M-3 6 H9"), ("d", (-8, -6)), ("d", (-8, 0)), ("d", (-8, 6))],
    "chevron.backward": [("s", "M4 -8 L-4 0 L4 8")],
    "chevron.forward": [("s", "M-3 -6 L3 0 L-3 6")],
    "camera": [("s", "M-10 -5 Q-10 -6 -9 -6 H-5 L-3 -9 H3 L5 -6 H9 Q10 -6 10 -5 V7 Q10 8 9 8 H-9 Q-10 8 -10 7 Z"),
               ("c", (0, 1, 4))],
    "keyboard": [("s", "M-10 -7 H10 Q11 -7 11 -6 V6 Q11 7 10 7 H-10 Q-11 7 -11 6 V-6 Q-11 -7 -10 -7 Z"
                       " M-7 -3 H-5 M-2 -3 H0 M3 -3 H5 M-5 3 H5")],
    "magnifyingglass": [("c", (-2, -2, 6)), ("s", "M2.5 2.5 L8 8")],
    "plus": [("s", "M0 -8 V8 M-8 0 H8")],
    "xmark": [("s", "M-6 -6 L6 6 M6 -6 L-6 6")],
    "square.and.arrow.up": [("s", "M-4 -2 H-8 V10 H8 V-2 H4 M0 -10 V4 M-4 -6 L0 -10 L4 -6")],
    "rectangle.portrait.and.arrow.right": [("s", "M2 -6 V-9 H-9 V9 H2 V6 M-3 0 H10 M6 -4 L10 0 L6 4")],
    "circle": [("c", (0, 0, 11))],
    "questionmark.circle": [("c", (0, 0, 9)), ("s", "M-3 -3 Q-3 -6 0 -6 Q3 -6 3 -3 Q3 -1 0 0 V2"), ("d", (0, 5))],
    "wifi.slash": [("s", "M-10 -2 Q0 -11 10 -2 M-6 2 Q0 -4 6 2 M-10 -10 L10 10"), ("d", (0, 7))],
    "exclamationmark.triangle": [("s", "M0 -10 L11 9 H-11 Z M0 -3 V3"), ("d", (0, 6))],
    "fork.knife": [("s", "M-9 -10 V-4 Q-9 -1 -6 -1 Q-3 -1 -3 -4 V-10 M-6 -10 V10 M6 10 V-10 Q10 -6 10 1 H6")],
    "cart": [("s", "M-11 -8 H-8 L-5 4 H8 L10 -4 H-7"), ("d", (-4, 8)), ("d", (7, 8))],
    "refrigerator.fill": [("f", "M-7 -10 H7 Q8 -10 8 -9 V9 Q8 10 7 10 H-7 Q-8 10 -8 9 V-9 Q-8 -10 -7 -10 Z"),
                          ("k", "M-8 -3 H8 M-4 -7.5 V-5.5 M-4 0 V4")],
    "book.fill": [("f", "M0 -6 Q-5 -9 -10 -8 V8 Q-5 7 0 10 Q5 7 10 8 V-8 Q5 -9 0 -6 Z"), ("k", "M0 -6 V10")],
    "book": [("s", "M0 -6 Q-5 -9 -10 -8 V8 Q-5 7 0 10 Q5 7 10 8 V-8 Q5 -9 0 -6 Z M0 -6 V10")],
    "photo.on.rectangle": [("s", "M-7 -9 H10 V4 M-10 -6 H7 V8 H-10 Z M-10 6 L-4 0 L1 5 L3 3 L7 7")],
}


class Screen:
    def __init__(self, theme, wire=False):
        self.c = theme
        self.wire = wire
        self.parts, self.rects, self.texts, self.targets, self.stack = [], [], [], [], []
        self.seed = 0
        self.r(0, 0, W, H, "bg")
        if not wire:   # faint ruled lines, like a notebook page
            lines = "".join(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="{theme["rule"]}" stroke-width="1"/>'
                            for y in range(196, H, 28))
            self.parts.append(f'<g id="defter-cizgileri">{lines}</g>')

    # primitives ---------------------------------------------------------------------------
    def r(self, x, y, w, h, fill="surface", rx=0, stroke=None, id=None):
        i = f' id="{id}"' if id else ""
        if fill is None:   # invisible hotspot, used as a prototype target in Figma
            self.parts.append(f'<rect{i} x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="#000000" fill-opacity="0"/>')
        elif not self.wire and rx > 0 and h >= 10 and w >= 20:   # hand-drawn box with an ink outline
            self.seed += 1
            d = wobble_rect(x, y, w, h, rx, self.seed * 7919 + int(x * 13 + y))
            self.parts.append(f'<path{i} d="{d}" fill="{self.c[fill]}" stroke="{self.c["ink"]}" '
                              f'stroke-opacity="0.55" stroke-width="1.2" stroke-linejoin="round"/>')
        else:
            s = f' stroke="{self.c[stroke]}" stroke-width="0.5"' if stroke else ""
            self.parts.append(f'<rect{i} x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{self.c[fill]}"{s}/>')
        self.rects.append((x, y, w, h, self.c[fill] if fill else None))

    def circle(self, cx, cy, r, fill=None, stroke=None, width=1.5):
        f = self.c[fill] if fill else "none"
        if not self.wire and r >= 8:
            self.seed += 1
            s = f' stroke="{self.c[stroke]}" stroke-width="{width}"' if stroke else ""
            self.parts.append(f'<path d="{wobble_circle(cx, cy, r, self.seed * 31 + int(cx + cy))}" fill="{f}"{s}/>')
            return
        s = f' stroke="{self.c[stroke]}" stroke-width="{width}"' if stroke else ""
        self.parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{f}"{s}/>')

    def painting(self, x, y, w, h, key, rx=0, id=None):
        """Embed a hand-painted gouache image (cream paper background)."""
        data = PAINTED.get(key)
        if self.wire or not data:
            self.r(x, y, w, h, "photo", rx, id=id)
            return
        i = f' id="{id}"' if id else f' id="cizim-{key}"'
        if data.startswith("data:image/png"):   # transparent cut-out: no clip, no background
            self.parts.append(f'<image{i} x="{x}" y="{y}" width="{w}" height="{h}" href="{data}"/>')
            return
        cid = f"kirp-{next(CLIP_IDS)}"
        self.parts.append(f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}"/></clipPath>'
                          f'<image{i} x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid slice" '
                          f'clip-path="url(#{cid})" href="{data}"/>')
        self.rects.append((x, y, w, h, "#F7EBDD"))

    def doodle(self, cx, cy, size, key, angle=0):
        """A small painted cut-out dropped onto the page (mockups only)."""
        data = PAINTED.get(key)
        if self.wire or not data:
            return
        self.parts.append(f'<image id="sus-{key[2:]}" x="{cx - size / 2:.1f}" y="{cy - size / 2:.1f}" width="{size}" '
                          f'height="{size}" transform="rotate({angle} {cx} {cy})" href="{data}"/>')

    def polaroid(self, cx, cy, size, key, angle=-3):
        """A painting stuck into the notebook: white border, slight tilt, a strip of tape."""
        pad, bottom = 8, 22
        w, h = size + 2 * pad, size + pad + bottom
        x, y = cx - w / 2, cy - h / 2
        self.parts.append(f'<g id="polaroid-{key}" transform="rotate({angle} {cx} {cy})">')
        self.r(x, y, w, h, "surface", 6)
        self.painting(x + pad, y + pad, size, size, key, 3)
        self.parts.append(f'<rect id="bant" x="{cx - 30}" y="{y - 9}" width="60" height="18" fill="{self.c["tape"]}" '
                          f'fill-opacity="0.75" transform="rotate({-angle * 2} {cx} {y})"/>')
        self.parts.append("</g>")

    def tag(self, right, cy, label, kind=None):
        """Coloured pill used for states and expiry (Var, Azaldı, Yarın, 2 gün)."""
        bg, fg = TAGS.get(label, ("tag_yellow", "tag_text_y")) if kind is None else kind
        w = self.tw(label, 15, 600) + 20
        self.r(round(right - w, 1), cy - 13, round(w, 1), 26, bg, 13)
        self.t(right - w / 2, cy + 5.5, label, 15, fg, 600, "middle")

    def font(self, size, weight, family=None):
        """Resolve the font actually drawn: handwriting on mockups, Inter on wireframes and system chrome."""
        if self.wire:
            return "Inter", size, weight
        if family is None or family == "Fraunces":
            if family == "Fraunces" or weight >= 600:
                return "Caveat", round(size * 1.3, 1), 700
            return "Patrick Hand", round(size * 1.1, 1), 400   # its x-height is smaller than Inter's
        if family == "Caveat":
            return family, size, 700
        return family, size, weight

    def tw(self, s, size, weight=400, family=None):
        f, sz, wt = self.font(size, weight, family)
        return text_width(s, sz, wt, f)

    def t(self, x, y, s, size=17, fill="text", weight=400, anchor="start", id=None, family=None):
        family, size, weight = self.font(size, weight, family)
        width = text_width(s, size, weight, family)
        left = {"start": x, "middle": x - width / 2, "end": x - width}[anchor]
        i = f' id="{id}"' if id else ""
        self.parts.append(f'<text{i} x="{left:.1f}" y="{y}" font-family="{family}" font-size="{size}" '
                          f'font-weight="{weight}" fill="{self.c[fill]}">{escape(s)}</text>')
        self.texts.append((left, y - size * 0.76, width, size * 0.98, s, size, self.c[fill], len(self.rects)))

    def icon(self, name, cx, cy, color="text", scale=1.0, width=1.7, knock="glass"):
        col = self.c[color]
        out = [f'<g id="sf-{name}" transform="translate({cx} {cy}) scale({scale})">']
        for kind, d in ICONS[name]:
            if kind == "s":
                out.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{width}" '
                           f'stroke-linecap="round" stroke-linejoin="round"/>')
            elif kind == "f":
                out.append(f'<path d="{d}" fill="{col}"/>')
            elif kind == "c":
                out.append(f'<circle cx="{d[0]}" cy="{d[1]}" r="{d[2]}" fill="none" stroke="{col}" stroke-width="{width}"/>')
            elif kind == "k":   # cut-out lines drawn in the colour behind the symbol
                out.append(f'<path d="{d}" fill="none" stroke="{self.c[knock]}" stroke-width="1.6" stroke-linecap="round"/>')
            else:
                out.append(f'<circle cx="{d[0]}" cy="{d[1]}" r="1.4" fill="{col}"/>')
        out.append("</g>")
        self.parts.append("".join(out))

    def spinner(self, cx, cy, color="text2"):
        out = ['<g id="etkinlik-gostergesi">']
        for i in range(8):
            import math
            a = math.pi / 4 * i
            x1, y1 = cx + 5 * math.cos(a), cy + 5 * math.sin(a)
            x2, y2 = cx + 10 * math.cos(a), cy + 10 * math.sin(a)
            out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{self.c[color]}" '
                       f'stroke-width="2.4" stroke-linecap="round" stroke-opacity="{0.25 + i * 0.1:.2f}"/>')
        out.append("</g>")
        self.parts.append("".join(out))

    def open(self, id):
        self.parts.append(f'<g id="{id}">')
        self.stack.append((id, len(self.rects)))

    def close(self):
        self.parts.append("</g>")
        id, start = self.stack.pop()
        rs = self.rects[start:]
        if rs:
            x0 = min(r[0] for r in rs)
            y0 = min(r[1] for r in rs)
            x1 = max(r[0] + r[2] for r in rs)
            y1 = max(r[1] + r[3] for r in rs)
            self.targets.append((id, x1 - x0, y1 - y0))

    # system chrome ------------------------------------------------------------------------
    def status(self, color="text"):
        self.open("durum-cubugu")
        self.t(58, 37, "9:41", 16, color, 600, "middle", family="Inter")
        c = self.c[color]
        bars = "".join(f'<rect x="{268 + i * 4.5}" y="{34 - 3 - i * 2}" width="3" height="{3 + i * 2}" rx="0.8" fill="{c}"/>'
                       for i in range(4))
        wifi = (f'<path d="M292 28 Q299.5 21 307 28 M295 31 Q299.5 27 304 31" fill="none" stroke="{c}" '
                f'stroke-width="1.8" stroke-linecap="round"/><circle cx="299.5" cy="34" r="1.5" fill="{c}"/>')
        batt = (f'<rect x="312" y="26" width="23" height="11" rx="3" fill="none" stroke="{c}" stroke-opacity="0.45"/>'
                f'<rect x="314" y="28" width="17" height="7" rx="1.5" fill="{c}"/>'
                f'<rect x="336" y="29.5" width="1.6" height="4" rx="0.8" fill="{c}" fill-opacity="0.45"/>')
        self.parts.append(bars + wifi + batt)
        self.close()

    def home_indicator(self, color="text"):
        self.r(113, 787, 134, 5, color, 2.5, id="ana-ekran-cubugu")

    def glass_button(self, x, y, icon, id, fill="glass", color="text"):
        self.open(id)
        self.r(x, y, 44, 44, fill, 22, "glass_line" if fill == "glass" else None)
        self.icon(icon, x + 22, y + 22, color)
        self.close()

    def prominent_pill(self, right, y, label, id):
        w = self.tw(label, 17, 600) + 32
        self.open(id)
        self.r(round(right - w, 1), y, round(w, 1), 44, "accent", 22)
        self.t(right - w / 2, y + 28, label, 17, "on_accent", 600, "middle")
        self.close()

    def navbar(self, title, sub=None, back=True, trailing=(), title_id=None, cover=None):
        self.status()
        if cover:
            self.doodle(W - M - 50, 150, 96, f"k-{cover}", 0)
        if back:
            self.glass_button(M, 58, "chevron.backward", "geri")
        x = W - M
        for icon, id in trailing:
            x -= 44
            self.glass_button(x, 58, icon, id)
            x -= 8
        self.t(M, 142, title, 34, "text", 700, id=title_id, family="Fraunces")
        if sub:
            self.t(M, 170, sub, 17, "text2")

    def tabbar(self, active):
        self.open("sekme-cubugu")
        self.r(21, TAB_Y, 318, 62, "glass", 31, "glass_line")
        self.close()
        tabs = [("Dolap", "dolap", "refrigerator.fill"), ("Tarifler", "tarifler", "book.fill"),
                ("Liste", "liste", "list.bullet")]
        for i, (label, key, icon) in enumerate(tabs):
            cx = 74 + i * 106
            on = i == active
            self.open(f"sekme-{key}")
            self.r(cx - 49, TAB_Y + 4, 98, 54, "tabsel" if on else None, 27)
            self.icon(icon, cx, TAB_Y + 22, "accent" if on else "text", knock="tabsel" if on else "glass")
            self.t(cx, TAB_Y + 49, label, 10, "accent" if on else "text", 600 if on else 500, "middle")
            self.close()
        self.home_indicator()

    # content ------------------------------------------------------------------------------
    def header(self, y, text, color="accent", doodle=None, angle=-12):
        if doodle and not self.wire:
            self.doodle(20 + self.tw(text, 26, 700, "Caveat") + 26, y - 8, 36, f"d-{doodle}", angle)
        if self.wire:
            self.t(20, y, text, 17, "text", 600)
        else:
            self.t(20, y + 2, text, 26, color, 700, family="Caveat")
            w = text_width(text, 26, 700, "Caveat")
            self.parts.append(f'<path d="M20 {y + 7} Q{20 + w * 0.3:.1f} {y + 4} {20 + w * 0.55:.1f} {y + 7} '
                              f'T{20 + w + 6:.1f} {y + 6}" fill="none" stroke="{self.c[color]}" stroke-opacity="0.45" '
                              f'stroke-width="2.4" stroke-linecap="round"/>')

    def footer(self, y, lines):
        for i, line in enumerate(lines):
            self.t(32, y + i * 18, line, 13, "text2")

    def group(self, y, heights, sep_x=32, fill="surface"):
        """Inset grouped section. Returns the top y of each row."""
        total = sum(heights)
        self.r(GX, y, GW, total, fill, RADIUS)
        tops, cur = [], y
        for i, h in enumerate(heights):
            tops.append(cur)
            cur += h
            if i < len(heights) - 1:
                sx = sep_x[i] if isinstance(sep_x, (list, tuple)) else sep_x
                self.r(sx, cur - 0.5, GX + GW - sx, 0.5, "sep")
        return tops

    def prominent(self, y, label, id, x=M, w=GW):
        self.open(id)
        self.r(x, y, w, 50, "accent", 25)
        self.t(x + w / 2, y + 31, label, 17, "on_accent", 600, "middle")
        self.close()

    def plain(self, y, label, id, cx=W / 2, weight=400):
        w = self.tw(label, 17, weight) + 32
        self.open(id)
        self.r(round(cx - w / 2, 1), y, round(w, 1), 44, None, 22)
        self.t(cx, y + 28, label, 17, "accent", weight, "middle")
        self.close()

    def photo(self, x, y, w, h, ratio, rx=0, dish=None):
        if dish and not self.wire and PAINTED:  # hand-painted gouache illustration
            name = f"{dish}-16x9" if ratio == "16x9" else f"{dish}-kare"
            data = PAINTED.get(name)
            if data:
                cid = f"kirp-{next(CLIP_IDS)}"
                self.parts.append(f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}"/></clipPath>'
                                  f'<image id="cizim-{dish}" x="{x}" y="{y}" width="{w}" height="{h}" '
                                  f'preserveAspectRatio="xMidYMid slice" clip-path="url(#{cid})" '
                                  f'href="{data}"/>')
                self.rects.append((x, y, w, h, "#F7EBDD"))
                return
        if dish and not self.wire:  # flat dish illustration on a tinted tile
            tint = TINT[dish] if self.c is LIGHT else self.c["photo"]
            self.parts.append(f'<rect id="foto-alani-{ratio}" x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{tint}"/>')
            self.rects.append((x, y, w, h, tint))
            if ratio == "16x9":
                self.parts.append(hero_garnish(dish))
                self.parts.append(dish_svg(dish, x + w / 2, y + h / 2 + 14, h / 100 * 0.78))
            else:
                self.parts.append(dish_svg(dish, x + w / 2, y + h / 2, w / 100 * 0.9))
            return
        self.r(x, y, w, h, "photo", rx, id=f"foto-alani-{ratio}")
        if not self.wire:  # a quiet placeholder icon, so the empty photo slot reads as intended
            self.icon("fork.knife", x + w / 2, y + h / 2, "gray3", 0.8 if w < 100 else 1.6, 1.6)
        if self.wire and w > 100:
            self.t(x + w / 2, y + h - 20, f"Fotoğraf alanı ({ratio.replace('x', ':')})", 13, "text2", 400, "middle")

    def recipe_row(self, top, name, meta, id, h=64, title_id=None):
        self.open(id)
        self.r(GX, top, GW, h, None)
        self.photo(32, top + 8, 48, 48, "1x1", 8, NAME_TO_DISH.get(name))
        self.t(92, top + 28, name, 17, "text", 400, id=title_id)
        self.t(92, top + 48, meta, 13, "text2")
        self.icon("chevron.forward", 322, top + h / 2, "gray3", 1, 2)
        self.close()

    def unavailable(self, cy, icon, title, lines, scene=None):
        if scene and not self.wire:
            left, right = SCENE_DOODLES.get(scene, (None, None))
            if left:
                self.doodle(W / 2 - 96, cy - 78, 48, f"d-{left}", -18)
            if right:
                self.doodle(W / 2 + 96, cy - 22, 48, f"d-{right}", 16)
            self.polaroid(W / 2, cy - 50, 104, f"s-{scene}", -3)
        else:
            self.icon(icon, W / 2, cy, "text2", 2.0, 1.4)
        self.t(W / 2, cy + 52, title, 22, "text", 700, "middle", family="Fraunces")
        for i, line in enumerate(lines):
            self.t(W / 2, cy + 80 + i * 22, line, 17, "text2", 400, "middle")
        return cy + 80 + (len(lines) - 1) * 22

    def switch(self, x, y, on):
        self.r(x, y, 51, 31, "accent" if on else "switch_off", 15.5)
        self.circle(x + (35.5 if on else 15.5), y + 15.5, 13.5, "thumb")

    def segmented(self, y, labels, selected, id):
        self.open(id)
        self.r(GX, y, GW, 32, "fill", 16)
        seg = GW / len(labels)
        for i, label in enumerate(labels):
            x = GX + i * seg
            if i == selected:
                self.r(round(x + 2, 1), y + 2, round(seg - 4, 1), 28, "thumb", 14)
            self.t(x + seg / 2, y + 21, label, 13, "text", 600 if i == selected else 500, "middle")
        self.close()

    def svg(self):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">\n'
                + "\n".join(self.parts) + "\n</svg>\n")


# screens --------------------------------------------------------------------------------------
def login(s):
    s.navbar("Giriş Yap", "Dolaptan hesabınla devam et.", back=False)
    rows = s.group(196, [44, 44], 32)
    s.open("alan-eposta")
    s.r(GX, rows[0], GW, 44, None)
    s.t(32, rows[0] + 28, "E-posta", 17, "text2")
    s.close()
    s.open("alan-sifre")
    s.r(GX, rows[1], GW, 44, None)
    s.t(32, rows[1] + 28, "Şifre", 17, "text2")
    s.close()
    s.prominent(304, "Giriş Yap", "btn-giris")
    s.plain(362, "Hesap Oluştur", "btn-hesap-olustur")
    s.plain(406, "Hesapsız Dene", "btn-hesapsiz", weight=400)
    if not s.wire:
        s.polaroid(W / 2, 600, 180, "s-dolap-dolu", 3)
        s.doodle(50, 520, 60, "d-maydanoz", -20)
        s.doodle(314, 500, 50, "d-limon", 12)
        s.doodle(310, 690, 64, "d-biber", 28)
        s.doodle(54, 700, 52, "d-cay", -8)
    s.home_indicator()


def thumb(s, x, cy, d, name):
    """Round ingredient painting; an empty circle on wireframes."""
    key = INGREDIENT.get(name)
    if s.wire or not key:
        s.r(x, cy - d / 2, d, d, "photo", d / 2)
    else:
        s.painting(x, cy - d / 2, d, d, f"m-{key}", d / 2)


def value_row(s, y, name, value, id, h=ROW, value_color="text2"):
    s.open(id)
    s.r(GX, y, GW, h, None)
    d = 36 if h >= 52 else 30
    thumb(s, 28, y + h / 2, d, name)
    s.t(28 + d + 12, y + h / 2 + 6, name, 17)
    if value:
        if value in TAGS or value.endswith("gün"):
            s.tag(330, y + h / 2, value)
        else:
            s.t(328, y + h / 2 + 6, value, 17, value_color, 400, "end")
    s.close()


def pantry_sections(s, top, soon, have):
    s.header(top, "Yakında bozulacak", doodle="biber", angle=20)
    tops = s.group(top + 12, [ROW] * len(soon), 76)
    for y, (name, when, id) in zip(tops, soon):
        value_row(s, y, name, when, id)
    y2 = top + 12 + ROW * len(soon) + 36
    s.header(y2, "Dolapta", "herb", doodle="maydanoz")
    return y2 + 12


def pantry(s, notify=False):
    s.navbar("Dolap", "Ev · 2 üye", back=False, cover="raf",
             trailing=[("camera", "btn-tara"), ("rectangle.portrait.and.arrow.right", "btn-cikis")])
    start = pantry_sections(s, 208, [("Yoğurt", "Yarın", "satir-yogurt"), ("Domates", "2 gün", "satir-domates")], None)
    have = [("Yumurta", "Var"), ("Peynir", "Azaldı"), ("Patates", "Var"), ("Maydanoz", "Azaldı")]
    tops = s.group(start, [ROW] * len(have) + [44], [76] * len(have))
    for y, (name, state) in zip(tops, have):
        value_row(s, y, name, state, f"satir-{name.lower().replace('ğ', 'g').replace('ı', 'i')}")
    s.open("btn-malzeme-yaz")
    s.r(GX, tops[-1], GW, 44, None)
    s.icon("plus", 42, tops[-1] + 22, "accent")
    s.t(60, tops[-1] + 28, "Malzeme Ekle", 17, "accent")
    s.close()
    s.prominent(tops[-1] + 60, "Ne Pişirsem?", "btn-ne-pisirsem")
    s.tabbar(0)
    if notify:
        s.open("bildirim")
        s.r(8, 50, 344, 84, "glass", 24, "glass_line")
        s.r(20, 62, 38, 38, "accent", 9)
        s.icon("refrigerator.fill", 39, 81, "on_accent", 0.9, knock="accent")
        s.t(70, 76, "Dolaptan", 15, "text", 600)
        s.t(340, 76, "şimdi", 13, "text2", 400, "end")
        s.t(70, 97, "Yoğurt yarın bozuluyor.", 15)
        s.t(70, 117, "Bu akşam cacık yapabilirsin.", 15)
        s.close()


def sheet_base(s, title, close_id="btn-kapat"):
    s.r(0, 0, W, H, "dim")
    s.status()
    s.r(12, 46, 336, 40, "surface", 12)
    s.r(0, 58, W, 760, "sheet", 38)
    s.r(162, 64, 36, 5, "gray3", 2.5, id="tutamac")
    s.glass_button(M, 78, "xmark", close_id, "sheet_cell")
    s.t(W / 2, 106, title, 17, "text", 600, "middle")


def edit_item(s):
    sheet_base(s, "Yoğurt")
    s.prominent_pill(W - M, 78, "Kaydet", "btn-kaydet")
    s.header(158, "Durum")
    s.segmented(170, ["Var", "Azaldı", "Bitti"], 0, "secim-durum")
    s.header(236, "Son kullanma", doodle="sarimsak")
    tops = s.group(248, [44, 44], 32, "sheet_cell")
    s.open("btn-tarih")
    s.r(GX, tops[0], GW, 44, None)
    s.t(32, tops[0] + 28, "Tarih", 17)
    w = s.tw("3 Kas 2026", 17, 400) + 22
    s.r(round(328 - w, 1), tops[0] + 7, round(w, 1), 30, "fill", 8)
    s.t(328 - 11, tops[0] + 28, "3 Kas 2026", 17, "text", 400, "end")
    s.close()
    s.open("satir-hatirlat")
    s.r(GX, tops[1], GW, 44, None)
    s.t(32, tops[1] + 28, "Hatırlat", 17)
    s.switch(277, tops[1] + 6.5, True)
    s.close()
    s.footer(360, ["Bozulmadan bir gün önce bildirim gelir."])
    (y,) = s.group(400, [44], 32, "sheet_cell")
    s.open("btn-dolaptan-cikar")
    s.r(GX, y, GW, 44, None)
    s.t(32, y + 28, "Dolaptan Çıkar", 17, "red_text")
    s.close()
    s.home_indicator()


def camera_base(s):
    s.r(0, 0, W, H, "cam")
    s.status("cam_text")
    s.r(0, 110, W, 480, "preview", id="kamera-onizleme")
    if s.wire:
        s.t(W / 2, 355, "Kamera önizlemesi (3:4)", 13, "cam_text", 400, "middle")


def scan(s):
    camera_base(s)
    s.glass_button(M, 58, "xmark", "btn-kapat", "cam_glass", "cam_text")
    s.t(W / 2, 622, "Rafları kadraja al", 13, "cam_text", 400, "middle")
    s.open("btn-galeri")
    s.r(40, 678, 44, 44, "cam_glass", 10)
    s.icon("photo.on.rectangle", 62, 700, "cam_text")
    s.close()
    s.open("btn-deklansor")
    s.r(143, 663, 74, 74, None, 37)
    s.circle(180, 700, 35, None, "cam_text", 4)
    s.circle(180, 700, 29, "cam_text")
    s.close()
    s.home_indicator("cam_text")


def analyzing(line_y):
    def draw(s):
        camera_base(s)
        s.r(0, line_y, W, 2, "cam_text", 1, id="tarama-cizgisi")
        s.spinner(W / 2, 622, "cam_text")
        s.t(W / 2, 660, "Malzemeler aranıyor…", 17, "cam_text", 600, "middle")
        s.open("btn-iptal")
        s.r(130, 690, 100, 44, "cam_glass", 22)
        s.t(180, 718, "İptal", 17, "cam_text", 400, "middle")
        s.close()
        s.home_indicator("cam_text")
    return draw


def new_items(s):
    s.navbar("Yeni Malzemeler", "Kontrol et, tarihleri biz tahmin ettik.")
    s.header(208, "8 malzeme bulundu", doodle="kasik", angle=30)
    rows = [("Yumurta", "12 Kas"), ("Domates", "4 Kas"), ("Biber", "10 Kas"), ("Soğan", "1 Ara"),
            ("Peynir", "20 Kas"), ("Patates", "25 Kas"), ("Maydanoz", "7 Kas")]
    tops = s.group(220, [60] + [44] * len(rows), 70)
    s.open("satir-yogurt")
    s.r(GX, tops[0], GW, 60, None)
    thumb(s, 28, tops[0] + 30, 30, "Yoğurt")
    s.t(70, tops[0] + 26, "Yoğurt", 17)
    s.t(70, tops[0] + 46, "Emin değiliz, kontrol et", 13, "text2")
    s.icon("questionmark.circle", 320, tops[0] + 30, "text2")
    s.close()
    for i, (name, date) in enumerate(rows):
        y = tops[i + 1]
        if name == "Domates":   # shown mid-swipe to document the delete action
            s.open(f"satir-{i + 2}")
            thumb(s, 28, y + 22, 30, name)
            s.t(70, y + 28, name, 17)
            s.r(270, y, 74, 44, "red")
            s.t(307, y + 28, "Sil", 17, "on_red", 400, "middle")
            s.close()
        else:
            value_row(s, y, name, date, f"satir-{i + 2}", h=44)
    s.footer(tops[-1] + 68, ["Tarihler tahmini. Yanlışsa satıra dokunup düzelt."])
    s.prominent(666, "Dolaba Ekle", "btn-dolaba-ekle")
    s.home_indicator()


def no_ingredients(s):
    s.navbar("Yeni Malzemeler")
    s.unavailable(270, "magnifyingglass", "Malzeme Bulunamadı",
                  ["Fotoğraf net değilse yeniden çek", "ya da malzemeleri kendin ekle."], "buyutec")
    s.prominent(400, "Malzeme Ekle", "btn-malzeme-ekle")
    s.plain(460, "Yeniden Çek", "btn-yeniden-cek")
    s.home_indicator()


def prefs(s):
    sheet_base(s, "Tercihler")
    s.prominent_pill(W - M, 78, "Tarif Öner", "btn-tarif-oner")
    s.header(158, "Süre", doodle="cay", angle=0)
    s.segmented(170, ["15 dk", "30 dk", "1 saat"], 1, "secim-sure")
    s.header(236, "Kişi sayısı")
    s.segmented(248, ["1", "2", "4", "6"], 1, "secim-kisi")
    s.header(314, "Eksik malzeme")
    s.segmented(326, ["Olmasın", "En fazla 1", "Fark etmez"], 1, "secim-eksik")
    s.header(392, "Alerjiler", doodle="dereotu")
    tops = s.group(404, [44] * 4, 32, "sheet_cell")
    allergens = [("Gluten", "gluten", False), ("Süt", "sut", True), ("Yumurta", "yumurta", False),
                 ("Fındık", "findik", False)]
    for y, (name, key, on) in zip(tops, allergens):
        s.open(f"satir-{key}")
        s.r(GX, y, GW, 44, None)
        s.t(32, y + 28, name, 17)
        s.switch(277, y + 6.5, on)
        s.close()
    s.footer(602, ["Önce bozulacak malzemeler kullanılır.", "Tarifler yapay zeka ile üretilir.",
                   "Alerjenleri yine de kontrol et."])
    s.home_indicator()


def recipes(s):
    s.navbar("Öneriler", "Önce bozulacaklara göre", cover="kitap")
    rows = [("Menemen", "15 dk · 2 kişilik", "Domatesi değerlendirir", "satir-menemen", None),
            ("Cacık", "10 dk · 2 kişilik", "Yoğurdu değerlendirir", "satir-cacik", None),
            ("Patatesli Omlet", "20 dk · 2 kişilik", "Eksik: Tereyağı", "satir-omlet", "tarif-baslik")]
    for i, (name, meta, note, id, tid) in enumerate(rows):
        y = 200 + i * 124
        s.open(id)
        s.r(GX, y, GW, 112, "surface", 18)
        s.photo(28, y + 8, 96, 96, "1x1", 12, NAME_TO_DISH.get(name))
        s.t(138, y + 36, name, 17, "text", 600, id=tid)
        s.t(138, y + 60, meta, 13, "text2")
        s.t(138, y + 84, note, 13, "text2" if note.startswith("Eksik") else "accent")
        s.icon("chevron.forward", 322, y + 56, "gray3", 1, 2)
        s.close()
    s.plain(584, "Başka Tarifler Öner", "btn-baska-tarif")
    s.home_indicator()


def recipes_loading(s):
    s.navbar("Öneriler", "Önce bozulacaklara göre", cover="kitap")
    s.spinner(W / 2, 330)
    s.t(W / 2, 372, "Tarifler hazırlanıyor…", 17, "text2", 400, "middle")
    s.home_indicator()


def recipes_error(s):
    s.navbar("Öneriler", "Önce bozulacaklara göre", cover="kitap")
    end = s.unavailable(300, "exclamationmark.triangle", "Tarifler Alınamadı",
                        ["Bağlantını kontrol edip", "tekrar dene."], "tencere")
    s.plain(end + 22, "Tekrar Dene", "btn-tekrar-dene", weight=600)
    s.home_indicator()


def recipe_body(s):
    s.photo(0, 0, W, 202, "16x9", dish="omlet")
    s.status("text" if s.wire else "on_paint")  # the painting stays cream in dark mode
    s.glass_button(M, 58, "chevron.backward", "geri")
    s.glass_button(W - M - 44, 58, "bookmark", "btn-kaydet")
    s.t(M, 250, "Patatesli Omlet", 34, "text", 700, id="tarif-baslik", family="Fraunces")
    s.t(M, 276, "20 dk · 2 kişilik", 17, "text2")
    s.header(314, "Malzemeler", doodle="maydanoz")
    tops = s.group(326, [44, 44], 32)
    s.t(32, tops[0] + 28, "Patates, yumurta, soğan, peynir", 17)
    s.t(32, tops[1] + 28, "Tereyağı (eksik)", 17)
    s.open("btn-listeye-ekle")
    s.r(220, tops[1], 124, 44, None)
    s.t(328, tops[1] + 28, "Listeye Ekle", 17, "accent", 400, "end")
    s.close()
    s.header(450, "Yapılışı", "herb", doodle="cirpici", angle=24)
    steps = ["Patatesleri küp küp doğra.", "Tavada kızarana dek kavur.", "Soğanı ekleyip karıştır.",
             "Yumurtaları çırpıp dök.", "Peyniri ekle, 5 dk pişir."]
    tops = s.group(462, [44] * 5, 56)
    for i, (y, step) in enumerate(zip(tops, steps)):
        if s.wire:
            s.t(32, y + 28, str(i + 1), 17, "text2")
        else:
            s.r(28, y + 9, 26, 26, ["tag_red", "tag_yellow", "tag_green"][i % 3], 13)
            s.t(41, y + 30, str(i + 1), 20, ["accent", "tag_text_y", "herb"][i % 3], 700, "middle", family="Caveat")
        s.t(64 if not s.wire else 56, y + 28, step, 17)
        if i == len(steps) - 1:   # a step with a time gets a one-tap timer
            s.open("btn-zamanlayici")
            s.r(262, y, 82, 44, None)
            s.tag(330, y + 22, "5 dk", ("tag_yellow", "tag_text_y"))
            s.close()


def recipe(s):
    recipe_body(s)
    s.prominent(704, "Pişirdim", "btn-pisirdim")
    s.home_indicator()


def cooked(s):
    s.r(0, 0, W, H, "dim")
    s.status()
    s.r(36, 278, 288, 212, "surface", 28, id="uyari")
    if not s.wire:
        s.parts[-1] = s.parts[-1].replace('y="278"', 'y="190"').replace('height="212"', 'height="300"')
        s.rects[-1] = (36, 190, 288, 300, s.c["surface"])
        s.painting(132, 206, 96, 96, "s-tencere", 48)
    s.t(W / 2, 318 + (10 if not s.wire else 0), "Afiyet olsun!", 22 if not s.wire else 17, "text", 700 if not s.wire else 600,
        "middle", family="Fraunces")
    for i, line in enumerate(["Kullanılan malzemeler dolapta", "“Azaldı” olarak işaretlenecek.",
                              "Bitenler listeye eklenecek."]):
        s.t(W / 2, 350 + i * 20, line, 15, "text2", 400, "middle")
    s.open("btn-vazgec")
    s.r(52, 422, 124, 48, "fill", 24)
    s.t(114, 452, "Vazgeç", 17, "text", 400, "middle")
    s.close()
    s.open("btn-tamam")
    s.r(184, 422, 124, 48, "accent", 24)
    s.t(246, 452, "Tamam", 17, "on_accent", 600, "middle")
    s.close()
    s.home_indicator()


def saved_rows(s, top, rows):
    tops = s.group(top, [64] * len(rows), 92)
    for y, (name, meta, id) in zip(tops, rows):
        s.recipe_row(y, name, meta, id)
    return top + 64 * len(rows)


def saved(s):
    s.navbar("Tarifler", back=False)
    s.open("alan-tarif-ara")
    s.r(GX, 156, GW, 44, None)
    s.r(GX, 158, GW, 40, "surface", 20)
    s.icon("magnifyingglass", 38, 178, "text2", 0.8)
    s.t(54, 184, "Ara", 17, "text2")
    s.close()
    s.header(240, "Kayıtlı", doodle="defne")
    cards = [("Menemen", ["Menemen"], "15 dk · 2 kişilik", "satir-menemen"),
             ("Mercimek Çorbası", ["Mercimek", "Çorbası"], "30 dk · 4 kişilik", "satir-mercimek"),
             ("Patatesli Omlet", ["Patatesli", "Omlet"], "20 dk · 2 kişilik", "satir-omlet"),
             ("Zeytinyağlı Fasulye", ["Zeytinyağlı", "Fasulye"], "40 dk · 4 kişilik", "satir-fasulye")]
    for i, (name, lines, meta, id) in enumerate(cards):
        x, y = GX + (i % 2) * 172, 256 + (i // 2) * 216
        s.open(id)
        s.r(x, y, 156, 204, "surface", 16)
        s.photo(x + 10, y + 10, 136, 104, "1x1", 10, NAME_TO_DISH.get(name))
        for j, line in enumerate(lines):
            s.t(x + 12, y + 140 + j * 24, line, 17, "text", 600)
        s.t(x + 12, y + 140 + len(lines) * 24, meta, 13, "text2")
        s.close()
    s.footer(694, ["Kayıtlı tarifler internet olmadan da açılır."])
    s.tabbar(1)


def saved_empty(s):
    s.navbar("Tarifler", back=False)
    s.unavailable(320, "book", "Kayıtlı Tarif Yok", ["Beğendiğin tarifi kaydet,", "internet olmadan da aç."], "defter")
    s.tabbar(1)


def shopping(s):
    s.navbar("Alışveriş Listesi", "Ev listesi · 2 üye", back=False,
             trailing=[("square.and.arrow.up", "btn-paylas")])
    items = [("Tereyağı", "Sen ekledin", False), ("Salatalık", "Ayşe ekledi", False),
             ("Ekmek", "Ayşe ekledi", False), ("Süt", "Alındı · dolaba eklendi", True)]
    tops = s.group(196, [60] * 4 + [44], 64)
    for i, (y, (name, who, done)) in enumerate(zip(tops, items)):
        s.open(f"satir-{i + 1}")
        s.r(GX, y, GW, 60, None)
        if done:
            s.circle(43, y + 30, 11, "accent")
            s.parts.append(f'<path d="M38 {y + 30} L42 {y + 34} L48 {y + 26}" fill="none" stroke="{s.c["on_accent"]}" '
                           f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
        else:
            s.circle(43, y + 30, 11, None, "control", 1.5)
        s.t(64, y + 27, name, 17, "text2" if done else "text")
        s.t(64, y + 46, who, 13, "text2")
        thumb(s, 290, y + 30, 40, name)
        s.close()
    s.open("satir-urun-ekle")
    s.r(GX, tops[-1], GW, 44, None)
    s.icon("plus", 43, tops[-1] + 22, "accent")
    s.t(64, tops[-1] + 28, "Ürün Ekle", 17, "accent")
    s.close()
    s.footer(504, ["Alındı işaretlenen ürünler dolaba eklenir."])
    s.header(552, "Ev", doodle="cay", angle=0)
    t2 = s.group(564, [44, 44], 32)
    s.t(32, t2[0] + 28, "Davet kodu", 17)
    s.t(328, t2[0] + 28, "7KQ2MX", 17, "text2", 400, "end")
    s.open("btn-koda-katil")
    s.r(GX, t2[1], GW, 44, None)
    s.t(32, t2[1] + 28, "Başka Bir Eve Katıl", 17, "accent")
    s.close()
    s.tabbar(2)


def shopping_empty(s):
    s.navbar("Alışveriş Listesi", "Ev listesi · 2 üye", back=False,
             trailing=[("square.and.arrow.up", "btn-paylas")])
    end = s.unavailable(320, "cart", "Liste Boş", ["Tariflerdeki eksikler ve biten", "ürünler buraya eklenir."], "sepet")
    s.plain(end + 22, "Ürün Ekle", "btn-urun-ekle", weight=600)
    s.tabbar(2)


def offline(s):
    s.navbar("Dolap", "Ev · 2 üye", back=False,
             trailing=[("camera", "btn-tara"), ("rectangle.portrait.and.arrow.right", "btn-cikis")])
    (y,) = s.group(196, [88])
    s.icon("wifi.slash", 46, y + 34, "text2", 1, 1.6)
    s.t(72, y + 30, "Çevrimdışısın", 17, "text", 600)
    s.t(72, y + 51, "Dolabın son hâli gösteriliyor.", 13, "text2")
    s.t(72, y + 69, "Tarif önerisi için internet gerekir.", 13, "text2")
    s.plain(292, "Tekrar Dene", "btn-tekrar-dene", weight=600)
    start = pantry_sections(s, 372, [("Yoğurt", "Yarın", "satir-yogurt"), ("Domates", "2 gün", "satir-domates")], None)
    tops = s.group(start, [ROW] * 3, 76)
    for y, (name, state) in zip(tops, [("Yumurta", "Var"), ("Peynir", "Azaldı"), ("Patates", "Var")]):
        value_row(s, y, name, state, f"satir-{name.lower()}")
    s.tabbar(0)


SCREENS = [("01-giris", login), ("02-dolap", pantry), ("02b-bozulma-bildirimi", lambda s: pantry(s, True)),
           ("02c-malzeme-duzenle", edit_item), ("03-tarama", scan),
           ("03b-tarama-analiz-1", analyzing(112)), ("03c-tarama-analiz-2", analyzing(586)),
           ("04-yeni-malzemeler", new_items), ("04b-malzeme-yok", no_ingredients),
           ("05-tercihler", prefs), ("06-tarif-onerileri", recipes),
           ("06b-tarifler-yukleniyor", recipes_loading), ("06c-tarif-hatasi", recipes_error),
           ("07-tarif-detay", recipe), ("07b-pisirdim", cooked), ("08-tarifler", saved),
           ("08b-tarifler-bos", saved_empty), ("09-alisveris-listesi", shopping),
           ("09b-liste-bos", shopping_empty), ("10-cevrimdisi", offline)]
THEMES = [("wireframes", WIRE, True), ("mockups", LIGHT, False), ("mockups-dark", DARK, False)]


# checks ---------------------------------------------------------------------------------------
def background_at(screen, x, y):
    for rx, ry, rw, rh, fill in reversed(screen.rects):
        if fill and rx <= x <= rx + rw and ry <= y <= ry + rh:
            return fill
    return screen.c["bg"]


def hidden(screen, text):
    """True when a shape drawn later (e.g. a notification banner) covers the text."""
    x, y, w, h, *_, order = text
    cx, cy = x + w / 2, y + h / 2
    return any(r[4] and r[0] <= cx <= r[0] + r[2] and r[1] <= cy <= r[1] + r[3] for r in screen.rects[order:])


def check(name, screen):
    problems = []
    visible = [t for t in screen.texts if not hidden(screen, t)]
    for x, y, w, h, s, size, color, _ in visible:
        if x < M - 0.01 or x + w > W - M + 0.01:
            problems.append(f"{name}: outside margin: {s!r}")
        hits = [r for r in screen.rects if r[4] and r[2] < W and r[0] <= x + w / 2 <= r[0] + r[2]
                and r[1] <= y + h / 2 <= r[1] + r[3]]
        if hits:
            bx, by, bw, bh, _ = hits[-1]
            if x < bx or x + w > bx + bw or y < by or y + h > by + bh:
                problems.append(f"{name}: overflows its box: {s!r}")
        ratio = contrast(color, background_at(screen, x + w / 2, y + h / 2))
        if ratio < 4.5:
            problems.append(f"{name}: contrast {ratio:.2f} on {s!r}")
    for i, a in enumerate(visible):
        for b in visible[i + 1:]:
            if a[0] < b[0] + b[2] and b[0] < a[0] + a[2] and a[1] < b[1] + b[3] and b[1] < a[1] + a[3]:
                problems.append(f"{name}: text overlap: {a[4]!r} / {b[4]!r}")
    for id, w, h in screen.targets:
        if id.startswith(("btn-", "satir-", "sekme-", "geri", "alan-")) and id != "sekme-cubugu" and (w < 44 or h < 44):
            problems.append(f"{name}: small target {id} {w:.0f}x{h:.0f}")
    return problems


def main():
    problems = []
    for folder, theme, wire in THEMES:
        out = ROOT / folder
        out.mkdir(parents=True, exist_ok=True)
        for old in out.glob("*.svg"):
            old.unlink()
        for name, draw in SCREENS:
            screen = Screen(theme, wire)
            draw(screen)
            (out / f"{name}.svg").write_text(screen.svg(), encoding="utf-8")
            problems += check(f"{folder}/{name}", screen)
    print("\n".join(problems) if problems else
          f"ok: {len(SCREENS)} screens x {len(THEMES)} themes, no layout, contrast or target problems")


if __name__ == "__main__":
    main()
