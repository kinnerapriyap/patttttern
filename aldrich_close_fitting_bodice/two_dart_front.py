from aldrich_close_fitting_bodice import pts
from aldrich_close_fitting_bodice.one_dart_front import get_rotated_one_dart_front_points
from render.svg_rendering import render_svg
from utils.geometry import get_horizontal_intersection_with_line
from utils.paths import generated_file
from utils.rotation import angle_between, rotate_point


def get_rotated_two_dart_front_points():
    rotated_points = get_rotated_one_dart_front_points();

    p2dart_1 = get_horizontal_intersection_with_line(
        pts["p26"][1],
        rotated_points["p32"],
        rotated_points["p33_2"],
    )
    rotated_points["p2dart_1"] = p2dart_1  
    rotated_points["p2dart_2"] = p2dart_1  

    angle2 = angle_between([pts["p6"], pts["p24_2"]], [rotated_points["p24_1"], rotated_points["p33_2"]])
    for key in ["p2dart_2", "p24_1", "p33_2"]:
        rotated_points[key] = tuple(rotate_point(rotated_points[key], pts["p26"], -angle2))

    return rotated_points;


def get_two_dart_front_shapes():
    rotated = get_rotated_two_dart_front_points()
    return [
        ("circle", rotated),
        ("curve", pts["p20"], pts["p21"], 0.45),
        ("polyline",
         [pts["p21"], pts["p6"], pts["p24_2"], pts["p26"], rotated["p24_1"], rotated["p33_2"], rotated["p2dart_2"], pts["p26"]]),
        ("french_curve", [rotated["p14a"], rotated["p32"], rotated["p22a"], rotated["p31"], rotated["p30"]], 6.0),
        ("line", rotated["p27"], rotated["p30"]),
        ("polyline", [pts["p26"], rotated["p2dart_1"], rotated["p32"]]),
    ]


if __name__ == "__main__":
    my_shapes = get_two_dart_front_shapes()
    output_file = generated_file("two_dart_front.svg")
    render_svg(
        my_shapes,
        filename=str(output_file),
        show_dashes=True,
        show_points=True,
        show_numbers=True,
        show_control_square=True,
    )
    print(f"Generated in {output_file}")
