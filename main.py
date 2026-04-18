from math import sqrt

import svgwrite

show_dashes = True
show_points = True

# Measurements in mm
size = 14

bust = 880
bust_ease = 50
bust_to_dart = 25
waist = 700
waist_ease = 30
hip = 1000
nape_to_waist = 410
waist_to_hip = 206
armscye_depth = 210
neck_size = 370
shoulder = 122.5
shoulder_dart = 10
back_width = 344
back_width_ease = 5
dart = 70
chest = 324

front_dart = 45
back_dart = 35
front_side_dart = 15
back_side_dart = 15

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


def reflect_point_across_line(p, a, b):
    dx, dy = [b[0] - a[0], b[1] - a[1]]
    den = dx * dx + dy * dy
    if den == 0:
        return [p[0], p[1]]

    t = ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / den
    q = [a[0] + t * dx, a[1] + t * dy]
    return [2 * q[0] - p[0], 2 * q[1] - p[1]]


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


def build_two_point_curve(start, end, k=0.45, draw_dir="rtl"):
    dx = abs(end[0] - start[0])
    dy = abs(end[1] - start[1])

    c1 = [start[0], start[1] + k * dy] if draw_dir == "rtl" else [start[0], start[1] + k * dy]
    c2 = [end[0] - k * dx, end[1]] if draw_dir == "rtl" else [end[0] + k * dx, end[1]]

    return "curve", start, end, [c1, c2]


def get_base_shapes():
    p0 = (0, 0)
    p1 = (0, 15)
    p2 = (0, p1[1] + (armscye_depth + 5))
    p3 = (p2[0] + (bust / 2) + bust_ease, p2[1])
    p4 = (p3[0], p3[1] - p2[1] - (size_above_14 * 5))
    p5 = (0, p1[1] + nape_to_waist)
    p6 = (p3[0], p5[1])
    p7 = (0, p5[1] + waist_to_hip)
    p8 = (p3[0], p7[1])

    # Back
    p9 = [(neck_size / 5) - 2, 0]
    p10 = [0, p1[1] + (armscye_depth / 5) - 7]
    p11 = [p9[0] + sqrt((shoulder + shoulder_dart) ** 2 - p10[1] ** 2), p10[1]]
    p12 = [(p9[0] + p11[0]) / 2, (p9[1] + p11[1]) / 2]
    p12a = [p12[0], p12[1] + 50]
    p13 = [p12[0] - 10, p12a[1]]
    p14 = [back_width / 2 + back_width_ease, p2[1]]
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
    p26 = [p23[0], p23[1] + bust_to_dart]
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

    d12_11 = sqrt((p11[0] - p12[0]) ** 2 + (p11[1] - p12[1]) ** 2)
    p12_1 = [
        p12[0] + (shoulder_dart / 2) * ((p11[0] - p12[0]) / d12_11),
        p12[1] + (shoulder_dart / 2) * ((p11[1] - p12[1]) / d12_11),
    ]
    p12_2 = reflect_point_across_line(p12_1, p12, p13)

    d_half_bust_with_ease = bust / 2 + bust_ease
    d_half_waist_with_ease = waist / 2 + waist_ease
    d_available_dart_ease = d_half_bust_with_ease - d_half_waist_with_ease
    print(f"Available dart ease: {d_available_dart_ease} mm")
    print(f"Used all dart ease? {front_dart + back_dart + front_side_dart + back_side_dart == d_available_dart_ease}")

    p24_1 = [p24[0] - (front_dart / 2), p24[1]]
    p24_2 = [p24[0] + (front_dart / 2), p24[1]]

    p18_1 = [p18[0] - (back_dart / 2), p18[1]]
    p18_2 = [p18[0] + (back_dart / 2), p18[1]]

    p33_1 = [p33[0] - (front_side_dart / 2), p33[1]]
    p33_2 = [p33[0] + (back_side_dart / 2), p33[1]]

    p35 = [p7[0] + (hip / 4), p7[1]]
    p36 = [p8[0] - (hip / 4), p8[1]]

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
        ("dash", p12, p12a),
        ("dash", p13, p12a),
        ("line", p13, p12_1),
        ("line", p13, p12_2),
        ("line", p12_1, p11),
        ("line", p12_2, p9),
        ("line", p26, p24_1),
        ("line", p26, p24_2),
        ("line", p24_1, p25),
        ("line", p24_2, p25),
        ("line", p17, p18_1),
        ("line", p17, p18_2),
        ("line", p18_1, p19),
        ("line", p18_2, p19),
        ("line", p32, p33_1),
        ("line", p32, p33_2),
        ("line", p33_1, p35),
        ("line", p33_2, p36),

        build_two_point_curve(p20, p21, draw_dir="rtl"),
        build_two_point_curve(p9, p1, draw_dir="ltr"),

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
