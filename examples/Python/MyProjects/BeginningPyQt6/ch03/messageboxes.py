""" messageboxes.py - display usage of QMessageBox """
import sys
import os

# os.environ["QT_API"] = "pyqt6"

from PyQt6.QtCore import PYQT_VERSION_STR, Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtGui import QFont

AppDir = os.path.dirname(__file__)
import chocolaf


class MainWindow(QWidget):
    def __init__(self, parent: QWidget = None):
        super(MainWindow, self).__init__(parent)
        self.initializeUi()

    def initializeUi(self):
        self.setGeometry(200, 100, 340, 140)
        self.setWindowTitle(f"PyQt {PYQT_VERSION_STR} MessageBoxes")
        self.setupMainWindow()

    def setupMainWindow(self):
        """ setup widgets & connect signals/slots """
        catalogue_label = QLabel("Author Catalogue", self)
        catalogue_label.setFont(QFont("Arial", 16))
        catalogue_label.move(80, 10)

        search_label = QLabel("Search the index for an author", self)
        search_label.move(40, 40)

        author_label = QLabel("Name:", self)
        author_label.move(20, 74)

        self.author_edit = QLineEdit(self)
        self.author_edit.move(70, 70)
        self.author_edit.resize(240, 24)
        self.author_edit.setPlaceholderText("Enter name as: First Last")

        search_button = QPushButton("Search", self)
        search_button.move(140, 100)
        search_button.clicked.connect(self.searchAuthors)

    def searchAuthors(self):
        """ search for author name in authors file """
        try:
            authors_file_path = os.path.join(AppDir, "files/authors.txt")
            with open(authors_file_path, "r") as f:
                authors = [line.rstrip("\n").strip() for line in f]

            if self.author_edit.text() in authors:
                QMessageBox.information(self, "Author found!",
                                        f"Author {self.author_edit.text()} found in catalogue",
                                        QMessageBox.StandardButton.Ok)
            else:
                answer = QMessageBox.question(self, "Author not found",
                                              """<p>Author not found in catalogue</p>
                                                 <p>Do you wish to continue?</p>""",
                                              QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                              QMessageBox.StandardButton.No)
                if answer == QMessageBox.StandardButton.No:
                    print("Closing application")
                    self.close()
        except FileNotFoundError as error:
            QMessageBox.warning(self, "Error",
                                f"""<p>File not found</p>
                                    <p>Error: {error}</p>
                                    Closing application.""",
                                QMessageBox.StandardButton.Ok)
            self.close()


def main():
    chocolaf.enable_hi_dpi()
    # app = chocolaf.ChocolafApp(sys.argv)
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # create the main window
    win = MainWindow()
    win.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
