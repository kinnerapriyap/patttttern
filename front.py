from utils.points import build_points
from svg_rendering import render_svg


def get_front_shapes():
    pts = build_points()
    return [
        ("curve", pts["p20"], pts["p21"], 0.45),
        ("line", pts["p21"], pts["p8"]),
        ("line", pts["p8"], pts["p36"]),
        ("line", pts["p33_2"], pts["p36"]),
        ("line", pts["p32"], pts["p33_2"]),
        ("french_curve", [pts["p11"], pts["p16"], pts["p14a"], pts["p32"], pts["p22a"], pts["p31"], pts["p30"]], 6.0),
        ("line", pts["p27"], pts["p30"]),
        ("line", pts["p27"], pts["p26"]),
        ("line", pts["p20"], pts["p26"]),
        ("line", pts["p26"], pts["p24_1"]),
        ("line", pts["p26"], pts["p24_2"]),
        ("line", pts["p24_1"], pts["p25"]),
        ("line", pts["p24_2"], pts["p25"]),

        ("dash", pts["p6"], pts["p33"]),
        ("dash", pts["p3"], pts["p32"]),
        ("dash", pts["p26"], pts["p25"]),
    ]


if __name__ == "__main__":
    my_shapes = get_front_shapes()
    render_svg(my_shapes, filename="generated/front.svg", show_dashes=True, show_points=True, show_numbers=False)
    print("Generated in front.svg")
