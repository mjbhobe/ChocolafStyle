import sys

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


def getDpiInfo() -> None:
    screens: QList[QScreen] = QGuiApplication.screens()

    if not screens:
        print(f"No screens found!")
        sys.exit(-1)
    else:
        print(f"Found {len(screens)} screens")
        for i, screen in enumerate(screens):
            name: str = screen.name()
            geometry: QRect = screen.geometry()
            available_geometry: QRect = screen.availableGeometry()
            logical_dpi: float = screen.logicalDotsPerInch()
            device_pixels_ratio: float = screen.devicePixelRatio()

            print(f"--- Screen {i} ({name}) ---")
            print(
                f"Geometry (Full Size): {geometry.width()}x{geometry.height()} @ ({geometry.x()}, {geometry.y()})"
            )
            print(
                f"Available Geometry (w/o Taskbars): {available_geometry.width()}x{available_geometry.height()}"
            )
            print(f"Logical DPI: {logical_dpi:.2f}")
            print(f"Device Pixel Ratio (Scale): {device_pixels_ratio:.2f}")
            print("-" * 30)
            print(f"So 14px font is {(14 / logical_dpi) * 72:.2f} points")
            print(f"And 12pt font is {(12 / 72) * logical_dpi:.2f} pixels")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    getDpiInfo()
