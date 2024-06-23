from functools import partial
from PyQt6 import QtWidgets, QtCore, QtGui
import sys
from ui.ui_ui import Ui_Base
from PyQt6.QtWidgets import QMessageBox
from utils.closest_poionts import cloest_pair_points_solver
from utils.convex_hull import convex_hull_solver


class main_ui(QtWidgets.QWidget, Ui_Base):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)  # 初始化UI组件
        self.ui_init()  # 自定义的初始化方法
        self.points = []
        self.messge = QMessageBox()
        self.messge.resize(200, 100)
        self.solver = None
        self.points_=[]
        self.lines=[]
        self.rects=[]

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
        self.x_range = self.x_max - self.x_min-1
        self.y_range = self.y_max - self.y_min-1
        # 绘制二维坐标系
        self.draw_coordinate_system()

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
            screen_x = (x - self.x_min) / self.x_range * self.graphics_view_width
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
                screen_x = (x - self.x_min) / self.x_range * self.graphics_view_width
                self.scene.addText(f"{x}", font).setPos(
                    screen_x, self.graphics_view_height / 2 + 5
                )
        for y in range(self.y_min, self.y_max + 1):
            if y != 0:
                screen_y = (
                    self.graphics_view_height
                    - (y - self.y_min) / self.y_range * self.graphics_view_height
                )
                self.scene.addText(f"{y}", font).setPos(
                    self.graphics_view_width / 2 + 5, screen_y
                )

    def convert_coordinates(self, p):
        x,y=p
        screen_x = (x - self.x_min) / self.x_range * self.graphics_view_width
        screen_y = (
            self.graphics_view_height
            - (y - self.y_min) / self.y_range * self.graphics_view_height
        )
        return (screen_x, screen_y)



    #画点
    def draw_point(self, p, color=QtCore.Qt.GlobalColor.red, radius=4):
        screen_x, screen_y = self.convert_coordinates(p)
        ellipse = QtWidgets.QGraphicsEllipseItem(
            screen_x - radius, screen_y - radius, 2 * radius, 2 * radius
        )
        ellipse.setBrush(QtGui.QBrush(color))
        self.scene.addItem(ellipse)
        self.points_.append(ellipse)


    #画线
    def draw_line(self, p1, p2, color=QtCore.Qt.GlobalColor.blue, width=2):
        screen_x1, screen_y1 = self.convert_coordinates(p1)
        screen_x2, screen_y2 = self.convert_coordinates(p2)
        pen = QtGui.QPen(color, width)
        line = QtWidgets.QGraphicsLineItem(screen_x1, screen_y1, screen_x2, screen_y2)
        line.setPen(pen)
        self.scene.addItem(line)
        self.lines.append(line)
    #画矩形
    def draw_rectangle(
        self, p1, p2, color=QtCore.Qt.GlobalColor.green, width=2
    ):
        screen_x1, screen_y1 = self.convert_coordinates(p1)
        screen_x2, screen_y2 = self.convert_coordinates(p2)
        pen = QtGui.QPen(color, width)
        rectangle = QtWidgets.QGraphicsRectItem(
            screen_x1, screen_y1, screen_x2 - screen_x1, screen_y2 - screen_y1
        )
        rectangle.setPen(pen)
        self.scene.addItem(rectangle)
        self.rects.append(rectangle)



    def __str__(self) -> str:
        print(f"Points:")
        for point in self.points:
            print(f"({point[0]}, {point[1]})")
        print("=====================================")
        return ""

    def start_clicked(self):
        self.points = self.plainTextEdit.toPlainText().strip()
        self.points = self.points.split("\n")
        if len(self.points) > 2:
            self.points = [point.strip().split() for point in self.points]
            self.points = [(float(point[0]), float(point[1])) for point in self.points]
            print(self)
            #选择的算法
            self.choose = self.chooses.currentIndex()
            match self.choose:
                case 0:
                    self.solver = cloest_pair_points_solver()
                    self.solver.brute_force(self.points)
                case 1:
                    self.solver = cloest_pair_points_solver()
                    self.solver.recursive(self.points)
                case 2:
                    self.solver = convex_hull_solver()
                    self.solver.brute_force(self.points)
                case 3:
                    self.solver = convex_hull_solver()
                    self.solver.graham_scan(self.points)
                case _:
                    print("error")
                    pass
        else:
            # self.please_input.setText("请至少输入两点")
            # self.please_input.show()
            pass

        self.draw_coordinate_system()
        #测试，传入点
        # self.draw_point([1, 1])
        # self.draw_line([2, 2], [6, 4])
        # self.draw_rectangle([3, 2], [4, 1])
        for point in self.points:
            self.draw_point(point)
        return

    def quit_clicked(self):
        sys.exit()

    def clear_clicked(self):
        self.plainTextEdit.clear()
        self.result.clear()
        if self.solver is not None:
            self.solver.clear()
        self.scene.clear()

    def pre_step_clicked(self):
        try:
            self.solver.current_step -= 1
            states = self.solver.steps[self.solver.current_step]
            p1 = (states[0][0], states[0][1])
            p2 = (states[1][0], states[1][1])
            match self.choose:
                case 0:
                    self.result.appendPlainText(
                        f"点({p1[0],p1[1]})和点{p2[0],p2[1]}的距离为{states[2]}")
                    self.scene.removeItem(self.lines[-1])
                    self.lines.pop()
                    pass
                case 1:
                    pass
                case 2:
                    pass
                case 3:
                    pass
                case _:
                    print("error")
                    pass

        except IndexError:

            self.messge.setText('已经是开始了')
            self.messge.show()
        pass
    def next_step_clicked(self):
        try:
            states = self.solver.steps[self.solver.current_step]
            p1 = (states[0][0], states[0][1])
            p2 = (states[1][0], states[1][1])
            match self.choose:
                case 0:
                    self.result.appendPlainText(
                        f"点({p1[0],p1[1]})和点{p2[0],p2[1]}的距离为{states[2]}")
                    self.draw_line(p1,p2)
                    pass
                case 1:
                    pass
                case 2:
                    pass
                case 3:
                    pass
                case _:
                    print("error")
                    pass
            self.solver.current_step+=1
        except IndexError:
            self.messge.setText('已经是最后一步')
            self.messge.show()
        pass
