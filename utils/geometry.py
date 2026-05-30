from __future__ import annotations

from typing import Sequence, Tuple

Point = Tuple[float, float]


def get_horizontal_intersection_with_line(y: float, line1: Point, line2: Point) -> Point:
    """Return the intersection of a horizontal line at y with the line through line1 and line2."""
    x1, y1 = line1
    x2, y2 = line2
    if y2 == y1:
        return (x1, y)
    t = (y - y1) / (y2 - y1)
    return (x1 + t * (x2 - x1), y)
