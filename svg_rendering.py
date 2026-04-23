import svgwrite


def get_bounds(shapes):
    xs, ys = [], []

    for s in shapes:
        if s[0] == "line":
            _, a, b = s
            xs += [a[0], b[0]]
            ys += [a[1], b[1]]

    return min(xs), min(ys), max(xs), max(ys)


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


def render_svg(
        shapes,
        filename="generated/pattern.svg",
        show_dashes=True,
        show_points=True,
        show_numbers=True,
):
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
            _, start, end, k = s
            dx = abs(end[0] - start[0])
            dy = abs(end[1] - start[1])
            c1 = [start[0], start[1] + k * dy]
            c2 = [end[0] - k * dx, end[1]] if end[0] >= start[0] else [end[0] + k * dx, end[1]]
            d = f"M {start[0]},{start[1]} C {c1[0]},{c1[1]} {c2[0]},{c2[1]} {end[0]},{end[1]}"
            dwg.add(dwg.path(d=d, **style))

        elif s[0] == "french_curve":
            _, pts, k = s
            d = build_french_curve_path(pts, k)
            if d:
                dwg.add(dwg.path(d=d, **style))

        elif s[0] == "circle" and show_points:
            _, named_pts = s
            for name, p in named_pts.items():
                dwg.add(dwg.circle(center=p, r=1, **style))
                dwg.add(dwg.text(name, insert=[p[0] + 2, p[1] + 2], **text_style)) if show_numbers else None

    dwg.save()
