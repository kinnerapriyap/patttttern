from math import hypot

from utils import measurements as m
from utils.geometry import (
    divide_segment_into_parts,
    get_midpoint,
    get_perpendicular_point_from_line,
    get_point_on_line_at_distance,
)


def build_points():
    s1 = (0, 0)
    s2 = (m.hip / 2 + 15, 0)
    s3 = (0, m.skirt_length)
    s4 = (s2[0], s3[1])
    s5 = (0, m.waist_to_hip)
    s6 = (s2[0], s5[1])

    s7 = (m.hip / 4 + m.skirt_hip_ease, s5[1])
    s8 = (s7[0], s3[1])
    s9 = (m.waist / 4 + m.skirt_back_waist_ease, 0)
    s10 = (s9[0], -12.5)
    s11, s12 = divide_segment_into_parts(start=s1, end=s10, parts=3)
    s11a = get_point_on_line_at_distance(line1=s11, line2=s10, distance=10)
    s11b = get_point_on_line_at_distance(line1=s11, line2=s10, distance=-10)
    s12a = get_point_on_line_at_distance(line1=s12, line2=s10, distance=10)
    s12b = get_point_on_line_at_distance(line1=s12, line2=s10, distance=-10)
    s13 = get_perpendicular_point_from_line(line1=s11, line2=s10, distance=140)
    s14 = get_perpendicular_point_from_line(line1=s12, line2=s10, distance=125)
    s10a = get_midpoint(line1=s10, line2=s7)
    s10b = get_perpendicular_point_from_line(line1=s10a, line2=s7, distance=-5)

    s15 = (s2[0] - m.waist / 4 - m.skirt_front_waist_ease, 0)
    s16 = (s15[0], -12.5)
    _, s17 = divide_segment_into_parts(start=s2, end=s16, parts=3)
    s18 = get_perpendicular_point_from_line(line1=s17, line2=s2, distance=100)
    s17a = get_point_on_line_at_distance(line1=s17, line2=s16, distance=10)
    s17b = get_point_on_line_at_distance(line1=s17, line2=s16, distance=-10)
    s16a = get_midpoint(line1=s16, line2=s7)
    s16b = get_perpendicular_point_from_line(line1=s16a, line2=s7, distance=5)

    point_values = {
        name: tuple(value) for name, value in locals().items() if name.startswith("s")
    }
    metadata: dict[str, object] = {
        "named_points": {
            name[1:]: value
            for name, value in point_values.items()
            if name.startswith("s")
        }
    }
    return {**point_values, **metadata}
