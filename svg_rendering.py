import svgwrite

from shape_drawing import build_french_curve_path, draw_shapes


def get_bounds(shapes):
    xs, ys = [], []

    for s in shapes:
        if s[0] == "line":
            _, a, b = s
            xs += [a[0], b[0]]
            ys += [a[1], b[1]]

    return min(xs), min(ys), max(xs), max(ys)


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

    draw_shapes(
        dwg,
        shapes,
        show_dashes=show_dashes,
        show_points=show_points,
        show_numbers=show_numbers,
    )

    dwg.save()
