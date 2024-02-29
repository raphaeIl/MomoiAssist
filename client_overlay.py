import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontDatabase, QFont, QPixmap, QKeyEvent
from PyQt5.QtGui import QPainter, QBrush, QLinearGradient, QColor, QFont, QPen
from PyQt5.QtCore import Qt, QRectF
import threading
from pynput import keyboard

class TransparentImageWidget(QWidget):
    def __init__(self):
        super().__init__()
        # self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowTransparentForInput)

        
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(0, 0, 1920, 1080)  # Fullscreen for 1920x1080 resolution

        self.imageLabel = QLabel(self)
        self.imageLabel.setGeometry(0, 0, 1920, 1080)
        
        self.pixmap = QPixmap("./res/kuro_overlay_red.png").scaled(1920, 1080, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        self.opacity = 0  # Start with half opacity

        self.updateImageOpacity()

    def updateImageOpacity(self):
        tempPixmap = QPixmap(self.pixmap.size())
        tempPixmap.fill(Qt.transparent)

        painter = QPainter(tempPixmap)
        painter.setOpacity(self.opacity)
        painter.drawPixmap(0, 0, self.pixmap)
        painter.end()

        self.imageLabel.setPixmap(tempPixmap)

    def onKeyPressEvent(self):
        def on_press(key):
            try:
                if key.char == 't':
                    print("T pressed")
                    self.opacity = 0.5 if self.opacity == 0 else 0
                    self.updateImageOpacity()
            except AttributeError:
                pass

        def on_release(key):
            pass
        
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()



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
    widget = TransparentImageWidget()
    widget.showFullScreen()
    
    keyListenerThread = threading.Thread(target=widget.onKeyPressEvent)
    keyListenerThread.start()

    print(tw.geometry())
    sys.exit(app.exec_())

def update_text_display(text):
    tw.update_text_display(text)

def update_progress_bar(percent):
    tw.setProgress(percent)