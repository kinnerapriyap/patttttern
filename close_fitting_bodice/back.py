from utils.points import build_points
from render.svg_rendering import render_svg


def get_back_shapes():
    pts = build_points()
    return [
        ("curve", pts["p9"], pts["p1"], 0.45),
        ("line", pts["p12_2"], pts["p9"]),
        ("line", pts["p13"], pts["p12_2"]),
        ("line", pts["p13"], pts["p12_1"]),
        ("line", pts["p12_1"], pts["p11"]),
        ("french_curve", [pts["p11"], pts["p16"], pts["p14a"], pts["p32"], pts["p22a"], pts["p31"], pts["p30"]], 6.0),
        ("line", pts["p32"], pts["p33_1"]),
        ("line", pts["p33_1"], pts["p35"]),
        ("line", pts["p35"], pts["p7"]),
        ("line", pts["p7"], pts["p1"]),
        ("line", pts["p17"], pts["p18_1"]),
        ("line", pts["p17"], pts["p18_2"]),
        ("line", pts["p18_1"], pts["p19"]),
        ("line", pts["p18_2"], pts["p19"]),

        ("dash", pts["p5"], pts["p33"]),
        ("dash", pts["p2"], pts["p32"]),
        ("dash", pts["p10"], pts["p11"]),
        ("dash", pts["p17"], pts["p19"]),
    ]


if __name__ == "__main__":
    my_shapes = get_back_shapes()
    render_svg(my_shapes, filename="../generated/back.svg", show_dashes=True, show_points=True, show_numbers=False)
    print("Generated in back.svg")
