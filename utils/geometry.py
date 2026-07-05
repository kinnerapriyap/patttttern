from __future__ import annotations

from math import hypot
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


def divide_segment_into_parts(start: Point, end: Point, parts: int) -> list[Point]:
    """Return equally spaced points dividing a segment into the requested number of parts."""
    if parts <= 1:
        return []

    step_x = (end[0] - start[0]) / parts
    step_y = (end[1] - start[1]) / parts
    return [(start[0] + step_x * i, start[1] + step_y * i) for i in range(1, parts)]


def get_point_on_line_at_distance(line1: Point, line2: Point, distance: float) -> Point:
    """Return a point on the line from line1 to line2 at the given distance from line1."""
    dx = line2[0] - line1[0]
    dy = line2[1] - line1[1]
    length = hypot(dx, dy)
    if length == 0:
        raise ValueError("line1 and line2 cannot be the same point")

    ratio = distance / length
    return (line1[0] + dx * ratio, line1[1] + dy * ratio)


def get_midpoint(line1: Point, line2: Point) -> Point:
    """Return the midpoint between two points."""
    return ((line1[0] + line2[0]) / 2, (line1[1] + line2[1]) / 2)


def get_perpendicular_point_from_line(
    line1: Point, line2: Point, distance: float
) -> Point:
    """Return a point offset perpendicularly from the line defined by line1 and line2."""
    dx = line2[0] - line1[0]
    dy = line2[1] - line1[1]
    if dx == 0 and dy == 0:
        raise ValueError("line1 and line2 cannot be the same point")

    length = hypot(dx, dy)
    if length == 0:
        raise ValueError("line1 and line2 cannot be the same point")

    normal_x = -dy / length
    normal_y = dx / length

    return (line1[0] + normal_x * distance, line1[1] + normal_y * distance)


def get_french_curve_length(points: Sequence[Point], k: float) -> float:
    """Estimate the length of a french-curve path from its control points."""
    if len(points) < 2:
        return 0.0

    def bezier_point(p0: Point, p1: Point, p2: Point, p3: Point, t: float) -> Point:
        mt = 1 - t
        return (
            mt * mt * mt * p0[0]
            + 3 * mt * mt * t * p1[0]
            + 3 * mt * t * t * p2[0]
            + t * t * t * p3[0],
            mt * mt * mt * p0[1]
            + 3 * mt * mt * t * p1[1]
            + 3 * mt * t * t * p2[1]
            + t * t * t * p3[1],
        )

    total = 0.0
    samples = 100
    for i in range(len(points) - 1):
        p0 = points[i - 1] if i > 0 else points[i]
        p1 = points[i]
        p2 = points[i + 1]
        p3 = points[i + 2] if i + 2 < len(points) else points[i + 1]

        c1 = (p1[0] + (p2[0] - p0[0]) / k, p1[1] + (p2[1] - p0[1]) / k)
        c2 = (p2[0] - (p3[0] - p1[0]) / k, p2[1] - (p3[1] - p1[1]) / k)

        prev = bezier_point(p1, c1, c2, p2, 0.0)
        for step in range(1, samples + 1):
            t = step / samples
            current = bezier_point(p1, c1, c2, p2, t)
            total += hypot(current[0] - prev[0], current[1] - prev[1])
            prev = current

    return total
