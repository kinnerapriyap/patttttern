from math import hypot, sqrt

from utils import measurements as m
from utils.geometry import (
    get_midpoint,
    get_perpendicular_point_from_line,
    reflect_point_across_line,
    divide_segment_into_parts,
    get_point_on_line_at_distance,
)


def build_points():
    t0 = (0, 0)
    t0a = (-10, 0)
    t0b = (10, 0)
    t0d = (0, 100)
    t1 = (0, m.body_rise)
    t2 = (0, m.waist_to_hip)
    t3 = (0, m.waist_to_floor)
    t3a = (0, t3[1] + 10)
    t4 = (0, (t3[1] + t1[1]) / 2 - 50)
    t5 = (t1[0] - (m.hip / 12 + 20), t1[1])
    t5a = [
        t5[0] - (m.distance_from_t5 / sqrt(2)),
        t5[1] - (m.distance_from_t5 / sqrt(2)),
    ]
    t6 = (t5[0], t2[1])
    t7 = (t5[0], t0[1])
    t8 = (t6[0] + m.hip / 4 + 5, t6[1])
    t9 = (t5[0] - (m.hip / 16 + 5), t5[1])
    t10 = (t7[0] + 10, t7[1])
    t11 = (t10[0] + m.waist / 4 + 22.5, t10[1])  # + 40?
    t12 = (t3[0] + m.trouser_bottom_width / 2 - 5, t3[1])
    t13 = (t12[0] - t3[0] + m.distance_for_knee, t4[1])
    t14 = reflect_point_across_line(point=t12, line1=t3, line2=t4)
    t15 = reflect_point_across_line(point=t13, line1=t3, line2=t4)
    t15a = get_midpoint(t15, t9)
    t15b = get_perpendicular_point_from_line(line1=t15a, line2=t9, distance=7.5)

    t16 = divide_segment_into_parts(start=t5, end=t1, parts=4)[0]
    t16a = [
        t16[0] - (m.distance_from_t16 / sqrt(2)),
        t16[1] - (m.distance_from_t16 / sqrt(2)),
    ]
    t17 = (t16[0], t2[1])
    t18 = (t16[0], t0[1])
    t19 = get_midpoint(t16, t18)
    t20 = (t18[0] + 20, t18[1])
    t21 = (t20[0], t20[1] - 20)
    t22 = get_point_on_line_at_distance(
        line1=t20, line2=t11, distance=m.waist / 4 + 42.5, from_point=t21
    )
    t23 = (t9[0] - (t5[0] - t9[0]) / 2 - 8, t9[1])  # remove 8mm extra if loose
    t24 = (t23[0], t23[1] + 5)
    t25 = (t17[0] + m.hip / 4 + 15, t17[1])
    t26 = (t12[0] + 10, t12[1])
    t27 = (t13[0] + 10, t13[1])
    t28 = (t14[0] - 10, t14[1])
    t29 = (t15[0] - 10, t15[1])
    t29a = get_midpoint(t29, t24)
    t29b = get_perpendicular_point_from_line(line1=t29a, line2=t24, distance=12.5)
    t30, t31 = divide_segment_into_parts(start=t21, end=t22, parts=3)
    t30d = get_perpendicular_point_from_line(line1=t30, line2=t22, distance=120)
    t31d = get_perpendicular_point_from_line(line1=t31, line2=t22, distance=100)
    t30a = get_point_on_line_at_distance(line1=t30, line2=t22, distance=10)
    t30b = get_point_on_line_at_distance(line1=t30, line2=t22, distance=-10)
    t31a = get_point_on_line_at_distance(line1=t31, line2=t22, distance=10)
    t31b = get_point_on_line_at_distance(line1=t31, line2=t22, distance=-10)

    point_values = {
        name: tuple(value) for name, value in locals().items() if name.startswith("t")
    }
    metadata: dict[str, object] = {
        "named_points": {
            name[1:]: value
            for name, value in point_values.items()
            if name.startswith("t")
        }
    }
    return {**point_values, **metadata}
