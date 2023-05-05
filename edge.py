from collections.abc import Iterable

def get_edges(polygon):
    """
    :param polygon: a list of points (point = list or tuple holding two numbers)
    :return: the edges of the polygon, i.e. all pairs of points
    """
    for i in range(len(polygon)):
        yield Edge(polygon[i - 1], polygon[i])


class Edge:
    def __init__(self, point_a, point_b):
        self._support_vector = point_a
        self._direction_vector = point_b - point_a

    def get_intersection_point(self, other):
        t = self._get_intersection_parameter(other)
        return None if t is None else self._get_point(t)

    def intersects(self, other):
        if isinstance(other, Iterable):
            return type(other)((self.intersects(x) for x in other))
        return self._get_intersection_parameter(other) is not None

    def _get_point(self, parameter):
        return self._support_vector + self._direction_vector * parameter

    def _get_intersection_parameter(self, other):
        # A = np.array([-self._direction_vector, other._direction_vector]).T
        # if np.linalg.matrix_rank(A) < 2:
        #     return None
        # b = np.subtract(self._support_vector, other._support_vector)
        # x = np.linalg.solve(A, b)
        # return x[0] if 0 <= x[0] <= 1 and 0 <= x[1] <= 1 else None

        det = self._direction_vector[1] * other._direction_vector[0] \
              - self._direction_vector[0] * other._direction_vector[1]
        if det == 0:
            return None

        b = self._support_vector - other._support_vector
        x0 = (other._direction_vector[1] * b[0] - other._direction_vector[0] * b[1]) / det
        x1 = (self._direction_vector[1] * b[0] - self._direction_vector[0] * b[1]) / det

        return x0 if 0 <= x0 <= 1 and 0 <= x1 <= 1 else None
