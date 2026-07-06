from aldrich_tailored_trousers import pts
from utils.paths import generated_file
from render.svg_rendering import render_svg


def get_front_shapes():
    return [
        ("circle", pts["named_points"]),
        ("line", pts["t6"], pts["t25"]),
        ("line", pts["t10"], pts["t11"]),
        ("line", pts["t0a"], pts["t0d"]),
        ("line", pts["t0b"], pts["t0d"]),
        ("line", pts["t12"], pts["t14"]),
        ("line", pts["t13"], pts["t15"]),
        ("dash", pts["t1"], pts["t9"]),
        ("dash", pts["t0d"], pts["t3"]),
        ("dash", pts["t5"], pts["t7"]),
        ("dash", pts["t5"], pts["t5a"]),
        (
            "french_curve",
            [
                pts["t10"],
                pts["t6"],
                pts["t5a"],
                pts["t9"],
            ],
            6,
        ),
        (
            "french_curve",
            [
                pts["t11"],
                pts["t8"],
                pts["t13"],
                pts["t12"],
            ],
            6,
        ),
        (
            "french_curve",
            [
                pts["t9"],
                pts["t15b"],
                pts["t15"],
                pts["t14"],
            ],
            6,
        ),
    ]


my_shapes = get_front_shapes()
output_file = generated_file("aldrich_tailored_trousers/base/front.svg")

render_svg(
    my_shapes,
    filename=str(output_file),
    show_dashes=False,
    show_points=False,
    show_numbers=False,
)

print(f"Generated in {output_file}")
