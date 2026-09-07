from render.svg_rendering import render_svg
from utils.geometry import (
    get_distance,
    get_horizontal_intersection_with_line,
    get_midpoint,
    get_perpendicular_intersection_with_line,
    get_point_on_line_at_distance,
    move_shapes,
)
from utils.paths import generated_file
from utils.points import build_points
from utils.rotation import rotate_point
from utils import measurements as m

pts = build_points(waist_ease=0, bust_ease=40, front_side_dart=20, back_side_dart=20)


def get_rotated_shoulder_princess_back_points():
    rotated_points = {key: value for key, value in pts.items() if key.startswith("p")}
    rotated_points["p9a"] = get_point_on_line_at_distance(
        line1=pts["p9"], line2=pts["p11"], distance=25
    )
    rotated_points["p11a"] = get_point_on_line_at_distance(
        line1=pts["p11"], line2=pts["p9"], distance=10
    )

    # Length for skirt
    length_from_hip = 300
    rotated_points["p7a"] = get_point_on_line_at_distance(
        line1=pts["p7"], line2=pts["p5"], distance=-length_from_hip
    )
    rotated_points["p19a"] = get_point_on_line_at_distance(
        line1=pts["p19"], line2=pts["p18"], distance=-length_from_hip
    )
    rotated_points["p35a"] = get_point_on_line_at_distance(
        line1=pts["p35"], line2=pts["p33_1"], distance=-length_from_hip
    )

    # Fullness for skirt
    rotated_points["px_1"] = get_point_on_line_at_distance(
        line1=pts["p18_1"], line2=pts["p18"], distance=-30
    )
    rotated_points["px_2"] = get_point_on_line_at_distance(
        line1=pts["p18_2"], line2=pts["p18"], distance=-30
    )
    rotated_points["px_3"] = get_point_on_line_at_distance(
        line1=rotated_points["px_2"], line2=pts["p18"], distance=-40
    )
    rotated_points["px_1a"] = get_perpendicular_intersection_with_line(
        point=rotated_points["px_1"],
        line1=rotated_points["p19a"],
        line2=rotated_points["p7a"],
    )
    rotated_points["px_2a"] = get_perpendicular_intersection_with_line(
        point=rotated_points["px_2"],
        line1=rotated_points["p19a"],
        line2=rotated_points["p35a"],
    )
    rotated_points["px_3a"] = get_perpendicular_intersection_with_line(
        point=rotated_points["px_3"],
        line1=rotated_points["p35a"],
        line2=rotated_points["p19a"],
    )

    angle = 10.5
    for key in ["px_1a", "p18_1", "p19a", "p19"]:
        rotated_points[key + "r"] = tuple(
            rotate_point(rotated_points[key], rotated_points["px_1"], -angle)
        )
    rotated_points["p18_1f"] = get_midpoint(pts["p18_1"], rotated_points["p18_1r"])
    for key in ["px_2a", "p18_2", "p19a", "p19"]:
        rotated_points[key + "s"] = tuple(
            rotate_point(rotated_points[key], rotated_points["px_2"], angle)
        )
    rotated_points["p18_2f"] = get_midpoint(pts["p18_2"], rotated_points["p18_2s"])
    for key in ["px_3a", "p35a", "p35", "p33_1"]:
        rotated_points[key + "t"] = tuple(
            rotate_point(rotated_points[key], rotated_points["px_3"], -angle)
        )
    rotated_points["p33_1f"] = get_midpoint(pts["p33_1"], rotated_points["p33_1t"])

    for key in ["p19ar", "px_1ar", "p19as", "px_2as", "px_3at", "p35at"]:
        rotated_points[key] = (rotated_points[key][0], rotated_points[key][1] + 5)

    # Shoulder
    rotated_points["p12_1d"] = get_point_on_line_at_distance(
        line1=rotated_points["p12_1"], line2=rotated_points["p13"], distance=4
    )
    rotated_points["p12_2d"] = get_point_on_line_at_distance(
        line1=rotated_points["p12_2"], line2=rotated_points["p13"], distance=4
    )
    rotated_points["p9ad"] = get_point_on_line_at_distance(
        line1=rotated_points["p9a"], line2=rotated_points["p2"], distance=4
    )

    # Contour
    rotated_points["p16a"] = get_horizontal_intersection_with_line(
        y=pts["p16"][1], line1=rotated_points["p13"], line2=rotated_points["p17"]
    )
    rotated_points["p16b"] = get_point_on_line_at_distance(
        line1=rotated_points["p16a"], line2=rotated_points["p17"], distance=40
    )

    rotated_points["p32a"] = get_point_on_line_at_distance(
        line1=pts["p32"], line2=rotated_points["p33_1f"], distance=10
    )

    # Notches
    rotated_points["p16b_1n"] = (
        rotated_points["p16b"][0] - 10,
        rotated_points["p16b"][1],
    )
    rotated_points["p16b_2n"] = (
        rotated_points["p16b"][0] + 10,
        rotated_points["p16b"][1],
    )
    rotated_points["p18_1fn"] = (
        rotated_points["p18_1f"][0] - 10,
        rotated_points["p18_1f"][1],
    )
    rotated_points["p18_2fn"] = (
        rotated_points["p18_2f"][0] + 10,
        rotated_points["p18_2f"][1],
    )

    return rotated_points


def get_shoulder_princess_back_center_shapes():
    rotated = get_rotated_shoulder_princess_back_points()
    print(f"Shoulder total: {get_distance(rotated["p9a"], rotated["p12_2d"]) +
                              get_distance(rotated["p11a"], rotated["p12_1d"])}")

    print(f"Width total: {get_distance(rotated["p7a"], rotated["p19ar"]) +
           get_distance(rotated["p19as"], rotated["p35at"])}")
    print(f"Skirt length: {get_distance(pts["p5"], rotated["p7a"])}")
    return [
        ("circle", rotated),
        ("curve", rotated["p9ad"], rotated["p2"], 0.05),
        ("line", rotated["p12_2d"], rotated["p9ad"]),
        ("line", pts["p7"], rotated["p7a"]),
        (
            "french_curve",
            [
                rotated["p12_2d"],
                pts["p13"],
                rotated["p16b"],
                rotated["p18_1f"],
                rotated["p19r"],
                rotated["p19ar"],
            ],
            15.0,
        ),
        (
            "french_curve",
            [
                rotated["p7a"],
                rotated["px_1a"],
                rotated["px_1ar"],
                rotated["p19ar"],
            ],
            6.0,
        ),
        ("dash", pts["p19"], pts["p7"]),
        ("line", pts["p7"], pts["p2"]),
        ("dash", pts["p2"], pts["p17"]),
        ("dash", pts["p17"], pts["p19"]),
        ("dash", pts["p18"], pts["p5"]),
        ("dash", rotated["px_1"], rotated["px_1a"]),
        ("dash", rotated["px_1"], rotated["px_1ar"]),
        ("dash", rotated["p19"], rotated["p19a"]),
        ("line", rotated["p16b_1n"], rotated["p16b"]),
        ("line", rotated["p18_1f"], rotated["p18_1fn"]),
    ]


def get_shoulder_princess_back_side_shapes():
    rotated = get_rotated_shoulder_princess_back_points()
    return [
        ("circle", rotated),
        ("line", rotated["p12_1d"], rotated["p11a"]),
        (
            "french_curve",
            [
                rotated["p12_1d"],
                pts["p13"],
                rotated["p16b"],
                rotated["p18_2f"],
                rotated["p19s"],
                rotated["p19as"],
            ],
            15.0,
        ),
        (
            "french_curve",
            [
                rotated["p11a"],
                pts["p16"],
                pts["p14a"],
                rotated["p32a"],
                pts["p22a"],
            ],
            6.0,
        ),
        (
            "french_curve",
            [
                rotated["p35at"],
                rotated["px_3at"],
                rotated["px_3a"],
                rotated["px_2a"],
                rotated["px_2as"],
                rotated["p19as"],
            ],
            6.0,
        ),
        (
            "french_curve",
            [
                rotated["p32a"],
                rotated["p33_1f"],
                rotated["p35t"],
                rotated["p35at"],
            ],
            6.0,
        ),
        ("dash", pts["p35"], pts["p19"]),
        ("dash", pts["p18"], pts["p33"]),
        ("dash", pts["p17"], pts["p32"]),
        ("dash", pts["p17"], pts["p19"]),
        ("dash", rotated["px_2"], rotated["px_2a"]),
        ("dash", rotated["px_2"], rotated["px_2as"]),
        ("dash", rotated["px_3"], rotated["px_3a"]),
        ("dash", rotated["px_3"], rotated["px_3at"]),
        ("dash", rotated["p19"], rotated["p19a"]),
        ("dash", pts["p35"], rotated["p35a"]),
        ("dash", rotated["p33_1"], rotated["p35"]),
        ("dash", rotated["p35t"], rotated["p35at"]),
        ("line", rotated["p16b_2n"], rotated["p16b"]),
        ("line", rotated["p18_2f"], rotated["p18_2fn"]),
    ]


if __name__ == "__main__":
    side_shapes = move_shapes(get_shoulder_princess_back_side_shapes(), 210)
    my_shapes = get_shoulder_princess_back_center_shapes() + side_shapes
    output_file = generated_file(
        "aldrich_close_fitting_bodice/designs/shoulder_princess/shoulder_princess_back.svg"
    )
    render_svg(
        my_shapes,
        filename=str(output_file),
        show_dashes=True,
        show_points=True,
        show_numbers=True,
    )
    print(f"Generated in {output_file}")
