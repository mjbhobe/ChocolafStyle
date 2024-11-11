""" registration.py - new user registration """

import sys
import os
import pathlib

os.environ["QT_API"] = "pyqt6"

from qtpy.QtCore import PYQT_VERSION_STR, Qt
from qtpy.QtWidgets import (
    QDialog,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QGridLayout,
    QVBoxLayout,
    QMessageBox,
)
from qtpy.QtGui import QFont, QPixmap

import chocolaf

_logger = chocolaf.get_logger(pathlib.Path(__file__).name)

custom_stylesheet = """
    QMessageBox {
        font-size: 13px;
    }
"""

AppDir = pathlib.Path(__file__).parents[0]
_logger.info(f"Appdir = {AppDir}")


class NewUserDialog(QDialog):
    def __init__(self, parent: QWidget = None):
        super(NewUserDialog, self).__init__(parent)
        self.setModal(True)
        self.initializeUi()

    def initializeUi(self):
        self.setFixedSize(360, 320)
        self.setWindowTitle(f"New User Registration")
        self.setupWindow()

    def setupWindow(self):
        login_label = QLabel("Create New Account", self)
        login_label.setFont(QFont("Arial", 16))
        login_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        user_image_path = os.path.join(AppDir, "images/new_user_icon.png")
        assert os.path.exists(
            user_image_path
        ), f"FATAL: {user_image_path} does not exist!"
        user_label = QLabel(self)
        user_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pixmap = QPixmap(user_image_path)
        user_label.setPixmap(pixmap)
        l1 = QVBoxLayout()
        l1.addWidget(login_label)
        l1.addWidget(user_label)

        # create the widgets for user input
        username_label = QLabel("Username:", self)
        self.username_edit = QLineEdit(self)
        password_label = QLabel("Password:", self)
        self.password_edit = QLineEdit(self)
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        confirm_password_label = QLabel("Confirm:", self)
        self.confirm_password_edit = QLineEdit(self)
        self.confirm_password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.signup_button = QPushButton("Sign up", self)
        self.signup_button.clicked.connect(self.confirmSignUp)

        l2 = QGridLayout()
        l2.addWidget(username_label, 0, 0)
        l2.addWidget(self.username_edit, 0, 1)
        l2.addWidget(password_label, 1, 0)
        l2.addWidget(self.password_edit, 1, 1)
        l2.addWidget(confirm_password_label, 2, 0)
        l2.addWidget(self.confirm_password_edit, 2, 1)
        l2.addWidget(self.signup_button, 3, 0, 1, 2)
        l1.addLayout(l2)
        self.setLayout(l1)

    def confirmSignUp(self):
        name_txt = self.username_edit.text()
        pwd_txt = self.password_edit.text()
        confirm_pwd = self.confirm_password_edit.text()

        # name & password must be entered
        if name_txt == "" or pwd_txt == "":
            QMessageBox.warning(
                self,
                "Error",
                "Please enter both user name & password values",
                QMessageBox.StandardButton.Ok,
            )
        elif pwd_txt != confirm_pwd:
            QMessageBox.warning(
                self,
                "Error",
                "Passwords entered do not match",
                QMessageBox.StandardButton.Ok,
            )
        else:
            # AppDir = pathlib.Path(__file__).parents[0]
            pwd_file_path = os.path.join(AppDir, "files/users.txt")
            with open(pwd_file_path, "a+") as f:
                f.write(f"\n{name_txt} {pwd_txt}")
                QMessageBox.information(
                    self,
                    "Registration Successful",
                    f"User {name_txt} registered successfully!",
                    QMessageBox.StandardButton.Ok,
                )
                self.username_edit.clear()
                self.password_edit.clear()
                self.confirm_password_edit.clear()


if __name__ == "__main__":
    from qtpy.QtWidgets import QApplication

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    dlg = NewUserDialog()
    dlg.show()

    sys.exit(app.exec())
