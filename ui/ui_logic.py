from functools import partial
from PyQt6 import QtWidgets
import sys
from ui.ui_ui import Ui_Base
from PyQt6.QtWidgets import QMessageBox
from utils.closest_poionts import cloest_pair_points_solver
from utils.convex_hull import convex_hull_solver


class main_ui(QtWidgets.QWidget, Ui_Base):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)  # 初始化UI组件
        self.ui_init()     # 自定义的初始化方法
        self.points  = []
        self.please_input=QMessageBox()
        self.please_input.resize(200, 100)
        self.solver= None


    def ui_init(self):
        self.start.clicked.connect(self.start_clicked)
        self.quit.clicked.connect(self.quit_clicked)
        self.clear.clicked.connect(self.clear_clicked)

    def __str__(self) -> str:
        print(f"Points:")
        for point in self.points :
            print(f"({point[0]}, {point[1]})")
        print("=====================================")
        return ""

    def start_clicked(self):
        self.points  = self.plainTextEdit.toPlainText().strip()
        self.points  = self.points.split("\n")
        if len(self.points) < 2:
            self.please_input.setText("请至少输入两点")

            self.please_input.show()
            return
        self.points  = [point.split() for point in self.points ]
        self.points  = [(float(point[0]), float(point[1])) for point in self.points ]
        print(self)
        choose=self.chooses.currentIndex()
        match choose:
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
                print('error')
                pass
        return

    def quit_clicked(self):
        sys.exit()

    def clear_clicked(self):
        self.plainTextEdit.clear()
        self.result.clear()
        if self.solver is not None:
            self.solver.clear()

    def pre_step_clicked(self):
        pass

    def next_step_clicked(self):
        pass