"""Builds a Figma development plugin into design/figma-eklentisi/.

Run it once in the Figma desktop app: it creates the Wireframes, Mockups and Mockups Koyu pages,
imports all SVG screens, and adds the prototype links listed in design/figma-rehberi.md.
"""
import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
DESIGN = BASE / "design"
OUT = DESIGN / "figma-eklentisi"
PAGES = [("Wireframes", "wireframes"), ("Mockups", "mockups"), ("Mockups Koyu", "mockups-dark")]
FLOWS = [("Ana akış", "01-giris"), ("Bozulma bildirimi", "02b-bozulma-bildirimi"),
         ("Çevrimdışı", "10-cevrimdisi"), ("Boş ve hata durumları", "04b-malzeme-yok")]


def ease(kind):
    return {"type": kind}


TRANSITIONS = {
    "Push": {"type": "PUSH", "direction": "LEFT", "matchLayers": False, "easing": ease("EASE_IN_AND_OUT"), "duration": 0.35},
    "Sheet": {"type": "MOVE_IN", "direction": "TOP", "matchLayers": False, "easing": ease("EASE_OUT"), "duration": 0.35},
    "Tam ekran": {"type": "MOVE_IN", "direction": "TOP", "matchLayers": False, "easing": ease("EASE_OUT"), "duration": 0.35},
    "Fade": {"type": "DISSOLVE", "easing": ease("EASE_OUT"), "duration": 0.2},
    "Tarif": {"type": "SMART_ANIMATE", "easing": ease("EASE_IN_AND_OUT"), "duration": 0.35},
    "Sekme": None,
}


def transition(text):
    text = text.strip()
    if text in TRANSITIONS:
        return TRANSITIONS[text]
    m = re.match(r"Smart Animate, Linear, (\d+) ms", text)
    if m:
        return {"type": "SMART_ANIMATE", "easing": ease("LINEAR"), "duration": int(m.group(1)) / 1000}
    raise ValueError(f"unknown transition: {text}")


def parse_links(guide):
    """Reads the link tables under '### <frame>' in the guide."""
    links = []
    body = guide.split("## 8. Bağlantılar", 1)[1].split("## 9.", 1)[0]
    for block in re.split(r"^### ", body, flags=re.M)[1:]:
        frame = block.split()[0]
        if not re.match(r"\d\d", frame):
            continue
        for row in re.findall(r"^\|(.+)\|\s*$", block, flags=re.M):
            cells = [c.strip() for c in row.split("|")]
            if cells[0] in ("Katman", "---") or set(cells[0]) <= {"-"}:
                continue
            layer = cells[0].strip("`")
            if len(cells) == 4:
                trigger, target, how = cells[1], cells[2], cells[3]
            else:
                trigger, target, how = "On tap", cells[1], cells[2]
            delay = None
            m = re.match(r"After delay, (\d+) ms", trigger)
            if m:
                delay = int(m.group(1))
            link = {"from": frame, "layer": None if layer == "Çerçevenin kendisi" else layer, "delay": delay}
            if target == "Önceki ekran" or how == "Geri":
                link["back"] = True
            else:
                link["to"] = target
                link["transition"] = transition(how)
            links.append(link)
    return links


def main():
    guide = (DESIGN / "figma-rehberi.md").read_text(encoding="utf-8")
    links = parse_links(guide)
    pages = []
    for name, folder in PAGES:
        frames = [{"name": f.stem, "svg": f.read_text(encoding="utf-8")}
                  for f in sorted((DESIGN / folder).glob("*.svg"))]
        pages.append({"name": name, "frames": frames})
    names = {f["name"] for f in pages[1]["frames"]}
    for link in links:
        assert link["from"] in names, link
        assert link.get("back") or link["to"] in names, link
    data = {"pages": pages, "links": links, "flows": [{"name": n, "frame": f} for n, f in FLOWS],
            "prototypePage": "Mockups"}

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "manifest.json").write_text(json.dumps({
        "name": "Dolaptan ekranları",
        "id": "dolaptan-ekranlari-dev",
        "api": "1.0.0",
        "main": "code.js",
        "editorType": ["figma"],
        "documentAccess": "dynamic-page",
        "networkAccess": {"allowedDomains": ["none"]},
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (OUT / "code.js").write_text("const DATA = " + json.dumps(data, ensure_ascii=False) + ";\n" + PLUGIN_JS,
                                 encoding="utf-8")
    print(f"ok: {sum(len(p['frames']) for p in pages)} frames, {len(links)} links")


PLUGIN_JS = r"""
const GAP = 80;
const ROW_GAP = 160;

async function run() {
  const report = { frames: 0, links: 0, missing: [], flows: "" };
  const byPage = {};
  let prototypePage = null;

  for (let i = 0; i < DATA.pages.length; i++) {
    const spec = DATA.pages[i];
    let page;
    if (i === 0 && figma.currentPage.children.length === 0) {
      page = figma.currentPage;
    } else {
      page = figma.createPage();
    }
    page.name = spec.name;
    await figma.setCurrentPageAsync(page);
    const frames = {};
    spec.frames.forEach((f, index) => {
      const node = figma.createNodeFromSvg(f.svg);
      node.name = f.name;
      node.x = (index % 10) * (360 + GAP);
      node.y = Math.floor(index / 10) * (800 + ROW_GAP);
      page.appendChild(node);
      frames[f.name] = node;
      report.frames++;
    });
    byPage[spec.name] = frames;
    if (spec.name === DATA.prototypePage) prototypePage = page;
  }

  await figma.setCurrentPageAsync(prototypePage);
  const frames = byPage[DATA.prototypePage];
  for (const link of DATA.links) {
    const frame = frames[link.from];
    const node = link.layer ? frame.findOne(n => n.name === link.layer) : frame;
    if (!node) {
      report.missing.push(link.from + " / " + link.layer);
      continue;
    }
    const action = link.back
      ? { type: "BACK" }
      : { type: "NODE", destinationId: frames[link.to].id, navigation: "NAVIGATE",
          transition: link.transition, preserveScrollPosition: false };
    const trigger = link.delay !== null
      ? { type: "AFTER_TIMEOUT", timeout: link.delay }
      : { type: "ON_CLICK" };
    const existing = node.reactions ? node.reactions.slice() : [];
    await node.setReactionsAsync(existing.concat([{ trigger: trigger, actions: [action] }]));
    report.links++;
  }

  try {
    prototypePage.flowStartingPoints = DATA.flows.map(f => ({ nodeId: frames[f.frame].id, name: f.name }));
    report.flows = "akışlar eklendi";
  } catch (e) {
    report.flows = "akışları elle ekle (rehber, 6. bölüm)";
  }
  figma.viewport.scrollAndZoomIntoView(Object.values(frames));
  return report;
}

run().then(r => {
  let msg = r.frames + " ekran, " + r.links + " bağlantı, " + r.flows;
  if (r.missing.length) msg += ". Bulunamayan katmanlar: " + r.missing.join(", ");
  figma.closePlugin(msg);
}).catch(e => figma.closePlugin("Hata: " + e.message));
"""

if __name__ == "__main__":
    main()
