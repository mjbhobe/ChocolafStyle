# basic.py - hello world with PySide6
import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QMessageBox,
    QHBoxLayout,
    QWidget,
)


class MainWindow(QMainWindow):
    """the main window of the application"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("My first QMainWindow")

        self.button = QPushButton("Click Me!")
        self.checkable_button = QPushButton("Checkable")
        self.checkable_button.setCheckable(True)
        # close this window when button is clicked
        self.button.clicked.connect(self.buttonClicked)
        self.checkable_button.clicked.connect(self.checkableButtonClicked)

        widget = QWidget()
        layout = QHBoxLayout()
        layout.addWidget(self.checkable_button)
        layout.addWidget(self.button)
        widget.setLayout(layout)

        self.setCentralWidget(widget)

    def checkableButtonClicked(self):
        if self.checkable_button.isChecked():
            self.checkable_button.setText("Checked")
        else:
            self.checkable_button.setText("Unchecked")

    def buttonClicked(self):
        """the slot for "Click Me" button"""
        resp = QMessageBox.warning(
            self,
            "Confirm Close",
            "Clicking this button will close the application\n" "Ok to close?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if resp == QMessageBox.StandardButton.Yes:
            self.close()


def main():
    # Step1: create an instance of QApplication
    app: QApplication = QApplication(sys.argv)

    # create the gui
    win = MainWindow()
    win.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
