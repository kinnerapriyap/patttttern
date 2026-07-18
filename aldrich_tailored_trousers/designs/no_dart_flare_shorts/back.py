from aldrich_tailored_trousers import pts
from aldrich_tailored_trousers.base.back import get_back_shapes
from utils.geometry import get_perpendicular_intersection_with_line
from utils.paths import generated_file
from render.svg_rendering import render_svg
from utils.rotation import angle_between, rotate_point


def get_rotated_no_dart_flare_front_points():
    tr1 = get_perpendicular_intersection_with_line(
        point=pts["t30d"], line1=pts["t29"], line2=pts["t27"]
    )
    tr2 = get_perpendicular_intersection_with_line(
        point=pts["t31d"], line1=pts["t29"], line2=pts["t27"]
    )
    source_points = pts | {"tr1": tr1, "tr2": tr2}

    angle = angle_between([pts["t30d"], pts["t30a"]], [pts["t30d"], pts["t30b"]])
    point_side_keys = [
        "t30d",
        "t30a",
        "t31a",
        "t31b",
        "t31d",
        "t22",
        "t25",
        "t27",
        "tr1",
        "tr2",
    ]
    rotated_points = {
        key: tuple(rotate_point(source_points[key], pts["t30d"], -angle))
        for key in point_side_keys
    }

    rotated_points["tr1_1"] = tr1
    rotated_points["tr2_1"] = tr2
    rotated_points["tr2_2"] = rotated_points["tr2"]

    angle2 = angle_between(
        [rotated_points["t31d"], rotated_points["t31a"]],
        [rotated_points["t31d"], rotated_points["t31b"]],
    )
    for key in ["t31a", "t22", "t25", "t27", "tr2"]:
        rotated_points[key] = tuple(
            rotate_point(rotated_points[key], pts["t31d"], -angle2)
        )

    return rotated_points


def get_no_dart_flare_back_shapes():
    rotated = get_rotated_no_dart_flare_front_points()
    return [
        ("circle", pts["named_points"]),
        ("circle", rotated),
        ("dash", pts["t6"], pts["t25"]),
        ("dash", pts["t29"], pts["t27"]),
        ("dash", pts["t1"], pts["t23"]),
        ("dash", pts["t2"], pts["t4"]),
        ("dash", pts["t16"], pts["t18"]),
        ("dash", pts["t30d"], rotated["tr1"]),
        ("dash", pts["t31d"], rotated["tr2"]),
        ("dash", rotated["tr1"], rotated["t27"]),
        ("dash", pts["t31d"], rotated["t22"]),
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
                rotated["t22"],
                rotated["t25"],
                rotated["t27"],
            ],
            6,
        ),
        (
            "french_curve",
            [
                pts["t24"],
                pts["t29b"],
                pts["t29"],
            ],
            6,
        ),
        (
            "french_curve",
            [
                pts["t29"],
                rotated["tr1_1"],
                rotated["tr1"],
                rotated["tr2_2"],
                rotated["tr2"],
                rotated["t27"],
            ],
            6,
        ),
        (
            "french_curve",
            [
                pts["t21"],
                pts["t30b"],
                rotated["t31b"],
                rotated["t22"],
            ],
            6,
        ),
    ]


my_shapes = get_no_dart_flare_back_shapes()
output_file = generated_file("aldrich_tailored_trousers/no_dart_flare_shorts/back.svg")

render_svg(
    my_shapes,
    filename=str(output_file),
    show_dashes=False,
    show_points=False,
    show_numbers=False,
)

print(f"Generated in {output_file}")
