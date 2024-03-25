from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt5.QtCore import pyqtSignal, QObject
import threading
import sys
import time

# Define a QObject derivative to emit signals
class SignalEmitter(QObject):
    colorChanged = pyqtSignal(str)

class ColorThread(threading.Thread):
    def __init__(self, emitter):
        threading.Thread.__init__(self)
        self.emitter = emitter

    def run(self):
        colors = ["#FF0000", "#00FF00", "#0000FF"]
        for color in colors:
            time.sleep(1)  # Simulate some work
            # Emit signal via the QObject-based emitter
            self.emitter.colorChanged.emit(color)

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.label = QLabel("Color will change")
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        # Signal emitter for communication from thread
        self.emitter = SignalEmitter()
        self.emitter.colorChanged.connect(self.updateColor)

        self.thread = ColorThread(self.emitter)
        self.thread.start()

    def updateColor(self, color):
        self.label.setStyleSheet(f"background-color: {color};")

app = QApplication(sys.argv)
window = MyWidget()
window.show()
sys.exit(app.exec_())
