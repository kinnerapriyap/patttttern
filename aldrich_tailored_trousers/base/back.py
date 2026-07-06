from aldrich_tailored_trousers import pts
from utils.paths import generated_file
from render.svg_rendering import render_svg


def get_back_shapes():
    return [
        ("circle", pts["named_points"]),
        ("line", pts["t6"], pts["t25"]),
        ("line", pts["t21"], pts["t22"]),
        ("line", pts["t30a"], pts["t30d"]),
        ("line", pts["t30b"], pts["t30d"]),
        ("line", pts["t31a"], pts["t31d"]),
        ("line", pts["t31b"], pts["t31d"]),
        ("line", pts["t29"], pts["t27"]),
        ("dash", pts["t1"], pts["t23"]),
        ("dash", pts["t2"], pts["t3"]),
        ("dash", pts["t16"], pts["t18"]),
        (
            "french_curve",
            [
                pts["t21"],
                pts["t19"],
                pts["t16a"],
                pts["t24"],
            ],
            6,
        ),
        (
            "french_curve",
            [
                pts["t22"],
                pts["t25"],
                pts["t27"],
                pts["t26"],
            ],
            6,
        ),
        (
            "french_curve",
            [
                pts["t24"],
                pts["t29b"],
                pts["t29"],
                pts["t28"],
            ],
            6,
        ),
        (
            "french_curve",
            [
                pts["t26"],
                pts["t3a"],
                pts["t28"],
            ],
            6,
        ),
    ]


my_shapes = get_back_shapes()
output_file = generated_file("aldrich_tailored_trousers/base/back.svg")

render_svg(
    my_shapes,
    filename=str(output_file),
    show_dashes=False,
    show_points=False,
    show_numbers=False,
)

print(f"Generated in {output_file}")
