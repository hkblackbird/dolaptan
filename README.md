# Dolaptan

Dolaptan is a Flutter mobile app for students who share a home and small households in Türkiye. It is a shared kitchen: everyone in the home sees one pantry, adds food by photo, gets Turkish recipes that use what is about to go off, and shares one shopping list. Cooking and shopping keep the pantry up to date.

MTM4681 Mobile Programming, Fall 2026. Milestone submission.

## Team

- Team number: [TAKIM NO]
- Members: Hatice Karakuş, Muhammed Ali Demirsoy

## Figma

- Wireframes: https://www.figma.com/design/ks28fOM7jsorGfZoWvIGpD/Dolaptan?node-id=0-1
- Mockups: https://www.figma.com/design/ks28fOM7jsorGfZoWvIGpD/Dolaptan?node-id=5-1061
- Mockups, dark mode: https://www.figma.com/design/ks28fOM7jsorGfZoWvIGpD/Dolaptan?node-id=5-2141
- Prototype: https://www.figma.com/proto/ks28fOM7jsorGfZoWvIGpD/Dolaptan?node-id=19-362&starting-point-node-id=19%3A362

## Files

| Path | Content |
|---|---|
| `docs/design-justification.pdf` | Color palette, typography, layout, accessibility, WCAG contrast values |
| `docs/user-flow.pdf` | Main user path, decision points, and screens |
| `docs/architecture-protocols.pdf` | MVVM, screen map, data model, Dart interfaces, protocols |
| `docs/project-overview.pdf` | Problem, evidence, competitors, features, weekly plan, risks |
| `design/wireframes/` | 20 SVG wireframes, 360x800 |
| `design/mockups/` | 20 SVG mockups, light mode, 360x800 |
| `design/mockups-dark/` | 20 SVG mockups, dark mode, 360x800 |
| `design/figma-rehberi.md` | Figma import and prototype guide (Turkish) |
| `design/figma-eklentisi/` | Figma development plugin that imports all screens and adds prototype links |
| `tools/build_screens.py` | Generates the SVG screens |
| `tools/build_docs.py` | Generates the PDFs |
| `tools/build_figma_plugin.py` | Generates the Figma plugin from the SVGs and the guide |
| `tools/fonts/` | Inter, Caveat and Patrick Hand font files and licenses (SIL OFL) |
| `design/cizimler/` | Gouache illustrations (Figma AI generated sheets in `setler/`, cut-outs in `web/`) |
| `app/` | Flutter app (MVVM + Provider, go_router, Hive). Works offline with an on-device Turkish recipe catalog; Firebase and AI come next |

Each folder has the 10 main screens, 3 extra states (expiry notification, edit item sheet, Cooked confirmation), 2 Scan states for the animation, and 5 empty, error and loading states. The visual language is a hand-written recipe notebook (cream paper, Caveat and Patrick Hand fonts, gouache food illustrations) on top of standard iOS patterns.

## Rebuild

```sh
pip install reportlab fonttools pillow
python tools/build_screens.py
python tools/build_docs.py
python tools/build_figma_plugin.py
```

`build_docs.py` uses the macOS Menlo font for code blocks.
