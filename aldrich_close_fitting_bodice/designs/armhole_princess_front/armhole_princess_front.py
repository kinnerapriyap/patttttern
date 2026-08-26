from aldrich_close_fitting_bodice import pts
from render.svg_rendering import render_svg
from utils.paths import generated_file
from utils.rotation import angle_between, rotate_point


def get_rotated_armhole_princess_front_points():
    rotated_points = {key: value for key, value in pts.items() if key.startswith("p")}
    angle = angle_between([pts["p26"], pts["p27"]], [pts["p26"], pts["p20"]])
    for key in ["p27", "p22a", "p31", "p30", "p32"]:
        rotated_points[key] = tuple(
            rotate_point(rotated_points[key], pts["p26"], angle)
        )
    return rotated_points


def get_armhole_princess_front_shapes():
    rotated = get_rotated_armhole_princess_front_points()
    return [
        ("circle", rotated),
        ("curve", pts["p20"], pts["p21"], 0.45),
        ("line", pts["p21"], pts["p8"]),
        ("line", pts["p8"], pts["p36"]),
        ("line", pts["p33_2"], pts["p36"]),
        ("line", pts["p32"], pts["p33_2"]),
        (
            "french_curve",
            [
                pts["p14a"],
                pts["p32"],
                pts["p22a"],
                pts["p31"],
            ],
            6.0,
        ),
        (
            "french_curve",
            [
                rotated["p32"],
                rotated["p22a"],
                rotated["p31"],
                rotated["p30"],
            ],
            6.0,
        ),
        ("line", pts["p20"], rotated["p30"]),
        ("line", pts["p22a"], pts["p26"]),
        ("line", rotated["p22a"], pts["p26"]),
        ("line", pts["p26"], pts["p24_1"]),
        ("line", pts["p26"], pts["p24_2"]),
        ("line", pts["p24_1"], pts["p25"]),
        ("line", pts["p24_2"], pts["p25"]),
        ("dash", pts["p6"], pts["p33"]),
        ("dash", pts["p3"], pts["p32"]),
        ("dash", pts["p26"], pts["p25"]),
    ]


if __name__ == "__main__":
    my_shapes = get_armhole_princess_front_shapes()
    output_file = generated_file(
        "aldrich_close_fitting_bodice/designs/armhole_princess_front/armhole_princess_front.svg"
    )
    render_svg(
        my_shapes,
        filename=str(output_file),
        show_dashes=True,
        show_points=True,
        show_numbers=True,
    )
    print(f"Generated in {output_file}")
