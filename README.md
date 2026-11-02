# Dolaptan

Dolaptan is a Flutter mobile app for students and small households in Türkiye. Users photograph their fridge or cupboard, AI detects the ingredients, users correct the list, choose time and servings, and the app suggests 3 Turkish recipes.

MTM4681 Mobile Programming, Fall 2026. Milestone submission.

## Team

- Team number: [TAKIM NO]
- Members: [AD SOYAD 1], [AD SOYAD 2]

## Figma

- Wireframes: [FIGMA WIREFRAME LİNKİ]
- Mockups: [FIGMA MOCKUP LİNKİ]
- Prototype: [FIGMA PROTOTİP LİNKİ]

## Files

| Path | Content |
|---|---|
| `docs/design-justification.pdf` | Color palette, typography, layout, accessibility, WCAG contrast values |
| `docs/user-flow.pdf` | Main user path, decision points, and screens |
| `docs/architecture-protocols.pdf` | MVVM, screen map, data model, Dart interfaces, protocols |
| `docs/project-overview.pdf` | Problem, evidence, competitors, features, weekly plan, risks |
| `design/wireframes/` | 17 SVG wireframes, 360x800 |
| `design/mockups/` | 17 SVG mockups, light mode, 360x800 |
| `design/mockups-dark/` | 17 SVG mockups, dark mode, 360x800 |
| `design/figma-rehberi.md` | Figma import and prototype guide (Turkish) |
| `design/figma-eklentisi/` | Figma development plugin that imports all screens and adds prototype links |
| `tools/build_screens.py` | Generates the SVG screens |
| `tools/build_docs.py` | Generates the PDFs |
| `tools/build_figma_plugin.py` | Generates the Figma plugin from the SVGs and the guide |
| `tools/fonts/` | Inter font files and license |

Each folder has the 10 app screens, 2 Scan states for the animation (`03b`, `03c`), and 5 empty, error and loading states (`04b`, `06b`, `06c`, `08b`, `09b`). The visual language follows Apple's iOS 26 guidelines.

## Rebuild

```sh
pip install reportlab fonttools
python tools/build_screens.py
python tools/build_docs.py
python tools/build_figma_plugin.py
```

`build_docs.py` uses the macOS Menlo font for code blocks.
