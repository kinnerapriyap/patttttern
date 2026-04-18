def reflect_point_across_line(p, a, b):
    dx, dy = [b[0] - a[0], b[1] - a[1]]
    den = dx * dx + dy * dy
    if den == 0:
        return [p[0], p[1]]

    t = ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / den
    q = [a[0] + t * dx, a[1] + t * dy]
    return [2 * q[0] - p[0], 2 * q[1] - p[1]]

