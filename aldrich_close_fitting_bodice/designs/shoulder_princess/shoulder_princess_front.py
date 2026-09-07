from render.svg_rendering import render_svg
from utils.geometry import (
    get_distance,
    get_midpoint,
    get_perpendicular_intersection_with_line,
    get_perpendicular_point_from_line,
    get_point_on_line_at_distance,
    move_shapes,
)
from utils.paths import generated_file
from utils.points import build_points
from utils.rotation import angle_between, rotate_point
from utils import measurements as m

# Ref fullness: https://www.youtube.com/shorts/T_-1WyAOK5k
# Ref: https://madetosew.com/blog/draft-an-a-line-v-neck-dress/

pts = build_points(waist_ease=0, bust_ease=40, front_side_dart=20, back_side_dart=20)


def get_rotated_shoulder_princess_front_points():
    rotated_points = {key: value for key, value in pts.items() if key.startswith("p")}

    # Rotate shoulder dart
    midpoint_between_p27_p30 = get_midpoint(pts["p27"], pts["p30"])
    rotated_points["p27a"] = midpoint_between_p27_p30
    rotated_points["p27b"] = midpoint_between_p27_p30
    angle = angle_between([pts["p26"], pts["p27"]], [pts["p26"], pts["p20"]])
    for key in ["p27", "p27a"]:
        rotated_points[key] = tuple(
            rotate_point(rotated_points[key], pts["p26"], angle)
        )

    # Length for skirt
    length_from_hip = 300
    rotated_points["p8a"] = get_point_on_line_at_distance(
        line1=pts["p8"], line2=pts["p6"], distance=-length_from_hip
    )
    rotated_points["p36a"] = get_perpendicular_point_from_line(
        line1=pts["p36"], line2=pts["p8"], distance=length_from_hip
    )
    rotated_points["p25a"] = get_perpendicular_intersection_with_line(
        point=pts["p25"], line1=rotated_points["p36a"], line2=rotated_points["p8a"]
    )

    # Fullness for skirt
    rotated_points["px_1"] = get_point_on_line_at_distance(
        line1=pts["p24_1"], line2=pts["p18"], distance=30
    )
    rotated_points["px_2"] = get_point_on_line_at_distance(
        line1=pts["p24_2"], line2=pts["p6"], distance=30
    )
    rotated_points["px_3"] = get_point_on_line_at_distance(
        line1=rotated_points["px_1"], line2=pts["p18"], distance=40
    )
    rotated_points["px_1a"] = get_perpendicular_intersection_with_line(
        point=rotated_points["px_1"],
        line1=rotated_points["p36a"],
        line2=rotated_points["p8a"],
    )
    rotated_points["px_2a"] = get_perpendicular_intersection_with_line(
        point=rotated_points["px_2"],
        line1=rotated_points["p36a"],
        line2=rotated_points["p8a"],
    )
    rotated_points["px_3a"] = get_perpendicular_intersection_with_line(
        point=rotated_points["px_3"],
        line1=rotated_points["p36a"],
        line2=rotated_points["p8a"],
    )

    angle = 11.4
    for key in ["px_2a", "p24_2", "p25a", "p25"]:
        rotated_points[key + "r"] = tuple(
            rotate_point(rotated_points[key], rotated_points["px_2"], angle)
        )
    for key in ["p24_1", "p25a", "p25", "px_1a"]:
        rotated_points[key + "t"] = tuple(
            rotate_point(rotated_points[key], rotated_points["px_1"], -angle)
        )
    for key in ["px_3a", "p36a", "p36", "p33_2"]:
        rotated_points[key + "s"] = tuple(
            rotate_point(rotated_points[key], rotated_points["px_3"], angle)
        )

    rotated_points["p24_2f"] = get_midpoint(pts["p24_2"], rotated_points["p24_2r"])
    rotated_points["p24_1f"] = get_midpoint(pts["p24_1"], rotated_points["p24_1t"])
    rotated_points["p33_2f"] = get_midpoint(pts["p33_2"], rotated_points["p33_2s"])

    for key in ["p36as", "px_3as", "px_1at", "p25at", "p25ar", "px_2ar"]:
        rotated_points[key] = (rotated_points[key][0], rotated_points[key][1] + 5)

    # Notches
    rotated_points["p26_1n"] = (rotated_points["p26"][0] - 10, rotated_points["p26"][1])
    rotated_points["p26_2n"] = (rotated_points["p26"][0] + 10, rotated_points["p26"][1])
    rotated_points["p24_1fn"] = (
        rotated_points["p24_1f"][0] - 10,
        rotated_points["p24_1f"][1],
    )
    rotated_points["p24_2fn"] = (
        rotated_points["p24_2f"][0] + 10,
        rotated_points["p24_2f"][1],
    )

    # Neckline
    rotated_points["p20a"] = get_point_on_line_at_distance(
        line1=pts["p20"], line2=rotated_points["p27a"], distance=25
    )
    rotated_points["p3d1"] = get_point_on_line_at_distance(
        line1=pts["p3"], line2=rotated_points["p20a"], distance=42
    )
    rotated_points["p3d1h"] = (
        rotated_points["p3d1"][0] - 100,
        rotated_points["p3d1"][1],
    )
    rotated_points["p3d2"] = get_point_on_line_at_distance(
        line1=pts["p3"], line2=rotated_points["p20a"], distance=20
    )
    angle = angle_between(
        [pts["p26"], rotated_points["p3d1"]], [pts["p26"], rotated_points["p3d2"]]
    )
    for key in ["p27a", "p20a"]:
        rotated_points[key] = tuple(
            rotate_point(rotated_points[key], rotated_points["p26"], angle)
        )

    # Shoulder
    rotated_points["p30a"] = get_point_on_line_at_distance(
        line1=pts["p30"], line2=rotated_points["p27b"], distance=10
    )

    rotated_points["p27ad"] = get_point_on_line_at_distance(
        line1=rotated_points["p27a"], line2=rotated_points["p23"], distance=4
    )
    rotated_points["p27bd"] = get_point_on_line_at_distance(
        line1=rotated_points["p27b"], line2=rotated_points["p26"], distance=4
    )
    rotated_points["p20ad"] = get_point_on_line_at_distance(
        line1=rotated_points["p20a"], line2=rotated_points["p3"], distance=4
    )

    rotated_points["p32a"] = get_point_on_line_at_distance(
        line1=pts["p32"], line2=rotated_points["p33_2f"], distance=10
    )

    return rotated_points


def get_shoulder_princess_front_center_shapes():
    rotated = get_rotated_shoulder_princess_front_points()
    print(f"Width total: {get_distance(rotated["p36as"], rotated["p25at"]) +
           get_distance(rotated["p25ar"], rotated["p8a"])}")
    print(f"Skirt length: {get_distance(pts["p6"], rotated["p8a"])}")
    print(f"Shoulder total: {get_distance(rotated["p20a"], rotated["p27ad"]) +
                              get_distance(rotated["p27bd"], rotated["p30a"])}")
    return [
        ("circle", rotated),
        ("curve", rotated["p20ad"], rotated["p3"], 0.05),
        ("line", rotated["p3"], rotated["p8a"]),
        ("dash", pts["p8"], pts["p25"]),
        ("dash", pts["p26"], rotated["p3d1"]),
        ("dash", pts["p26"], rotated["p3d2"]),
        ("dash", rotated["p3d1"], rotated["p3d1h"]),
        (
            "french_curve",
            [
                rotated["p27ad"],
                pts["p26"],
                rotated["p24_2f"],
                rotated["p25r"],
                rotated["p25ar"],
            ],
            15.0,
        ),
        (
            "french_curve",
            [
                rotated["p8a"],
                rotated["px_2a"],
                rotated["px_2ar"],
                rotated["p25ar"],
            ],
            15.0,
        ),
        ("line", rotated["p27ad"], rotated["p20ad"]),
        ("dash", pts["p26"], pts["p24_2"]),
        ("dash", pts["p24_2"], pts["p25"]),
        ("dash", pts["p6"], pts["p24"]),
        ("dash", pts["p3"], pts["p23"]),
        ("dash", pts["p26"], pts["p25"]),
        ("dash", rotated["p25"], rotated["p25a"]),
        ("dash", rotated["p24"], rotated["p25ar"]),
        ("dash", rotated["px_2"], rotated["px_2a"]),
        ("dash", rotated["px_2"], rotated["px_2ar"]),
        ("line", rotated["p26_2n"], pts["p26"]),
        ("line", rotated["p24_2fn"], rotated["p24_2f"]),
        ("circle", [pts["p26"]], m.bust_radius),
    ]


def get_shoulder_princess_front_side_shapes():
    rotated = get_rotated_shoulder_princess_front_points()
    return [
        ("circle", rotated),
        ("dash", pts["p25"], pts["p36"]),
        ("dash", pts["p33_2"], pts["p36"]),
        ("dash", rotated["p36a"], pts["p36"]),
        ("dash", rotated["p36as"], rotated["p36a"]),
        (
            "french_curve",
            [
                rotated["p32a"],
                rotated["p33_2f"],
                rotated["p36s"],
                rotated["p36as"],
            ],
            15.0,
        ),
        (
            "french_curve",
            [
                pts["p14a"],
                rotated["p32a"],
                pts["p22a"],
                pts["p31"],
                rotated["p30a"],
            ],
            7.0,
        ),
        (
            "french_curve",
            [
                rotated["p27bd"],
                pts["p26"],
                rotated["p24_1f"],
                rotated["p25t"],
                rotated["p25at"],
            ],
            15.0,
        ),
        (
            "french_curve",
            [
                rotated["p36as"],
                rotated["px_3as"],
                rotated["px_3a"],
                rotated["px_1a"],
                rotated["px_1at"],
                rotated["p25at"],
            ],
            15.0,
        ),
        ("line", rotated["p27bd"], rotated["p30a"]),
        ("dash", rotated["p27bd"], pts["p26"]),
        ("dash", pts["p26"], pts["p24_1"]),
        ("dash", pts["p24_1"], pts["p25"]),
        ("dash", pts["p24"], pts["p33"]),
        ("dash", pts["p23"], pts["p32"]),
        ("dash", pts["p26"], pts["p25"]),
        ("dash", rotated["p25"], rotated["p25a"]),
        ("dash", rotated["p25at"], rotated["p25t"]),
        ("dash", rotated["px_1"], rotated["px_1a"]),
        ("dash", rotated["px_3"], rotated["px_3a"]),
        ("dash", rotated["px_3"], rotated["px_3as"]),
        ("dash", rotated["px_1"], rotated["px_1a"]),
        ("dash", rotated["p24_1"], rotated["p25"]),
        ("dash", rotated["px_1"], rotated["px_1at"]),
        ("dash", rotated["p24_1t"], rotated["p25t"]),
        ("line", rotated["p26_1n"], pts["p26"]),
        ("line", rotated["p24_1fn"], rotated["p24_1f"]),
    ]


if __name__ == "__main__":
    side_shapes = move_shapes(get_shoulder_princess_front_side_shapes(), -210.0)
    my_shapes = get_shoulder_princess_front_center_shapes() + side_shapes
    output_file = generated_file(
        "aldrich_close_fitting_bodice/designs/shoulder_princess/shoulder_princess_front.svg"
    )
    render_svg(
        my_shapes,
        filename=str(output_file),
        show_dashes=True,
        show_points=True,
        show_numbers=True,
    )
    print(f"Generated in {output_file}")
