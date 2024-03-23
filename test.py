import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QColor, QFontDatabase, QLinearGradient
from PyQt5.QtCore import Qt, QRectF
import utils

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

from PyQt5.QtGui import QColor

# Initial array of rainbow colors with alpha values
rainbow_colors_with_alpha = [
    QColor(255, 0, 0, 150),    # Red with alpha 150
    QColor(255, 127, 0, 150),  # Orange with alpha 150
    QColor(255, 255, 0, 150),  # Yellow with alpha 150
    QColor(0, 255, 0, 150),    # Green with alpha 150
    QColor(0, 0, 255, 150),    # Blue with alpha 150
    QColor(75, 0, 130, 150),   # Indigo with alpha 150
    QColor(148, 0, 211, 150)   # Violet with alpha 150
]

# Function to linearly interpolate (lerp) between two QColor objects
def lerp_color(color1, color2, t):
    """
    Linearly interpolates between color1 and color2 by t.
    t = 0 returns color1, t = 1 returns color2.
    """
    return QColor(
        int(color1.red() + (color2.red() - color1.red()) * t),
        int(color1.green() + (color2.green() - color1.green()) * t),
        int(color1.blue() + (color2.blue() - color1.blue()) * t),
        int(color1.alpha() + (color2.alpha() - color1.alpha()) * t),
    )

# Generate the new array of colors with 10 interpolated colors between each pair of original colors
expanded_rainbow_colors = []

for i in range(len(rainbow_colors_with_alpha) - 1):
    expanded_rainbow_colors.append(rainbow_colors_with_alpha[i])
    for t in range(1, 11):
        interpolated_color = lerp_color(rainbow_colors_with_alpha[i], rainbow_colors_with_alpha[i + 1], t / 11.0)
        expanded_rainbow_colors.append(interpolated_color)
expanded_rainbow_colors.append(rainbow_colors_with_alpha[-1])

# Extracting the colors as requested, no code output
for color in expanded_rainbow_colors:
    print(f"""QColor({color.red()}, {color.green()}, {color.blue()}, {color.alpha()}),""")