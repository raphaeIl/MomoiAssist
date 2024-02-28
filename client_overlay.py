import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtGui import QPainter, QBrush, QLinearGradient, QColor, QFont, QPen
from PyQt5.QtCore import Qt, QRectF

class OverlayWindow(QWidget):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.progress = 0  # Initial progress

        self.setGeometry(x, y, width, height)
        self.initUI()
 
    def initUI(self):
        fontPath = './res/Roboto-Black.ttf'
        QFontDatabase.addApplicationFont(fontPath)
        self.setWindowTitle('Overlay Window')
        self.text = QLabel('TYPE TIME DESCRIPTION', self)

        with open('./res/style.qss', 'r') as f:
            style = f.read()
            self.setStyleSheet(style)
            self.text.setStyleSheet(style)
        
        self.setWindowOpacity(1)
        self.text.setAlignment(Qt.AlignCenter)
        layout = QVBoxLayout(self)
        layout.addWidget(self.text)

        self.setLayout(layout)

        # Alternatively, to make the window's background completely transparent (including no frame):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowTransparentForInput)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.show()

    def setProgress(self, value):
        self.progress = max(0, min(100, value))  # Clamp value between 0 and 100
        self.update()  # Trigger repaint

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        gradient = QLinearGradient(0, 0, self.width() * (self.progress / 50.0), 0)
        gradient.setColorAt(0.49, QColor(79, 197, 255, 220))
        gradient.setColorAt(0.51, QColor(0, 0, 0, 100))
        
        rect = QRectF(0, 0, self.width(), self.height())
        painter.fillRect(rect, QBrush(gradient))
        
        # pen = QPen(QColor(0, 0, 0, 255), 2)  # Black border with 5 pixels thickness
        # painter.setPen(pen)
        # painter.drawRect(0, 0, self.width(), self.height(), 10, 10)  # Subtract 1 to ensure the border is fully visible

        super(OverlayWindow, self).paintEvent(event)

    def update_text_display(self, text):
        self.text.setText(str(text))
        

tw = None
def start():
    app = QApplication(sys.argv)

    WINDOW_X, WINDOW_Y, WINDOW_WIDTH, WINDOW_HEIGHT = 100, -100, 100, 100
    global tw
    tw = OverlayWindow(WINDOW_X, WINDOW_Y, WINDOW_WIDTH, WINDOW_HEIGHT)
    tw.setProgress(50)  # Set initial progress here
    tw.move(int(1920 / 2 - 394 / 2), -15)
    # tw.move(int(1920 / 2 - tw.width() / 2), 200)
    # tw.move(1400, 70)

    print(tw.geometry())
    sys.exit(app.exec_())

def update_text_display(text):
    tw.update_text_display(text)

def update_progress_bar(percent):
    tw.setProgress(percent)