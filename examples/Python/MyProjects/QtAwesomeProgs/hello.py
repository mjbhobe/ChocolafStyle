""" hello.py - illustrates use of icons inside PyQt widgets """
import sys

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import qtawesome as qta
import chocolaf

STYLE_SHEET = """
    QPushButton {
        min-height: 1.3em;
    }
    QMenuBar {
        background-color: rgb(25, 25, 25);
    }
    QToolBar {
        background-color: rgb(26, 32, 47);
    }
    QStatusBar {
        background-color: rgb(26, 32, 47);
    }
"""


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi()

    def createActions(self):
        self.color_options = [
            {
                "color": QColor(180, 180, 180),
                "color_active": QColor(180, 180, 180),
                "color_disabled": QColor(127, 127, 127),
                "color_selected": QColor(220, 220, 220),
            }
        ]
        self.cut_icon = qta.icon("mdi6.content-cut", options=self.color_options)
        self.cut_action = QAction(self.cut_icon, "&Cut", self)
        self.cut_action.triggered.connect(self.edit_cut)
        self.cut_action.setShortcut(QKeySequence.StandardKey.Cut)
        self.cut_action.setStatusTip("Cut selection to clipboard")
        self.cut_action.setToolTip("Cut")

        self.copy_icon = qta.icon("mdi6.content-copy", options=self.color_options)
        self.copy_action = QAction(self.copy_icon, "C&opy", self)
        self.copy_action.triggered.connect(self.edit_copy)
        self.copy_action.setShortcut(QKeySequence.StandardKey.Copy)
        self.copy_action.setStatusTip("Copy selection to clipboard")
        self.copy_action.setToolTip("Copy")

        self.paste_icon = qta.icon("mdi6.content-paste", options=self.color_options)
        self.paste_action = QAction(self.paste_icon, "&Paste", self)
        self.paste_action.triggered.connect(self.edit_paste)
        self.paste_action.setShortcut(QKeySequence.StandardKey.Paste)
        self.paste_action.setStatusTip("Paste contents from clipboard")
        self.paste_action.setToolTip("Paste")

    def createMenus(self):
        self.actionsMenu = self.menuBar().addMenu("&Actions")
        self.actionsMenu.addAction(self.cut_action)
        self.actionsMenu.addAction(self.copy_action)
        self.actionsMenu.addAction(self.paste_action)

    def createToolbar(self):
        self.editToolbar = self.addToolBar("Edit")
        self.editToolbar.setObjectName("EditToolbar")
        self.editToolbar.addAction(self.cut_action)
        self.editToolbar.addAction(self.copy_action)
        self.editToolbar.addAction(self.paste_action)
        # self.editToolbar.setStyleSheet(STYLE_SHEET)

    def edit_cut(self):
        self.label.setText("You selected the 'Cut' option")

    def edit_copy(self):
        self.label.setText("You selected the 'Copy' option")

    def edit_paste(self):
        self.label.setText("You selected the 'Paste' option")

    def setupUi(self):
        self.createActions()
        self.createMenus()
        self.createToolbar()
        status = self.statusBar()
        status.setSizeGripEnabled(False)

        # create the UI
        self.label = QLabel(f"Welcome to PyQt {PYQT_VERSION_STR}")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        enable_icon = qta.icon("mdi6.check", color="#25AD6B")
        close_icon = qta.icon("mdi6.close-thick", color="red")
        self.enabledBtn = QPushButton(enable_icon, "Enabled")
        self.disabledBtn = QPushButton("Disabled")
        self.disabledBtn.setEnabled(False)
        self.closeBtn = QPushButton(close_icon, "&Close")
        self.closeBtn.setDefault(True)
        self.closeBtn.clicked.connect(QApplication.instance().quit)
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.enabledBtn)
        hlayout.addWidget(self.disabledBtn)
        hlayout.addWidget(self.closeBtn)

        win = QWidget()
        win.setObjectName("MainWidget")
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addLayout(hlayout)
        win.setLayout(layout)
        self.setFixedSize(QSize(350, 200))
        self.setCentralWidget(win)


def main():
    chocolaf.enable_hi_dpi()
    app = chocolaf.ChocolafApp(sys.argv)
    app.setStyle("WindowsDark")

    mainWin = MainWindow()
    # mainWin.setStyleSheet(STYLE_SHEET)
    mainWin.setWindowTitle("Chocolaf and QtAwesome Icons")
    mainWin.show()
    # or Material Design Icons:
    # my_icon = qta.icon('msc.chevron-left')
    # mdi6_button = QPushButton(my_icon, 'Works?')
    # mdi6_button.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
