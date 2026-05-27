from __future__ import annotations

import math
from typing import Iterable, Union
from math import acos, degrees, sqrt

Point = Union[tuple[float, float], list[float]]
Shape = tuple


def angle_between(line1, line2):
    a1, a2 = line1
    b1, b2 = line2

    v1 = [a2[0] - a1[0], a2[1] - a1[1]]
    v2 = [b2[0] - b1[0], b2[1] - b1[1]]

    mag1 = sqrt(v1[0] ** 2 + v1[1] ** 2)
    mag2 = sqrt(v2[0] ** 2 + v2[1] ** 2)
    if mag1 == 0 or mag2 == 0:
        return 0.0

    dot = v1[0] * v2[0] + v1[1] * v2[1]
    cos_theta = dot / (mag1 * mag2)

    cos_theta = max(-1.0, min(1.0, cos_theta))
    return degrees(acos(cos_theta))


def rotate_point(point: Point, pivot: Point, rotation_angle: float) -> list[float]:
    angle = math.radians(rotation_angle)
    px, py = pivot[0], pivot[1]
    x, y = point[0], point[1]

    tx = x - px
    ty = y - py

    rx = tx * math.cos(angle) - ty * math.sin(angle)
    ry = tx * math.sin(angle) + ty * math.cos(angle)

    return [rx + px, ry + py]


def rotate_shape(shape: Shape, pivot: Point, rotation_angle: float) -> Shape:
    kind = shape[0]

    if kind in ("line", "dash"):
        _, a, b = shape
        return kind, rotate_point(a, pivot, rotation_angle), rotate_point(b, pivot, rotation_angle)

    if kind == "polyline":
        _, pts = shape
        return kind, [rotate_point(p, pivot, rotation_angle) for p in pts]

    if kind == "curve":
        _, start, end, k = shape
        return kind, rotate_point(start, pivot, rotation_angle), rotate_point(end, pivot, rotation_angle), k

    if kind == "french_curve":
        _, pts, k = shape
        return kind, [rotate_point(p, pivot, rotation_angle) for p in pts], k

    if kind == "circle":
        _, named_pts = shape
        rotated_named = {
            name: rotate_point(point, pivot, rotation_angle)
            for name, point in named_pts.items()
        }
        return kind, rotated_named

    return shape


def rotate_shapes(shapes: Iterable[Shape], pivot: Point, rotation_angle: float) -> list[Shape]:
    return [rotate_shape(shape, pivot, rotation_angle) for shape in shapes]
