from aldrich_tailored_skirt import pts
from render.svg_rendering import render_svg
from utils.paths import generated_file


def get_back_shapes():
    return [
        ("circle", pts["named_points"]),
        ("line", pts["s1"], pts["s3"]),
        ("line", pts["s3"], pts["s8"]),
        ("dash", pts["s5"], pts["s7"]),
        ("line", pts["s7"], pts["s8"]),
        ("line", pts["s11a"], pts["s13"]),
        ("line", pts["s11b"], pts["s13"]),
        ("line", pts["s12a"], pts["s14"]),
        ("line", pts["s12b"], pts["s14"]),
        ("dash", pts["s10"], pts["s1"]),
        ("dash", pts["s11"], pts["s13"]),
        ("dash", pts["s12"], pts["s14"]),
        ("dash", pts["s10"], pts["s7"]),
        ("dash", pts["s10a"], pts["s10b"]),
        (
            "french_curve",
            [pts["s10"], pts["s10b"], pts["s7"]],
            6,
        ),
        ("curve", pts["s11b"], pts["s1"], 0.45),
        ("curve", pts["s12b"], pts["s11a"], 0.45),
        ("curve", pts["s10"], pts["s12a"], 0.45),
    ]


if __name__ == "__main__":
    my_shapes = get_back_shapes()
    output_file = generated_file("aldrich_tailored_skirt/base/back.svg")
    render_svg(
        my_shapes,
        filename=str(output_file),
        show_dashes=True,
        show_points=True,
        show_numbers=True,
    )
    print(f"Generated in {output_file}")
