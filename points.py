from math import sqrt

import measurements as m
from utils import reflect_point_across_line


def named_points_from_keys(points, keys):
    return {
        key[1:]: points[key]
        for key in keys
        if key.startswith("p") and key in points
    }


def build_points():
    p0 = (0, 0)
    p1 = (0, 15)
    p2 = (0, p1[1] + (m.armscye_depth + 5))
    p3 = (p2[0] + (m.bust / 2) + m.bust_ease, p2[1])
    p4 = (p3[0], p3[1] - p2[1] - (m.size_above_14 * 5))
    p5 = (0, p1[1] + m.nape_to_waist)
    p6 = (p3[0], p5[1])
    p7 = (0, p5[1] + m.waist_to_hip)
    p8 = (p3[0], p7[1])

    # Back
    p9 = [(m.neck_size / 5) - 2, 0]
    p10 = [0, p1[1] + (m.armscye_depth / 5) - 7]
    p11 = [p9[0] + sqrt((m.shoulder + m.shoulder_dart) ** 2 - p10[1] ** 2), p10[1]]
    p12 = [(p9[0] + p11[0]) / 2, (p9[1] + p11[1]) / 2]
    p12a = [p12[0], p12[1] + 50]
    p13 = [p12[0] - 10, p12a[1]]
    p14 = [m.back_width / 2 + m.back_width_ease, p2[1]]
    p15 = [p14[0], p10[1]]
    p16 = [(p14[0] + p15[0]) / 2, (p14[1] + p15[1]) / 2]
    p17 = [(p2[0] + p14[0]) / 2, (p2[1] + p14[1]) / 2]
    p18 = [p17[0], p5[1]]
    p19 = [p17[0], p7[1]]

    # Front
    p20 = [p4[0] - (m.neck_size / 5 - 7), p4[1]]
    p21 = [p4[0], p4[1] + m.neck_size / 5 - 2]
    p22 = [p3[0] - (m.chest / 2 + m.dart / 2), p3[1]]
    p23 = [(p3[0] + p22[0]) / 2, (p3[1] + p22[1]) / 2]
    p24 = [p23[0], p6[1]]
    p25 = [p23[0], p8[1]]
    p26 = [p23[0], p23[1] + m.bust_to_dart]
    p27 = [p20[0] - m.dart, p20[1]]
    p28 = [p11[0], p11[1] + 15]
    p29 = [p28[0] + 100, p28[1]]
    p30 = [p27[0] - sqrt(m.shoulder ** 2 - (p29[1] - p27[1]) ** 2), p29[1]]
    p31 = [p22[0], p22[1] - ((p3[1] - p21[1]) / 3)]
    p32 = [(p14[0] + p22[0]) / 2, (p14[1] + p22[1]) / 2]
    p33 = [p32[0], p5[1]]
    p34 = [p32[0], p7[1]]

    p14a = [p14[0] + (m.distance_from_p14 / sqrt(2)), p14[1] - (m.distance_from_p14 / sqrt(2))]
    p22a = [p22[0] - (m.distance_from_p22 / sqrt(2)), p22[1] - (m.distance_from_p22 / sqrt(2))]

    d12_11 = sqrt((p11[0] - p12[0]) ** 2 + (p11[1] - p12[1]) ** 2)
    p12_1 = [
        p12[0] + (m.shoulder_dart / 2) * ((p11[0] - p12[0]) / d12_11),
        p12[1] + (m.shoulder_dart / 2) * ((p11[1] - p12[1]) / d12_11),
    ]
    p12_2 = reflect_point_across_line(p12_1, p12, p13)

    d_half_bust_with_ease = m.bust / 2 + m.bust_ease
    d_half_waist_with_ease = m.waist / 2 + m.waist_ease
    d_available_dart_ease = d_half_bust_with_ease - d_half_waist_with_ease

    p24_1 = [p24[0] - (m.front_dart / 2), p24[1]]
    p24_2 = [p24[0] + (m.front_dart / 2), p24[1]]

    p18_1 = [p18[0] - (m.back_dart / 2), p18[1]]
    p18_2 = [p18[0] + (m.back_dart / 2), p18[1]]

    p33_1 = [p33[0] - (m.front_side_dart / 2), p33[1]]
    p33_2 = [p33[0] + (m.back_side_dart / 2), p33[1]]

    p35 = [p7[0] + (m.hip / 4), p7[1]]
    p36 = [p8[0] - (m.hip / 4), p8[1]]

    point_values = {
        name: tuple(value)
        for name, value in locals().items()
        if name.startswith("p")
    }
    metadata: dict[str, object] = {
        "named_points": {
            name[1:]: value
            for name, value in point_values.items()
            if name.startswith("p")
        },
        "available_dart_ease": d_available_dart_ease,
        "used_all_dart_ease": (
                m.front_dart + m.back_dart + m.front_side_dart + m.back_side_dart == d_available_dart_ease
        ),
    }
    return {**point_values, **metadata}
