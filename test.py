from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QLinearGradient, QPen
from PyQt5.QtCore import Qt
import sys

class GradientWidget(QWidget):
    def __init__(self, parent=None):
        super(GradientWidget, self).__init__(parent)
        self.setGeometry(300, 300, 400, 300)  # Set the window size

    def paintEvent(self, event):
        painter = QPainter(self)
        
        # Create a linear gradient
        gradient = QLinearGradient(0, 0, self.width(), self.height())  # diagonal gradient
        
        # Add color stops
        gradient.setColorAt(0.0, Qt.red)  # Start with red
        gradient.setColorAt(0.49, Qt.red)  # End red abruptly
        gradient.setColorAt(0.51, Qt.blue)  # Start blue abruptly
        gradient.setColorAt(1.0, Qt.blue)  # End with blue
        
        # Use the gradient as a brush
        painter.setBrush(gradient)
        
        # Set the pen for the border
        pen = QPen(Qt.white, 20)  # Black border with 5 pixels thickness
        painter.setPen(pen)
        
        # Draw the rectangle with the border
        painter.drawRect(0, 0, self.width()-1, self.height()-1)  # Subtract 1 to ensure the border is fully visible

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GradientWidget()
    window.show()
    sys.exit(app.exec_())
