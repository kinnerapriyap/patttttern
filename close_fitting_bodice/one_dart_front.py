from close_fitting_bodice import pts
from render.svg_rendering import render_svg
from utils.rotation import angle_between, rotate_shapes


def get_one_dart_front_center():
    return [
        ("polyline", [pts["p21"], pts["p6"], pts["p24_2"], pts["p26"], pts["p20"]]),
        ("curve", pts["p20"], pts["p21"], 0.45),
    ]


def get_one_dart_front_side():
    return [
        ("polyline", [pts["p32"], pts["p33_2"], pts["p24_1"], pts["p26"], pts["p27"], pts["p30"]]),
        ("french_curve", [pts["p11"], pts["p16"], pts["p14a"], pts["p32"], pts["p22a"], pts["p31"], pts["p30"]], 6.0),
    ]


def get_one_dart_front_shapes():
    angle = angle_between([pts["p26"], pts["p27"]], [pts["p26"], pts["p20"]])
    rotated = rotate_shapes(get_one_dart_front_side(), pts["p26"], angle)
    final = get_one_dart_front_center() + rotated
    return final


if __name__ == "__main__":
    my_shapes = get_one_dart_front_shapes()
    render_svg(
        my_shapes,
        filename="../generated/one_dart_front.svg",
        show_dashes=True,
        show_points=True,
        show_numbers=False
    )
    print("Generated in one_dart_front.svg")
