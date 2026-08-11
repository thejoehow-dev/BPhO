## BPhO Computational Challenge 2026 - Quantum Mechanics

Our entry into the BPhO 2026 Computational Challenge

If you haven't yet, watch [our video](https://youtu.be/iYlwVAAoyEA).

---

### Running our program

Our master file dynamically finds all tasks the task from folders. It can be ran with missing tasks.

All task scripts can be run on their own (excluding the helper scripts e.g. task2.py as it requires task2_2D.py and task2_3D.py).

To make running individual tasks easier you can download individual tasks from the [standalone code folder](https://github.com/thejoehow-dev/BPhO/tree/main/standalone%20code). The files in this folder are designed to run on their own, e.g. without use of image files.

### Imports Needed

| **Task**          |**Imports**| **pip command** |
| :---------------- | :------- | :------- |
| Task 1, 2, 5, 6, 7           | matplotlib, numpy (installed by matplotlib) | pip install matplotlib |
| Task 3, 4, 9            | matplotlib, numpy (installed by matplotlib), customtkinter | pip install matplotlib customtkinter |
| Task 8            | customtkinter | pip install customtkinter |
| Task 10           | matplotlib, numpy (installed by matplotlib), customtkinter, mayavi, pyqt5, scipy | pip install matplotlib customtkinter mayavi pyqt5 scipy |

* master.py requires customtkinter if not installed
