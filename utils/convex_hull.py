import itertools
from utils.solver import sovler
class convex_hull_solver(sovler):
    def __init__(self):
        super().__init__()

    def is_left_turn(self, p1, p2, p3):
        return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0]) > 0

    def brute_force(self, points):
        hull = []
        n = len(points)
        for i, j in itertools.combinations(range(n), 2):
            all_left = True
            for k in range(n):
                if k != i and k != j:
                    if not self.is_left_turn(points[i], points[j], points[k]):
                        all_left = False
                        break
            if all_left:
                hull.append((i, j))
            self.steps.append((i, j, all_left))
        return hull

    def graham_scan(self):
        pass