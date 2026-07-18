from aldrich_tailored_trousers import pts
from utils.paths import generated_file
from render.svg_rendering import render_svg
from utils.rotation import angle_between, rotate_point


def get_rotated_no_dart_flare_front_points():
    angle = angle_between([pts["t0d"], pts["t0a"]], [pts["t0d"], pts["t0b"]])

    point_side_keys = ["t0b", "t11", "t8", "t13", "t4"]
    rotated_points = {
        key: tuple(rotate_point(pts[key], pts["t0d"], -angle))
        for key in point_side_keys
    }

    return rotated_points


def get_no_dart_flare_front_shapes():
    rotated = get_rotated_no_dart_flare_front_points()
    return [
        ("circle", pts["named_points"]),
        ("circle", rotated),
        ("dash", pts["t1"], pts["t9"]),
        ("dash", pts["t0d"], pts["t4"]),
        ("dash", pts["t5"], pts["t7"]),
        ("dash", pts["t5"], pts["t5a"]),
        ("dash", pts["t6"], pts["t25"]),
        ("dash", pts["t15"], rotated["t13"]),
        ("dash", pts["t2"], rotated["t11"]),
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
                rotated["t11"],
                rotated["t8"],
                rotated["t13"],
            ],
            6,
        ),
        (
            "french_curve",
            [
                pts["t9"],
                pts["t15b"],
                pts["t15"],
            ],
            6,
        ),
        (
            "french_curve",
            [
                pts["t10"],
                pts["t0a"],
                rotated["t11"],
            ],
            6,
        ),
        (
            "french_curve",
            [
                rotated["t13"],
                rotated["t4"],
                pts["t4"],
                pts["t15"],
            ],
            6,
        ),
    ]


my_shapes = get_no_dart_flare_front_shapes()
output_file = generated_file("aldrich_tailored_trousers/no_dart_flare_shorts/front.svg")

render_svg(
    my_shapes,
    filename=str(output_file),
    show_dashes=True,
    show_points=True,
    show_numbers=True,
)

print(f"Generated in {output_file}")
