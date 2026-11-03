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

MEMBER_1 = "Hatice Karakuş"
MEMBER_2 = "Muhammed Ali Demirsoy"
TEAM = f"{MEMBER_1}, {MEMBER_2}"
TEAM_NO = "[TAKIM NO]"
EVIDENCE = ("<b>[TO FILL: interview 5-10 people who cook at home, including people who share a flat. Write how "
            "many you spoke to, how many struggle to decide what to cook and how often, how they share shopping today "
            "(for example a group chat), what food went off at home last month, and one short quote. Do not submit "
            "this placeholder.]</b>")

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


pdfmetrics.registerFont(TTFont("Hand", str(FONTS / "PatrickHand-Regular.ttf")))
pdfmetrics.registerFont(TTFont("Script", str(FONTS / "Caveat-Bold.ttf")))


def design_justification():
    tokens = [
        ("Paper", "bg", "Page background with faint ruled lines (#EADBC6)"),
        ("Card", "surface", "Hand-drawn cards, fields and the tab bar"),
        ("Ink", "text", "Text and the pen outline around cards and buttons"),
        ("Pencil", "text2", "Times, servings, who added an item, hints"),
        ("Terracotta", "accent", "Only things you can tap, and urgent expiry"),
        ("Herb green", "herb", "The Dolapta header and the Var state"),
        ("Tag red / green / yellow", "tag_red", "Backgrounds of Yarın, Var and Azaldı tags"),
    ]
    rows = [["", "Token", "Light", "Dark", "Use"]] + [
        [Swatch(LIGHT[k]), name, LIGHT[k], DARK[k], use] for name, k, use in tokens]
    pairs = [("text", "bg", "Ink on paper"), ("text2", "surface", "Pencil text on a card"),
             ("accent", "surface", "Tappable text on a card"), ("on_accent", "accent", "Label on the main button"),
             ("accent", "tag_red", "Yarın tag"), ("herb", "tag_green", "Var tag"),
             ("tag_text_y", "tag_yellow", "Azaldı tag")]
    check = [["Text / background", "Light", "Dark", "AA (4.5:1)"]]
    for fg, bg, use in pairs:
        lo, da = contrast(LIGHT[fg], LIGHT[bg]), contrast(DARK[fg], DARK[bg])
        check.append([use, f"{lo:.2f}:1", f"{da:.2f}:1", "Pass" if min(lo, da) >= 4.5 else "Fail"])
    def sample(text, font, size):
        style = ParagraphStyle(f"sample-{size}", parent=BODY, fontName=font, fontSize=size,
                               leading=size * 1.2, spaceAfter=0)
        return Paragraph(text, style)
    type_rows = [["Role", "Font, size", "Sample", "Use"],
                 ["Screen title", "Caveat Bold 44", sample("Dolap", "Script", 20), "Large titles"],
                 ["Section header", "Caveat Bold 26", sample("Yakında bozulacak", "Script", 14), "With a brush underline"],
                 ["Button, tag", "Caveat Bold 22", sample("Ne Pişirsem?", "Script", 13), "Short labels only"],
                 ["Body", "Patrick Hand 18.7", sample("Yumurtaları çırpıp dök.", "Hand", 11), "Rows, steps, fields"],
                 ["Small", "Patrick Hand 14.3", sample("15 dk · 2 kişilik", "Hand", 9), "Times, servings, hints"]]
    build("design-justification.pdf", header("Design Justification") + [
        P("<b>Dolaptan</b> is a shared kitchen for people who live together: one pantry everyone sees, Turkish "
          "recipes that use what is about to go off, and a shared shopping list. The screens look like a "
          "<b>hand-written family recipe notebook</b>: cream paper, pen outlines, hand-written titles and painted "
          "food. Cooking at home is personal, and a notebook feels warmer and more inviting than a store app, "
          "which matters for a habit people have to keep up every day. The structure underneath stays standard "
          "iOS (large titles, a floating tab bar with three tabs, grouped lists, sheets, segmented controls and "
          "switches), so the app is still quick to learn."),
        Paragraph("Color", H2),
        P("The paper color matches the cream background of our illustrations, so paintings sit on the page "
          "without boxes. Terracotta appears only on things you can tap and on items that expire tomorrow, "
          "so the warmest color always means act now. Pantry states are tags with both a word and a color: "
          "Var green, Azaldı mustard, Yarın red. Dark Mode is a warm dark brown, not black, so the notebook "
          "feel stays at night."),
        table(rows, [10, 40, 18, 18, 88]),
        Spacer(1, 5),
        P("Contrast uses the WCAG 2.2 formula on linearized channels, ratio = (L1 + 0.05) / (L2 + 0.05). Every "
          "pair passes AA in both modes. The build script also checks every text on all 60 screens."),
        table(check, [80, 32, 32, 30]),
        Paragraph("Typography", H2),
        P("Two free Google Fonts (SIL Open Font License) that include every Turkish letter (ğ, ı, İ, ş, ç). "
          "<b>Caveat</b>, a pen script, is used only for short text such as titles, headers, buttons and tags, "
          "where personality matters and words are few. Longer text uses <b>Patrick Hand</b>, which looks "
          "hand-written but has print letter shapes, so recipe steps stay easy to read. Its letters are smaller "
          "than Inter at the same size, so we set it 10% larger. The iOS status bar and the wireframes keep Inter."),
        table(type_rows, [36, 38, 52, 48]),
        Paragraph("Illustrations and layout", H2),
        *bullets([
            "All food art is gouache style: dishes, 12 ingredients, 6 scenes for empty states, 12 small doodles "
            "(herbs, spoon, tea glass) and 6 vignettes. We generated them with Figma AI in batches with one "
            "shared style prompt, then cut, cleaned and selected them by hand. We keep only art that shows "
            "food accurately. Recipe pictures are illustrations, not photos, so nobody mistakes them for the "
            "real result.",
            "Cards, buttons and tags have a slightly uneven pen outline. Section headers have a brush underline "
            "and a small doodle. Empty states show a taped-in picture with a short title, one sentence and one action.",
            "Frame 360 x 800 pt, 16 pt margins, 28 pt ruled-line rhythm. Every tappable element is at least "
            "44 x 44 pt, checked by the build script on every screen.",
        ]),
        Paragraph("Accessibility and how the design supports users", H2),
        *bullets([
            "Color is never the only signal: states are words, checked items get a check mark, and uncertain "
            "scan results say \"Emin değiliz, kontrol et\".",
            "Less typing, the main complaint about competing apps: photo scan, estimated expiry dates the user "
            "only corrects, and Cooked / Bought update the pantry automatically.",
            "Fewer surprises: a \"missing ingredients\" limit in Preferences, a timer on steps that need one, "
            "and \"Hesapsız Dene\" to try the app before signing up.",
            "Icon buttons will have VoiceOver and TalkBack labels, and text will follow the system size setting.",
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
    c.setFillColor(INK)
    c.setFont("Bold", 8.5)
    c.drawString(30, height - 66, "Core loop:")
    c.setFont("Body", 8.5)
    c.drawString(30 + pdfmetrics.stringWidth("Core loop: ", "Bold", 8.5), height - 66,
                 "Pantry → recipes that use what expires first → Cooked → missing and finished items go to the "
                 "shared list → Bought → back in the pantry.")

    bw, bh, dw, dh = 70, 40, 70, 54
    pitch = (width - 60 - bw) / 8
    xs = [30 + bw / 2 + i * pitch for i in range(9)]
    lanes = {1: 448, 2: 300, 3: 152}
    drop = 64
    nodes, segments = {}, []

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

    def label(cx, cy, title, limit):
        lines = wrap(title, limit, "Bold", 7.4)
        y = cy + (len(lines) - 1) * 4.5 - 2.6
        c.setFillColor(INK)
        c.setFont("Bold", 7.4)
        for line in lines:
            c.drawCentredString(cx, y, line)
            y -= 9

    def box(key, x, y, title, fill="#FFFFFF", stroke=MOCK["primary"], h=bh):
        nodes[key] = (x, y, bw / 2, h / 2)
        c.setFillColor(colors.HexColor(fill))
        c.setStrokeColor(colors.HexColor(stroke))
        c.setLineWidth(1)
        c.roundRect(x - bw / 2, y - h / 2, bw, h, 6, fill=1)
        label(x, y, title, bw - 10)

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
        label(x, y, title, 42)

    def edge(points, text=None, at=None):
        c.setStrokeColor(INK)
        c.setLineWidth(0.9)
        for a, b in zip(points, points[1:]):
            c.line(*a, *b)
            segments.append((a, b))
        (x1, y1), (x2, y2) = points[-2], points[-1]
        c.setFillColor(INK)
        p = c.beginPath()
        p.moveTo(x2, y2)
        if x1 == x2:
            s = 1 if y2 > y1 else -1
            p.lineTo(x2 - 3, y2 - s * 5.5)
            p.lineTo(x2 + 3, y2 - s * 5.5)
        else:
            s = 1 if x2 > x1 else -1
            p.lineTo(x2 - s * 5.5, y2 - 3)
            p.lineTo(x2 - s * 5.5, y2 + 3)
        p.close()
        c.drawPath(p, fill=1, stroke=0)
        if text:
            tw = pdfmetrics.stringWidth(text, "Bold", 7)
            c.setFillColor(colors.white)
            c.rect(at[0] - 1, at[1] - 2, tw + 2, 9, fill=1, stroke=0)
            c.setFillColor(WARN)
            c.setFont("Bold", 7)
            c.drawString(*at, text)

    def side(key, where):
        x, y, rx, ry = nodes[key]
        return {"r": (x + rx, y), "l": (x - rx, y), "t": (x, y + ry), "b": (x, y - ry)}[where]

    screen, system, start = "#FFFFFF", MOCK["ok_soft"], MOCK["soft"]

    def lane(n, title, items):
        y = lanes[n]
        c.setFillColor(MUTED)
        c.setFont("Bold", 8.5)
        c.drawString(30, y + 42, title)
        keys = []
        for col, kind, text in items:
            key = f"{n}-{col}"
            if kind == "d":
                diamond(key, xs[col], y, text)
            else:
                fill, stroke = {"s": (screen, MOCK["primary"]), "a": (system, MOCK["ok"]),
                                "p": (start, MOCK["primary"])}[kind]
                box(key, xs[col], y, text, fill, stroke)
            keys.append(key)
        return keys

    def chain(keys, labels=None):
        labels = labels or {}
        for a, b in zip(keys, keys[1:]):
            pa = side(a, "r")
            text = labels.get(a)
            edge([pa, side(b, "l")], text, (pa[0] + 3, pa[1] + 3) if text else None)

    def branch(src, col, n, title, kind="s", text="No"):
        y = lanes[n] - drop
        key = f"{n}-b{col}"
        fill, stroke = {"s": (screen, MOCK["primary"]), "a": (system, MOCK["ok"])}[kind]
        box(key, xs[col], y, title, fill, stroke, h=34)
        p = side(src, "b")
        edge([p, side(key, "t")], text, (p[0] + 4, p[1] - 10))
        return key

    def back_up(key, target):
        tx = nodes[target][0]
        start_pt = side(key, "r" if tx > nodes[key][0] else "l")
        edge([start_pt, (tx, start_pt[1]), side(target, "b")])

    l1 = lane(1, "1  Add food to the shared pantry", [
        (0, "p", "Open app"), (1, "d", "Signed in?"), (2, "p", "Shared pantry"), (3, "d", "Online?"),
        (4, "s", "Scan shelves"), (5, "d", "Items found?"), (6, "s", "Review items, check estimated dates"),
        (7, "a", "Saved to shared pantry"), (8, "a", "Expiry reminders scheduled")])
    chain(l1, {"1-1": "Yes", "1-3": "Yes", "1-5": "Yes"})
    back_up(branch("1-1", 1, 1, "Log in, sign up or try as guest"), "1-2")
    branch("1-3", 3, 1, "Offline: cached pantry, no AI")
    back_up(branch("1-5", 5, 1, "Type items by hand"), "1-6")

    l2 = lane(2, "2  Decide what to cook", [
        (0, "p", "Pantry: Ne Pişirsem?"), (1, "s", "Preferences sheet"),
        (2, "a", "AI suggests 3 recipes, expiring items first"), (3, "d", "Request OK?"),
        (4, "s", "Recipe suggestions"), (5, "s", "Recipe detail"), (6, "d", "Missing items?"),
        (7, "s", "Tap Cooked"), (8, "a", "Used items set to Low, finished ones to list")])
    chain(l2, {"2-3": "Yes", "2-6": "No"})
    back_up(branch("2-3", 3, 2, "Error, retry"), "2-2")
    back_up(branch("2-6", 6, 2, "Add to shared list", "a", "Yes"), "2-7")

    l3 = lane(3, "3  Shop and stay ahead of expiry", [
        (0, "s", "Shared shopping list"), (1, "s", "Tick Bought"), (2, "a", "Item back in pantry"),
        (3, "p", "Shared pantry"), (5, "a", "Reminder: item expires tomorrow"), (6, "s", "Pantry, expiring first"),
        (7, "p", "Continue in lane 2")])
    chain(l3[:4])
    chain(l3[4:])

    ly = 30
    items = [("#FFFFFF", MOCK["primary"], "Screen"), (MOCK["warn_soft"], MOCK["warn"], "Decision"),
             (MOCK["ok_soft"], MOCK["ok"], "Automatic (AI, sync, reminder)"), (MOCK["soft"], MOCK["primary"], "Pantry, start or end")]
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
    c.drawRightString(width - 30, ly + 2, "Bottom tabs: Dolap (pantry), Tarifler (saved recipes), Liste (shopping list).")
    c.save()

    problems = []
    for (a, b) in segments:
        x0, x1 = sorted((a[0], b[0]))
        y0, y1 = sorted((a[1], b[1]))
        for key, (nx, ny, rx, ry) in nodes.items():
            if x0 < nx + rx - 1 and x1 > nx - rx + 1 and y0 < ny + ry - 1 and y1 > ny - ry + 1:
                problems.append(f"edge {a}->{b} crosses node {key}")
    keys = list(nodes.items())
    for i, (ka, (ax, ay, arx, ary)) in enumerate(keys):
        for kb, (bx, by, brx, bry) in keys[i + 1:]:
            if abs(ax - bx) < arx + brx and abs(ay - by) < ary + bry:
                problems.append(f"nodes overlap {ka} {kb}")
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
            c.setFont("Bold", 8.4)
            c.drawCentredString(x + w / 2, y + h / 2 + 2, title)
            c.setFont("Body", 7.2)
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

        w, h = 386, 38
        y_view, y_vm, y_repo, y_src = 178, 118, 58, 0
        box(0, y_view, w, h, "View", "Cupertino screens and widgets. No business logic. go_router moves between them")
        box(0, y_vm, w, h, "ViewModel", "ChangeNotifier classes exposed with Provider. Loading, data, error state, loop rules")
        box(0, y_repo, w, h, "Repository and service interfaces", "Dart abstract classes. ViewModels depend only on these")
        src = colors.white
        sw = (w - 3 * 8) / 4
        sources = [("Hive", "Pantry copy, saved"), ("Firebase", "Auth, Firestore"),
                   ("firebase_ai", "Gemini + App Check"), ("Notifications", "Local reminders")]
        for i, (title, detail) in enumerate(sources):
            box(i * (sw + 8), y_src, sw, h, title, detail, src)
            arrow(sw / 2 + i * (sw + 8), y_repo, y_src + h)
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


def architecture():
    interfaces = """abstract class AuthService {
  Stream<AppUser?> get userChanges;
  Future<void> signIn(String email, String password);
  Future<void> signUp(String email, String password, String name);
  Future<void> signOut();
}

abstract class PantryRepository {
  Stream<List<PantryItem>> watch(String householdId);
  Future<void> addAll(String householdId, List<ScannedItem> items);
  Future<void> update(String householdId, PantryItem item);
  Future<void> markCooked(String householdId, Recipe recipe);  // one batched write
  Future<void> remove(String householdId, String itemId);
}

abstract class ShoppingListRepository {
  Stream<List<ListItem>> watchItems(String householdId);
  Future<void> add(String householdId, String name);
  Future<void> markBought(String householdId, ListItem item); // also puts it in the pantry
}

abstract class RecipeAiService {
  Future<List<ScannedItem>> detectItems(Uint8List photo);
  Future<List<Recipe>> suggestRecipes(List<PantryItem> pantry, Preferences prefs);
}

abstract class SavedRecipeRepository {
  Stream<List<Recipe>> watchAll();
  Future<void> save(Recipe recipe);
  Future<void> delete(String recipeId);
}

abstract class ReminderService {
  Future<void> schedule(PantryItem item);   // the day before expiresOn
  Future<void> cancel(String itemId);
}

abstract class HouseholdRepository {
  Future<Household> create();
  Future<Household> joinWithCode(String inviteCode);
}"""
    response = """{
  "recipes": [{
    "title": "Menemen",
    "minutes": 15,
    "servings": 2,
    "usedIngredients": ["domates", "yumurta", "biber", "soğan"],
    "usesExpiring": ["domates"],
    "missingIngredients": [],
    "steps": ["Biberi ve soğanı kavur.", "Domatesi ekle.", "Yumurtaları kır, karıştır."]
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
               ["Model", "Plain Dart classes with JSON and Hive conversion", "PantryItem, ScannedItem, Recipe, ListItem, Preferences, Household"],
               ["View", "Display state and forward events. They never call Firebase", "PantryScreen, ReviewItemsScreen, RecipeDetailScreen"],
               ["ViewModel", "Screen state and the loop rules: Cooked lowers items, Bought restocks them", "PantryViewModel, ScanViewModel, RecipeViewModel, ShoppingListViewModel"],
               ["Repository / Service", "Hide where data comes from, so ViewModels can be tested with fakes", "PantryRepository, RecipeAiService, ReminderService"]],
              [34, 80, 60]),
        Paragraph("2. Screen map", H2),
        table([["Screen", "go_router path", "ViewModel", "Main data"],
               ["Login", "/login", "AuthViewModel", "Firebase Auth"],
               ["Pantry (tab)", "/pantry", "PantryViewModel", "Firestore stream, Hive copy, offline banner"],
               ["Edit item (sheet)", "/pantry/:id", "PantryViewModel", "State, expiry date, reminder"],
               ["Scan", "/scan", "ScanViewModel", "Camera image, AI detection"],
               ["New items", "/scan/review", "ScanViewModel", "Detected items, expiry dates"],
               ["Preferences (sheet)", "/cook", "RecipeViewModel", "Time, servings, allergies"],
               ["Recipe suggestions", "/cook/results", "RecipeViewModel", "3 AI recipes, expiring first"],
               ["Recipe detail", "/recipe/:id", "RecipeViewModel", "Save, add to list, Cooked"],
               ["Recipes (tab)", "/recipes", "SavedViewModel", "Saved recipes in Hive"],
               ["Shopping list (tab)", "/list", "ShoppingListViewModel", "Firestore stream, Bought restocks"]],
              [38, 30, 44, 62]),
        Spacer(1, 3),
        P("A <font face='Mono'>redirect</font> in go_router sends signed-out users to /login. A "
          "<font face='Mono'>StatefulShellRoute</font> keeps the three tabs. Offline status is a banner inside the "
          "Pantry screen. Scan uses an <font face='Mono'>AnimationController</font> for the moving line. Screens "
          "open with iOS push transitions (<font face='Mono'>CupertinoPage</font>), sheets slide up, and the recipe "
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
               ["Edit item, Preferences", "showCupertinoSheet"],
               ["Item state, time, servings", "CupertinoSlidingSegmentedControl"],
               ["Expiry date, reminders", "CupertinoDatePicker, CupertinoSwitch"],
               ["Cooked confirmation", "CupertinoAlertDialog"],
               ["Search, loading", "CupertinoSearchTextField, CupertinoActivityIndicator"],
               ["Swipe to delete", "flutter_slidable (MIT, Android and iOS)"],
               ["Icons", "cupertino_icons (MIT)"]],
              [58, 116]),
        Spacer(1, 3),
        P("<b>Android:</b> SafeArea keeps content clear of the Android status and navigation bars, and the system "
          "Back gesture pops the go_router stack. The notebook fonts Patrick Hand and Caveat (SIL OFL) are "
          "bundled, so text looks the same on both systems. Bars use the notebook paper and card colors instead of "
          "Liquid Glass, so they look the same on iOS and Android."),
        Paragraph("3. Data model", H2),
        Preformatted("""Dart models
  PantryItem   id, name, state (have | low | out), expiresOn?, remind, addedBy, updatedAt
  ScannedItem  name, isUncertain, expiresOn?
  Preferences  minutes, servings, allergies[]
  Recipe       id, title, minutes, servings, usedIngredients[], usesExpiring[],
               missingIngredients[], steps[], photoPath? (photo space hidden when empty)
  ListItem     id, name, addedBy, addedByName, checked, createdAt

Firestore (shared by the household)
  users/{uid}                        name, householdId
  households/{id}                    name, inviteCode, memberIds[]
  households/{id}/pantry/{itemId}    name, state, expiresOn, addedBy, updatedAt
  households/{id}/items/{itemId}     name, addedBy, addedByName, checked, createdAt
  inviteCodes/{code}                 householdId

Hive (device)
  pantry_{householdId}               last synced pantry, opens offline
  saved_{uid}                        saved recipes
  prefs                              last used preferences""", CODE),
        P("<b>Loop rules.</b> <i>Cooked</i>: every used item goes from have to low, or from low to out. Items that "
          "run out leave the pantry and join the shopping list in one batched write. <i>Bought</i>: the item "
          "returns to the pantry as have and leaves the list in one batched write. When two people edit the same "
          "item, the last write wins, which is enough for a household."),
        P("Photos are compressed, sent only for analysis, and never stored. Firestore security rules allow only "
          "household members to read or change that household's pantry and list. A user joins by reading one "
          "invite code document and can add only their own uid to memberIds."),
        Paragraph("4. Key interfaces (Dart abstract classes)", H2),
        P("Dart has no <font face='Mono'>protocol</font> keyword, so abstract classes define these contracts. "
          "ViewModels depend on them rather than on Firebase, so an implementation can be replaced by a fake in "
          "tests, or the AI provider can change without touching the UI."),
        Preformatted(interfaces, CODE),
        Paragraph("5. Communication protocols", H2),
        table([["Protocol / technology", "Purpose in the app"],
               ["HTTPS (TLS)", "Encrypts traffic between the app and Firebase services"],
               ["Firebase Authentication", "Signs users in with email and password and gives requests a verified identity"],
               ["Firestore real-time listeners", "Push pantry and list changes to every household member as Dart Streams"],
               ["Firestore batched writes", "Keep the loop consistent: Cooked and Bought change pantry and list together"],
               ["Firestore security rules", "Check on the server who can read or change each document"],
               ["Firebase AI Logic (firebase_ai)", "Sends the photo or pantry list to the Gemini Developer API through Firebase, so no Gemini API key ships in the app. Planned model: gemini-3.8-flash, kept in one constant"],
               ["Firebase App Check", "Proves that AI requests come from our real app. Play Integrity on Android, debug provider in development"],
               ["JSON with a response schema", "Requests structured output (responseMimeType + responseSchema), then parses it into Dart models"],
               ["Local notifications", "flutter_local_notifications schedules expiry reminders on the device. Android 13 and later asks for permission"]],
              [58, 116]),
        Paragraph("6. Main sequences", H2),
        P("<b>Add food:</b> (1) The photo goes to ScanViewModel. (2) RecipeAiService returns items, and unclear "
          "ones are marked uncertain. (3) The user fixes the list and adds expiry dates. (4) PantryRepository saves "
          "them for the household, and ReminderService schedules reminders."),
        KeepTogether([
        P("<b>Cook:</b> (1) RecipeViewModel sorts the pantry so that items close to expiry come first. (2) "
          "RecipeAiService asks for 3 Turkish recipes as JSON, as shown below. (3) The ViewModel validates the "
          "response; if the request or parsing fails, it retries once and then shows a retry message. (4) After "
          "Cooked, PantryRepository.markCooked updates the pantry and the list together."),
        Preformatted(response, CODE)]),
    ])


# 4. Overview --------------------------------------------------------------------------------
def overview():
    plan = [["Course week (topic)", MEMBER_1, MEMBER_2],
            ["7 (milestone)", "Interviews, Figma import, prototype links", "Review PDFs, GitHub repository"],
            ["8 (midterm)", "Flutter project, go_router routes, screen skeletons", "Firebase project, Auth, App Check debug setup"],
            ["9 (Hive)", "Pantry copy and saved recipes in Hive, offline banner", "Camera, AI item detection, review screen"],
            ["10 (Firestore, Auth)", "Household, shared pantry and list streams, security rules", "Recipe generation with JSON schema, Cooked and Bought loop"],
            ["11 (Animations)", "Scan animation, sheets, recipe transitions", "Error states, retry, response validation"],
            ["12 (Device, publishing)", "Expiry reminders with local notifications", "Two-account and real-phone tests, APK build, README"],
            ["13 (Presentations)", "5-minute demo and presentation", "2-minute backup video, peer contribution form"]]
    build("project-overview.pdf", header("Project Overview") + [
        Paragraph("1. Problem and user", H2),
        P("Our users are students who share a home and small households in Türkiye. We expect them to face two "
          "connected problems. First, they open the fridge and cannot decide what to cook with what is there. "
          "Second, nobody knows exactly what is at home: food goes off, someone buys milk twice, and shopping is "
          "organized through a group chat. These are assumptions, and the interviews below test them."),
        P("<b>Our answer:</b> Dolaptan is a shared kitchen. Everyone in the home sees one pantry, gets recipes "
          "that use what is about to go off, and shares one shopping list. Cooking and shopping update the pantry, "
          "so it stays current without much typing."),
        Paragraph("2. Evidence", H2),
        P("<b>Interviews:</b> " + EVIDENCE),
        P("<b>Statistic:</b> The UNEP Food Waste Index Report 2024 estimates 1.05 billion tonnes of food waste "
          "worldwide in 2022, and around 60% of it came from households. Its annex lists a Türkiye household "
          "estimate of 102 kg per person per year (about 8.7 million tonnes). This is a <b>low-confidence</b> "
          "value: the report found no household study for Türkiye, so the number is extrapolated from other "
          "countries. We use it as context, not as proof of our problem."),
        Paragraph("3. Why existing apps fall short", H2),
        table([["App", "What we verified (2 Nov 2026)", "Gap for our user"],
               ["ChatGPT, Gemini", "General assistants. They can suggest recipes from a photo", "Not built to keep one structured pantry that several people update"],
               ["FridgeBuddy", "Shared pantry and list, expiry reminders, barcode scan. UK App Store listing: sharing through iCloud, household invites in Pro, meal ideas only with Apple Intelligence, Turkish not listed, 22 ratings", "Paid household sharing, no Turkish, recipe ideas tied to Apple devices"],
               ["the fifo", "Free shared list and pantry with expiry countdowns (Product Hunt page)", "No recipe suggestions mentioned"],
               ["Nefis Yemek Tarifleri", "Turkish recipe brand, 4.8 from 94k ratings on the Turkish App Store. The website has ingredient selection and an AI assistant. The app listing says it needs internet", "No shared pantry or list. Photo detection not mentioned"],
               ["SnapChef AI", "Detects ingredients from a fridge photo. Premium $14.99 per month or $19.99-$29.99 per year", "Single user, no shared pantry. Turkish [TO CHECK]"]],
              [30, 90, 54]),
        Spacer(1, 4),
        P("Pantry apps, recipe apps and AI assistants all exist. We did not confirm any app that combines a free "
          "shared household pantry, Turkish recipes that use what is about to go off, and a list that restocks the "
          "pantry. This is a desk check of store listings, not a full market review. <b>[TO CHECK: install "
          "FridgeBuddy and the fifo and test them before submission.]</b>"),
        Paragraph("4. Must-have features and course topics", H2),
        table([["Must-have feature", "Course topic"],
               ["Add food by photo, then get 3 recipes that use expiring items (firebase_ai + App Check)", "HTTP/API, JSON, async (Future)"],
               ["Shared pantry and shopping list that update live, with Cooked and Bought rules", "Firebase Auth, Firestore, Streams, StreamBuilder"],
               ["Pantry copy and saved recipes that open without internet", "Local DB (Hive)"],
               ["Expiry reminders the day before", "Device features: local notifications"],
               ["Tabs, sheets, scan animation and recipe transitions", "Navigation (go_router), animations"],
               ["Separation of screens, state and data", "MVVM, Provider"]],
              [104, 70]),
        KeepTogether([Paragraph("5. Weekly plan", H2), table(plan, [36, 69, 69])]),
        KeepTogether([Paragraph("6. Risks and responses", H2),
        table([["Risk", "Response"],
               ["The pantry gets out of date", "Cooked and Bought update it automatically; states are only have, low and out, not exact counts"],
               ["AI detects an item incorrectly", "Users review every item, and uncertain ones are flagged before saving"],
               ["AI suggests unsafe or allergenic food", "Pass allergies in the prompt, show a reminder, and ask users to check"],
               ["AI free-tier limit, outage or invalid JSON", "Response schema, validation, one retry, then a retry message. The pantry and saved recipes still work"],
               ["App Check blocks AI requests in the demo build", "Firebase docs list required enforcement from 2 Nov 2026. Use the debug provider in development. For an APK outside Google Play, register its SHA-256, turn off PLAY_RECOGNIZED, and test early"],
               ["Reminders do not fire", "Ask for notification permission on Android 13+, and test on real phones; some Android brands stop background apps"],
               ["Two people edit the same item", "Last write wins; batched writes keep pantry and list consistent"],
               ["Photos may contain personal content", "Gemini free-tier input may be reviewed by people and used to improve Google products. Tell users to photograph only shelves, and do not store photos"],
               ["Short schedule", "Keep to the six must-haves. Cooking mode and barcode scanning wait until after the demo"]],
              [58, 116])]),
        Paragraph("Sources (accessed 2 Nov 2026)", H2),
        *[Paragraph(s, SMALL) for s in [
            "UNEP (2024), Food Waste Index Report 2024: totals p. 64 of PDF, Türkiye data status p. 41, Annex 3 p. 190. "
            "Copy: sdg2advocacyhub.org/wp-content/uploads/2024/03/food_waste_index_report_2024.pdf",
            "FridgeBuddy: apps.apple.com/gb/app/id1500190823. the fifo: producthunt.com/products/the-fifo",
            "Nefis Yemek Tarifleri: apps.apple.com/tr/app/nefis-yemek-tarifleri/id947863045, nefisyemektarifleri.com",
            "SnapChef AI: apps.apple.com/us/app/snapchef-ai/id6749183626",
            "Firebase AI Logic: firebase.google.com/docs/ai-logic/get-started, /app-check, /models, /generate-structured-output",
            "flutter_local_notifications: pub.dev/packages/flutter_local_notifications. Gemini API terms: ai.google.dev/gemini-api/terms",
        ]],
    ])


if __name__ == "__main__":
    design_justification()
    user_flow()
    architecture()
    overview()
    print("ok")
