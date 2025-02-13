import itertools
from utils.solver import sovler
import sys

class convex_hull_solver(sovler):
    def __init__(self):
        super().__init__()

    def is_left_turn(self, a, b, c):
        '''
        判断c是否在直线ab的左侧
        '''
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]) > 0

    def is_right_turn(self, a, b, c):
        '''
        判断p3是否在直线p1p2的右侧
        '''
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]) < 0

    def brute_force(self, points):
        hull = []
        n = len(points)
        def is_all_left(i, j):
            for k in points:
                if k != i and k != j:
                    if not self.is_left_turn(i, j, k):
                        return False
            return True

        def is_all_right(i, j):
            for k in points:
                if k != i and k != j:
                    if not self.is_right_turn(i, j, k):
                        return False
            return True
        for i, j in itertools.combinations(points, 2):
            all_left = is_all_left(i, j)
            all_right = is_all_right(i, j)
            self.steps.append((i, j, all_left or all_right))
            if all_left or all_right:
                hull.append((i,j))
        self.result = hull
        return hull

    def divide_and_conquer(self, points):
        if len(points) <= 1:
            return points
        # 按照x 排序
        min_point = min(points, key=lambda p: p[0])
        max_point = max(points, key=lambda p: p[0])

        def distance(p, a, b):
            # 点p到直线ab的距离
            return abs((b[0] - a[0]) * (a[1] - p[1]) - (a[0] - p[0]) * (b[1] - a[1]))

        def find_hull(points, p1, p2):
            # 在p1p2左侧的点集找凸包
            if len(points)==0:
                self.steps.append((p1, p2, True))
                return []
            farthest_point = max(points, key=lambda p: distance(p, p1, p2))
            left_set_p1_farthest = [
                p for p in points if self.is_left_turn(p1, farthest_point, p)]
            left_set_farthest_p2 = [
                p for p in points if self.is_left_turn(farthest_point, p2, p)]

            self.steps.append((p1,  p2, False))
            self.steps.append((p1, farthest_point, False))
            self.steps.append((p2, farthest_point, False))

            hull = find_hull(left_set_p1_farthest, p1, farthest_point) + \
                [farthest_point] + \
                find_hull(left_set_farthest_p2, farthest_point, p2)
            return hull
        left_set = [p for p in points if self.is_left_turn(
            min_point, max_point, p)]
        right_set = [p for p in points if self.is_left_turn(
            max_point, min_point, p)]

        hull = [min_point] + find_hull(left_set, min_point, max_point) + [
            max_point] + find_hull(right_set, max_point, min_point)

        self.result = hull
        return hull  # hull存储了最终凸包的所有点

    def graham_scan(self):
        pass
