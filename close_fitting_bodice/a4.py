from close_fitting_bodice.back import get_back_shapes
from close_fitting_bodice.front import get_front_shapes
from render.a4_rendering import render_svg_a4_pages


def render_all_a4_patterns(output_dir=".", **kwargs):
    return {
        "front": render_svg_a4_pages(
            get_front_shapes(),
            base_filename="front_a4",
            output_dir=output_dir,
            **kwargs,
        ),
        "back": render_svg_a4_pages(
            get_back_shapes(),
            base_filename="back_a4",
            output_dir=output_dir,
            **kwargs,
        ),
    }


if __name__ == "__main__":
    results = render_all_a4_patterns(
        output_dir="../generated/",
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
