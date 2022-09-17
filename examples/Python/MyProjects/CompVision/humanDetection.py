# -*- coding: utf-8 -*-
"""
* humanDetection.py - detecting humans in videos using OpenCV
* @author (Chocolaf): Manish Bhobe
*
* My experiments with Python, PyQt, Data Science & Deep Learning
* The code is made available for illustration purposes only.
* Use at your own risk!!
"""
import sys
import os
import cv2
import numpy as np

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from chocolaf.palettes import ChocolafPalette
from chocolaf.utils.chocolafapp import ChocolafApp

import textEditor_rc

Window_Title = "PyQt Detecting Humans in Videos using OpenCV"

# add some custom styling above & beyond stysheet set
style_sheet = """
    QLabel#VideoLabel {
        border: 2px dashed rgb(102, 102, 102);
        qproperty-alignment: AlignCenter;
    }
"""


class VideoWorkerThread(QThread):
    frame_data_updated = pyqtSignal(np.ndarray)
    invalid_video_file = pyqtSignal()

    def __init__(self, parent, video_file=None, render_frames_per_sec=60):
        super().__init__()
        self.parent = parent
        self.video_file = video_file
        self.render_frames_per_sec = render_frames_per_sec

    def run(self):
        """ actual thread code - capture video using openCV"""
        capture = cv2.VideoCapture(self.video_file)  # open default camera

        if not capture.isOpened():
            self.invalid_video_file.emit()
        else:
            while self.parent.thread_is_running:
                # read the frames & display them
                ret_val, frame = capture.read()
                if not ret_val:
                    break  # error or end of video
                else:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame = cv2.resize(frame, (600, 400))
                    rects = self.createHOGDescriptor(frame)
                    # draw blue rectangles around humans detected in video
                    for (x_tr, y_tr, x_br, y_br) in rects:
                        frame = cv2.rectangle(frame, (x_tr, y_tr), (x_br, y_br),
                                              (0, 0, 255), 2)
                    self.frame_data_updated.emit(frame)
                    # wait certain interval depending on desired frames/sec
                    #self.msleep(1000 // self.render_frames_per_sec)

    def createHOGDescriptor(self, frame):
        """Function creates the HOG Descriptor for human detection and
           returns the detections (rects)."""
        hog = cv2.HOGDescriptor()
        hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

        # Detect people in the image and return the bounding rectangles.
        # Altering the parameters in detectMultiScale() can affect the
        # accuracy of detections. winStride refers to the number of steps the
        # sliding window moves in the x and y directions the sliding window
        # is padded to improve accuracya smaller scale value will increase
        # detection accuracy, but also increase processing time
        rects, weights = hog.detectMultiScale(frame, winStride=(4, 4),
                                              padding=(8, 8), scale=1.1)
        # For each of the rects detected in an image, add the values
        # for the corners of the rect to an array
        rects = np.array([[x, y, x + width, y + height]
                          for (x, y, width, height) in rects])
        return rects

    def stopThread(self):
        """ process all pending events & stop thread """
        self.wait()
        QApplication.processEvents()


class DisplayVideoWindow(QMainWindow):
    def __init__(self):
        super(DisplayVideoWindow, self).__init__()
        self.thread_is_running = False
        self.initializeUi()
        # set custom styling
        self.setStyleSheet(style_sheet)

    def initializeUi(self):
        """ initialize the window & display contents to the screen """
        self.setMinimumSize(800, 500)
        self.setWindowTitle(Window_Title)
        self.thread_is_running = False
        self.setupWindow()
        self.setupMenu()

    def setupWindow(self):
        self.videoDisplayLabel = QLabel()
        self.videoDisplayLabel.setObjectName("VideoLabel")

        self.displayVideoPathLine = QLineEdit()
        self.displayVideoPathLine.setClearButtonEnabled(True)
        self.displayVideoPathLine.setPlaceholderText("Select a video or use webcam")

        self.startButton = QPushButton("Start Video")
        self.startButton.clicked.connect(self.startVideo)

        self.stopButton = QPushButton("Stop Video")
        self.stopButton.clicked.connect(self.stopVideo)

        sidePanelVBox = QVBoxLayout()
        sidePanelVBox.setAlignment(Qt.AlignTop)
        sidePanelVBox.addWidget(self.displayVideoPathLine)
        sidePanelVBox.addWidget(self.startButton)
        sidePanelVBox.addWidget(self.stopButton)

        sidePanelFrame = QFrame()
        sidePanelFrame.setMidLineWidth(200)
        sidePanelFrame.setLayout(sidePanelVBox)

        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.videoDisplayLabel, 1)
        mainLayout.addWidget(sidePanelFrame)

        container = QWidget()
        container.setLayout(mainLayout)
        self.setCentralWidget(container)

    def setupMenu(self):
        openAction = QAction(QIcon(":/file_open.png"), "&Open", self)
        openAction.setStatusTip("Open video file from disk")
        openAction.setShortcut(QKeySequence.Open)
        openAction.triggered.connect(self.openVideo)

        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu("&File")
        fileMenu.addAction(openAction)

    def startVideo(self):
        self.thread_is_running = True
        self.startButton.setEnabled(False)
        self.startButton.repaint()
        # for local files, use worker thread
        if self.displayVideoPathLine.text() != "":
            video_file = self.displayVideoPathLine.text()
            self.videoThreadWorker = VideoWorkerThread(self, video_file)
        else:
            # use webcam
            self.videoThreadWorker = VideoWorkerThread(self, 0)

        self.videoThreadWorker.frame_data_updated.connect(self.updateVideoFrames)
        self.videoThreadWorker.invalid_video_file.connect(self.invalidVideoFile)
        # and let's go....
        self.videoThreadWorker.start()

    def stopVideo(self):
        if self.thread_is_running:
            self.thread_is_running = False
            self.videoThreadWorker.stopThread()
            self.videoDisplayLabel.clear()
            self.startButton.setEnabled(True)

    def openVideo(self):
        """ displays the standard file dialog so user can select video to view
            Video path is captured to displayVideoPathLine edit control - video will
            be displayed only when 'start video' button is clicked """
        videosLoc = QStandardPaths.standardLocations(QStandardPaths.MoviesLocation)
        videoFile, _ = QFileDialog.getOpenFileName(self, "Open Video", videosLoc[-1],
                                                   "Videos (*.mp4 *.avi)")
        if videoFile:
            self.displayVideoPathLine.setText(videoFile)
        else:
            QMessageBox.information(self, "Error", "No video was loaded", QMessageBox.Ok)

    def updateVideoFrames(self, video_frame):
        """ video is a collection of frames. For each frame, convert it to a QImage
            and display it on the QLabel """
        height, width, channels = video_frame.shape
        bytes_per_line = width * channels
        convertedQImage = QImage(video_frame, width, height, bytes_per_line, QImage.Format_RGB888)
        self.videoDisplayLabel.setPixmap(QPixmap.fromImage(convertedQImage).scaled(
            self.videoDisplayLabel.width(), self.videoDisplayLabel.height(),
            Qt.KeepAspectRatioByExpanding
        ))

    def invalidVideoFile(self):
        """ display messagebox to inform user that an error has occured """
        QMessageBox.warning(self, "Error", "No video was loaded", QMessageBox.Ok)
        self.startButton.setEnabled(True)

    def closeEvent(self, event):
        """ reimplement close event to ensure that thread closes """
        if self.thread_is_running == True:
            self.video_thread_worker.quit()


if __name__ == "__main__":
    app = ChocolafApp(sys.argv)
    app.setStyle("Chocolaf")
    # app.setStyle("Fusion")

    win = DisplayVideoWindow()
    win.show()

    sys.exit(app.exec())
