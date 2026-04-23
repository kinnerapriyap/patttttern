import math
import os

import svgwrite

from back import get_back_shapes
from front import get_front_shapes
from shape_drawing import draw_shapes
from svg_rendering import get_bounds


def _add_tape_notches(
    dwg,
    x0,
    y0,
    page_w,
    page_h,
    row,
    col,
    rows,
    cols,
    notch_size_mm,
    notch_count,
    notch_inset_mm,
):
    if notch_size_mm <= 0 or notch_count <= 0:
        return

    # Thicker, high-contrast seam marks for easier visual alignment.
    style = {"stroke": "black", "stroke_width": 0.8, "fill": "none"}

    xs = [x0 + page_w * (i + 1) / (notch_count + 1) for i in range(notch_count)]
    ys = [y0 + page_h * (i + 1) / (notch_count + 1) for i in range(notch_count)]

    left = x0
    right = x0 + page_w
    top = y0
    bottom = y0 + page_h

    # Draw notches inset from borders so SVG viewers don't clip edge strokes.
    if col > 0:  # internal seam on left
        for y in ys:
            dwg.add(dwg.line((left + notch_inset_mm, y), (left + notch_inset_mm + notch_size_mm, y), **style))
    if col < cols - 1:  # internal seam on right
        for y in ys:
            dwg.add(dwg.line((right - notch_inset_mm - notch_size_mm, y), (right - notch_inset_mm, y), **style))
    if row > 0:  # internal seam on top
        for x in xs:
            dwg.add(dwg.line((x, top + notch_inset_mm), (x, top + notch_inset_mm + notch_size_mm), **style))
    if row < rows - 1:  # internal seam on bottom
        for x in xs:
            dwg.add(dwg.line((x, bottom - notch_inset_mm - notch_size_mm), (x, bottom - notch_inset_mm), **style))


def _add_page_marks(
    dwg,
    x0,
    y0,
    page_w,
    page_h,
    row,
    col,
    rows,
    cols,
    show_page_labels,
    show_overlap_arrows,
    arrow_size_mm,
):
    if show_page_labels:
        label_style = {"fill": "black", "font_size": "10px"}
        label = f"R{row + 1}C{col + 1}"
        dwg.add(dwg.text(label, insert=(x0 + 4, y0 + 12), **label_style))

    if not show_overlap_arrows or arrow_size_mm <= 0:
        return

    style = {"stroke": "black", "stroke_width": 0.6, "fill": "none"}
    cx = x0 + page_w / 2
    cy = y0 + page_h / 2

    # Tiny seam arrows to indicate adjoining page direction.
    if col > 0:  # seam to left page
        x = x0 + 6
        y = cy
        dwg.add(dwg.line((x + arrow_size_mm, y), (x, y), **style))
        dwg.add(dwg.line((x, y), (x + arrow_size_mm * 0.5, y - arrow_size_mm * 0.4), **style))
        dwg.add(dwg.line((x, y), (x + arrow_size_mm * 0.5, y + arrow_size_mm * 0.4), **style))
    if col < cols - 1:  # seam to right page
        x = x0 + page_w - 6
        y = cy
        dwg.add(dwg.line((x - arrow_size_mm, y), (x, y), **style))
        dwg.add(dwg.line((x, y), (x - arrow_size_mm * 0.5, y - arrow_size_mm * 0.4), **style))
        dwg.add(dwg.line((x, y), (x - arrow_size_mm * 0.5, y + arrow_size_mm * 0.4), **style))
    if row > 0:  # seam to top page
        x = cx
        y = y0 + 6
        dwg.add(dwg.line((x, y + arrow_size_mm), (x, y), **style))
        dwg.add(dwg.line((x, y), (x - arrow_size_mm * 0.4, y + arrow_size_mm * 0.5), **style))
        dwg.add(dwg.line((x, y), (x + arrow_size_mm * 0.4, y + arrow_size_mm * 0.5), **style))
    if row < rows - 1:  # seam to bottom page
        x = cx
        y = y0 + page_h - 6
        dwg.add(dwg.line((x, y - arrow_size_mm), (x, y), **style))
        dwg.add(dwg.line((x, y), (x - arrow_size_mm * 0.4, y - arrow_size_mm * 0.5), **style))
        dwg.add(dwg.line((x, y), (x + arrow_size_mm * 0.4, y - arrow_size_mm * 0.5), **style))


def _add_page_border(
    dwg,
    x0,
    y0,
    page_w,
    page_h,
    show_page_border,
    page_border_color,
    page_border_width_mm,
    page_border_inset_mm,
):
    if not show_page_border:
        return

    inset = max(0, page_border_inset_mm)
    w = max(0, page_w - 2 * inset)
    h = max(0, page_h - 2 * inset)
    style = {
        "stroke": page_border_color,
        "stroke_width": page_border_width_mm,
        "fill": "none",
    }
    dwg.add(dwg.rect(insert=(x0 + inset, y0 + inset), size=(w, h), **style))


def _add_test_square(
    dwg,
    x0,
    y0,
    page_w,
    show_test_square,
    test_square_mm,
):
    if not show_test_square or test_square_mm <= 0:
        return

    # Place in top-right with small inset to avoid overlaps with border clipping.
    inset = 8
    x = x0 + page_w - inset - test_square_mm
    y = y0 + inset

    square_style = {"stroke": "black", "stroke_width": 0.7, "fill": "none"}
    text_style = {"fill": "black", "font_size": "7px"}

    dwg.add(dwg.rect(insert=(x, y), size=(test_square_mm, test_square_mm), **square_style))
    dwg.add(dwg.text(f"{int(test_square_mm)} mm", insert=(x, y - 2), **text_style))


def render_svg_a4_pages(
    shapes,
    base_filename="pattern_a4",
    output_dir=".",
    page_size_mm=(210, 297),
    margin_mm=10,
    overlap_mm=5,
    padding_mm=20,
    show_dashes=True,
    show_points=True,
    show_numbers=True,
    show_notches=True,
    notch_size_mm=8,
    notch_count=3,
    notch_inset_mm=1.5,
    show_page_labels=True,
    show_overlap_arrows=True,
    arrow_size_mm=4,
    show_page_border=True,
    page_border_color="black",
    page_border_width_mm=0.6,
    page_border_inset_mm=0.5,
    show_test_square=True,
    test_square_mm=50,
):
    minx, miny, maxx, maxy = get_bounds(shapes)

    content_minx = minx - padding_mm
    content_miny = miny - padding_mm
    content_w = (maxx - minx) + 2 * padding_mm
    content_h = (maxy - miny) + 2 * padding_mm

    page_w, page_h = page_size_mm
    usable_w = page_w - 2 * margin_mm
    usable_h = page_h - 2 * margin_mm

    if usable_w <= 0 or usable_h <= 0:
        raise ValueError("Margins are too large for the selected page size.")

    step_x = max(1, usable_w - overlap_mm)
    step_y = max(1, usable_h - overlap_mm)

    cols = max(1, math.ceil((content_w - usable_w) / step_x) + 1)
    rows = max(1, math.ceil((content_h - usable_h) / step_y) + 1)

    stem = os.path.splitext(base_filename)[0]
    generated_files = []

    for row in range(rows):
        for col in range(cols):
            tile_x = content_minx + col * step_x
            tile_y = content_miny + row * step_y

            filename = os.path.join(output_dir, f"{stem}_r{row + 1}_c{col + 1}.svg")
            dwg = svgwrite.Drawing(
                filename,
                size=(f"{page_w}mm", f"{page_h}mm"),
                viewBox=f"{tile_x - margin_mm} {tile_y - margin_mm} {page_w} {page_h}",
                profile="full",
            )

            draw_shapes(
                dwg,
                shapes,
                show_dashes=show_dashes,
                show_points=show_points,
                show_numbers=show_numbers,
            )
            if show_notches:
                _add_tape_notches(
                    dwg,
                    tile_x - margin_mm,
                    tile_y - margin_mm,
                    page_w,
                    page_h,
                    row,
                    col,
                    rows,
                    cols,
                    notch_size_mm,
                    notch_count,
                    notch_inset_mm,
                )
            _add_page_marks(
                dwg,
                tile_x - margin_mm,
                tile_y - margin_mm,
                page_w,
                page_h,
                row,
                col,
                rows,
                cols,
                show_page_labels,
                show_overlap_arrows,
                arrow_size_mm,
            )
            _add_page_border(
                dwg,
                tile_x - margin_mm,
                tile_y - margin_mm,
                page_w,
                page_h,
                show_page_border,
                page_border_color,
                page_border_width_mm,
                page_border_inset_mm,
            )
            _add_test_square(
                dwg,
                tile_x - margin_mm,
                tile_y - margin_mm,
                page_w,
                show_test_square,
                test_square_mm,
            )
            dwg.save()
            generated_files.append(filename)

    return generated_files


def render_all_a4_patterns(output_dir=".", **kwargs):
    return {
        "front": render_svg_a4_pages(
            get_front_shapes(),
            base_filename="generated/front_a4",
            output_dir=output_dir,
            **kwargs,
        ),
        "back": render_svg_a4_pages(
            get_back_shapes(),
            base_filename="generated/back_a4",
            output_dir=output_dir,
            **kwargs,
        ),
    }


if __name__ == "__main__":
    results = render_all_a4_patterns(
        output_dir=".",
        show_dashes=True,
        show_points=False,
        show_numbers=False,
        show_notches=True,
        notch_size_mm=8,
        notch_count=3,
        notch_inset_mm=1.5,
        show_page_labels=True,
        show_overlap_arrows=True,
        arrow_size_mm=4,
        show_page_border=True,
        page_border_color="black",
        page_border_width_mm=0.6,
        page_border_inset_mm=0.5,
        show_test_square=True,
        test_square_mm=50,
    )
    print(f"Generated {len(results['front'])} A4 page(s) for front pattern")
    print(f"Generated {len(results['back'])} A4 page(s) for back pattern")
