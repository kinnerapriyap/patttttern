from math import sqrt

import svgwrite

show_dashes = True
show_points = True

# Measurements in mm
size = 14

bust = 880
nape_to_waist = 410
waist_to_hip = 206
armscye_depth = 210
neck_size = 370
shoulder = 122.5
back_width = 344
dart = 70
chest = 324
size_above_14 = max(size - 14, 0)
distance_from_p14 = 22.5 if 6 <= size <= 8 \
    else 25 if 10 <= size <= 14 \
    else 30 if 16 <= size <= 20 \
    else 35 if 22 <= size <= 26 \
    else 30
distance_from_p22 = 17.5 if 6 <= size <= 8 \
    else 20 if 10 <= size <= 14 \
    else 25 if 16 <= size <= 20 \
    else 30 if 22 <= size <= 26 \
    else 25


def build_french_curve_path(points):
    pts = [tuple(p) for p in points]
    if len(pts) < 2:
        return ""

    path = [f"M {pts[0][0]},{pts[0][1]}"]
    for i in range(len(pts) - 1):
        p0 = pts[i - 1] if i > 0 else pts[i]
        p1 = pts[i]
        p2 = pts[i + 1]
        p3 = pts[i + 2] if i + 2 < len(pts) else pts[i + 1]

        c1 = (p1[0] + (p2[0] - p0[0]) / 6.0, p1[1] + (p2[1] - p0[1]) / 6.0)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6.0, p2[1] - (p3[1] - p1[1]) / 6.0)
        path.append(f"C {c1[0]},{c1[1]} {c2[0]},{c2[1]} {p2[0]},{p2[1]}")

    return " ".join(path)


def get_base_shapes():
    p0 = (0, 0)
    p1 = (0, 15)
    p2 = (0, p1[1] + (armscye_depth + 5))
    p3 = (p2[0] + (bust / 2) + 50, p2[1])
    p4 = (p3[0], p3[1] - p2[1] - (size_above_14 * 5))
    p5 = (0, p1[1] + nape_to_waist)
    p6 = (p3[0], p5[1])
    p7 = (0, p5[1] + waist_to_hip)
    p8 = (p3[0], p7[1])

    # Back
    p9 = [(neck_size / 5) - 2, 0]
    p10 = [0, p1[1] + (armscye_depth / 5) - 7]
    p11 = [p9[0] + sqrt((shoulder + 10) ** 2 - p10[1] ** 2), p10[1]]
    p12 = [(p9[0] + p11[0]) / 2, (p9[1] + p11[1]) / 2]
    # p13 = neck dart back
    p14 = [back_width / 2 + 5, p2[1]]
    p15 = [p14[0], p10[1]]
    p16 = [(p14[0] + p15[0]) / 2, (p14[1] + p15[1]) / 2]
    p17 = [(p2[0] + p14[0]) / 2, (p2[1] + p14[1]) / 2]
    p18 = [p17[0], p5[1]]
    p19 = [p17[0], p7[1]]

    # Front
    p20 = [p4[0] - (neck_size / 5 - 7), p4[1]]
    p21 = [p4[0], p4[1] + neck_size / 5 - 2]
    p22 = [p3[0] - (chest / 2 + dart / 2), p3[1]]
    p23 = [(p3[0] + p22[0]) / 2, (p3[1] + p22[1]) / 2]
    p24 = [p23[0], p6[1]]
    p25 = [p23[0], p8[1]]
    p26 = [p23[0], p23[1] + 25]
    p27 = [p20[0] - dart, p20[1]]
    p28 = [p11[0], p11[1] + 15]
    p29 = [p28[0] + 100, p28[1]]
    p30 = [p27[0] - sqrt(shoulder ** 2 - (p29[1] - p27[1]) ** 2), p29[1]]
    p31 = [p22[0], p22[1] - ((p3[1] - p21[1]) / 3)]
    p32 = [(p14[0] + p22[0]) / 2, (p14[1] + p22[1]) / 2]
    p33 = [p32[0], p5[1]]
    p34 = [p32[0], p7[1]]

    p14a = [p14[0] + (distance_from_p14 / sqrt(2)), p14[1] - (distance_from_p14 / sqrt(2))]
    p22a = [p22[0] - (distance_from_p22 / sqrt(2)), p22[1] - (distance_from_p22 / sqrt(2))]

    named_points = {
        name[1:]: tuple(value)
        for name, value in locals().items()
        if name.startswith("p")
    }

    return [
        ("circle", named_points),
        ("dash", p0, p1),
        ("line", p1, p7),
        ("dash", p2, p3),
        ("dash", p4, p21),
        ("line", p21, p8),
        ("dash", p5, p6),
        ("line", p7, p8),
        ("dash", p0, p9),
        ("dash", p10, p11),
        ("line", p9, p11),
        ("dash", p14, p15),
        ("dash", p17, p19),
        ("dash", p4, p27),
        ("dash", p23, p25),
        ("line", p20, p26),
        ("line", p27, p26),
        ("dash", p11, p28),
        ("dash", p28, p29),
        ("line", p27, p30),
        ("dash", p22, p31),
        ("dash", p32, p34),
        ("dash", p14, p14a),
        ("dash", p22, p22a),
        ("curve", p20, p21, [[p20[0], p21[1]]]),
        ("curve", p1, p9, [[p9[0], p1[1]]]),
        ("french_curve", [p11, p16, p14a, p32, p22a, p31, p30]),
    ]


def get_bounds(shapes):
    xs, ys = [], []

    for s in shapes:
        if s[0] == "line":
            _, a, b = s
            xs += [a[0], b[0]]
            ys += [a[1], b[1]]

    return min(xs), min(ys), max(xs), max(ys)


def render_svg(shapes, filename="pattern.svg"):
    minx, miny, maxx, maxy = get_bounds(shapes)

    padding = 20
    width = maxx - minx + padding * 2
    height = maxy - miny + padding * 2

    dwg = svgwrite.Drawing(
        filename,
        size=(f"{width}mm", f"{height}mm"),
        viewBox=f"{minx - padding} {miny - padding} {width} {height}",
        profile="full",
    )

    style = {"stroke": "pink", "stroke_width": 1, "fill": "none"}
    dash_style = {"stroke": "pink", "stroke_width": 0.5, "fill": "none", "stroke_dasharray": "5,5"}
    text_style = {"fill": "purple", "font_size": "8px"}

    for s in shapes:
        if s[0] == "line":
            _, a, b = s
            dwg.add(dwg.line(a, b, **style))

        elif s[0] == "dash" and show_dashes:
            _, a, b = s
            dwg.add(dwg.line(a, b, **dash_style))

        elif s[0] == "polyline":
            _, pts = s
            dwg.add(dwg.polyline(pts, **style))

        elif s[0] == "curve":
            _, start, end, controls = s
            if len(controls) == 1:
                c1 = controls[0]
                d = f"M {start[0]},{start[1]} Q {c1[0]},{c1[1]} {end[0]},{end[1]}"
                dwg.add(dwg.path(d=d, **style))
            elif len(controls) == 2:
                c1, c2 = controls
                d = f"M {start[0]},{start[1]} C {c1[0]},{c1[1]} {c2[0]},{c2[1]} {end[0]},{end[1]}"
                dwg.add(dwg.path(d=d, **style))

        elif s[0] == "french_curve":
            _, pts = s
            d = build_french_curve_path(pts)
            if d:
                dwg.add(dwg.path(d=d, **style))

        elif s[0] == "circle" and show_points:
            _, named_pts = s
            for name, p in named_pts.items():
                dwg.add(dwg.circle(center=p, r=1, **style))
                dwg.add(dwg.text(name, insert=[p[0] + 2, p[1] + 2], **text_style))

    dwg.save()


my_shapes = get_base_shapes()
render_svg(my_shapes)

print("Generated in pattern.svg")
