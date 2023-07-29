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

class OptionsMenu(QWidget):
    def __init__(self, crosshair):
        super().__init__()
        self.crosshair = crosshair
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Crosshair Options")
        self.setGeometry(100, 100, 300, 200)

        diameter_label = QLabel("Crosshair Diameter:")
        self.diameter_input = QLineEdit(str(self.crosshair.diameter))

        alpha_label = QLabel("Crosshair Transparency:")
        self.alpha_input = QLineEdit(str(self.crosshair.alpha))

        apply_button = QPushButton("Apply")
        apply_button.clicked.connect(self.apply_changes)

        layout = QVBoxLayout()
        layout.addWidget(diameter_label)
        layout.addWidget(self.diameter_input)
        layout.addWidget(alpha_label)
        layout.addWidget(self.alpha_input)
        layout.addWidget(apply_button)
        layout.addStretch()

        self.setLayout(layout)

    def apply_changes(self):
        try:
            diameter = int(self.diameter_input.text())
            alpha = float(self.alpha_input.text())
        except ValueError:
            pass

def main():
    app = QApplication(sys.argv)
    crosshair_app = CrosshairApp()
    options_menu = OptionsMenu(crosshair_app)
    options_menu.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
