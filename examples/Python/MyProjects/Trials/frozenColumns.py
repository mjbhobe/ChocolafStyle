import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTableView, QHBoxLayout, QHeaderView
from PyQt5.QtCore import QAbstractTableModel, Qt


class MyTableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._data[0])


class FrozenTableView(QWidget):
    def __init__(self, data, frozen_columns):
        super().__init__()

        self.main_table = QTableView()
        self.frozen_table = QTableView()

        self.model = MyTableModel(data)
        self.main_table.setModel(self.model)
        self.frozen_table.setModel(self.model)

        # Set up frozen table
        self.frozen_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.frozen_table.verticalHeader().setVisible(False)
        self.frozen_table.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        for col in range(frozen_columns, self.model.columnCount()):
            self.frozen_table.hideColumn(col)

        # Set up main table
        self.main_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.main_table.verticalHeader().setVisible(False)
        for col in range(frozen_columns):
            self.main_table.hideColumn(col)

        layout = QHBoxLayout(self)
        layout.setSpacing(0)
        layout.addWidget(self.frozen_table)
        layout.addWidget(self.main_table)

        # Synchronize scrolling
        self.main_table.verticalScrollBar().valueChanged.connect(
            self.frozen_table.verticalScrollBar().setValue
        )
        self.frozen_table.verticalScrollBar().valueChanged.connect(
            self.main_table.verticalScrollBar().setValue
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    data = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
    window = FrozenTableView(data, 2)
    window.show()
    sys.exit(app.exec())
