"""
// ============================================================================
// mainWindow.py: custom QMainWindow derived class for main window
//
// Tutorial - PyQt5 ImageChanger application
// Based on a similar tutorial for Borland ObjectWindows Library (OWL)
// @author: Manish Bhobe
// My experiments with the Qt Framework with PyQt. Use at your own risk!!
// ============================================================================
"""
import os
import platform

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import helpform
import newimagedlg
import resources_rc

__version__ = "1.0.1"


class MainWindow(QMainWindow):

    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)

        self.image = QImage()
        self.dirty = False
        self.filename = None
        self.mirroredVertically = False
        self.mirroredHorizontally = False

        self.imageLabel = QLabel()
        self.imageLabel.setMinimumSize(200, 200)
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.imageLabel.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.setCentralWidget(self.imageLabel)

        logDockWidget = QDockWidget("Log", self)
        logDockWidget.setObjectName("LogDockWidget")
        logDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.listWidget = QListWidget()
        logDockWidget.setWidget(self.listWidget)
        self.addDockWidget(Qt.RightDockWidgetArea, logDockWidget)

        self.printer = None

        self.sizeLabel = QLabel()
        self.sizeLabel.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.addPermanentWidget(self.sizeLabel)
        status.showMessage(f"PyQt {PYQT_VERSION_STR} ImageViewe using Chocolaf", 5000)

        self.createActions()
        self.createMenus()
        self.createToolbars()

        self.imageLabel.addAction(self.editInvertAction)
        self.imageLabel.addAction(self.editSwapRedAndBlueAction)
        self.imageLabel.addAction(self.editUnMirrorAction)
        self.imageLabel.addAction(self.editMirrorVerticalAction)
        self.imageLabel.addAction(self.editMirrorHorizontalAction)

        self.resetableActions = ((self.editInvertAction, False),
                                 (self.editSwapRedAndBlueAction, False),
                                 (self.editUnMirrorAction, True))

        settings = QSettings()
        self.recentFiles = settings.value("RecentFiles") or []
        self.restoreGeometry(settings.value("MainWindow/Geometry", QByteArray()))
        self.restoreState(settings.value("MainWindow/State", QByteArray()))

        self.setWindowTitle("Image Changer")
        # self.updateFileMenu()
        QTimer.singleShot(0, self.loadInitialFile)

    def createActions(self):
        self.fileNewAction = QAction(QIcon(":/file_new.png"), "&New", self)
        self.fileNewAction.triggered.connect(self.fileNew)
        self.fileNewAction.setShortcut(QKeySequence.New)
        self.fileNewAction.setStatusTip("Create a new image file")

        self.fileOpenAction = QAction(QIcon(":/file_open.png"), "&Open...", self)
        self.fileOpenAction.triggered.connect(self.fileOpen)
        self.fileOpenAction.setShortcut(QKeySequence.Open)
        self.fileOpenAction.setStatusTip("Open an existing image file")

        self.fileSaveAction = QAction(QIcon(":/file_save.png"), "&Save", self)
        self.fileSaveAction.triggered.connect(self.fileSave)
        self.fileSaveAction.setShortcut(QKeySequence.Save)
        self.fileSaveAction.setStatusTip("Save the image")

        self.fileSaveAsAction = QAction(QIcon(":/file_saveas.png"), "&Save as...", self)
        self.fileSaveAsAction.triggered.connect(self.fileSaveAs)
        self.fileSaveAsAction.setStatusTip("Save the image using a new name")

        self.filePrintAction = QAction(QIcon(":/file_print.png"), "&Print...", self)
        self.filePrintAction.triggered.connect(self.filePrint)
        self.filePrintAction.setShortcut(QKeySequence.Print)
        self.filePrintAction.setStatusTip("Print the image")

        self.fileQuitAction = QAction(QIcon(":/file_quit.png"), "&Quit", self)
        self.fileQuitAction.triggered.connect(self.close)
        self.fileQuitAction.setShortcut("Ctrl+Q")
        self.fileQuitAction.setStatusTip("Close the application")

        self.editInvertAction = QAction(QIcon(":/edit_invert.png"), "&Invert", self)
        self.editInvertAction.toggled.connect(self.editInvert)
        self.editInvertAction.setShortcut("Ctrl+I")
        self.editInvertAction.setStatusTip("Invert the image's colors")
        self.editInvertAction.setCheckable(True)

        self.editSwapRedAndBlueAction = QAction(QIcon(":/edit_swap.png"), "Sw&ap Red and Blue", self)
        self.editSwapRedAndBlueAction.toggled.connect(self.editSwapRedAndBlue)
        self.editSwapRedAndBlueAction.setShortcut("Ctrl+A")
        self.editSwapRedAndBlueAction.setStatusTip("Swap the images red & blue color components")
        self.editSwapRedAndBlueAction.setCheckable(True)

        self.editZoomAction = QAction(QIcon(":/edit_zoom.png"), "&Zoom...", self)
        self.editZoomAction.triggered.connect(self.editZoom)
        self.editZoomAction.setShortcut("Alt+Z")
        self.editZoomAction.setStatusTip("Zoom the image")

        self.mirrorGroup = QActionGroup(self)

        self.editUnMirrorAction = QAction(QIcon(":/edit_unmirror.png"), "&Unmirror", self)
        self.editUnMirrorAction.toggled.connect(self.editUnMirror)
        self.editUnMirrorAction.setShortcut("Ctrl+U")
        self.editUnMirrorAction.setStatusTip("Unmirror the image")
        self.editUnMirrorAction.setCheckable(True)
        self.mirrorGroup.addAction(self.editUnMirrorAction)

        self.editMirrorHorizontalAction = QAction(QIcon(":/edit_mirrorhoriz.png"), "Mirror &Horizontally", self)
        self.editMirrorHorizontalAction.toggled.connect(self.editMirrorHorizontal)
        self.editMirrorHorizontalAction.setShortcut("Ctrl+H")
        self.editMirrorHorizontalAction.setStatusTip("Horizontally mirror the image")
        self.editMirrorHorizontalAction.setCheckable(True)
        self.mirrorGroup.addAction(self.editMirrorHorizontalAction)

        self.editMirrorVerticalAction = QAction(QIcon(":/edit_mirrorvert.png"), "Mirror &Vertically", self)
        self.editMirrorVerticalAction.toggled.connect(self.editMirrorVertical)
        self.editMirrorVerticalAction.setShortcut("Ctrl+H")
        self.editMirrorVerticalAction.setStatusTip("Vertically mirror the image")
        self.editMirrorVerticalAction.setCheckable(True)
        self.mirrorGroup.addAction(self.editMirrorVerticalAction)

        self.editUnMirrorAction.setChecked(True)

        self.helpAboutAction = QAction("&About Image Changer...", self)
        self.helpAboutAction.triggered.connect(self.helpAbout)
        self.helpAboutAction.setStatusTip("Display information about application")

        self.helpHelpAction = QAction("&Help", self)
        self.helpHelpAction.setShortcut(QKeySequence.HelpContents)
        self.helpHelpAction.triggered.connect(self.helpHelp)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        # self.fileMenu.aboutToShow.connect(self.updateFileMenu)
        self.fileMenu.addAction(self.fileNewAction)
        self.fileMenu.addAction(self.fileOpenAction)
        self.fileMenu.addAction(self.fileSaveAction)
        self.fileMenu.addAction(self.fileSaveAsAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.filePrintAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.fileQuitAction)

        self.editMenu = self.menuBar().addMenu("&Edit")
        self.editMenu.addAction(self.editInvertAction)
        self.editMenu.addAction(self.editSwapRedAndBlueAction)
        self.editMenu.addAction(self.editZoomAction)
        mirrorMenu = self.editMenu.addMenu(QIcon(":/edit_mirror.png"), "&Mirror")
        mirrorMenu.addAction(self.editUnMirrorAction)
        mirrorMenu.addAction(self.editMirrorHorizontalAction)
        mirrorMenu.addAction(self.editMirrorVerticalAction)

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.helpAboutAction)
        self.helpMenu.addAction(self.helpHelpAction)

    def createToolbars(self):
        self.fileToolbar = self.addToolBar("File")
        self.fileToolbar.setObjectName("FileToolBar")
        self.fileToolbar.addAction(self.fileNewAction)
        self.fileToolbar.addAction(self.fileOpenAction)
        self.fileToolbar.addAction(self.fileSaveAsAction)

        self.editToolbar = self.addToolBar("Edit")
        self.editToolbar.setObjectName("EditToolBar")
        self.editToolbar.addAction(self.editInvertAction)
        self.editToolbar.addAction(self.editSwapRedAndBlueAction)
        self.editToolbar.addAction(self.editUnMirrorAction)
        self.editToolbar.addAction(self.editMirrorVerticalAction)
        self.editToolbar.addAction(self.editMirrorHorizontalAction)

        self.zoomSpinBox = QSpinBox()
        self.zoomSpinBox.setRange(1, 400)
        self.zoomSpinBox.setSuffix(" %")
        self.zoomSpinBox.setValue(100)
        self.zoomSpinBox.setToolTip("Zoom the image")
        self.zoomSpinBox.setStatusTip(self.zoomSpinBox.toolTip())
        self.zoomSpinBox.setFocusPolicy(Qt.NoFocus)
        self.zoomSpinBox.valueChanged.connect(self.showImage)
        self.editToolbar.addWidget(self.zoomSpinBox)

    # def createAction(self, text, slot = None, shortcut = None, icon = None,
    #                  tip = None, checkable = False, signal = "triggered()"):
    #     action=QAction(text, self)
    #     if icon is not None:
    #         action.setIcon(QIcon(":/{}.png".format(icon)))
    #     if shortcut is not None:
    #         action.setShortcut(shortcut)
    #     if tip is not None:
    #         action.setToolTip(tip)
    #         action.setStatusTip(tip)
    #     if slot is not None:
    #         self.connect(action, SIGNAL(signal), slot)
    #     if checkable:
    #         action.setCheckable(True)
    #     return action

    # def addActions(self, target, actions):
    #     for action in actions:
    #         if action is None:
    #             target.addSeparator()
    #         else:
    #             target.addAction(action)

    def closeEvent(self, event):
        if self.okToContinue():
            settings = QSettings()
            settings.setValue("LastFile", self.filename)
            settings.setValue("RecentFiles", self.recentFiles or [])
            settings.setValue("MainWindow/Geometry", self.saveGeometry())
            settings.setValue("MainWindow/State", self.saveState())
        else:
            event.ignore()

    def okToContinue(self):
        if self.dirty:
            reply = QMessageBox.question(self, "Image Changer - Unsaved Changes",
                                         "Save unsaved changes?",
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if reply == QMessageBox.Cancel:
                return False
            elif reply == QMessageBox.Yes:
                return self.fileSave()
        return True

    def loadInitialFile(self):
        settings = QSettings()
        fname = settings.value("LastFile")
        if fname and QFile.exists(fname):
            self.loadFile(fname)

    def updateStatus(self, message):
        self.statusBar().showMessage(message, 5000)
        self.listWidget.addItem(message)
        if self.filename:
            self.setWindowTitle("Image Changer - {}[*]".format(
                os.path.basename(self.filename)))
        elif not self.image.isNull():
            self.setWindowTitle("Image Changer - Unnamed[*]")
        else:
            self.setWindowTitle("Image Changer[*]")
        self.setWindowModified(self.dirty)

    def updateFileMenu(self):
        self.fileMenu.clear()
        self.addActions(self.fileMenu, self.fileMenuActions[:-1])
        current = self.filename
        recentFiles = []
        for fname in self.recentFiles:
            if fname != current and QFile.exists(fname):
                recentFiles.append(fname)
        if recentFiles:
            self.fileMenu.addSeparator()
            for i, fname in enumerate(recentFiles):
                action = QAction(QIcon(":/icon.png"),
                                 "&{} {}".format(i + 1, QFileInfo(
                                     fname).fileName()), self)
                action.setData(fname)
                self.connect(action, SIGNAL("triggered()"),
                             self.loadFile)
                self.fileMenu.addAction(action)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.fileMenuActions[-1])

    def fileNew(self):
        if not self.okToContinue():
            return
        dialog = newimagedlg.NewImageDlg(self)
        if dialog.exec_():
            self.addRecentFile(self.filename)
            self.image = QImage()
            for action, check in self.resetableActions:
                action.setChecked(check)
            self.image = dialog.image()
            self.filename = None
            self.dirty = True
            self.showImage()
            self.sizeLabel.setText("{} x {}".format(self.image.width(),
                                                    self.image.height()))
            self.updateStatus("Created new image")

    def fileOpen(self):
        if not self.okToContinue():
            return
        dir = (os.path.dirname(self.filename)
               if self.filename is not None else ".")
        formats = (["*.{}".format(format.data().decode("ascii").lower())
                    for format in QImageReader.supportedImageFormats()])
        fname = QFileDialog.getOpenFileName(self,
                                            "Image Changer - Choose Image", dir,
                                            "Image files ({})".format(" ".join(formats)))
        if fname:
            self.loadFile(fname[0])

    def loadFile(self, fname = None):
        if fname is None:
            action = self.sender()
            if isinstance(action, QAction):
                fname = action.data()
                if not self.okToContinue():
                    return
            else:
                return
        if fname:
            self.filename = None
            image = QImage(fname)
            if image.isNull():
                message = "Failed to read {}".format(fname)
            else:
                self.addRecentFile(fname)
                self.image = QImage()
                for action, check in self.resetableActions:
                    action.setChecked(check)
                self.image = image
                self.filename = fname
                self.showImage()
                self.dirty = False
                self.sizeLabel.setText("{} x {}".format(
                    image.width(), image.height()))
                message = "Loaded {}".format(os.path.basename(fname))
            self.updateStatus(message)

    def addRecentFile(self, fname):
        if fname is None:
            return
        if fname not in self.recentFiles:
            self.recentFiles = [fname] + self.recentFiles[:8]

    def fileSave(self):
        if self.image.isNull():
            return True
        if self.filename is None:
            return self.fileSaveAs()
        else:
            if self.image.save(self.filename, None):
                self.updateStatus("Saved as {}".format(self.filename))
                self.dirty = False
                return True
            else:
                self.updateStatus("Failed to save {}".format(
                    self.filename))
                return False

    def fileSaveAs(self):
        if self.image.isNull():
            return True
        fname = self.filename if self.filename is not None else "."
        formats = (["*.{}".format(format.data().decode("ascii").lower())
                    for format in QImageWriter.supportedImageFormats()])
        fname = QFileDialog.getSaveFileName(self,
                                            "Image Changer - Save Image", fname,
                                            "Image files ({})".format(" ".join(formats)))
        if fname:
            if "." not in fname:
                fname += ".png"
            self.addRecentFile(fname)
            self.filename = fname
            return self.fileSave()
        return False

    def filePrint(self):
        if self.image.isNull():
            return
        if self.printer is None:
            self.printer = QPrinter(QPrinter.HighResolution)
            self.printer.setPageSize(QPrinter.Letter)
        form = QPrintDialog(self.printer, self)
        if form.exec_():
            painter = QPainter(self.printer)
            rect = painter.viewport()
            size = self.image.size()
            size.scale(rect.size(), Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(),
                                size.height())
            painter.drawImage(0, 0, self.image)

    def editInvert(self, on):
        if self.image.isNull():
            return
        self.image.invertPixels()
        self.showImage()
        self.dirty = True
        self.updateStatus("Inverted" if on else "Uninverted")

    def editSwapRedAndBlue(self, on):
        if self.image.isNull():
            return
        self.image = self.image.rgbSwapped()
        self.showImage()
        self.dirty = True
        self.updateStatus(("Swapped Red and Blue"
                           if on else "Unswapped Red and Blue"))

    def editUnMirror(self, on):
        if self.image.isNull():
            return
        if self.mirroredHorizontally:
            self.editMirrorHorizontal(False)
        if self.mirroredVertically:
            self.editMirrorVertical(False)

    def editMirrorHorizontal(self, on):
        if self.image.isNull():
            return
        self.image = self.image.mirrored(True, False)
        self.showImage()
        self.mirroredHorizontally = not self.mirroredHorizontally
        self.dirty = True
        self.updateStatus(("Mirrored Horizontally"
                           if on else "Unmirrored Horizontally"))

    def editMirrorVertical(self, on):
        if self.image.isNull():
            return
        self.image = self.image.mirrored(False, True)
        self.showImage()
        self.mirroredVertically = not self.mirroredVertically
        self.dirty = True
        self.updateStatus(("Mirrored Vertically"
                           if on else "Unmirrored Vertically"))

    def editZoom(self):
        if self.image.isNull():
            return
        percent, ok = QInputDialog.getInteger(self,
                                              "Image Changer - Zoom", "Percent:",
                                              self.zoomSpinBox.value(), 1, 400)
        if ok:
            self.zoomSpinBox.setValue(percent)

    def showImage(self, percent = None):
        if self.image.isNull():
            return
        if percent is None:
            percent = self.zoomSpinBox.value()
        factor = percent / 100.0
        width = self.image.width() * factor
        height = self.image.height() * factor
        image = self.image.scaled(width, height, Qt.KeepAspectRatio)
        self.imageLabel.setPixmap(QPixmap.fromImage(image))

    def helpAbout(self):
        QMessageBox.about(self, "About Image Changer",
                          """<b>Image Changer</b> v {0}
                <p>Copyright &copy; 2008-10 Qtrac Ltd. 
                All rights reserved.
                <p>This application can be used to perform simple image manipulations.
                <p>Python {1} - Qt {2} - PyQt {3} on {4}""".format(
                              __version__, platform.python_version(),
                              QT_VERSION_STR, PYQT_VERSION_STR,
                              platform.system()))

    def helpHelp(self):
        form = helpform.HelpForm("index.html", self)
        form.show()
