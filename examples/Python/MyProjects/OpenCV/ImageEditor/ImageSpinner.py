#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ImageSpinner.py: cycle through images in a folder
import sys
import os
import pathlib
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class ImageSpinner(QObject):
    def __init__(self, imagePath: str):
        assert (os.path.exists(imagePath)), f"ERROR: {imagePath} - invalid path!"
        self.currIndex = -1
        fileInfo = QFileInfo(imagePath)
        self.dir = fileInfo.absoluteDir()
        fileName = fileInfo.fileName()
        imageFilters = ["*.tiff", "*.tif", "*.jpg", "*.jpeg", "*.gif", "*.bmp", "*.png"]
        self.fileNames = self.dir.entryList(imageFilters, QDir.Files, QDir.Name)
        self.currIndex = self.fileNames.index(fileName)
        # self.currIndex = self.fileNames.index(
        #     QRegExp(QRegExp.escape(fileInfo.fileName()))
        # )

    def prevImagePath(self) -> str:
        self.currIndex = self.currIndex - 1
        if (self.currIndex < 0):
            self.currIndex = 0
        prevImagePath = self.dir.absolutePath() + QDir.separator() + \
            self.fileNames[self.currIndex]
        return prevImagePath

    def nextImagePath(self) -> str:
        self.currIndex = self.currIndex + 1
        if (self.currIndex > len(self.fileNames) - 1):
            self.currIndex = len(self.fileNames) - 1
        nextImagePath = self.dir.absolutePath() + QDir.separator() + \
            self.fileNames[self.currIndex]
        return nextImagePath

    def atFirstPath(self):
        return self.currIndex == 0

    def atLastPath(self):
        return self.currIndex == len(self.fileNames) - 1

    def size(self):
        return len(self.fileNames)
