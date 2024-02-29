import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QColor, QFontDatabase, QLinearGradient
from PyQt5.QtCore import Qt, QRectF

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # fontPath = './res/ResourceHanRoundedCN-Bold.ttf'
        fontPath = './res/Google_Sans-500-100_0-0_0.ttf'
        QFontDatabase.addApplicationFont(fontPath)

        self.setWindowTitle("Profile UI")
        menu_width, menu_height = 960, 150

        self.setGeometry(int(1920 / 2) - 483, 1080 - menu_height + 10, menu_width, menu_height)  # Set the size of the window
        # self.setGeometry(int(1920 / 2) - 483, -10, menu_width, menu_height)  # Set the size of the window
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
        title = QLabel("通关10次任务或活动任务关卡", self)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        layout.addStretch(2)

        with open('./res/style.qss', 'r') as f:
            style = f.read()
            title.setStyleSheet(style)

        self.setLayout(layout)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # For smooth edges
        painter.setBrush(QBrush(QColor(0, 0, 100, 50)))  # Background color
        painter.setPen(Qt.NoPen)  # No border
        painter.drawRoundedRect(self.rect(), 15, 15)  # Rounded corners

        # Progress Bar
        bar_width, bar_height = 2999, 25
        bottom_padding = 30
        self.progress = 0.75
        gradient = QLinearGradient(200+self.width() / 2 - bar_width / 2, self.height() - bar_height - bottom_padding, bar_width, bar_height)
        gradient.setColorAt(self.progress, QColor(79, 197, 255, 220))
        gradient.setColorAt(self.progress, QColor(0, 0, 0, 100))

        rect = QRectF(self.width() / 2 - bar_width / 2, self.height() - bar_height - bottom_padding, bar_width, bar_height)
        painter.fillRect(rect, QBrush(gradient))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
