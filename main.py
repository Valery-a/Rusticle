import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QSlider, QVBoxLayout, QMainWindow, QPushButton
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt, QPoint, pyqtSignal

class CrosshairApp(QMainWindow):
    diameterChanged = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.diameter = 50
        self.alpha = 0.5
        self.initUI()

    def initUI(self):
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowTransparentForInput)

        self.center_crosshair()
        self.setGeometry(self.new_window_x, self.new_window_y, self.window_width, self.window_height)
        self.show()

    def center_crosshair(self):
        screen_geometry = QApplication.desktop().availableGeometry()
        screen_center_x = screen_geometry.x() + screen_geometry.width() // 2
        screen_center_y = screen_geometry.y() + screen_geometry.height() // 2

        title_bar_height = self.frameGeometry().height() - self.geometry().height()

        self.window_width = self.geometry().width()
        self.window_height = self.geometry().height()

        self.new_window_x = screen_center_x - self.window_width // 2
        self.new_window_y = screen_center_y - self.window_height // 2 - title_bar_height // 2

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(Qt.white, 2))

        center_x = self.width() // 2
        center_y = self.height() // 2
        half_line = self.diameter // 2

        painter.drawLine(center_x, center_y - half_line, center_x, center_y + half_line)


        painter.drawLine(center_x - half_line, center_y, center_x + half_line, center_y)

        painter.end()

    def set_transparency(self, alpha):
        self.setWindowOpacity(alpha)

    def update_diameter(self, diameter):
        try:
            self.diameter = diameter
            self.center_crosshair()
            self.repaint()
            self.diameterChanged.emit(diameter)
        except ValueError:
            pass

class OptionsMenu(QWidget):
    def __init__(self, crosshair):
        super().__init__()
        self.crosshair = crosshair
        self.initUI()

    def initUI(self):
        self.setWindowTitle("BOMBA MENU")
        self.setGeometry(100, 100, 300, 200)

        diameter_label = QLabel("Bomba the diameter of the crosshair in pixels:")
        self.diameter_input = QLineEdit(str(self.crosshair.diameter))
        self.diameter_input.setStyleSheet(
            """
            QLineEdit {
                background-color: #222;
                color: #fff;
                border: 2px solid #555;
                border-radius: 5px;
                padding: 5px;
            }
            """
        )

        vertical_adjust_label = QLabel("Lower the crosshair position in bomba pixels")
        self.vertical_adjust_input = QLineEdit(str(0))
        self.vertical_adjust_input.setStyleSheet(
            """
            QLineEdit {
                background-color: #222;
                color: #fff;
                border: 2px solid #555;
                border-radius: 5px;
                padding: 5px;
            }
            """
        )

        self.apply_button = QPushButton("Apply")
        self.apply_button.clicked.connect(self.apply_changes)
        self.apply_button.setStyleSheet(
            """
            QPushButton {
                background-color: #007BFF;
                color: #fff;
                border: 2px solid #0056b3;
                border-radius: 5px;
                padding: 5px;
            }

            QPushButton:hover {
                background-color: #0056b3;
            }
            """
        )

        alpha_label = QLabel("Hide your bomba? (0 to 1)")
        self.alpha_slider = QSlider(Qt.Horizontal)
        self.alpha_slider.setMinimum(0)
        self.alpha_slider.setMaximum(100)
        self.alpha_slider.setValue(int(self.crosshair.alpha * 100))
        self.alpha_slider.valueChanged.connect(self.update_alpha)
        self.alpha_slider.setStyleSheet(
            """
            QSlider::groove:horizontal {
                height: 6px;
                background: #777;
            }

            QSlider::handle:horizontal {
                width: 16px;
                height: 16px;
                margin: -5px 0;
                background: #007BFF;
                border: 2px solid #0056b3;
                border-radius: 8px;
            }
            """
        )

        layout = QVBoxLayout()
        layout.addWidget(diameter_label)
        layout.addWidget(self.diameter_input)
        layout.addWidget(vertical_adjust_label)
        layout.addWidget(self.vertical_adjust_input)
        layout.addWidget(self.apply_button)
        layout.addWidget(alpha_label)
        layout.addWidget(self.alpha_slider)
        layout.addStretch()

        self.setLayout(layout)

    def apply_changes(self):
        diameter_text = self.diameter_input.text()
        vertical_adjust_text = self.vertical_adjust_input.text()

        try:
            diameter = int(diameter_text)
            vertical_adjust = int(vertical_adjust_text)
            self.crosshair.update_diameter(diameter)

            self.crosshair.new_window_y += vertical_adjust
            self.crosshair.setGeometry(self.crosshair.new_window_x, self.crosshair.new_window_y,
                                       self.crosshair.window_width, self.crosshair.window_height)

        except ValueError:
            pass

    def update_alpha(self, value):
        self.crosshair.alpha = value / 100.0
        self.crosshair.set_transparency(self.crosshair.alpha)
        self.crosshair.repaint()

def main():
    app = QApplication(sys.argv)

    crosshair_app = CrosshairApp()

    options_menu = OptionsMenu(crosshair_app)
    options_menu.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
