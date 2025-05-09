from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableView,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QStandardItemModel, QStandardItem


class FrozenTable(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Frozen Columns in QTableView")
        self.setGeometry(100, 100, 800, 400)

        # Create main widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)

        # Create Data Model
        self.model = self.create_model()

        # Create Table Views
        self.frozen_table = QTableView(self)  # Left frozen columns
        self.main_table = QTableView(self)  # Main table

        # Set models
        self.frozen_table.setModel(self.model)
        self.main_table.setModel(self.model)

        # Freeze first 2 columns
        self.frozen_table.setColumnWidth(0, 100)
        self.frozen_table.setColumnWidth(1, 100)
        self.frozen_table.setFixedWidth(200)  # Width of 2 frozen columns

        # Hide horizontal scrolling in frozen table
        self.frozen_table.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        # Hide first 2 columns in main table (so they don't appear twice)
        self.main_table.setColumnHidden(0, True)
        self.main_table.setColumnHidden(1, True)

        # Sync vertical scrolling
        self.frozen_table.verticalScrollBar().valueChanged.connect(
            self.main_table.verticalScrollBar().setValue
        )
        self.main_table.verticalScrollBar().valueChanged.connect(
            self.frozen_table.verticalScrollBar().setValue
        )

        # Add tables to layout
        layout.addWidget(self.frozen_table)
        layout.addWidget(self.main_table)

    def create_model(self):
        """Create a sample model with data."""
        model = QStandardItemModel(10, 5)  # 10 rows, 5 columns
        model.setHorizontalHeaderLabels([f"Col {i}" for i in range(5)])

        for row in range(10):
            for col in range(5):
                item = QStandardItem(f"({row},{col})")
                model.setItem(row, col, item)

        return model


if __name__ == "__main__":
    app = QApplication([])
    window = FrozenTable()
    window.show()
    app.exec()
