"""
analyze_company_pyqt6.py - embeds a streamlib web application in a PytQt6 window

Author: Manish Bhobé
My experiments with Python, ML and Generative AI.
Code is meant for illustration purposes ONLY. Use at your own risk!
Author is not liable for any damages arising from direct/indirect use of this code.
"""

import sys
import subprocess
import time
import pathlib
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtWebEngineWidgets import QWebEngineView

app_file_path = pathlib.Path(__file__).parent / "analyze_company.py"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Start the Streamlit process
        self.streamlit_process = subprocess.Popen(
            ["streamlit", "run", str(app_file_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        # Optional: wait a couple of seconds for Streamlit to initialize
        time.sleep(2)

        # Create a QWebEngineView and load the Streamlit UI (default URL: http://localhost:8501)
        self.web_view = QWebEngineView(self)
        self.web_view.setUrl("http://localhost:8501")
        self.setCentralWidget(self.web_view)
        self.setWindowTitle("PyQt6 with Embedded Streamlit")

    def closeEvent(self, event):
        # Terminate the Streamlit process when the window is closing
        if self.streamlit_process.poll() is None:  # Check if process is still running
            self.streamlit_process.terminate()  # Graceful termination
            try:
                self.streamlit_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.streamlit_process.kill()  # Force kill if not terminated in time
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
