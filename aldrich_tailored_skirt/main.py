from . import pts
from utils.paths import generated_file
from render.svg_rendering import render_svg


def get_base_shapes():
    return [
        ("circle", pts["named_points"]),
        ("line", pts["s1"], pts["s3"]),
        ("line", pts["s3"], pts["s4"]),
        ("line", pts["s2"], pts["s4"]),
        ("line", pts["s5"], pts["s6"]),
        ("line", pts["s7"], pts["s8"]),
        ("line", pts["s11a"], pts["s13"]),
        ("line", pts["s11b"], pts["s13"]),
        ("line", pts["s12a"], pts["s14"]),
        ("line", pts["s12b"], pts["s14"]),
        ("line", pts["s17a"], pts["s18"]),
        ("line", pts["s17b"], pts["s18"]),
        ("dash", pts["s1"], pts["s2"]),
        ("dash", pts["s10"], pts["s1"]),
        ("dash", pts["s11"], pts["s13"]),
        ("dash", pts["s12"], pts["s14"]),
        ("dash", pts["s2"], pts["s16"]),
        ("dash", pts["s17"], pts["s18"]),
        ("dash", pts["s10"], pts["s7"]),
        ("dash", pts["s16"], pts["s7"]),
        ("dash", pts["s10a"], pts["s10b"]),
        (
            "french_curve",
            [pts["s10"], pts["s10b"], pts["s7"]],
            6,
        ),
        (
            "french_curve",
            [pts["s16"], pts["s16b"], pts["s7"]],
            6,
        ),
        ("curve", pts["s11b"], pts["s1"], 0.45),
        ("curve", pts["s12b"], pts["s11a"], 0.45),
        ("curve", pts["s10"], pts["s12a"], 0.45),
        ("curve", pts["s17b"], pts["s2"], 0.45),
        ("curve", pts["s16"], pts["s17a"], 0.45),
    ]


my_shapes = get_base_shapes()
output_file = generated_file("aldrich_tailored_skirt/base.svg")

render_svg(
    my_shapes,
    filename=str(output_file),
    show_dashes=True,
    show_points=True,
    show_numbers=True,
)

print(f"Generated in {output_file}")
