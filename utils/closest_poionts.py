import numpy as np

class cloest_pair_points_solver:
    def __init__(self) -> None:
        self.steps = []

    def distance(self,p1, p2):
        return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

    def brute_force(self,points):
        min_dist = float('inf')
        closest_pair = (None, None)

        n = len(points)
        for i in range(n):
            for j in range(i + 1, n):
                dist = self.distance(points[i], points[j])
                self.steps.append((points[i], points[j], dist))
                if dist < min_dist:
                    min_dist = dist
                    closest_pair = (points[i], points[j])

        return closest_pair, min_dist

    def recursive(self,points):
        n = len(points)
        if n <= 3:
            # 使用蛮力法解决小规模问题
            min_dist = float('inf')
            closest_pair = (None, None)
            for i in range(n):
                for j in range(i + 1, n):
                    dist = self.distance(points[i], points[j])
                    self.steps.append((points[i], points[j], dist))
                    if dist < min_dist:
                        min_dist = dist
                        closest_pair = (points[i], points[j])
            return closest_pair, min_dist

        # 分治法
        mid = n // 2
        mid_point = points[mid]

        # 递归解决左右子集
        left_closest_pair, left_min_dist = self.recursive(points[:mid])
        right_closest_pair, right_min_dist = self.recursive(points[mid:])

        # 找到左右子集的最近点对
        if left_min_dist < right_min_dist:
            min_dist = left_min_dist
            closest_pair = left_closest_pair
        else:
            min_dist = right_min_dist
            closest_pair = right_closest_pair

        # 检查跨越分割线的点对
        strip = []
        for i in range(n):
            if abs(points[i][0] - mid_point[0]) < min_dist:
                strip.append(points[i])

        # 以y坐标排序
        strip.sort(key=lambda point: point[1])

        for i in range(len(strip)):
            for j in range(i + 1, len(strip)):
                if strip[j][1] - strip[i][1] >= min_dist:
                    break
                dist = self.distance(strip[i], strip[j])
                self.steps.append((strip[i], strip[j], dist))
                if dist < min_dist:
                    min_dist = dist
                    closest_pair = (strip[i], strip[j])

        return closest_pair, min_dist


    def closest_pair(self,points):
        points.sort(key=lambda point: point[0])
        return self.recursive(points)

    def clear(self):
        self.steps = []

if __name__ == '__main__':
    points = np.array([[0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, 5]])
    solver=cloest_pair_points_solver()
    closest_pair, min_dist = solver.brute_force(points)
    print("Closest pair:", closest_pair)
    print("Minimum distance:", min_dist)
    print("Steps:")
    for step in solver.steps:
        print(f"Points: {step[0]}, {step[1]}, Distance: {step[2]}")
