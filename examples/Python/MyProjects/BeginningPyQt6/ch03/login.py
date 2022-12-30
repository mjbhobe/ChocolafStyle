""" login.py - login dialog """
import sys
import os

os.environ["QT_API"] = "pyqt6"

from qtpy.QtCore import PYQT_VERSION_STR, Qt
from qtpy.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QCheckBox, QGridLayout, QHBoxLayout, QMessageBox
)
from qtpy.QtGui import QFont, QPixmap

import chocolaf

custom_stylesheet = """
    QMessageBox {
        font-size: 12pt;
    }
"""


class LoginWindow(QWidget):
    def __init__(self, parent: QWidget = None):
        super(LoginWindow, self).__init__(parent)
        self.initializeUi()

    def initializeUi(self):
        self.setFixedSize(360, 220)
        self.setWindowTitle(f"PyQt {PYQT_VERSION_STR}: Login")
        self.setupMainWindow()

    def setupMainWindow(self):
        """ setup widgets & connect signals/slots """
        self.login_successful = False

        login_label = QLabel("Login", self)
        login_label.setFont(QFont("Arial", 16))
        login_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        username_label = QLabel("Username:", self)
        self.username_edit = QLineEdit(self)
        password_label = QLabel("Password:", self)
        self.password_edit = QLineEdit(self)
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)

        self.show_password_cb = QCheckBox("Show Password", self)
        self.show_password_cb.toggled.connect(self.displayPasswordIfChecked)

        login_button = QPushButton("Login", self)
        login_button.clicked.connect(self.clickLoginButton)

        not_member_label = QLabel("Not a member?", self)
        sign_up_button = QPushButton("Sign up", self)
        sign_up_button.clicked.connect(self.createNewUser)

        layout = QGridLayout()
        layout.addWidget(login_label, 0, 0, 1, 2)
        layout.addWidget(username_label, 1, 0)
        layout.addWidget(self.username_edit, 1, 1)
        layout.addWidget(password_label, 2, 0)
        layout.addWidget(self.password_edit, 2, 1)
        layout.addWidget(self.show_password_cb, 3, 1)
        layout.addWidget(login_button, 4, 0, 1, 2)
        hl1 = QHBoxLayout()
        hl1.addStretch()
        hl1.addWidget(not_member_label)
        hl1.addWidget(sign_up_button)
        hl1.addStretch()
        layout.addLayout(hl1, 5, 1)
        # layout.addWidget(not_member_label, 5, 0)
        # layout.addWidget(sign_up_button, 5, 1)

        self.setLayout(layout)

    def displayPasswordIfChecked(self):
        pass

    def clickLoginButton(self):
        QMessageBox.information(self, "Login",
                                f"Trying to login as {self.username_edit.text()}/{self.password_edit.text()}")

    def createNewUser(self):
        pass


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(custom_stylesheet)
    # chocolaf.enable_hi_dpi()
    # app = chocolaf.ChocolafApp(sys.argv)
    # app.setStyle("Chocolaf")

    # create the main window
    win = LoginWindow()
    win.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
