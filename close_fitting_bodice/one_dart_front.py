from close_fitting_bodice import pts
from render.svg_rendering import render_svg
from utils.rotation import angle_between, rotate_point


def get_rotated_one_dart_front_points():
    angle = angle_between([pts["p26"], pts["p27"]], [pts["p26"], pts["p20"]])

    point_side_keys = [
        "p32", "p33_2", "p24_1", "p27", "p11",
        "p16", "p14a", "p22a", "p31", "p30",
    ]
    rotated_points = {
        key: tuple(rotate_point(pts[key], pts["p26"], angle))
        for key in point_side_keys
    }

    point_center_keys = ["p21", "p6", "p24_2", "p26"]
    return rotated_points | {key: pts[key] for key in point_center_keys}


def get_one_dart_front_shapes():
    rotated = get_rotated_one_dart_front_points()
    return [
        ("circle", rotated),
        ("curve", pts["p20"], pts["p21"], 0.45),
        ("polyline",
         [pts["p21"], pts["p6"], pts["p24_2"], pts["p26"], rotated["p24_1"], rotated["p33_2"], rotated["p32"]]),
        ("french_curve",
         [rotated["p11"], rotated["p16"], rotated["p14a"], rotated["p32"], rotated["p22a"], rotated["p31"],
          rotated["p30"]], 6.0),
        ("line", rotated["p27"], rotated["p30"]),

    ]


if __name__ == "__main__":
    my_shapes = get_one_dart_front_shapes()
    render_svg(
        my_shapes,
        filename="../generated/one_dart_front.svg",
        show_dashes=True,
        show_points=True,
        show_numbers=True,
    )
    print("Generated in one_dart_front.svg")
