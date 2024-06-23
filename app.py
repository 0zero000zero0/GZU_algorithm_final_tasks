# -*- coding: utf-8 -*-
from functools import partial
from PyQt6 import QtWidgets
import sys
from PyQt6.QtWidgets import QApplication
from ui.ui_logic import main_ui


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    ui = main_ui()
    main_window.setCentralWidget(ui)
    main_window.show()
    main_window.setWindowTitle("几何:最近点对与凸包")
    main_window.setGeometry(400, 200, 1066, 742)
    sys.exit(app.exec())
