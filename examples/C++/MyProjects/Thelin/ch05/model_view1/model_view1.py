# model_view1.py
import sys
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi()

    def setupUi(self):
        self.tree = QTreeView()
        self.list = QListView()
        self.table = QTableView()
        self.splitter = QSplitter()

        self.splitter.addWidget(self.tree)
        self.splitter.addWidget(self.list)
        self.splitter.addWidget(self.table)

        self.model = QStandardItemModel(5, 2)
        for r in range(5):
            for c in range(3):
                data = f"Row:{r}, Col:{c}"
                item = QStandardItem(data)

                if c == 0:
                    for i in range(3):
                        child = QStandardItem(f"Item {i}")
                        child.setEditable(False)
                        item.appendRow(child)

                self.model.setItem(r, c, item)

        self.model.setHorizontalHeaderItem(0, QStandardItem("Name"))
        self.model.setHorizontalHeaderItem(1, QStandardItem("Address"))
        self.model.setHorizontalHeaderItem(2, QStandardItem("Phone"))

        self.tree.setModel(self.model)
        self.list.setModel(self.model)
        self.table.setModel(self.model)

        self.list.setSelectionModel(self.tree.selectionModel())
        self.table.setSelectionModel(self.tree.selectionModel())

        self.layout = QVBoxLayout()        
        self.layout.addWidget(self.splitter)
        self.setLayout(self.layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    win = MainWindow()
    win.setWindowTitle(f"PyQt{PYQT_VERSION_STR} - Model View Example")
    win.show()

    sys.exit(app.exec())

