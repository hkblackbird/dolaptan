"""Flat, top-down dish illustrations for the recipe image slots.

Each dish is drawn in a 100x100 box centred on (0, 0); the plate or pan has a radius of about 42.
The app ships a small fixed set like this, one per dish category, so AI-generated recipes always
get a consistent drawing instead of a photo.
"""

import math

# light-mode tile tint behind each dish; dark mode uses the theme's photo colour
TINT = {
    "menemen": "#FBE4DA", "cacik": "#E3EFDC", "omlet": "#FBEFD2",
    "mercimek": "#FBE5D3", "fasulye": "#E5EFDA",
}

NAME_TO_DISH = {
    "Menemen": "menemen", "Cacık": "cacik", "Patatesli Omlet": "omlet",
    "Mercimek Çorbası": "mercimek", "Zeytinyağlı Fasulye": "fasulye",
}


def _shadow(r=42):
    return f'<circle cx="1.5" cy="3.5" r="{r}" fill="#000000" fill-opacity="0.10"/>'


def _pan():
    return (_shadow() + '<circle r="42" fill="#3B4045"/><circle r="38" fill="#2A2E32"/>'
            '<path d="M-30 -22 A37 37 0 0 1 -8 -36" fill="none" stroke="#FFFFFF" stroke-opacity="0.18" '
            'stroke-width="2" stroke-linecap="round"/>')


def _bowl(inner="#F1ECE4"):
    return (_shadow() + '<circle r="42" fill="#FFFFFF"/>'
            '<circle r="42" fill="none" stroke="#E4DACD" stroke-width="1.2"/>'
            f'<circle r="34" fill="{inner}"/>')


def _leaf(x, y, angle, size=1.0, color="#3E8E41"):
    return (f'<ellipse cx="{x}" cy="{y}" rx="{5 * size:.1f}" ry="{2.4 * size:.1f}" fill="{color}" '
            f'transform="rotate({angle} {x} {y})"/>')


def _dots(points, color, r=1.3):
    return "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}"/>' for x, y in points)


def _cube(x, y, s, fill, stroke, angle=0):
    return (f'<rect x="{x - s / 2}" y="{y - s / 2}" width="{s}" height="{s}" rx="{s * 0.22:.1f}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="0.8" transform="rotate({angle} {x} {y})"/>')


def menemen():
    out = [_pan(), '<circle r="34" fill="#D2442A"/>',
           '<circle cx="-14" cy="12" r="9" fill="#E05A38"/><circle cx="16" cy="-14" r="8" fill="#E05A38"/>']
    for x, y, a in [(-20, -6, 20), (8, 20, -30), (22, 6, 60), (-4, -22, 80), (-24, 14, -10)]:
        out.append(f'<rect x="{x - 3}" y="{y - 2.5}" width="7" height="5" rx="1.5" fill="#A92E1A" '
                   f'transform="rotate({a} {x} {y})"/>')
    for cx, cy, rot in [(-8, -6, 0), (12, 10, 40)]:
        out.append(f'<g transform="translate({cx} {cy}) rotate({rot})">'
                   '<path d="M-12 -3 Q-10 -12 0 -11 Q11 -10 11 -1 Q12 9 1 10 Q-11 11 -12 -3 Z" fill="#FFF4DE"/>'
                   '<circle cx="-1" cy="0" r="5" fill="#F5B21B"/><circle cx="-2.5" cy="-1.5" r="1.5" '
                   'fill="#FFFFFF" fill-opacity="0.7"/></g>')
    for x, y, a in [(-22, 2, 35), (2, 24, -20), (24, -6, 75), (-6, -26, -40)]:
        out.append(f'<rect x="{x - 6}" y="{y - 2}" width="12" height="4" rx="2" fill="#4F9A2E" '
                   f'transform="rotate({a} {x} {y})"/>')
    out.append(_dots([(-16, -16), (4, -18), (20, 18), (-18, 24), (26, 10), (-28, -4), (6, 2)], "#2F7D32"))
    return "".join(out)


def cacik():
    out = [_bowl("#F6F3EC"), '<circle r="31" fill="#FBFAF6"/>',
           '<path d="M-18 -12 Q-4 -22 10 -14" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round"/>']
    for x, y, a in [(-14, 4, 10), (-4, 14, -15), (10, 8, 25), (16, -6, -10), (2, -10, 40),
                    (-18, -8, 30), (-6, 24, 5), (20, 16, -30), (4, 0, 15)]:
        out.append(_cube(x, y, 6, "#9CCB5A", "#4E8A2B", a))
    out.append('<path d="M-20 18 Q-8 4 6 14 Q18 22 24 6" fill="none" stroke="#C9A82A" stroke-opacity="0.85" '
               'stroke-width="1.8" stroke-linecap="round"/>')
    out += [_leaf(-2, -22, 30), _leaf(6, -24, -20), _leaf(22, -16, 60, 0.9)]
    out.append(_dots([(-10, 20), (14, -18), (-24, -2), (12, 24)], "#B8352A", 1.0))
    return "".join(out)


def omlet():
    out = [_pan(), '<circle r="34" fill="#F2C24E"/>',
           '<path d="M-26 -8 Q-20 -24 -4 -26 Q-14 -14 -26 -8 Z" fill="#E3A23A"/>',
           '<circle cx="18" cy="16" r="7" fill="#E7AC40"/><circle cx="-16" cy="20" r="5" fill="#E7AC40"/>']
    for x, y, a in [(-12, -6, 10), (6, -14, -20), (14, 2, 30), (-2, 10, 5), (-20, 8, -25),
                    (4, 22, 15), (22, -12, 40), (-6, -22, -10)]:
        out.append(_cube(x, y, 7, "#FBE2A0", "#D49B3A", a))
    out.append(_dots([(-4, 0), (10, 12), (-14, 14)], "#FFF8E6", 2.2))
    out += [_leaf(0, -4, 20, 0.7, "#3E8E41"), _leaf(16, 18, -40, 0.7, "#3E8E41"), _leaf(-18, -16, 60, 0.7, "#3E8E41")]
    out.append(_dots([(8, -4), (-10, 22), (20, 6), (-24, 0), (2, 16)], "#2F7D32", 1.1))
    return "".join(out)


def mercimek():
    out = [_bowl("#F1ECE4"), '<circle r="31" fill="#E8843A"/>',
           '<path d="M-20 -6 Q-12 -22 6 -20" fill="none" stroke="#F2A55E" stroke-width="5" stroke-linecap="round"/>',
           '<path d="M-14 8 Q-2 -4 10 6 Q18 14 8 20 Q-2 24 -8 16" fill="none" stroke="#B8321E" '
           'stroke-width="2.2" stroke-linecap="round"/>']
    out.append(_dots([(-6, -8), (4, -2), (14, -10), (-16, 14), (16, 12), (0, 12), (-20, 2)], "#9A2A18", 1.0))
    out.append(_dots([(-10, -14), (10, -16), (20, 0), (-4, 22)], "#4E7D3A", 1.1))
    # lemon wedge on the rim
    out.append('<g transform="translate(29 -27) rotate(40)">'
               '<path d="M-11 0 A11 11 0 0 0 11 0 Z" fill="#F7D84A" stroke="#E2B92A" stroke-width="1"/>'
               '<path d="M0 0 L-7 6 M0 0 L0 9 M0 0 L7 6" stroke="#FFF6C8" stroke-width="1.2"/></g>')
    return "".join(out)


def fasulye():
    out = [_shadow(44), '<circle r="44" fill="#FFFFFF"/>',
           '<circle r="44" fill="none" stroke="#E4DACD" stroke-width="1.2"/>',
           '<circle r="35" fill="none" stroke="#F1ECE4" stroke-width="1.5"/>',
           '<path d="M-26 -4 Q-22 -26 2 -28 Q26 -26 28 -2 Q30 22 4 28 Q-24 30 -26 -4 Z" fill="#E8956A" fill-opacity="0.75"/>']
    beans = [(-18, -10, 25), (-6, -16, -15), (8, -12, 35), (18, -2, -40), (-14, 4, -30), (0, 0, 15),
             (12, 12, 50), (-6, 16, -5), (-20, 16, 40), (6, 24, -25), (20, 18, 10)]
    for x, y, a in beans:
        rad = math.radians(a)
        dx, dy = 11 * math.cos(rad), 11 * math.sin(rad)
        out.append(f'<path d="M{x - dx:.1f} {y - dy:.1f} L{x + dx:.1f} {y + dy:.1f}" stroke="#4E9230" '
                   f'stroke-width="5" stroke-linecap="round"/>'
                   f'<path d="M{x - dx * 0.7:.1f} {y - dy * 0.7 - 0.8:.1f} L{x + dx * 0.7:.1f} {y + dy * 0.7 - 0.8:.1f}" '
                   f'stroke="#7DBE4E" stroke-width="1.3" stroke-linecap="round"/>')
    for x, y in [(-10, -4), (14, 4), (-2, 22), (4, -22), (-22, 6)]:
        out.append(f'<circle cx="{x}" cy="{y}" r="2.6" fill="#C73E24"/>')
    out.append('<path d="M-12 -24 Q-6 -20 -2 -24 M16 22 Q20 16 24 18" fill="none" stroke="#F5E9D6" '
               'stroke-width="1.8" stroke-linecap="round"/>')
    return "".join(out)


DRAW = {"menemen": menemen, "cacik": cacik, "omlet": omlet, "mercimek": mercimek, "fasulye": fasulye}


def hero_garnish(dish):
    """A few ingredients scattered around the dish on the 16:9 recipe header (coordinates in px)."""
    if dish != "omlet":
        return ""
    potato = ('<ellipse cx="0" cy="0" rx="17" ry="12" fill="#D6A464"/>'
              '<circle cx="-6" cy="-3" r="1.3" fill="#A97A3E"/><circle cx="5" cy="3" r="1.3" fill="#A97A3E"/>'
              '<circle cx="8" cy="-4" r="1" fill="#A97A3E"/>')
    egg = ('<ellipse cx="1.5" cy="2.5" rx="11" ry="14" fill="#000000" fill-opacity="0.08"/>'
           '<ellipse cx="0" cy="0" rx="11" ry="14" fill="#FFF9F0"/>'
           '<ellipse cx="-4" cy="-5" rx="3" ry="4" fill="#FFFFFF"/>')
    return (f'<g transform="translate(64 150) rotate(-15)">{potato}</g>'
            f'<g transform="translate(40 118) rotate(20) scale(0.8)">{potato}</g>'
            f'<g transform="translate(294 148) rotate(25)">{egg}</g>'
            f'<g transform="translate(318 120) rotate(-10) scale(0.85)">{egg}</g>'
            + _leaf(92, 176, 30, 1.2) + _leaf(100, 172, -20, 1.2) + _leaf(270, 178, 50, 1.2)
            + _leaf(84, 110, -40, 1.0))


def dish_svg(dish, cx, cy, scale):
    return (f'<g id="cizim-{dish}" transform="translate({cx} {cy}) scale({scale:.3f})">'
            + DRAW[dish]() + "</g>")
