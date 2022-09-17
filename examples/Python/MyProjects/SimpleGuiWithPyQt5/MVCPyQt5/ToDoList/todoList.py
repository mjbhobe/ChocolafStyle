# -*- coding: utf-8 -*-
"""
* todoList.py - a TO DO list using PyQt5 ModelView Controller
* 
* My experiments with Python, PyQt, Data Science & Deep Learning
* The code is made available for illustration purposes only.
* Use at your own risk!!

"""
import sys
import os
import json

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

from chocolaf.palettes import ChocolafPalette
from chocolaf.utils.chocolafapp import ChocolafApp

APP_PATH = os.path.dirname(__file__)
Window_Title = f"PyQt {PYQT_VERSION_STR} MVC - TODO List"

# add some custom styling above & beyond stysheet set
style_sheet = """
    QLabel#CanvasLabel {
        border: 2px dashed rgb(102, 102, 102);
    }
    QLabel {
        qproperty-alignment: AlignCenter;
    }
"""
TICK_IMAGE = QImage(os.path.join(APP_PATH, "tick.png"))
TODO_DATA_PATH = os.path.join(APP_PATH, "todos.json")


class ToDoModel(QAbstractListModel):
    def __init__(self, *args, todos=None, **kwargs):
        super(ToDoModel, self).__init__(*args, **kwargs)
        # list of tuples [(status1, todo1), (status2, todo2, ...]
        self.todos = todos or []

    def data(self, index, role):
        status, text = self.todos[index.row()]
        if role == Qt.DisplayRole:
            # what does view display in row?
            return text
        if role == Qt.DecorationRole:
            # what decorations/annotations to add during display
            if status:
                return TICK_IMAGE # show tick is status = True (or To Do is complete)

    def rowCount(self, index):
        return len(self.todos)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi(os.path.join(APP_PATH, "mainwindow.ui"))
        self.model = ToDoModel()
        self.load() # load the ToDos
        self.ui.todoView.setModel(self.model)
        self.ui.addButton.clicked.connect(self.addToDo)
        self.ui.deleteButton.clicked.connect(self.deleteToDo)
        self.ui.completeButton.clicked.connect(self.completeToDo)
        self.setWindowIcon(QIcon(os.path.join(APP_PATH, "todo.png")))

    def setupUi(self):
        pass

    def load(self) -> bool:
        try:
            with open(TODO_DATA_PATH, "r") as f:
                self.model.todos = json.load(f)
                return True
        except:
            return False

    def save(self) -> bool:
        try:
            with open(TODO_DATA_PATH, "w") as f:
                json.dump(self.model.todos, f)
                return True
        except:
            return False

    def addToDo(self):
        text = self.ui.todoEdit.text().strip()
        if len(text) != 0:
            # don't add blank text
            self.model.todos.append((False, text))
            self.model.layoutChanged.emit()
            self.ui.todoEdit.setText("")
            self.save()

    def deleteToDo(self):
        indexes = self.ui.todoView.selectedIndexes()
        if indexes:
            index = indexes[0]
            del self.model.todos[index.row()]
            self.model.layoutChanged.emit()
            self.ui.todoView.clearSelection()
            self.save()

    def completeToDo(self):
        indexes = self.ui.todoView.selectedIndexes()
        if indexes:
            row = indexes[0].row()
            _, text = self.model.todos[row]
            self.model.todos[row] = (True, text)
            self.model.dataChanged.emit(indexes[0], indexes[0])
            self.ui.todoView.clearSelection()
            self.save()


    def show(self):
        self.ui.show()


if __name__ == "__main__":
    app = ChocolafApp(sys.argv)
    #app.setStyle("Fusion")
    app.setStyle("Chocolaf")

    win = MainWindow()
    win.show()

    sys.exit(app.exec())
