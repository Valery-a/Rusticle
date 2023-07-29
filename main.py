import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen

class CrosshairApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowTransparentForInput)
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(Qt.white, 2))

        center_x = self.width() // 2
        center_y = self.height() // 2
        diameter = 50
        half_line = diameter // 2

        painter.drawLine(center_x, center_y - half_line, center_x, center_y + half_line)
        painter.drawLine(center_x - half_line, center_y, center_x + half_line, center_y)

def main():
    app = QApplication(sys.argv)
    crosshair_app = CrosshairApp()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
