"""Generates Figma-importable SVG screens into design/ (wireframes, mockups, mockups-dark).

Visual language: iOS 26 (inset grouped lists, large-title navigation, floating tab bar, sheets).
Text is start-anchored using real Inter metrics, so it lands in the same place in Figma.
Each run checks every text for overflow, overlap and WCAG contrast, and every tappable layer
(btn-, satir-, sekme-, geri) for a 44 x 44 pt minimum.
"""
from pathlib import Path
from xml.sax.saxutils import escape

from fontTools.ttLib import TTFont

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE / "design"
FONTS = BASE / "tools" / "fonts"
W, H = 360, 800
M = 16                 # side margin
GX, GW = 16, 328       # inset grouped list
RADIUS = 20
TAB_Y = 717            # floating tab bar: 21 pt from the bottom edge

LIGHT = {
    "bg": "#F2F2F7", "surface": "#FFFFFF", "text": "#000000", "text2": "#6C6C70",
    "sep": "#C6C6C8", "accent": "#B3401E", "on_accent": "#FFFFFF", "fill": "#E3E3E8",
    "thumb": "#FFFFFF", "glass": "#FFFFFF", "glass_line": "#E5E5EA", "tabsel": "#F2F2F7",
    "photo": "#E5E5EA", "dim": "#C7C7CC", "gray3": "#C7C7CC", "control": "#6C6C70",
    "red": "#E9152D", "on_red": "#FFFFFF", "switch_off": "#E9E9EA",
    "sheet": "#F2F2F7", "sheet_cell": "#FFFFFF",
    "cam": "#000000", "preview": "#1C1C1E", "cam_text": "#FFFFFF", "cam_glass": "#3A3A3C",
}
DARK = {
    "bg": "#000000", "surface": "#1C1C1E", "text": "#FFFFFF", "text2": "#AEAEB2",
    "sep": "#38383A", "accent": "#FF8A65", "on_accent": "#000000", "fill": "#2C2C2E",
    "thumb": "#636366", "glass": "#2C2C2E", "glass_line": "#3A3A3C", "tabsel": "#3A3A3C",
    "photo": "#2C2C2E", "dim": "#000000", "gray3": "#48484A", "control": "#AEAEB2",
    "red": "#E9152D", "on_red": "#FFFFFF", "switch_off": "#39393D",
    "sheet": "#1C1C1E", "sheet_cell": "#2C2C2E",
    "cam": "#000000", "preview": "#1C1C1E", "cam_text": "#FFFFFF", "cam_glass": "#3A3A3C",
}
WIRE = {
    "bg": "#F2F2F2", "surface": "#FFFFFF", "text": "#1A1A1A", "text2": "#5E5E5E",
    "sep": "#C8C8C8", "accent": "#3A3A3A", "on_accent": "#FFFFFF", "fill": "#E2E2E2",
    "thumb": "#FFFFFF", "glass": "#FFFFFF", "glass_line": "#D0D0D0", "tabsel": "#EDEDED",
    "photo": "#DADADA", "dim": "#C8C8C8", "gray3": "#B0B0B0", "control": "#5E5E5E",
    "red": "#3A3A3A", "on_red": "#FFFFFF", "switch_off": "#DADADA",
    "sheet": "#F2F2F2", "sheet_cell": "#FFFFFF",
    "cam": "#222222", "preview": "#444444", "cam_text": "#FFFFFF", "cam_glass": "#555555",
}
MOCK = LIGHT  # kept for older imports

WEIGHTS = {400: "Regular", 500: "Medium", 600: "SemiBold", 700: "Bold"}
METRICS = {}
for weight, name in WEIGHTS.items():
    font = TTFont(FONTS / f"Inter-{name}.ttf", lazy=True)
    METRICS[weight] = (font.getBestCmap(), font["hmtx"].metrics, font["head"].unitsPerEm)


def text_width(s, size, weight):
    cmap, hmtx, upem = METRICS[weight]
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
    "photo.on.rectangle": [("s", "M-7 -9 H10 V4 M-10 -6 H7 V8 H-10 Z M-10 6 L-4 0 L1 5 L3 3 L7 7")],
}


class Screen:
    def __init__(self, theme, wire=False):
        self.c = theme
        self.wire = wire
        self.parts, self.rects, self.texts, self.targets, self.stack = [], [], [], [], []
        self.r(0, 0, W, H, "bg")

    # primitives ---------------------------------------------------------------------------
    def r(self, x, y, w, h, fill="surface", rx=0, stroke=None, id=None):
        i = f' id="{id}"' if id else ""
        if fill is None:   # invisible hotspot, used as a prototype target in Figma
            self.parts.append(f'<rect{i} x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="#000000" fill-opacity="0"/>')
        else:
            s = f' stroke="{self.c[stroke]}" stroke-width="0.5"' if stroke else ""
            self.parts.append(f'<rect{i} x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{self.c[fill]}"{s}/>')
        self.rects.append((x, y, w, h, self.c[fill] if fill else None))

    def circle(self, cx, cy, r, fill=None, stroke=None, width=1.5):
        f = self.c[fill] if fill else "none"
        s = f' stroke="{self.c[stroke]}" stroke-width="{width}"' if stroke else ""
        self.parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{f}"{s}/>')

    def t(self, x, y, s, size=17, fill="text", weight=400, anchor="start", id=None):
        width = text_width(s, size, weight)
        left = {"start": x, "middle": x - width / 2, "end": x - width}[anchor]
        i = f' id="{id}"' if id else ""
        self.parts.append(f'<text{i} x="{left:.1f}" y="{y}" font-family="Inter" font-size="{size}" '
                          f'font-weight="{weight}" fill="{self.c[fill]}">{escape(s)}</text>')
        self.texts.append((left, y - size * 0.76, width, size * 0.98, s, size, self.c[fill]))

    def icon(self, name, cx, cy, color="text", scale=1.0, width=1.7):
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
        self.t(58, 37, "9:41", 16, color, 600, "middle")
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
        w = text_width(label, 17, 600) + 32
        self.open(id)
        self.r(round(right - w, 1), y, round(w, 1), 44, "accent", 22)
        self.t(right - w / 2, y + 28, label, 17, "on_accent", 600, "middle")
        self.close()

    def navbar(self, title, sub=None, back=True, trailing=(), title_id=None):
        self.status()
        if back:
            self.glass_button(M, 58, "chevron.backward", "geri")
        x = W - M
        for icon, id in trailing:
            x -= 44
            self.glass_button(x, 58, icon, id)
            x -= 8
        self.t(M, 142, title, 34, "text", 700, id=title_id)
        if sub:
            self.t(M, 170, sub, 17, "text2")

    def tabbar(self, active):
        self.open("sekme-cubugu")
        self.r(21, TAB_Y, 318, 62, "glass", 31, "glass_line")
        self.close()
        tabs = [("Ana Sayfa", "ana-sayfa", "house.fill"), ("Kayıtlı", "kayitli", "bookmark.fill"),
                ("Liste", "liste", "list.bullet")]
        for i, (label, key, icon) in enumerate(tabs):
            cx = 74 + i * 106
            on = i == active
            self.open(f"sekme-{key}")
            self.r(cx - 49, TAB_Y + 4, 98, 54, "tabsel" if on else None, 27)
            self.icon(icon, cx, TAB_Y + 22, "accent" if on else "text")
            self.t(cx, TAB_Y + 49, label, 10, "accent" if on else "text", 600 if on else 500, "middle")
            self.close()
        self.home_indicator()

    # content ------------------------------------------------------------------------------
    def header(self, y, text):
        self.t(20, y, text, 17, "text", 600)

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
        w = text_width(label, 17, weight) + 32
        self.open(id)
        self.r(round(cx - w / 2, 1), y, round(w, 1), 44, None, 22)
        self.t(cx, y + 28, label, 17, "accent", weight, "middle")
        self.close()

    def photo(self, x, y, w, h, ratio, rx=0):
        self.r(x, y, w, h, "photo", rx, id=f"foto-alani-{ratio}")
        if self.wire and w > 100:
            self.t(x + w / 2, y + h - 20, f"Fotoğraf alanı ({ratio.replace('x', ':')})", 13, "text2", 400, "middle")

    def recipe_row(self, top, name, meta, id, h=64, title_id=None):
        self.open(id)
        self.r(GX, top, GW, h, None)
        self.photo(32, top + 8, 48, 48, "1x1", 8)
        self.t(92, top + 28, name, 17, "text", 400, id=title_id)
        self.t(92, top + 48, meta, 13, "text2")
        self.icon("chevron.forward", 322, top + h / 2, "gray3", 1, 2)
        self.close()

    def unavailable(self, cy, icon, title, lines):
        self.icon(icon, W / 2, cy, "text2", 2.0, 1.4)
        self.t(W / 2, cy + 52, title, 22, "text", 700, "middle")
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
    s.home_indicator()


def saved_rows(s, top, rows):
    tops = s.group(top, [64] * len(rows), 92)
    for y, (name, meta, id) in zip(tops, rows):
        s.recipe_row(y, name, meta, id)
    return top + 64 * len(rows)


def home(s):
    s.navbar("Ana Sayfa", back=False, trailing=[("rectangle.portrait.and.arrow.right", "btn-cikis")])
    s.prominent(166, "Fotoğraf Çek", "btn-fotograf-cek")
    s.plain(222, "Malzemeleri Yaz", "btn-malzeme-yaz")
    s.header(306, "Son Kaydedilenler")
    saved_rows(s, 318, [("Patatesli Omlet", "20 dk · 2 kişilik", "satir-omlet"),
                        ("Mercimek Çorbası", "30 dk · 4 kişilik", "satir-mercimek")])
    s.tabbar(0)


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


def ingredients(s):
    s.navbar("Malzemeler", "Yanlış olanı sola kaydırıp sil.")
    s.header(208, "8 malzeme bulundu")
    names = ["Yumurta", "Domates", "Biber", "Soğan", "Peynir", "Patates", "Maydanoz"]
    heights = [60] + [44] * len(names) + [44]
    tops = s.group(220, heights, 32)
    s.open("satir-yogurt")
    s.t(32, tops[0] + 26, "Yoğurt", 17)
    s.t(32, tops[0] + 46, "Emin değiliz, kontrol et", 13, "text2")
    s.icon("questionmark.circle", 320, tops[0] + 30, "text2")
    s.close()
    for i, name in enumerate(names):
        y = tops[i + 1]
        s.open(f"satir-{i + 2}")
        s.t(32, y + 28, name, 17)
        if name == "Domates":   # one row shown mid-swipe to document the delete action
            s.r(270, y, 74, 44, "red")
            s.t(307, y + 28, "Sil", 17, "on_red", 400, "middle")
        s.close()
    s.open("satir-malzeme-ekle")
    s.r(GX, tops[-1], GW, 44, None)
    s.icon("plus", 42, tops[-1] + 22, "accent")
    s.t(60, tops[-1] + 28, "Malzeme Ekle", 17, "accent")
    s.close()
    s.prominent(666, "Devam Et", "btn-devam")
    s.home_indicator()


def no_ingredients(s):
    s.navbar("Malzemeler")
    s.unavailable(250, "magnifyingglass", "Malzeme Bulunamadı",
                  ["Fotoğraf net değilse yeniden çek", "ya da malzemeleri kendin ekle."])
    s.prominent(380, "Malzeme Ekle", "btn-malzeme-ekle")
    s.plain(440, "Yeniden Çek", "btn-yeniden-cek")
    s.home_indicator()


def prefs(s):
    s.r(0, 0, W, H, "dim")
    s.status()
    s.r(12, 46, 336, 40, "surface", 12)
    s.r(0, 58, W, 760, "sheet", 38)
    s.r(162, 64, 36, 5, "gray3", 2.5, id="tutamac")
    s.glass_button(M, 78, "xmark", "btn-kapat", "sheet_cell")
    s.t(W / 2, 106, "Tercihler", 17, "text", 600, "middle")
    s.prominent_pill(W - M, 78, "Tarif Öner", "btn-tarif-oner")
    s.header(158, "Süre")
    s.segmented(170, ["15 dk", "30 dk", "1 saat"], 1, "secim-sure")
    s.header(236, "Kişi sayısı")
    s.segmented(248, ["1", "2", "4", "6"], 1, "secim-kisi")
    s.header(314, "Alerjiler")
    tops = s.group(326, [44] * 4, 32, "sheet_cell")
    allergens = [("Gluten", "gluten", False), ("Süt", "sut", True), ("Yumurta", "yumurta", False),
                 ("Fındık", "findik", False)]
    for y, (name, key, on) in zip(tops, allergens):
        s.open(f"satir-{key}")
        s.r(GX, y, GW, 44, None)
        s.t(32, y + 28, name, 17)
        s.switch(277, y + 6.5, on)
        s.close()
    s.footer(524, ["Tarifler yapay zeka ile üretilir.", "Alerjenleri yine de kontrol et."])
    s.home_indicator()


def recipes(s):
    s.navbar("Öneriler", "8 malzemene göre")
    rows = [("Menemen", "15 dk · 2 kişilik · %100 uyum", "Eksik yok", "satir-menemen", None),
            ("Patatesli Omlet", "20 dk · 2 kişilik · %80 uyum", "Eksik: Tereyağı", "satir-omlet", "tarif-baslik"),
            ("Patates Mücveri", "30 dk · 2 kişilik · %60 uyum", "Eksik: Un, Kabartma tozu", "satir-mucver", None)]
    tops = s.group(196, [76] * 3, 100)
    for y, (name, meta, missing, id, tid) in zip(tops, rows):
        s.open(id)
        s.r(GX, y, GW, 76, None)
        s.photo(32, y + 10, 56, 56, "1x1", 10)
        s.t(100, y + 26, name, 17, "text", 600, id=tid)
        s.t(100, y + 46, meta, 13, "text2")
        s.t(100, y + 64, missing, 13, "text2")
        s.icon("chevron.forward", 322, y + 38, "gray3", 1, 2)
        s.close()
    s.plain(440, "Başka Tarifler Öner", "btn-baska-tarif")
    s.home_indicator()


def recipes_loading(s):
    s.navbar("Öneriler", "8 malzemene göre")
    s.spinner(W / 2, 330)
    s.t(W / 2, 372, "Tarifler hazırlanıyor…", 17, "text2", 400, "middle")
    s.home_indicator()


def recipes_error(s):
    s.navbar("Öneriler", "8 malzemene göre")
    end = s.unavailable(270, "exclamationmark.triangle", "Tarifler Alınamadı",
                        ["Bağlantını kontrol edip", "tekrar dene."])
    s.plain(end + 22, "Tekrar Dene", "btn-tekrar-dene", weight=600)
    s.home_indicator()


def recipe(s):
    s.photo(0, 0, W, 202, "16x9")
    s.status()
    s.glass_button(M, 58, "chevron.backward", "geri")
    s.glass_button(W - M - 44, 58, "bookmark", "btn-kaydet")
    s.t(M, 250, "Patatesli Omlet", 34, "text", 700, id="tarif-baslik")
    s.t(M, 276, "20 dk · 2 kişilik · %80 uyum", 17, "text2")
    s.header(314, "Eksik")
    (y,) = s.group(326, [44])
    s.t(32, y + 28, "Tereyağı", 17)
    s.open("btn-listeye-ekle")
    s.r(220, y, 124, 44, None)
    s.t(328, y + 28, "Listeye Ekle", 17, "accent", 400, "end")
    s.close()
    s.header(406, "Malzemeler")
    (y,) = s.group(418, [44])
    s.t(32, y + 28, "Patates, yumurta, soğan, peynir", 17)
    s.header(498, "Yapılışı")
    steps = ["Patatesleri küp küp doğra.", "Tavada kızarana dek kavur.", "Soğanı ekleyip karıştır.",
             "Yumurtaları çırpıp dök.", "Peyniri ekle, 5 dk pişir."]
    tops = s.group(510, [44] * 5, 56)
    for i, (y, step) in enumerate(zip(tops, steps)):
        s.t(32, y + 28, str(i + 1), 17, "text2")
        s.t(56, y + 28, step, 17)
    s.home_indicator()


def saved(s):
    s.navbar("Kayıtlı Tarifler", back=False)
    s.open("alan-tarif-ara")
    s.r(GX, 156, GW, 44, None)
    s.r(GX, 158, GW, 40, "surface", 20)
    s.icon("magnifyingglass", 38, 178, "text2", 0.8)
    s.t(54, 184, "Ara", 17, "text2")
    s.close()
    end = saved_rows(s, 214, [("Menemen", "15 dk · 2 kişilik", "satir-menemen"),
                              ("Mercimek Çorbası", "30 dk · 4 kişilik", "satir-mercimek"),
                              ("Patatesli Omlet", "20 dk · 2 kişilik", "satir-omlet"),
                              ("Zeytinyağlı Fasulye", "40 dk · 4 kişilik", "satir-fasulye")])
    s.footer(end + 24, ["Kayıtlı tarifler internet olmadan da açılır."])
    s.tabbar(1)


def saved_empty(s):
    s.navbar("Kayıtlı Tarifler", back=False)
    s.unavailable(300, "bookmark", "Kayıtlı Tarif Yok", ["Beğendiğin tarifi kaydet,", "internet olmadan da aç."])
    s.tabbar(1)


def shopping(s):
    s.navbar("Alışveriş Listesi", "Ev listesi · 2 üye", back=False,
             trailing=[("square.and.arrow.up", "btn-paylas")])
    items = [("Tereyağı", "Sen ekledin", False), ("Un", "Ayşe ekledi", False),
             ("Kabartma tozu", "Ayşe ekledi", False), ("Süt", "Sen ekledin", True)]
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
        s.close()
    s.open("satir-urun-ekle")
    s.r(GX, tops[-1], GW, 44, None)
    s.icon("plus", 43, tops[-1] + 22, "accent")
    s.t(64, tops[-1] + 28, "Ürün Ekle", 17, "accent")
    s.close()
    s.header(528, "Ev")
    t2 = s.group(540, [44, 44], 32)
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
    end = s.unavailable(300, "cart", "Liste Boş", ["Tariflerdeki eksikleri", "buraya ekleyebilirsin."])
    s.plain(end + 22, "Ürün Ekle", "btn-urun-ekle", weight=600)
    s.tabbar(2)


def offline(s):
    s.navbar("Ana Sayfa", back=False, trailing=[("rectangle.portrait.and.arrow.right", "btn-cikis")])
    s.icon("wifi.slash", W / 2, 210, "text2", 1.6, 1.5)
    s.t(W / 2, 262, "İnternet Bağlantısı Yok", 22, "text", 700, "middle")
    s.t(W / 2, 290, "Fotoğraftan tarif için internet gerekir.", 15, "text2", 400, "middle")
    s.t(W / 2, 310, "Kayıtlı tariflerin yine açılır.", 15, "text2", 400, "middle")
    s.plain(324, "Tekrar Dene", "btn-tekrar-dene", weight=600)
    s.header(410, "Kayıtlı Tarifler")
    saved_rows(s, 422, [("Patatesli Omlet", "20 dk · 2 kişilik", "satir-omlet"),
                        ("Mercimek Çorbası", "30 dk · 4 kişilik", "satir-mercimek")])
    s.tabbar(0)


SCREENS = [("01-giris", login), ("02-ana-sayfa", home), ("03-tarama", scan),
           ("03b-tarama-analiz-1", analyzing(112)), ("03c-tarama-analiz-2", analyzing(586)),
           ("04-malzemeler", ingredients), ("04b-malzeme-yok", no_ingredients),
           ("05-tercihler", prefs), ("06-tarif-onerileri", recipes),
           ("06b-tarifler-yukleniyor", recipes_loading), ("06c-tarif-hatasi", recipes_error),
           ("07-tarif-detay", recipe), ("08-kayitli", saved), ("08b-kayitli-bos", saved_empty),
           ("09-alisveris-listesi", shopping), ("09b-liste-bos", shopping_empty),
           ("10-cevrimdisi", offline)]
THEMES = [("wireframes", WIRE, True), ("mockups", LIGHT, False), ("mockups-dark", DARK, False)]


# checks ---------------------------------------------------------------------------------------
def background_at(screen, x, y):
    for rx, ry, rw, rh, fill in reversed(screen.rects):
        if fill and rx <= x <= rx + rw and ry <= y <= ry + rh:
            return fill
    return screen.c["bg"]


def check(name, screen):
    problems = []
    for x, y, w, h, s, size, color in screen.texts:
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
    for i, a in enumerate(screen.texts):
        for b in screen.texts[i + 1:]:
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
