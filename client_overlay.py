import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontDatabase, QFont

class OverlayWindow(QWidget):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.setGeometry(x, y, width, height)
        self.initUI()
 
    def initUI(self):
        fontPath = './Roboto-Black.ttf'
        fontId = QFontDatabase.addApplicationFont(fontPath)
        self.setWindowTitle('Overlay Window')
        self.text = QLabel('TYPE TIME DESCRIPTION', self)

        with open('style.qss', 'r') as f:
            style = f.read()
            self.setStyleSheet(style)
            self.text.setStyleSheet(style)
        
        self.setWindowOpacity(0.75)
        self.text.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("background-color: black;")
        layout = QVBoxLayout(self)
        layout.addWidget(self.text)

        self.setLayout(layout)

        # Alternatively, to make the window's background completely transparent (including no frame):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowTransparentForInput)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.show()

    def update_text_display(self, text):
        self.text.setText(str(text))
        

tw = None
def start():
    app = QApplication(sys.argv)

    WINDOW_X, WINDOW_Y, WINDOW_WIDTH, WINDOW_HEIGHT = 100, -100, 100, 100
    global tw
    tw = OverlayWindow(WINDOW_X, WINDOW_Y, WINDOW_WIDTH, WINDOW_HEIGHT)
    
    # tw.move(int(1920 / 2 - tw.width() / 2), -15)
    tw.move(int(1920 / 2 - tw.width() / 2), 200)
    # tw.move(1600, -15)

    print(tw.geometry())
    sys.exit(app.exec_())

def update_text_display(text):
    tw.update_text_display(text)