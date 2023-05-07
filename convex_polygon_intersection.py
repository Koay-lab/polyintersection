import random
import math

from .edge import get_edges


def polyintersect(polygon1, polygon2, tolerance=None):
    """
    The given polygons must be convex and their vertices must be in anti-clockwise order (this is not checked!)

    Example: polygon1 = [[0,0], [0,1], [1,1]]

    """
    # Degenerate cases where one or both of the polygons is a point
    if len(polygon1) < 2 or len(polygon2) < 2:
        return []

    polygon3 = list()
    polygon3 += _get_vertices_lying_in_the_other_polygon(polygon1, polygon2, tolerance or 0)
    polygon3 += _get_edge_intersection_points(polygon1, polygon2)
    return _sort_vertices_anti_clockwise_and_remove_duplicates(polygon3, tolerance or 1e-7)


def _nondegenerate_polygon(polygon, tolerance=1e-7):
    if len(polygon) < 3:
        return False

    pi = polygon[-1]
    pj = polygon[0]
    signed_area = pi[0] * pj[1] - pj[0] * pi[1]
    for pi, pj in zip(polygon[:-1], polygon[1:]):
        signed_area += pi[0] * pj[1] - pj[0] * pi[1]

    return abs(signed_area) > tolerance

def _get_vertices_lying_in_the_other_polygon(polygon1, polygon2, tolerance=0):
    vertices = list()
    if _nondegenerate_polygon(polygon2):
        vertices += [vertex for vertex in polygon1 if _polygon_contains_point(polygon2, vertex, tolerance)]
    if _nondegenerate_polygon(polygon1):
        vertices += [vertex for vertex in polygon2 if _polygon_contains_point(polygon1, vertex, tolerance)]
    return vertices


def _get_edge_intersection_points(polygon1, polygon2):
    intersection_points = list()
    for edge1 in get_edges(polygon1):
        for edge2 in get_edges(polygon2):
            intersection_point = edge1.get_intersection_point(edge2)
            if intersection_point is not None:
                intersection_points.append(intersection_point)
    return intersection_points


def _polygon_contains_point(polygon, point, tolerance=0):
    for i in range(len(polygon)):
        # a = np.subtract(polygon[i], polygon[i - 1])
        # b = np.subtract(point, polygon[i - 1])
        # if np.cross(a, b) < 0:
        #     return False

        a = polygon[i] - polygon[i - 1]
        b = point - polygon[i - 1]
        if a[0] * b[1] - a[1] * b[0] < -tolerance:
            return False
    return True


def _sort_vertices_anti_clockwise_and_remove_duplicates(polygon, tolerance=1e-7):
    polygon = sorted(polygon, key=lambda p: _get_angle_in_radians(_get_bounding_box_midpoint(polygon), p))

    def vertex_not_similar_to_previous(_polygon, i):
        # diff = np.subtract(_polygon[i - 1], _polygon[i])
        # return np.linalg.norm(diff, np.inf) > tolerance
        diff = _polygon[i - 1] - _polygon[i]
        return any((abs(x - y) > tolerance for x, y in zip(_polygon[i - 1], _polygon[i])))

    vertices = [p for i, p in enumerate(polygon) if vertex_not_similar_to_previous(polygon, i)]
    if len(vertices) > 2 and not _nondegenerate_polygon(vertices):
        print(vertices)
    return [p for i, p in enumerate(polygon) if vertex_not_similar_to_previous(polygon, i)]


def _get_angle_in_radians(point1, point2):
    return math.atan2(point2[1] - point1[1], point2[0] - point1[0])


def _get_bounding_box_midpoint(polygon):
    x = [p[0] for p in polygon]
    y = [p[1] for p in polygon]
    return [(max(x) + min(x)) / 2., (max(y) + min(y)) / 2.]


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import numpy as np
    import wx
    import wx_tools

    def generate_random_convex_polygon():
        return _sort_vertices_anti_clockwise_and_remove_duplicates(
            # [[np.cos(x), np.sin(x)] for x in np.random.rand(random.randint(3, 6)) * 2 * np.pi]
            [wx.Point2D(math.cos(x), math.sin(x)) for x in np.random.rand(random.randint(3, 6)) * 2 * np.pi]
        )


    def plot_polygon(polygon):
        if polygon:
            _polygon = list(polygon)
            _polygon.append(_polygon[0])
            x, y = zip(*_polygon)
            plt.plot(x, y, 'o-')
            plt.fill(x, y, alpha=0.25)


    polygon1 = generate_random_convex_polygon()
    polygon2 = generate_random_convex_polygon()
    polygon3 = polyintersect(polygon1, polygon2)

    plot_polygon(polygon1)
    plot_polygon(polygon2)
    plot_polygon(polygon3)
    plt.show()
