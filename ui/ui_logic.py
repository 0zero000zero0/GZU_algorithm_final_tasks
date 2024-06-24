from functools import partial
from PyQt6 import QtWidgets, QtCore, QtGui
import sys
from ui.ui_ui import Ui_Base
from PyQt6.QtWidgets import QMessageBox
from utils.closest_poionts import cloest_pair_points_solver
from utils.convex_hull import convex_hull_solver
from typing import overload


class main_ui(QtWidgets.QWidget, Ui_Base):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)  # 初始化UI组件
        self.ui_init()  # 自定义的初始化方法
        self.points = []
        self.messge = QMessageBox()
        self.messge.resize(200, 100)
        self.solver = None
        self.points_ = []
        self.lines = []
        self.rects = []

    def __str__(self) -> str:
        print(f"Points:")
        for point in self.points:
            print(f"({point[0]}, {point[1]})")
        print("=====================================")
        return ""

    def ui_init(self):
        self.start.clicked.connect(self.start_clicked)
        self.quit.clicked.connect(self.quit_clicked)
        self.clear.clicked.connect(self.clear_clicked)
        self.pre_step.clicked.connect(self.pre_step_clicked)
        self.next_step.clicked.connect(self.next_step_clicked)
        self.scene = QtWidgets.QGraphicsScene()
        self.graphicsView.setScene(self.scene)
        self.graphicsView.resize(800, 600)
        # 坐标范围
        self.x_min, self.x_max = -10, 12
        self.y_min, self.y_max = -10, 12
        self.graphics_view_width = self.graphicsView.width()
        self.graphics_view_height = self.graphicsView.height()
        self.x_range = self.x_max - self.x_min - 2
        self.y_range = self.y_max - self.y_min - 2
        # 绘制二维坐标系
        self.draw_coordinate_system()

    # ======================================================================
    def draw_coordinate_system(self):
        # 场景范围
        self.scene.setSceneRect(
            0, 0, self.graphics_view_width, self.graphics_view_height
        )
        pen = QtGui.QPen(QtCore.Qt.GlobalColor.black, 2)
        self.scene.addLine(
            0,
            self.graphics_view_height / 2,
            self.graphics_view_width,
            self.graphics_view_height / 2,
            pen,
        )  # x 轴
        self.scene.addLine(
            self.graphics_view_width / 2,
            0,
            self.graphics_view_width / 2,
            self.graphics_view_height,
            pen,
        )  # y 轴

        # 网格
        grid_pen = QtGui.QPen(
            QtCore.Qt.GlobalColor.gray, 1, QtCore.Qt.PenStyle.DashLine
        )

        # 垂直线条
        for x in range(self.x_min, self.x_max + 1):
            screen_x = (x - self.x_min) / self.x_range * \
                self.graphics_view_width
            self.scene.addLine(
                screen_x, 0, screen_x, self.graphics_view_height, grid_pen
            )
        # 水平线条
        for y in range(self.y_min, self.y_max + 1):
            screen_y = (
                self.graphics_view_height
                - (y - self.y_min) / self.y_range * self.graphics_view_height
            )
            self.scene.addLine(
                0, screen_y, self.graphics_view_width, screen_y, grid_pen
            )

        # 刻度和标签
        font = QtGui.QFont("微软雅黑", 8)
        for x in range(self.x_min, self.x_max + 1):
            if x != 0:
                screen_x = (x - self.x_min) / self.x_range * \
                    self.graphics_view_width
                self.scene.addText(f"{x}", font).setPos(
                    screen_x, self.graphics_view_height / 2 + 5
                )
        for y in range(self.y_min, self.y_max + 1):
            if y != 0:
                screen_y = (
                    self.graphics_view_height
                    - (y - self.y_min) / self.y_range *
                    self.graphics_view_height
                )
                self.scene.addText(f"{y}", font).setPos(
                    self.graphics_view_width / 2 + 5, screen_y
                )

    # 坐标变换，把坐标转换为屏幕坐标
    def convert_coordinates(self, p):
        x, y = p
        screen_x = (x - self.x_min) / self.x_range * self.graphics_view_width
        screen_y = (
            self.graphics_view_height
            - (y - self.y_min) / self.y_range * self.graphics_view_height
        )
        return (screen_x, screen_y)

    # 画点
    def draw_point(self, p: list[list[float]], color=QtCore.Qt.GlobalColor.red, radius=4):
        screen_x, screen_y = self.convert_coordinates(p)
        ellipse = QtWidgets.QGraphicsEllipseItem(
            screen_x - radius, screen_y - radius, 2 * radius, 2 * radius
        )
        ellipse.setBrush(QtGui.QBrush(color))
        self.scene.addItem(ellipse)
        self.points_.append(ellipse)

    # 画线
    def draw_line(self, p1: list[list[float]], p2: list[list[float]], color=QtCore.Qt.GlobalColor.blue, width=2):
        screen_x1, screen_y1 = self.convert_coordinates(p1)
        screen_x2, screen_y2 = self.convert_coordinates(p2)
        pen = QtGui.QPen(color, width)
        line = QtWidgets.QGraphicsLineItem(
            screen_x1, screen_y1, screen_x2, screen_y2)
        line.setPen(pen)
        self.scene.addItem(line)
        self.lines.append(line)

    # 画矩形
    def draw_rectangle(self, p1: list[list[float]], p2: list[list[float]], color=QtCore.Qt.GlobalColor.green, width=2):
        screen_x1, screen_y1 = self.convert_coordinates(p1)
        screen_x2, screen_y2 = self.convert_coordinates(p2)
        pen = QtGui.QPen(color, width)
        rectangle = QtWidgets.QGraphicsRectItem(
            screen_x1, screen_y1, screen_x2 - screen_x1, screen_y2 - screen_y1
        )
        rectangle.setPen(pen)
        self.scene.addItem(rectangle)
        self.rects.append(rectangle)

    # ======================================================================

    def quit_clicked(self):
        sys.exit()

    def clear_clicked(self):
        self.plainTextEdit.clear()
        self.result.clear()
        if self.solver is not None:
            self.solver.clear()
        self.scene.clear()

    def start_clicked(self):
        self.draw_coordinate_system()
        self.points = self.plainTextEdit.toPlainText().strip()
        self.points = self.points.split("\n")
        if len(self.points) > 1:
            self.points = [point.strip().split() for point in self.points]
            self.points = [(float(point[0]), float(point[1]))
                           for point in self.points]
            print(self)
            for point in self.points:
                self.draw_point(point)
            # 选择的算法
            self.choose = self.chooses.currentIndex()
            # 0:最近点对(蛮力) 1:最近点对(递归) 2:凸包(蛮力) 3:凸包(扫描)
            match self.choose:
                case 0:
                    self.solver = cloest_pair_points_solver()
                    self.solver.brute_force(self.points)
                    self.result.appendHtml('<font color="red">结果:</font>')
                    self.result.appendHtml(
                        f'最近点对为<font color="red">{self.solver.result[0][0][0]}</font>和<font color="red">{self.solver.result[0][0][1]}</font>,距离为 <font color="red">{self.solver.result[0][1]}</font>'
                    )
                case 1:
                    self.solver = cloest_pair_points_solver()
                    self.solver.closest_pair(self.points)
                    self.result.appendHtml('<font color="red">结果:</font>')
                    self.result.appendHtml(
                        f'最近点对为<font color="red">{self.solver.result[0][0][0]}</font>和<font color="red">{self.solver.result[0][0][1]}</font>,距离为 <font color="red">{self.solver.result[0][1]}</font>'
                    )
                    # 分治线
                    for mid in self.solver.mids:
                        self.draw_line(
                            [mid[0], self.y_min], [mid[0], self.y_max], color=QtCore.Qt.GlobalColor.darkBlue)
                        self.result.appendPlainText(
                            f"分治线为 x={mid[0]}")
                case 2:
                    self.solver = convex_hull_solver()
                    self.solver.brute_force(self.points)
                case 3:
                    self.solver = convex_hull_solver()
                    self.solver.graham_scan(self.points)
                case _:
                    self.messge.setText("请选择算法")
                    self.messge.show()
        else:
            self.messge.setText("请至少输入两点")
            self.messge.show()
            pass

    def pre_step_clicked(self):
        try:
            match self.choose:
                case 0:
                    self.case0pre()
                    pass
                case 1:
                    self.case1pre()
                    pass
                case 2:
                    pass
                case 3:
                    pass
                case _:
                    print("error")
                    pass
        except IndexError:
            self.messge.setText("已经是最开始了")
            self.messge.show()
        pass

    def next_step_clicked(self):
        try:
            match self.choose:
                case 0:
                    self.case0next()
                    pass
                case 1:
                    self.case1next()
                    pass
                case 2:
                    pass
                case 3:
                    pass
                case _:
                    print("error")
                    pass
            self.solver.current_step += 1
        except IndexError:
            self.messge.setText("已经是最后一步")
            self.messge.show()
        pass

    # ======================================================================
    def case0next(self):
        states = self.solver.steps[self.solver.current_step]
        p1 = (states[0][0], states[0][1])
        p2 = (states[1][0], states[1][1])
        self.result.appendPlainText(
            f"点{p1[0],p1[1]}和点{p2[0],p2[1]}的距离为{states[2]}"
        )
        self.draw_line(p1, p2)

    def case0pre(self):
        self.solver.current_step -= 1
        states = self.solver.steps[self.solver.current_step]
        p1 = (states[0][0], states[0][1])
        p2 = (states[1][0], states[1][1])
        self.result.appendPlainText(
            f"点{p1[0],p1[1]}和点{p2[0],p2[1]}的距离为{states[2]}"
        )
        self.scene.removeItem(self.lines[-1])
        self.lines.pop()

    def case1next(self):
        states = self.solver.steps[self.solver.current_step]
        p1 = (states[0][0], states[0][1])
        p2 = (states[1][0], states[1][1])
        self.result.appendPlainText(
            f"点{p1[0],p1[1]}和点{p2[0],p2[1]}的距离为{states[2]}"
        )
        self.draw_line(p1, p2)

    def case1pre(self):
        self.solver.current_step -= 1
        states = self.solver.steps[self.solver.current_step]
        p1 = (states[0][0], states[0][1])
        p2 = (states[1][0], states[1][1])
        self.result.appendPlainText(
            f"点{p1[0],p1[1]}和点{p2[0],p2[1]}的距离为{states[2]}"
        )
        self.scene.removeItem(self.lines[-1])
        self.lines.pop()
