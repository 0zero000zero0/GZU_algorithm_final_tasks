## GZU 数据结构与算法分析课程设计

基于PyQt6的两个几何算法可视化实现:
- 最近点对
    - 蛮力法
    - 分治法
- 凸包
  - 蛮力法
  - Graham's scan法

项目结构
Project
│  .gitignore
│  app.py
│  README.md
│  requirements.txt
│
├─ui
│  │  ui.ui
│  │  ui_logic.py
│  │  ui_ui.py
│  │  __init__.py
│
├─utils
│  │  closest_poionts.py
│  │  convex_hull.py
│  │  point.py
│  │  solver.py
│  │  __init__.py


### UI
UI文件夹中:
- ui.ui是通过Qt Designer设计的UI界面
- ui_ui.py是通过pyuic6工具生成的UI界面的Python代码
- ui_logic.py是UI界面的**逻辑实现**。

### Utils
Utils文件夹中:
- point.py是点的类，但是实际上没有使用
- solver是解决方案的基类
- closest_points.py是最近点对算法的实现,实现了蛮力法和分治法，使用的是继承`solver`实现了`cloest_pair_points_solver`
- convex_hull.py是凸包算法的实现,实现了蛮力法和Graham's scan法，使用的是继承`solver`实现了`convex_hull_solver`
