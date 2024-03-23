import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontDatabase, QFont, QPixmap, QKeyEvent
from PyQt5.QtGui import QPainter, QBrush, QLinearGradient, QColor, QFont, QPen
from PyQt5.QtCore import Qt, QRectF
import threading
from pynput import keyboard
import random
import utils
import os

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
        self.target_progress = 0  # Initial progress
        self.progress = 0

        menu_width, menu_height = 780, 150

        self.setGeometry(10, 1080 - menu_height - 10, menu_width, menu_height)  # Set the size of the window
        # self.setGeometry(0 - menu_height + 10, menu_width, menu_height)  # Set the size of the window
        self.initUI()
        self.color_rot = 0
        self.progress_bar_color = QColor(79, 197, 255, 150)
        self.current_character = "mika"

 
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
        self.profile_pic = QLabel(self)
        pixmap = QPixmap("./res/skill_icons/mika.png")  # Replace with the path to your image
        self.profile_pic.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))
        layout.addWidget(self.profile_pic)
        layout.addStretch(1)

        # Title
        title = QLabel("Idle", self)
        # title = QLabel("TYPE TIME DESCRIPTION", self)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        self.title = title

        layout.addStretch(2)

        with open('./res/style.qss', 'r') as f:
            style = f.read()
            title.setStyleSheet(style)


        self.setLayout(layout)

        self.show()


    def setProgress(self, value, immediate=False):
        if immediate == True: 
            self.progress = value
            self.target_progress = value
        else:
            self.target_progress = value  
            self.target_progress = max(0, min(1, self.target_progress))
        
        self.update() 

    def updateProgress(self):
        """Gradually update current progress towards the target progress."""
        # print(self.progress, self.target_progress)
        if self.progress < self.target_progress:
            self.progress += ((self.target_progress - self.progress) * 0.01) # Increment progress
            if self.progress > self.target_progress:
                self.progress = self.target_progress
        elif self.progress > self.target_progress:
            self.progress -= 0.0001  # Decrement progress
            if self.progress < self.target_progress:
                self.progress = self.target_progress

        self.update()  # Trigger repaint


    def update_text_display(self, text):
        menu_width, menu_height = 780, 150

        if (len(str(text)) != len(str(self.title.text())) and len(str(text)) < 35 and self.geometry().width() != menu_width):
            print("hi")
            self.setGeometry(10, 1080 - menu_height - 10, menu_width, menu_height) 

        self.title.setText(str(text))
        

    def update_image_display(self, character_name):
        if self.current_character is not character_name and os.path.isfile(f"./res/skill_icons/{character_name}.png"):
            pixmap = QPixmap(f"./res/skill_icons/{character_name}.png")  # Replace with the path to your image
            self.profile_pic.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))
            self.current_character = character_name


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
        self.updateProgress()
        
        speed = 100
        if (self.color_rot % speed == 0):
            self.progress_bar_color = utils.rainbow_colors[int(self.color_rot / speed) % len(utils.rainbow_colors)]

        gradient.setColorAt(max(self.progress - 0.001, 0), self.progress_bar_color)  # Blue end at progress 79, 197, 255, 150
        gradient.setColorAt(min(self.progress + 0.001, 1), QColor(0, 0, 0, 30))  # Black starts immediately after progress
        
        rect = QRectF(rect_x, rect_y, bar_width, bar_height)
        painter.fillRect(rect, QBrush(gradient))
        
        self.color_rot += 1
        self.color_rot %= 1_000_000_000


tw = None
def start():
    app = QApplication(sys.argv)

    global tw
    tw = OverlayWindow()
    tw.setProgress(0.5, True)  # Set initial progress here
    widget = TransparentImageWidget()
    widget.showFullScreen()
    
    # keyListenerThread = threading.Thread(target=widget.onKeyPressEvent)
    # keyListenerThread.start()

    print(tw.geometry())

    exit_code = app.exec_()
    print("Exit")
    sys.exit(exit_code)

def update_display(text, character_name):
    tw.update_text_display(text)
    tw.update_image_display(character_name)


def update_progress_bar(percent, immediate=False):
    tw.setProgress(percent, immediate)