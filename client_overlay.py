import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontDatabase, QFont, QPixmap, QKeyEvent
from PyQt5.QtGui import QPainter, QBrush, QLinearGradient, QColor, QFont, QPen
from PyQt5.QtCore import Qt, QRectF
import threading
from pynput import keyboard
from PyQt5.QtGui import QPalette, QColor
import total_assault_helper
import random
import utils
import os
import invisible_overlay
import time
from PyQt5.QtCore import pyqtSignal, QObject

from total_assault_helper import TotalAssaultHelper

class SignalEmitter(QObject):
    update_display = pyqtSignal(str, str, str, str)

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
        self.current_text_display = ""

    def init_update_fn(self, update_actions, update_display):
        self.update_actions = update_actions
        self.update_display = update_display

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
        self.profile_pic.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio))
        layout.addWidget(self.profile_pic)
        layout.addStretch(1)

        self.profile_pic.setAlignment(Qt.AlignLeft)
        # self.profile_pic.setStyleSheet("""QLabel { padding-right: 100px; }""")

        # Title
        title = QLabel("Idle", self)
        subtitle = QLabel("subtitle", self)

        # title = QLabel("TYPE TIME DESCRIPTION", self)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        
        self.title = title
        self.subtitle = subtitle

        layout.addStretch(2)
        layout.setContentsMargins(15, 15, 0, 0)

        with open('./res/style.qss', 'r') as f:
            style = f.read()
            title.setStyleSheet(style)

        palette = QPalette()
        palette.setColor(QPalette.WindowText, QColor("red"))
        self.subtitle.setPalette(palette)
        self.subtitle.setStyleSheet("""QLabel {
    font-family: "Resource Han Rounded CN";
    font-size: 25pt;
    padding-top: 0px;
    padding-right: 0px;
    padding-bottom: 70px;
    padding-left: 50px;
}""")
        self.setLayout(layout)

        self.show()


    def onKeyPressEvent(self):
        def on_press(key):
            try:
                if key.char == 't':
                    self.update_actions()
                    self.update_display()

            except AttributeError:
                pass

        def on_release(key):
            pass
        
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()


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

    def update_text_display(self, text, colored_text, color):
        menu_width, menu_height = 780, 150

        if ((str(self.title.text()) != self.current_text_display) and ((self.geometry().width()) != (822))):
            if ((len(str(self.title.text())) < len(self.current_text_display))):
                print("updated window size")
                self.setGeometry(10, 1080 - menu_height - 10, 822, menu_height)
            
            self.current_text_display = str(self.title.text())
    
        # if self.title.text() != str(str(text) + f"<span style=\"color:{color};\">{colored_text}</span>"):
            # self.title.setText(str(text) + f"<span style=\"color:{color};\">{colored_text}</span>")
        self.title.setText(str(text))

        if (self.subtitle.text() != colored_text):
            self.subtitle.setText(colored_text)
            
            if (self.subtitle.palette().color(QPalette.WindowText).rgba() != QColor(color).rgba()):
                palette = QPalette()
                palette.setColor(QPalette.WindowText, QColor(color))
                self.subtitle.setPalette(palette)
                pass

    def update_image_display(self, character_name):
        if self.current_character is not character_name and os.path.isfile(f"./res/skill_icons/{character_name}.webp"):
            pixmap = QPixmap(f"./res/skill_icons/{character_name}.webp")  # Replace with the path to your image
            self.profile_pic.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio))
            self.current_character = character_name


    def paintEvent(self, event):
        # menu_width, menu_height = 780, 150

        # print(len(str (self.title.text())), str(self.title.text()))
        # print(self.title.text(), self.current_text_display)
        # if ((str(self.title.text()) != self.current_text_display) and ((self.geometry().width()) != (822))):
        #     if ((len(str(self.title.text())) < len(self.current_text_display))):
        #         print("updated window size")
        #         self.setGeometry(10, 1080 - menu_height - 10, 822, menu_height)
            
        #     self.current_text_display = str(self.title.text())
        
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

    rotation_file_paths = ["./res/idle.txt", "./res/p1.txt", "./res/p2.txt"]
    rotation_names = ["Idle", "P1", "P2"]

    # total_assault_helper_thread = threading.Thread(target=total_assault_helper.start, args=(f"./res/{sys.argv[1]}", update_display, update_progress_bar))
    emitter = SignalEmitter()
    emitter.update_display.connect(update_display)

    helper_client = TotalAssaultHelper(emitter, rotation_file_paths, update_display, update_progress_bar)

    helper_client_thread = threading.Thread(target=helper_client.start, )
    helper_client_thread.start()

    keyListenerThread = threading.Thread(target=tw.onKeyPressEvent)
    keyListenerThread.start()

    invisOverlay = invisible_overlay.InvisibleOverlay(rotation_names)
    invisOverlay.show()

    time.sleep(1)
    tw.init_update_fn(helper_client.update_actions, invisOverlay.onKeyPressEvent)
    
    # helper_client.update_label_signal.connect(tw.update_text_display)
    # invisible_overlay_thread = threading.Thread(target=invisible_overlay.start)
    # invisible_overlay_thread.start()

    print(tw.geometry())

    exit_code = app.exec_()
    print("Exit")
    sys.exit(exit_code)

def update_display(text, colored_text, color, character_name):
    tw.update_text_display(text, colored_text, color)
    tw.update_image_display(character_name)

def update_progress_bar(percent, immediate=False):
    tw.setProgress(percent, immediate)


