from aldrich_tailored_skirt import pts
from render.svg_rendering import render_svg
from utils.paths import generated_file


def get_front_shapes():
    return [
        ("circle", pts["named_points"]),
        ("line", pts["s8"], pts["s4"]),
        ("line", pts["s2"], pts["s4"]),
        ("line", pts["s7"], pts["s6"]),
        ("line", pts["s7"], pts["s8"]),
        ("line", pts["s17a"], pts["s18"]),
        ("line", pts["s17b"], pts["s18"]),
        ("dash", pts["s2"], pts["s16"]),
        ("dash", pts["s17"], pts["s18"]),
        ("dash", pts["s16"], pts["s7"]),
        (
            "french_curve",
            [pts["s16"], pts["s16b"], pts["s7"]],
            6,
        ),
        ("curve", pts["s17b"], pts["s2"], 0.45),
        ("curve", pts["s16"], pts["s17a"], 0.45),
    ]


if __name__ == "__main__":
    my_shapes = get_front_shapes()
    output_file = generated_file("aldrich_tailored_skirt/base/front.svg")
    render_svg(
        my_shapes,
        filename=str(output_file),
        show_dashes=True,
        show_points=True,
        show_numbers=True,
    )
    print(f"Generated in {output_file}")
