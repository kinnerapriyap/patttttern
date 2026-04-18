from points import build_points
from svg_rendering import render_svg


def get_front_shapes():
    pts = build_points()
    return [
        ("curve", pts["p9"], pts["p1"], 0.45),
        ("line", pts["p12_2"], pts["p9"]),
        ("line", pts["p13"], pts["p12_2"]),
        ("line", pts["p13"], pts["p12_1"]),
        ("line", pts["p12_1"], pts["p11"]),
        ("french_curve", [pts["p11"], pts["p16"], pts["p14a"], pts["p32"]]),
        ("line", pts["p32"], pts["p33_1"]),
        ("line", pts["p33_1"], pts["p35"]),
        ("line", pts["p35"], pts["p7"]),
        ("line", pts["p7"], pts["p1"]),
    ]


if __name__ == "__main__":
    my_shapes = get_front_shapes()
    render_svg(my_shapes, filename="front.svg", show_dashes=True, show_points=True)
    print("Generated in front.svg")
