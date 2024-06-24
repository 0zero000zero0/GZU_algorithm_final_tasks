## GZU 数据结构与算法分析课程设计

基于 PyQt6 的两个几何算法可视化实现:

- 最近点对
  - 蛮力法
  - 分治法
- 凸包
  - 蛮力法
  - Graham's scan 法

项目结构

```
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
```

### UI

UI 文件夹中:

- ui.ui 是通过 Qt Designer 设计的 UI 界面
- ui_ui.py 是通过 pyuic6 工具生成的 UI 界面的 Python 代码
- ui_logic.py 是 UI 界面的**逻辑实现**。

### Utils

Utils 文件夹中:

- point.py 是点的类，但是实际上没有使用
- solver 是解决方案的基类
- closest_points.py 是最近点对算法的实现,实现了蛮力法和分治法，使用的是继承`solver`实现了`cloest_pair_points_solver`
- convex_hull.py 是凸包算法的实现,实现了蛮力法和 Graham's scan 法，使用的是继承`solver`实现了`convex_hull_solver`

### RUN

```bash
pip install -r requirements.txt
python app.py
```
