from close_fitting_bodice import pts
from render.svg_rendering import render_svg


def get_base_shapes():
    print(f"Available dart ease: {pts['available_dart_ease']} mm")
    print(f"Used all dart ease? {pts['used_all_dart_ease']}")

    return [
        ("circle", pts["named_points"]),
        ("dash", pts["p0"], pts["p1"]),
        ("line", pts["p1"], pts["p7"]),
        ("dash", pts["p2"], pts["p3"]),
        ("dash", pts["p4"], pts["p21"]),
        ("line", pts["p21"], pts["p8"]),
        ("dash", pts["p5"], pts["p6"]),
        ("line", pts["p7"], pts["p8"]),
        ("dash", pts["p0"], pts["p9"]),
        ("dash", pts["p10"], pts["p11"]),
        ("dash", pts["p14"], pts["p15"]),
        ("dash", pts["p17"], pts["p19"]),
        ("dash", pts["p4"], pts["p27"]),
        ("dash", pts["p23"], pts["p25"]),
        ("line", pts["p20"], pts["p26"]),
        ("line", pts["p27"], pts["p26"]),
        ("dash", pts["p11"], pts["p28"]),
        ("dash", pts["p28"], pts["p29"]),
        ("line", pts["p27"], pts["p30"]),
        ("dash", pts["p22"], pts["p31"]),
        ("dash", pts["p32"], pts["p34"]),
        ("dash", pts["p14"], pts["p14a"]),
        ("dash", pts["p22"], pts["p22a"]),
        ("dash", pts["p12"], pts["p12a"]),
        ("dash", pts["p13"], pts["p12a"]),
        ("line", pts["p13"], pts["p12_1"]),
        ("line", pts["p13"], pts["p12_2"]),
        ("line", pts["p12_1"], pts["p11"]),
        ("line", pts["p12_2"], pts["p9"]),
        ("line", pts["p26"], pts["p24_1"]),
        ("line", pts["p26"], pts["p24_2"]),
        ("line", pts["p24_1"], pts["p25"]),
        ("line", pts["p24_2"], pts["p25"]),
        ("line", pts["p17"], pts["p18_1"]),
        ("line", pts["p17"], pts["p18_2"]),
        ("line", pts["p18_1"], pts["p19"]),
        ("line", pts["p18_2"], pts["p19"]),
        ("line", pts["p32"], pts["p33_1"]),
        ("line", pts["p32"], pts["p33_2"]),
        ("line", pts["p33_1"], pts["p35"]),
        ("line", pts["p33_2"], pts["p36"]),

        ("curve", pts["p20"], pts["p21"], 0.45),
        ("curve", pts["p9"], pts["p1"], 0.45),

        ("french_curve", [pts["p11"], pts["p16"], pts["p14a"], pts["p32"], pts["p22a"], pts["p31"], pts["p30"]], 6),
    ]


my_shapes = get_base_shapes()
render_svg(
    my_shapes,
    filename="../generated/pattern.svg",
    show_dashes=True,
    show_points=True,
    show_numbers=True,
)

print("Generated in pattern.svg")
