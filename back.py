from points import build_points, named_points_from_keys
from svg_rendering import render_svg


def get_back_shapes():
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

        ("dash", pts["p6"], pts["p33"]),
        ("dash", pts["p3"], pts["p32"]),
    ]


if __name__ == "__main__":
    my_shapes = get_back_shapes()
    render_svg(my_shapes, filename="back.svg", show_dashes=True, show_points=True, show_numbers=False)
    print("Generated in back.svg")
