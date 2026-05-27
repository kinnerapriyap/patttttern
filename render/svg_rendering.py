import svgwrite
from pathlib import Path

from utils.shape_drawing import draw_shapes


def get_bounds(shapes):
    xs, ys = [], []

    for s in shapes:
        if s[0] in ("line", "dash"):
            _, a, b = s
            xs += [a[0], b[0]]
            ys += [a[1], b[1]]
        elif s[0] == "polyline":
            _, pts = s
            for p in pts:
                xs.append(p[0])
                ys.append(p[1])

    return min(xs), min(ys), max(xs), max(ys)


def render_svg(
        shapes,
        filename,
        show_dashes,
        show_points,
        show_numbers,
        show_control_square,
):
    Path(filename).parent.mkdir(parents=True, exist_ok=True)

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

    if show_control_square:
        square_size = 50
        square_x = minx - padding + 5
        square_y = miny - padding + 5
        square_style = {"stroke": "pink", "stroke_width": 1, "fill": "none"}
        dwg.add(
            dwg.rect(
                insert=(square_x, square_y),
                size=(square_size, square_size),
                **square_style,
            )
        )

    dwg.save()
