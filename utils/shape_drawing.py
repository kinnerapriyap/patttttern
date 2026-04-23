def _curve_controls(start, end, k):
    dx = abs(end[0] - start[0])
    dy = abs(end[1] - start[1])
    c1 = [start[0], start[1] + k * dy]
    c2 = [end[0] - k * dx, end[1]] if end[0] >= start[0] else [end[0] + k * dx, end[1]]
    return c1, c2


def build_french_curve_path(points, k):
    pts = [tuple(p) for p in points]
    if len(pts) < 2:
        return ""

    path = [f"M {pts[0][0]},{pts[0][1]}"]
    for i in range(len(pts) - 1):
        p0 = pts[i - 1] if i > 0 else pts[i]
        p1 = pts[i]
        p2 = pts[i + 1]
        p3 = pts[i + 2] if i + 2 < len(pts) else pts[i + 1]

        c1 = (p1[0] + (p2[0] - p0[0]) / k, p1[1] + (p2[1] - p0[1]) / k)
        c2 = (p2[0] - (p3[0] - p1[0]) / k, p2[1] - (p3[1] - p1[1]) / k)
        path.append(f"C {c1[0]},{c1[1]} {c2[0]},{c2[1]} {p2[0]},{p2[1]}")

    return " ".join(path)


def draw_shapes(
    dwg,
    shapes,
    show_dashes=True,
    show_points=True,
    show_numbers=True,
    style=None,
    dash_style=None,
    text_style=None,
):
    style = style or {"stroke": "pink", "stroke_width": 1, "fill": "none"}
    dash_style = dash_style or {"stroke": "pink", "stroke_width": 0.5, "fill": "none", "stroke_dasharray": "5,5"}
    text_style = text_style or {"fill": "purple", "font_size": "8px"}

    for shape in shapes:
        kind = shape[0]

        if kind == "line":
            _, a, b = shape
            dwg.add(dwg.line(a, b, **style))

        elif kind == "dash" and show_dashes:
            _, a, b = shape
            dwg.add(dwg.line(a, b, **dash_style))

        elif kind == "polyline":
            _, pts = shape
            dwg.add(dwg.polyline(pts, **style))

        elif kind == "curve":
            _, start, end, k = shape
            c1, c2 = _curve_controls(start, end, k)
            d = f"M {start[0]},{start[1]} C {c1[0]},{c1[1]} {c2[0]},{c2[1]} {end[0]},{end[1]}"
            dwg.add(dwg.path(d=d, **style))

        elif kind == "french_curve":
            _, pts, k = shape
            d = build_french_curve_path(pts, k)
            if d:
                dwg.add(dwg.path(d=d, **style))

        elif kind == "circle" and show_points:
            _, named_pts = shape
            for name, p in named_pts.items():
                dwg.add(dwg.circle(center=p, r=1, **style))
                if show_numbers:
                    dwg.add(dwg.text(name, insert=[p[0] + 2, p[1] + 2], **text_style))


