import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt

class TransparentWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Transparent Window with Text')
        self.setGeometry(100, 100, 400, 300)

        # Set the window transparency
        self.setWindowOpacity(0.5)  # Adjust the opacity here

        # Adding a label with non-transparent text
        self.label = QLabel('This text is not transparent', self)
        self.label.setStyleSheet("QLabel { color : black; font: 20pt; }")
        self.label.setAlignment(Qt.AlignCenter)

        # Layout to center the label
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)

        self.setLayout(layout)

        # Alternatively, to make the window's background completely transparent (including no frame):
        # self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.show()

def main():
    app = QApplication(sys.argv)
    tw = TransparentWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
