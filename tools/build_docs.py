"""Builds the milestone PDFs into docs/. Edit TEAM and the [TO FILL] text, then run again."""
import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import (Flowable, KeepTogether, Paragraph, Preformatted, SimpleDocTemplate,
                                Spacer, Table, TableStyle)

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_screens import DARK, LIGHT, contrast  # noqa: E402

# Palette for the PDF pages themselves (headings, tables, the flow chart). The app's own colors
# are LIGHT and DARK from build_screens.
MOCK = {"bg": "#FBF7F2", "line": "#E3D9CE", "text": "#2A211C", "muted": "#6B5E55",
        "primary": "#B3401E", "soft": "#F8E3DA", "ok": "#4F6B2C", "ok_soft": "#E5EDD6",
        "warn": "#7A4F00", "warn_soft": "#FBEBC8"}

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "docs"
OUT.mkdir(exist_ok=True)
FONTS = BASE / "tools" / "fonts"

MEMBER_1 = "[AD SOYAD 1]"
MEMBER_2 = "[AD SOYAD 2]"
TEAM = f"{MEMBER_1}, {MEMBER_2}"
TEAM_NO = "[TAKIM NO]"
EVIDENCE = ("<b>[TO FILL: interview 5-10 people who cook at home. Write how many people you spoke to, how many "
            "struggle to decide what to cook, how often this happens each week, and one short quote. "
            "Do not submit this placeholder.]</b>")

pdfmetrics.registerFont(TTFont("Body", str(FONTS / "Inter-Regular.ttf")))
pdfmetrics.registerFont(TTFont("Bold", str(FONTS / "Inter-Bold.ttf")))
pdfmetrics.registerFont(TTFont("Mono", "/System/Library/Fonts/Menlo.ttc", subfontIndex=0))
pdfmetrics.registerFontFamily("Body", normal="Body", bold="Bold", italic="Body", boldItalic="Bold")

TEXT_WIDTH = A4[0] - 36 * mm - 12  # page minus margins and the frame's 6 pt side padding
INK = colors.HexColor(MOCK["text"])
MUTED = colors.HexColor(MOCK["muted"])
PRIMARY = colors.HexColor(MOCK["primary"])
LINE = colors.HexColor(MOCK["line"])
HEAD = colors.HexColor(MOCK["soft"])
WARN = colors.HexColor(MOCK["warn"])
WARN_SOFT = colors.HexColor(MOCK["warn_soft"])

H1 = ParagraphStyle("H1", fontName="Bold", fontSize=18, leading=22, textColor=PRIMARY, spaceAfter=2)
SUB = ParagraphStyle("SUB", fontName="Body", fontSize=8.5, leading=12, textColor=MUTED, spaceAfter=7)
H2 = ParagraphStyle("H2", fontName="Bold", fontSize=11, leading=14, textColor=INK, spaceBefore=8,
                    spaceAfter=3, keepWithNext=1)
BODY = ParagraphStyle("BODY", fontName="Body", fontSize=8.8, leading=12.4, textColor=INK, spaceAfter=4)
BULLET = ParagraphStyle("BULLET", parent=BODY, leftIndent=10, bulletIndent=0, spaceAfter=2.5)
CELL = ParagraphStyle("CELL", fontName="Body", fontSize=7.9, leading=10.6, textColor=INK)
SMALL = ParagraphStyle("SMALL", fontName="Body", fontSize=7.4, leading=10, textColor=INK, spaceAfter=2)
CODE = ParagraphStyle("CODE", fontName="Mono", fontSize=7.2, leading=9.6, textColor=INK,
                      backColor=colors.HexColor(MOCK["bg"]), borderPadding=5, spaceBefore=6, spaceAfter=11)


def P(text):
    return Paragraph(text, BODY)


def bullets(items):
    return [Paragraph(i, BULLET, bulletText="•") for i in items]


def table(rows, widths):
    data = [[Paragraph(f"<b>{c}</b>" if i == 0 else str(c), CELL) if isinstance(c, str) else c
             for c in row] for i, row in enumerate(rows)]
    scale = TEXT_WIDTH / (sum(widths) * mm)
    t = Table(data, colWidths=[w * mm * scale for w in widths], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HEAD), ("GRID", (0, 0), (-1, -1), 0.4, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 2.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
    ]))
    return t


def header(title):
    return [Paragraph(title, H1),
            Paragraph(f"Dolaptan · MTM4681 Mobile Programming · Milestone · Team {TEAM_NO} · {TEAM}", SUB)]


def footer(c, doc):
    c.setFont("Body", 7.5)
    c.setFillColor(MUTED)
    c.drawRightString(A4[0] - 18 * mm, 8 * mm, f"Page {doc.page}")


def build(name, story):
    SimpleDocTemplate(str(OUT / name), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm,
                      topMargin=14 * mm, bottomMargin=13 * mm, title=f"Dolaptan: {name[:-4]}",
                      author=TEAM).build(story, onFirstPage=footer, onLaterPages=footer)


class Swatch(Flowable):
    def __init__(self, color):
        super().__init__()
        self.color, self.width, self.height = color, 22, 11

    def draw(self):
        self.canv.setFillColor(colors.HexColor(self.color))
        self.canv.setStrokeColor(LINE)
        self.canv.roundRect(0, 0, 22, 11, 2, fill=1)


def design_justification():
    tokens = [
        ("Grouped background", "bg", "Screen background behind lists"),
        ("Cell", "surface", "List rows and fields"),
        ("Label", "text", "Titles and body text"),
        ("Secondary label", "text2", "Times, servings, hints"),
        ("Separator", "sep", "Hairlines between rows"),
        ("Accent (terracotta)", "accent", "Only on things you can tap"),
        ("Destructive", "red", "Swipe-to-delete only"),
    ]
    rows = [["", "Token", "Light", "Dark", "Use"]] + [
        [Swatch(LIGHT[k]), name, LIGHT[k], DARK[k], use] for name, k, use in tokens]
    pairs = [("text", "bg", "Label on background"), ("text2", "bg", "Secondary label on background"),
             ("text2", "surface", "Secondary label on a row"), ("accent", "surface", "Tappable text on a row"),
             ("accent", "bg", "Tappable text on background"), ("on_accent", "accent", "Label on the filled button"),
             ("accent", "tabsel", "Selected tab label"), ("on_red", "red", "Delete label on red")]
    check = [["Text / background", "Light", "Dark", "AA (4.5:1)"]]
    for fg, bg, use in pairs:
        lo, da = contrast(LIGHT[fg], LIGHT[bg]), contrast(DARK[fg], DARK[bg])
        check.append([use, f"{lo:.2f}:1", f"{da:.2f}:1", "Pass" if min(lo, da) >= 4.5 else "Fail"])
    type_rows = [["iOS text style", "Size / weight", "Use in Dolaptan"],
                 ["Large Title", "34 pt bold", "Screen titles"],
                 ["Title 2", "22 pt bold", "Empty, error and offline states"],
                 ["Headline", "17 pt semibold", "Section headers, recipe names"],
                 ["Body", "17 pt regular", "Rows, steps, buttons"],
                 ["Footnote", "13 pt regular", "Times, servings, list footers"]]
    build("design-justification.pdf", header("Design Justification") + [
        P("<b>Dolaptan</b> turns a photo of a fridge or cupboard into three Turkish recipes. People use it while "
          "tired, in a hurry, or with one free hand in the kitchen. The design aims for few decisions, readable "
          "text, and clear control over what the AI suggests. It follows Apple's Human Interface Guidelines for "
          "iOS 26, so the app feels familiar to people who use Notes, Reminders or Health."),
        Paragraph("Visual language", H2),
        *bullets([
            "<b>Standard iOS patterns:</b> large-title navigation bars, a floating tab bar with three tabs "
            "(Ana Sayfa, Kayıtlı, Liste), inset grouped lists, a sheet for Preferences, segmented controls for time "
            "and servings, switches for allergies, and swipe to delete.",
            "<b>Rows instead of cards:</b> ingredients, recipes and list items are list rows, which are easier to "
            "scan and edit than stacked cards.",
            "<b>One emphasis per screen:</b> at most one filled button per screen (for example, Fotoğraf Çek or "
            "Devam Et). Other actions are plain text buttons.",
            "<b>Liquid Glass only for navigation:</b> following the HIG, the glass treatment is limited to the tab "
            "bar and the bar buttons. Content stays on solid system backgrounds. There are no gradients, large "
            "shadows or decorative shapes.",
        ]),
        Paragraph("Color", H2),
        P("Backgrounds are Apple's system colors. A single accent color, our terracotta, appears only on elements "
          "you can tap, so color always means an action. For secondary text we use Apple's increased-contrast "
          f"gray {LIGHT['text2']}, because the default gray #8E8E93 reaches only "
          f"{contrast('#8E8E93', '#FFFFFF'):.2f}:1 on white. In Dark Mode the accent becomes lighter "
          f"({DARK['accent']}) with a black label, because white on that color would fail AA."),
        table(rows, [10, 36, 20, 20, 88]),
        Spacer(1, 5),
        P("Contrast uses the WCAG 2.2 formula: L = 0.2126 R + 0.7152 G + 0.0722 B on linearized channels, "
          "ratio = (L1 + 0.05) / (L2 + 0.05). Every pair passes AA in both modes. The build script also checks "
          "every text in every screen."),
        table(check, [80, 32, 32, 30]),
        Paragraph("Typography", H2),
        P("The scale follows iOS Dynamic Type at the default size. On iOS the app uses the system font, SF Pro. "
          "Mockups and the Android build use <b>Inter</b>. It is free, supports Turkish letters such as ğ, ı, İ "
          "and ş, and looks close to SF Pro. Apple's SF Pro license allows it only for Apple platforms."),
        table(type_rows, [44, 40, 90]),
        Paragraph("Layout", H2),
        *bullets([
            "We keep the course frame of 360 x 800 pt, 16 pt side margins and an 8 pt rhythm.",
            "Every tappable element is at least 44 x 44 pt. The build script measures this on every screen.",
            "Content stays clear of the status bar and the home indicator. The tab bar floats 21 pt from the "
            "edges.",
            "Food photos get fixed spaces: 16:9 at the top of a recipe and 1:1 in list rows. Recipes are generated "
            "as text, so the space stays empty and is hidden until a real photo exists. We do not use stock or "
            "AI-generated images.",
            "Icons follow SF Symbols. Each symbol name is listed in the Figma guide. In code we use the "
            "MIT-licensed cupertino_icons font, which also works on Android.",
        ]),
        Paragraph("States and Dark Mode", H2),
        P("Empty, error and loading states use the standard iOS empty-state pattern: one symbol, a short title, "
          "one sentence and at most one action. Examples are an empty saved list, recipes that failed to load, "
          "and a loading spinner while recipes are prepared. Every screen exists in light and dark versions with "
          "its own color tokens, and both versions pass the same checks."),
        Paragraph("Accessibility and how the design supports users", H2),
        *bullets([
            "Color is never the only signal: checked items use a filled circle with a check mark, uncertain "
            "ingredients have a symbol and a sentence, and switches change position as well as color.",
            "The app will support Dynamic Type, and it will label icon buttons and the delete action for VoiceOver and TalkBack.",
            "AI can make mistakes, so detected ingredients appear in an editable list before any recipe is "
            "generated, and uncertain items are listed first. The allergen note stays under the allergy switches.",
            "Saved recipes open offline, and the Offline screen explains what still works.",
        ]),
    ])


# 2. User flow -------------------------------------------------------------------------------
def user_flow():
    width, height = landscape(A4)
    c = canvas.Canvas(str(OUT / "user-flow.pdf"), pagesize=(width, height))
    c.setTitle("Dolaptan: user-flow")
    c.setAuthor(TEAM)
    c.setFillColor(PRIMARY)
    c.setFont("Bold", 17)
    c.drawString(30, height - 34, "User Flow")
    c.setFillColor(MUTED)
    c.setFont("Body", 8.5)
    c.drawString(30, height - 49, f"Dolaptan · MTM4681 Mobile Programming · Milestone · Team {TEAM_NO} · {TEAM}")

    bw, bh, dw, dh = 114, 46, 114, 70
    xs = [30 + 57 + i * 133.5 for i in range(6)]  # column centres
    ya, ya2, yb, yb2, yc, yc2 = 456, 382, 306, 232, 148, 76
    c.setFillColor(INK)
    c.setFont("Bold", 8.5)
    c.drawString(30, height - 66, "Main path:")
    c.setFont("Body", 8.5)
    c.drawString(30 + pdfmetrics.stringWidth("Main path: ", "Bold", 8.5), height - 66,
                 "Home → Scan → Ingredients → Preferences → Recipe suggestions → Recipe detail → Saved recipes. "
                 "Diamonds mark decision points.")
    nodes = {}
    labels = []
    segments = []

    def wrap(text, limit, font, size):
        lines, cur = [], ""
        for word in text.split():
            trial = f"{cur} {word}".strip()
            if pdfmetrics.stringWidth(trial, font, size) > limit:
                lines.append(cur)
                cur = word
            else:
                cur = trial
        return lines + [cur]

    def label(cx, cy, title, detail=None, limit=102):
        lines = [("Bold", t) for t in wrap(title, limit, "Bold", 8)]
        if detail:
            lines += [("Body", t) for t in wrap(detail, limit, "Body", 7.2)]
        y = cy + (len(lines) - 1) * 4.8 - 2.8
        c.setFillColor(INK)
        for font, line in lines:
            c.setFont(font, 8 if font == "Bold" else 7.2)
            c.drawCentredString(cx, y, line)
            y -= 9.6

    def box(key, x, y, title, detail=None, fill="#FFFFFF", stroke=MOCK["primary"]):
        nodes[key] = (x, y, bw / 2, bh / 2)
        c.setFillColor(colors.HexColor(fill))
        c.setStrokeColor(colors.HexColor(stroke))
        c.setLineWidth(1)
        c.roundRect(x - bw / 2, y - bh / 2, bw, bh, 7, fill=1)
        label(x, y, title, detail)

    def diamond(key, x, y, title):
        nodes[key] = (x, y, dw / 2, dh / 2)
        p = c.beginPath()
        p.moveTo(x, y + dh / 2)
        p.lineTo(x + dw / 2, y)
        p.lineTo(x, y - dh / 2)
        p.lineTo(x - dw / 2, y)
        p.close()
        c.setFillColor(WARN_SOFT)
        c.setStrokeColor(WARN)
        c.setLineWidth(1)
        c.drawPath(p, fill=1)
        label(x, y, title, limit=66)

    def edge(points, text=None, at=None):
        c.setStrokeColor(INK)
        c.setLineWidth(0.9)
        for a, b in zip(points, points[1:]):
            c.line(*a, *b)
            segments.append((a, b))
        (x1, y1), (x2, y2) = points[-2], points[-1]
        d = 5.5
        c.setFillColor(INK)
        p = c.beginPath()
        p.moveTo(x2, y2)
        if x1 == x2:
            s = 1 if y2 > y1 else -1
            p.lineTo(x2 - 3, y2 - s * d)
            p.lineTo(x2 + 3, y2 - s * d)
        else:
            s = 1 if x2 > x1 else -1
            p.lineTo(x2 - s * d, y2 - 3)
            p.lineTo(x2 - s * d, y2 + 3)
        p.close()
        c.drawPath(p, fill=1, stroke=0)
        if text:
            tw = pdfmetrics.stringWidth(text, "Bold", 7.4)
            c.setFillColor(colors.white)
            c.rect(at[0] - 1.5, at[1] - 2, tw + 3, 10, fill=1, stroke=0)
            c.setFillColor(WARN)
            c.setFont("Bold", 7.4)
            c.drawString(*at, text)
            labels.append((at[0], at[1] - 2, tw, 10))

    def side(key, where):
        x, y, rx, ry = nodes[key]
        return {"r": (x + rx, y), "l": (x - rx, y), "t": (x, y + ry), "b": (x, y - ry)}[where]

    screen, system, start = "#FFFFFF", MOCK["ok_soft"], MOCK["soft"]

    # Row A: entry, left to right.
    box("open", xs[0], ya, "Open app", fill=start)
    diamond("auth", xs[1], ya, "Signed in?")
    box("home", xs[2], ya, "Home")
    diamond("online", xs[3], ya, "Online?")
    diamond("input", xs[4], ya, "How to add ingredients?")
    box("scan", xs[5], ya, "Scan", "Photo, scan animation")
    box("login", xs[1], ya2, "Login", "Sign in or create account")
    box("offline", xs[3], ya2, "Offline status", "Saved recipes still open")

    # Row B: AI path, right to left.
    diamond("found", xs[5], yb, "Ingredients found?")
    box("edit", xs[4], yb, "Ingredients", "Remove, fix, add items")
    box("prefs", xs[3], yb, "Preferences", "Time, servings, allergies")
    box("gen", xs[2], yb, "AI generates 3 recipes", fill=system, stroke=MOCK["ok"])
    diamond("ok", xs[1], yb, "Request OK?")
    box("list", xs[0], yb, "Recipe suggestions", "Compare 3 cards")
    box("manual", xs[5], yb2, "Nothing detected", "Type items by hand")
    box("error", xs[1], yb2, "Error message", "Offer retry")

    # Row C: outcome, left to right.
    box("detail", xs[0], yc, "Recipe detail")
    diamond("missing", xs[1], yc, "Missing items?")
    box("shop", xs[2], yc, "Shopping list", "Syncs live to household", fill=system, stroke=MOCK["ok"])
    diamond("save", xs[3], yc, "Save recipe?")
    box("saved", xs[4], yc, "Saved recipes", "Stored on device, opens offline", fill=system, stroke=MOCK["ok"])
    box("end", xs[5], yc, "Back to Home", fill=start)

    def h(a, b, text=None):
        edge([side(a, "r" if nodes[b][0] > nodes[a][0] else "l"), side(b, "l" if nodes[b][0] > nodes[a][0] else "r")],
             text, (side(a, "r")[0] + 3, nodes[a][1] + 3) if text and nodes[b][0] > nodes[a][0]
             else ((side(a, "l")[0] - 15, nodes[a][1] + 3) if text else None))

    def v(a, b, text=None):
        p = side(a, "b")
        edge([p, side(b, "t")], text, (p[0] + 4, p[1] - 11) if text else None)

    h("open", "auth")
    h("auth", "home", "Yes")
    v("auth", "login", "No")
    h("home", "online")
    h("online", "input", "Yes")
    v("online", "offline", "No")
    tip = side("input", "r")
    edge([tip, side("scan", "l")], "Photo", (tip[0] - 9, tip[1] + 8))
    edge([side("input", "b"), side("edit", "t")], "Type", (xs[4] + 4, side("input", "b")[1] - 11))
    v("scan", "found")
    h("found", "edit", "Yes")
    v("found", "manual", "No")
    edge([side("manual", "l"), (xs[4], yb2), side("edit", "b")])
    h("edit", "prefs")
    h("prefs", "gen")
    h("gen", "ok")
    h("ok", "list", "Yes")
    v("ok", "error", "No")
    edge([side("error", "r"), (xs[2], yb2), side("gen", "b")], "Retry", (side("error", "r")[0] + 3, yb2 + 3))
    v("list", "detail")
    h("detail", "missing")
    h("missing", "shop", "Yes")
    h("shop", "save")
    h("save", "saved", "Yes")
    h("saved", "end")
    # A login joins Home from below; so does a retry from the Offline screen.
    edge([side("login", "r"), (xs[2], ya2), side("home", "b")])
    edge([side("offline", "l"), (xs[2], ya2)], "Retry", (side("offline", "l")[0] - 24, ya2 + 3))
    miss_low = side("missing", "b")
    edge([miss_low, (xs[1], yc2), (xs[3], yc2), side("save", "b")], "No", (xs[1] + 4, miss_low[1] - 11))
    save_top = side("save", "t")
    edge([save_top, (xs[3], yc + 56), (xs[5], yc + 56), side("end", "t")], "No", (xs[3] + 4, save_top[1] + 2))

    # Legend.
    ly = 30
    items = [("#FFFFFF", MOCK["primary"], "Screen"), (MOCK["warn_soft"], MOCK["warn"], "Decision"),
             (MOCK["ok_soft"], MOCK["ok"], "AI or stored data"), (MOCK["soft"], MOCK["primary"], "Start or end")]
    x = 30
    for fill, stroke, text in items:
        c.setFillColor(colors.HexColor(fill))
        c.setStrokeColor(colors.HexColor(stroke))
        c.roundRect(x, ly, 16, 10, 2, fill=1)
        c.setFillColor(INK)
        c.setFont("Body", 7.8)
        c.drawString(x + 21, ly + 2, text)
        x += 30 + pdfmetrics.stringWidth(text, "Body", 7.8)
    c.setFillColor(MUTED)
    c.setFont("Body", 7.8)
    c.drawRightString(width - 30, ly + 2, "Bottom navigation links Home, Saved recipes and Shopping list at any time. "
                                          "Saved recipes also open offline.")
    c.save()

    # Geometry self-check: edges must not run through unrelated nodes or cross each other.
    problems = []
    for (a, b) in segments:
        x0, x1 = sorted((a[0], b[0]))
        y0, y1 = sorted((a[1], b[1]))
        for key, (nx, ny, rx, ry) in nodes.items():
            if x0 < nx + rx - 1 and x1 > nx - rx + 1 and y0 < ny + ry - 1 and y1 > ny - ry + 1:
                problems.append(f"edge {a}->{b} crosses node {key}")
    for i, (a, b) in enumerate(segments):
        for (e, f) in segments[i + 1:]:
            ah, eh = a[1] == b[1], e[1] == f[1]
            if ah == eh:
                continue
            (hp, hq), (vp, vq) = ((a, b), (e, f)) if ah else ((e, f), (a, b))
            hx0, hx1 = sorted((hp[0], hq[0]))
            vy0, vy1 = sorted((vp[1], vq[1]))
            if hx0 + 1 < vp[0] < hx1 - 1 and vy0 + 1 < hp[1] < vy1 - 1:
                problems.append(f"edges cross at {vp[0]},{hp[1]}")
    for problem in problems:
        print("user-flow:", problem)


# 3. Architecture ----------------------------------------------------------------------------
class MvvmDiagram(Flowable):
    def __init__(self):
        super().__init__()
        self.width, self.height = TEXT_WIDTH, 216

    def draw(self):
        c = self.canv

        def box(x, y, w, h, title, detail, fill=HEAD, stroke=PRIMARY):
            c.setFillColor(fill)
            c.setStrokeColor(stroke)
            c.setLineWidth(0.9)
            c.roundRect(x, y, w, h, 6, fill=1)
            c.setFillColor(INK)
            c.setFont("Bold", 8.8)
            c.drawCentredString(x + w / 2, y + h / 2 + 2, title)
            c.setFont("Body", 7.4)
            c.drawCentredString(x + w / 2, y + h / 2 - 9, detail)

        def arrow(x, y0, y1):
            c.setStrokeColor(INK)
            c.setFillColor(INK)
            c.setLineWidth(0.9)
            c.line(x, y0, x, y1)
            s = 1 if y1 > y0 else -1
            p = c.beginPath()
            p.moveTo(x, y1)
            p.lineTo(x - 3, y1 - s * 5)
            p.lineTo(x + 3, y1 - s * 5)
            p.close()
            c.drawPath(p, fill=1, stroke=0)

        def note(x, y, text):
            c.setFillColor(MUTED)
            c.setFont("Body", 7.3)
            c.drawString(x, y, text)

        left, w, h = 0, 386, 38
        y_view, y_vm, y_repo, y_src = 178, 118, 58, 0
        box(left, y_view, w, h, "View", "Screens and widgets (Flutter). No business logic. go_router moves between them")
        box(left, y_vm, w, h, "ViewModel", "ChangeNotifier classes exposed with Provider. Hold loading, data and error state")
        box(left, y_repo, w, h, "Repository and service interfaces", "Dart abstract classes. ViewModels depend only on these")
        src = colors.white
        sw = (w - 24) / 3
        box(0, y_src, sw, h, "Hive", "Saved recipes on device", src)
        box(sw + 12, y_src, sw, h, "Firebase", "Auth, Firestore", src)
        box(2 * (sw + 12), y_src, sw, h, "firebase_ai + App Check", "Gemini: image + JSON", src)
        box(402, 0, TEXT_WIDTH - 402, y_view + h, "Model", "Plain Dart classes", colors.HexColor(MOCK["warn_soft"]),
            colors.HexColor(MOCK["warn"]))
        arrow(150, y_view, y_vm + h)
        note(157, y_vm + h + 8, "user events, method calls")
        arrow(120, y_vm + h, y_view)
        note(14, y_vm + h + 8, "notifyListeners()")
        arrow(150, y_vm, y_repo + h)
        note(157, y_repo + h + 8, "Future and Stream calls")
        arrow(120, y_repo + h, y_vm)
        note(14, y_repo + h + 8, "data or typed errors")
        for i in range(3):
            arrow(sw / 2 + i * (sw + 12), y_repo, y_src + h)


def architecture():
    interfaces = """abstract class AuthService {
  Stream<AppUser?> get userChanges;
  Future<void> signIn(String email, String password);
  Future<void> signUp(String email, String password, String name);
  Future<void> signOut();
}

abstract class RecipeAiService {
  Future<List<Ingredient>> detectIngredients(Uint8List photo);
  Future<List<Recipe>> suggestRecipes(List<Ingredient> items, Preferences prefs);
}

abstract class SavedRecipeRepository {
  Stream<List<Recipe>> watchAll();
  Future<void> save(Recipe recipe);
  Future<void> delete(String recipeId);
}

abstract class ShoppingListRepository {
  Stream<List<ListItem>> watchItems(String householdId);
  Future<void> add(String householdId, String name);
  Future<void> setChecked(String householdId, String itemId, bool checked);
}

abstract class HouseholdRepository {
  Future<Household> create();
  Future<Household> joinWithCode(String inviteCode);
}

abstract class ConnectivityService {
  Stream<bool> get isOnline;
}"""
    response = """{
  "recipes": [{
    "title": "Patatesli Omlet",
    "minutes": 20,
    "servings": 2,
    "usedIngredients": ["patates", "yumurta", "soğan", "peynir"],
    "missingIngredients": ["tereyağı"],
    "steps": ["Patatesleri küp küp doğra.", "Tavada altın rengi olana kadar kavur."]
  }]
}"""
    build("architecture-protocols.pdf", header("Architecture and Protocols") + [
        Paragraph("1. Software design pattern: MVVM with Provider", H2),
        P("Dolaptan uses <b>Model-View-ViewModel</b>, the clean structure the course asks for. Each ViewModel is a "
          "<font face='Mono'>ChangeNotifier</font> exposed with <b>Provider</b>, and widgets rebuild when it notifies. "
          "We chose Provider over Riverpod because it is simpler and enough for a two-person team on a short schedule."),
        MvvmDiagram(),
        Spacer(1, 7),
        table([["Layer", "Role in Dolaptan", "Examples"],
               ["Model", "Plain Dart classes with JSON and Hive conversion", "Recipe, Ingredient, Preferences, ListItem, Household, AppUser"],
               ["View", "Display state and forward events. They never call Firebase", "HomeScreen, IngredientsScreen, RecipeListScreen"],
               ["ViewModel", "Screen state and rules, such as validating AI output and calculating match %", "ScanViewModel, RecipeViewModel, ShoppingListViewModel"],
               ["Repository / Service", "Hide where data comes from, so ViewModels can be tested with fakes", "RecipeAiService, SavedRecipeRepository, ShoppingListRepository"]],
              [34, 80, 60]),
        Paragraph("2. Screen map", H2),
        table([["Screen", "go_router path", "ViewModel", "Main data"],
               ["Login", "/login", "AuthViewModel", "Firebase Auth"],
               ["Home", "/home", "SavedViewModel", "Recent saved recipes (Hive)"],
               ["Scan", "/scan", "ScanViewModel", "Camera image, AI detection"],
               ["Ingredients", "/ingredients", "ScanViewModel", "Editable detected list"],
               ["Preferences", "/preferences", "RecipeViewModel", "Time, servings, allergies"],
               ["Recipe suggestions", "/recipes", "RecipeViewModel", "3 AI recipes"],
               ["Recipe detail", "/recipes/:id", "RecipeViewModel", "Recipe, save and add-to-list actions"],
               ["Saved recipes", "/saved", "SavedViewModel", "Hive, works offline"],
               ["Shopping list", "/list", "ShoppingListViewModel", "Firestore real-time stream"],
               ["Offline status", "/offline", "ConnectivityViewModel", "Network state, saved recipes"]],
              [38, 34, 44, 58]),
        Spacer(1, 3),
        P("A <font face='Mono'>redirect</font> in go_router sends signed-out users to /login. A "
          "<font face='Mono'>StatefulShellRoute</font> keeps the three tabs. Scan uses an "
          "<font face='Mono'>AnimationController</font> for the moving line. Screens open with iOS push "
          "transitions (<font face='Mono'>CupertinoPage</font>), Preferences opens as a sheet, and the recipe "
          "title moves into the detail screen with a <font face='Mono'>Hero</font>."),
        Paragraph("UI layer: Cupertino widgets on iOS and Android", H2),
        P("The interface follows iOS design, so the View layer uses Flutter's Cupertino widgets. They now ship in "
          "the <b>cupertino_ui</b> package (version 1.1.5 on pub.dev, published by flutter.dev), which supports "
          "both Android and iOS. The same widgets render on both platforms, so one codebase gives the same look."),
        table([["Design element", "Flutter widget"],
               ["App shell and routing", "CupertinoApp.router with go_router, CupertinoPage for push transitions"],
               ["Large-title navigation bar", "CupertinoSliverNavigationBar"],
               ["Tab bar", "CupertinoTabBar inside a StatefulShellRoute"],
               ["Inset grouped list", "CupertinoListSection.insetGrouped, CupertinoListTile"],
               ["Preferences sheet", "showCupertinoSheet"],
               ["Time and servings", "CupertinoSlidingSegmentedControl"],
               ["Allergy switches", "CupertinoSwitch"],
               ["Search, loading", "CupertinoSearchTextField, CupertinoActivityIndicator"],
               ["Swipe to delete", "flutter_slidable (MIT, Android and iOS)"],
               ["Icons", "cupertino_icons (MIT)"]],
              [58, 116]),
        Spacer(1, 3),
        P("<b>Android:</b> SafeArea keeps content clear of the Android status and navigation bars, and the system "
          "Back gesture pops the go_router stack. Inter is bundled as the app font, because Apple's SF Pro "
          "license does not allow use on non-Apple systems. The cupertino_ui page does not mention Liquid Glass, "
          "so bars use a plain translucent background. <b>[TO CHECK: Liquid Glass support in cupertino_ui "
          "before week 11.]</b>"),
        Paragraph("3. Data model", H2),
        Preformatted("""Dart models
  Ingredient   name, isUncertain
  Preferences  minutes, servings, allergies[]
  Recipe       id, title, minutes, servings, usedIngredients[], missingIngredients[], steps[]
               photoPath (optional, empty until a real photo exists; the photo space is hidden)
               matchPercent = used / (used + missing), calculated in the app, never by the AI
  ListItem     id, name, addedBy, addedByName, checked, createdAt

Firestore (shared data only)
  users/{uid}                     name, householdId
  households/{id}                 name, inviteCode, memberIds[]
  households/{id}/items/{itemId}  name, addedBy, addedByName, checked, createdAt
  inviteCodes/{code}              householdId

Hive (device)
  saved_{uid}                     saved recipes, one box per user, for offline reading
  prefs                           last used preferences""", CODE),
        P("Photos are compressed, sent only for analysis, and never stored in our database. Firestore security "
          "rules allow only household members to read or change that household's items. A user joins by reading "
          "one invite code document (no listing) and can add only their own uid to memberIds."),
        Paragraph("4. Key interfaces (Dart abstract classes)", H2),
        P("Dart has no <font face='Mono'>protocol</font> keyword, so abstract classes define these contracts. "
          "ViewModels depend on them rather than on Firebase, so an implementation can be replaced by a fake in "
          "tests, or the AI provider can change without touching the UI."),
        Preformatted(interfaces, CODE),
        Paragraph("5. Communication protocols", H2),
        table([["Protocol / technology", "Purpose in the app"],
               ["HTTPS (TLS)", "Encrypts traffic between the app and Firebase services"],
               ["Firebase Authentication", "Signs users in with email and password and gives requests a verified identity"],
               ["Firestore real-time listeners", "Push shopping list changes to every household member as a Dart Stream"],
               ["Firestore security rules", "Check on the server who can read or change each document"],
               ["Firebase AI Logic (firebase_ai)", "Sends the photo and prompt to the Gemini Developer API through Firebase, so no Gemini API key ships in the app. Planned model: gemini-3.8-flash, kept in one constant so it can change"],
               ["Firebase App Check", "Proves that AI requests come from our real app. Uses Play Integrity on Android, and the debug provider during development"],
               ["JSON with a response schema", "Requests structured output (responseMimeType + responseSchema), then parses it into Dart models"]],
              [58, 116]),
        Paragraph("6. Recipe generation sequence", H2),
        P("(1) The View passes the photo to ScanViewModel. (2) RecipeAiService returns ingredients, and unclear ones "
          "are marked uncertain. (3) The user edits the list and sets time, servings and allergies. (4) The service "
          "requests 3 Turkish recipes as JSON in the format below. (5) The ViewModel validates the response, "
          "calculates match %, and exposes the cards. If a request or parsing fails, it retries once and then shows "
          "a retry message."),
        Preformatted(response, CODE),
    ])


# 4. Overview --------------------------------------------------------------------------------
def overview():
    plan = [["Course week (topic)", MEMBER_1, MEMBER_2],
            ["7 (milestone)", "Interviews, Figma import, prototype links", "Review PDFs, GitHub repository"],
            ["8 (midterm)", "Flutter project, go_router routes, screen skeletons", "Firebase project, Auth, App Check debug setup"],
            ["9 (Hive)", "Saved recipes in Hive, Offline status", "Camera, AI ingredient detection, editable list"],
            ["10 (Firestore, Auth)", "Household, shopping list stream, security rules", "Recipe generation with JSON schema, recipe screens"],
            ["11 (Animations)", "Scan animation, recipe transitions", "Error states, retry, response validation"],
            ["12 (Device, publishing)", "Real-phone tests with two accounts, bug fixes", "APK build, README, screenshots"],
            ["13 (Presentations)", "5-minute demo and presentation", "2-minute backup video, peer contribution form"]]
    build("project-overview.pdf", header("Project Overview") + [
        Paragraph("1. Problem and user", H2),
        P("Our users are students and small households in Türkiye who cook at home. Our starting assumption is that "
          "they open the fridge, see ingredients, and still cannot decide what to make, which can lead to a takeaway "
          "order or food that spoils. The interviews below test this assumption and show how often it happens."),
        Paragraph("2. Evidence", H2),
        P("<b>Interviews:</b> " + EVIDENCE),
        P("<b>Statistic:</b> The UNEP Food Waste Index Report 2024 estimates 1.05 billion tonnes of food waste "
          "worldwide in 2022, and around 60% of it came from households. Its annex lists a Türkiye household estimate of "
          "102 kg per person per year (about 8.7 million tonnes). This is a <b>low-confidence</b> value: the report "
          "states it found no household study for Türkiye, so the number is extrapolated from other countries. "
          "We use it as context, not as proof of our problem."),
        Paragraph("3. Why existing apps fall short", H2),
        table([["App", "What we verified (2 Nov 2026)", "Gap for our user"],
               ["Nefis Yemek Tarifleri", "Strong Turkish recipe brand: 4.8 from 94k ratings on the Turkish App Store. Its website offers ingredient selection and an AI assistant. The app listing says it does not work without internet", "Listing does not mention photo detection. No offline use. Shared list [TO CHECK]"],
               ["SnapChef AI", "Detects ingredients from a fridge or pantry photo. Premium costs $14.99 per month or $19.99-$29.99 per year", "Turkish recipes and interface [TO CHECK]"],
               ["Recipez", "Fridge scan and 3 recipes, like ours. Filters listed: Italian, Chinese, Thai, Mexican, Indian. Exports to Walmart. 4 ratings", "No listed Turkish focus. US grocery link. Paid plans after trial"],
               ["Samsung Food", "Phone photo scanning is reported as part of paid Food+", "Scan reported as paid only. Turkish support [TO CHECK]"]],
              [32, 92, 50]),
        Spacer(1, 4),
        P("Photo-to-recipe apps and Turkish recipe apps both exist. We did not confirm any app that combines all four parts: "
          "Turkish-first recipes, editable photo detection, offline saved recipes, and a shared household list. "
          "This is a desk check of store listings, not a full market review. "
          "<b>[TO CHECK: install the apps above and test them in Turkish before submission.]</b>"),
        Paragraph("4. Must-have features and course topics", H2),
        table([["Must-have feature", "Course topic"],
               ["Photo to editable ingredient list and 3 recipes (firebase_ai + App Check)", "HTTP/API, JSON, async (Future)"],
               ["Saved recipes that open without internet", "Local DB (Hive)"],
               ["Sign in, and a real-time shared shopping list", "Firebase Auth, Firestore, Streams, StreamBuilder"],
               ["Multi-step flow from photo to recipe, with bottom tabs", "Navigation, go_router"],
               ["Scan animation and recipe transitions", "Animations and gestures"],
               ["Separation of screens, state and data", "MVVM, Provider"]],
              [104, 70]),
        KeepTogether([Paragraph("5. Weekly plan", H2), table(plan, [36, 69, 69])]),
        KeepTogether([Paragraph("6. Risks and responses", H2),
        table([["Risk", "Response"],
               ["AI detects an ingredient incorrectly", "Users review every item, and uncertain ones are flagged before recipes are generated"],
               ["AI suggests unsafe or allergenic food", "Pass allergies in the prompt, show a reminder, and ask users to check"],
               ["AI free-tier limit or outage", "Show a retry message and keep manual input and saved recipes available"],
               ["AI returns invalid JSON", "Use a response schema, validate the result, and retry once"],
               ["App Check blocks AI requests in the demo build", "Firebase docs list required enforcement from 2 Nov 2026. Use the debug provider in development. For an APK outside Google Play, register its SHA-256, turn off PLAY_RECOGNIZED, and test early"],
               ["Photos may contain personal content", "Gemini free-tier input may be reviewed by people and used to improve Google products. Tell users to photograph only shelves, and do not store photos"],
               ["Security rules are misconfigured", "Test the rules with two accounts before the demo"],
               ["Hive package maintenance", "Stable hive 2.2.3 is about 4 years old. Use the compatible community fork hive_ce if hive causes problems"],
               ["Short schedule", "Keep to the must-have features and leave extras until after the demo"]],
              [62, 112])]),
        Paragraph("Sources (accessed 2 Nov 2026)", H2),
        *[Paragraph(s, SMALL) for s in [
            "UNEP (2024), Food Waste Index Report 2024: totals p. 64 of PDF, Türkiye data status p. 41, Annex 3 p. 190. "
            "Copy: sdg2advocacyhub.org/wp-content/uploads/2024/03/food_waste_index_report_2024.pdf",
            "Nefis Yemek Tarifleri: apps.apple.com/tr/app/nefis-yemek-tarifleri/id947863045, nefisyemektarifleri.com",
            "SnapChef AI: apps.apple.com/us/app/snapchef-ai/id6749183626",
            "Recipez: apps.apple.com/us/app/id6765974915",
            "Samsung Food: sammobile.com/news/samsung-food-update-scan-ingredients-using-phone",
            "Firebase AI Logic: firebase.google.com/docs/ai-logic/get-started, /app-check, /models, /generate-structured-output",
            "Gemini API terms: ai.google.dev/gemini-api/terms. Hive: pub.dev/packages/hive, pub.dev/packages/hive_ce",
        ]],
    ])


if __name__ == "__main__":
    design_justification()
    user_flow()
    architecture()
    overview()
    print("ok")
