import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout
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
    def __init__(self):
        super().__init__()
        self.progress = 0  # Initial progress

        menu_width, menu_height = 780, 150

        self.setGeometry(10, 1080 - menu_height - 10, menu_width, menu_height)  # Set the size of the window
        # self.setGeometry(0 - menu_height + 10, menu_width, menu_height)  # Set the size of the window
        self.initUI()
 
    def initUI(self):
        # fontPath = './res/ResourceHanRoundedCN-Bold.ttf'
        fontPath = './res/Google_Sans-500-100_0-0_0.ttf'
        QFontDatabase.addApplicationFont(fontPath)

        self.setWindowTitle("Overlay Window")

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowTransparentForInput)
        self.setAttribute(Qt.WA_TranslucentBackground)

        layout = QHBoxLayout()
        layout.setContentsMargins(40, 15, 0, 0) 

        # Profile Picture
        profile_pic = QLabel(self)
        pixmap = QPixmap("./res/skill_icons/mika.png")  # Replace with the path to your image
        profile_pic.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))
        layout.addWidget(profile_pic)
        layout.addStretch(1)

        # Title
        title = QLabel("TYPE TIME DESCRIPTION", self)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        self.title = title

        layout.addStretch(2)

        with open('./res/style.qss', 'r') as f:
            style = f.read()
            title.setStyleSheet(style)

        self.setLayout(layout)

        self.show()

    def setProgress(self, value):
        self.progress = value  
        self.update() 
    def update_text_display(self, text):
        self.title.setText(str(text))
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # For smooth edges
        painter.setBrush(QBrush(QColor(2, 0, 31, 150)))  # Background color
        painter.setPen(Qt.NoPen)  # No border
        painter.drawRoundedRect(self.rect(), 15, 15)  # Rounded corners

        bar_width, bar_height = 450, 25
        bottom_padding = 30
        rect_x = self.width() / 2 - bar_width / 2
        rect_y = self.height() - bar_height - bottom_padding
        # Progress Bar

        gradient = QLinearGradient(rect_x, 0, rect_x + bar_width, 0)
        gradient.setColorAt(max(self.progress - 0.1, 0), QColor(79, 197, 255, 220))  # Blue end at progress
        gradient.setColorAt(min(self.progress + 0.1, 1), QColor(0, 0, 0, 50))  # Black starts immediately after progress
        
        rect = QRectF(rect_x, rect_y, bar_width, bar_height)
        painter.fillRect(rect, QBrush(gradient))


tw = None
def start():
    app = QApplication(sys.argv)

    global tw
    tw = OverlayWindow()
    tw.setProgress(50)  # Set initial progress here
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