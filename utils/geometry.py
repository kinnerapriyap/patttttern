from __future__ import annotations

from typing import Sequence, Tuple

Point = Tuple[float, float]


def get_horizontal_intersection_with_line(
    y: float, line1: Point, line2: Point
) -> Point:
    """Return the intersection of a horizontal line at y with the line through line1 and line2."""
    x1, y1 = line1
    x2, y2 = line2
    if y2 == y1:
        return (x1, y)
    t = (y - y1) / (y2 - y1)
    return (x1 + t * (x2 - x1), y)


def get_perpendicular_intersection_with_line(
    point: Point, line1: Point, line2: Point
) -> Point:
    """Return the intersection of a perpendicular line through point with the line through line1 and line2."""
    x0, y0 = point
    x1, y1 = line1
    x2, y2 = line2

    dx = x2 - x1
    dy = y2 - y1
    if dx == 0 and dy == 0:
        raise ValueError("line1 and line2 cannot be the same point")

    t = ((x0 - x1) * dx + (y0 - y1) * dy) / (dx * dx + dy * dy)
    return (x1 + t * dx, y1 + t * dy)


def reflect_point_across_line(p, a, b):
    dx, dy = [b[0] - a[0], b[1] - a[1]]
    den = dx * dx + dy * dy
    if den == 0:
        return [p[0], p[1]]

    t = ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / den
    q = [a[0] + t * dx, a[1] + t * dy]
    return [2 * q[0] - p[0], 2 * q[1] - p[1]]
