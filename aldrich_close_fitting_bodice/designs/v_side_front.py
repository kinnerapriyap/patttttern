from aldrich_close_fitting_bodice import pts
from render.svg_rendering import render_svg
from utils.geometry import get_perpendicular_intersection_with_line
from utils.paths import generated_file
from utils.rotation import angle_between, rotate_point
from aldrich_close_fitting_bodice.designs.shoulder_dart_front import (
    get_rotated_shoulder_dart_front_points,
)


def get_rotated_v_side_front_points():
    angle = angle_between([pts["p26"], pts["p24_2"]], [pts["p26"], pts["p24_1"]])

    point_side_keys = ["p32", "p33_2", "p27", "p14a", "p22a", "p31", "p30"]
    rotated_points = {
        key: tuple(rotate_point(pts[key], pts["p26"], -angle))
        for key in point_side_keys
    }

    point_center_keys = ["p20", "p21", "p6", "p24_2", "p26"]
    rotated_points = rotated_points | {key: pts[key] for key in point_center_keys}

    pv_1 = get_perpendicular_intersection_with_line(pts["p26"], pts["p6"], pts["p21"])
    rotated_points["pv_1"] = pv_1
    rotated_points["pv_2"] = pv_1

    angle2 = angle_between(
        [rotated_points["p26"], rotated_points["p20"]],
        [rotated_points["p26"], rotated_points["p27"]],
    )
    for key in ["p20", "p21", "pv_1"]:
        rotated_points[key] = tuple(
            rotate_point(rotated_points[key], pts["p26"], -angle2)
        )

    return rotated_points


def get_v_side_front_shapes():
    rotated = get_rotated_v_side_front_points()
    return [
        ("circle", rotated),
        ("curve", rotated["p20"], rotated["p21"], 0.45),
        (
            "polyline",
            [
                rotated["p21"],
                rotated["pv_1"],
                rotated["pv_2"],
                rotated["p6"],
                rotated["p24_2"],
                rotated["p33_2"],
                rotated["p32"],
            ],
        ),
        (
            "french_curve",
            [
                rotated["p14a"],
                rotated["p32"],
                rotated["p22a"],
                rotated["p31"],
                rotated["p30"],
            ],
            6.0,
        ),
        ("polyline", [rotated["p30"], rotated["p20"]]),
        ("line", rotated["p22a"], rotated["p6"]),
        ("line", rotated["pv_1"], rotated["p26"]),
        ("line", rotated["pv_2"], rotated["p26"]),
    ]


if __name__ == "__main__":
    my_shapes = get_v_side_front_shapes()
    output_file = generated_file("v_side_front.svg")
    render_svg(
        my_shapes,
        filename=str(output_file),
        show_dashes=True,
        show_points=False,
        show_numbers=True,
    )
    print(f"Generated in {output_file}")
