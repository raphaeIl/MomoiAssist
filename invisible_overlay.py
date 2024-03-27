from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QMainWindow, QDesktopWidget

import threading
import time

class InvisibleOverlay(QMainWindow):
    def __init__(self, rotation_names):
        super().__init__()
        fontPath = './res/fonts/Google_Sans-500-100_0-0_0.ttf'
        QFontDatabase.addApplicationFont(fontPath)

        self.setWindowTitle("Overlay Window")

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowTransparentForInput)
        self.setAttribute(Qt.WA_TranslucentBackground)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.current_rotation_index = 0
        self.rotation_names = rotation_names
        
        layout = QVBoxLayout()
        
        self.label = QLabel('This is a centered label')
        self.label.setAlignment(Qt.AlignCenter) 
        
        layout.addWidget(self.label)
        self.setWindowOpacity(0)

        with open('./res/styles/invis_style.qss', 'r') as f:
            style = f.read()
            self.label.setStyleSheet(style)

        central_widget.setLayout(layout)
        
        self.setGeometry(100, 100, 600, 400)  # x, y, width, height
        self.centerWindow()

    def onKeyPressEvent(self):
        self.current_rotation_index += 1
        self.setWindowOpacity(1)
        self.label.setText(self.rotation_names[self.current_rotation_index % len(self.rotation_names)])

        if self.windowOpacity() == 1:
            threading.Thread(target=self.decrease_opacity).start()
                    
    def decrease_opacity(self):
        while self.windowOpacity() > 0:
            self.setWindowOpacity(self.windowOpacity() - 0.05)
            time.sleep(0.05)

    def centerWindow(self):
        qr = self.frameGeometry()
        screen_geometry = QDesktopWidget().availableGeometry()
        qr.moveTop(screen_geometry.top())
        qr.setX(int(1080 / 2) - 250)
        self.move(qr.topLeft())