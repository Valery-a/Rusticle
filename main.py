import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QSlider, QVBoxLayout, QMainWindow, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QPen

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

class TitleBar(QWidget):
    import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QSlider, QVBoxLayout, QMainWindow, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QPen

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

class TitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setAutoFillBackground(True)

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.title_label = QLabel("BOMBA MENU", self)
        self.title_label.setStyleSheet("color: black; font-size: 18px; padding-left: 10px;")

        self.close_button = QPushButton("×", self)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: black;
                font-size: 20px;
                width: 30px;
                height: 30px;
                border: none;
                margin: 0;
            }
            QPushButton:hover {
                background-color: #dc3545;
            }
        """)
        self.close_button.clicked.connect(self.parent().close)

        self.layout.addWidget(self.title_label, 1, Qt.AlignLeft)
        self.layout.addWidget(self.close_button, 0, Qt.AlignRight)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.globalPos() - self.parent().pos()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and hasattr(self, 'drag_start_position'):
            self.parent().move(event.globalPos() - self.drag_start_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and hasattr(self, 'drag_start_position'):
            del self.drag_start_position

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 1))  # Set border color and thickness

        # Draw the border around all sides of the widget
        painter.drawRect(0, 0, self.width()-1, self.height()-1)

        painter.end()
        
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QSlider, QVBoxLayout, QHBoxLayout, QPushButton
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QPen

class OptionsMenu(QWidget):
    def __init__(self, crosshair):
        super().__init__()
        self.crosshair = crosshair
        self.is_night_theme = False  # We start with the day theme
        self.initUI()

    def initUI(self):
        self.setWindowTitle("BOMBA MENU")
        self.setGeometry(100, 100, 300, 200)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        # Main layout
        layout = QVBoxLayout()

        # Title Bar
        self.title_bar = TitleBar(self)
        layout.addWidget(self.title_bar)

        # Apply Button
        self.apply_button = QPushButton("Apply")
        self.apply_button.clicked.connect(self.apply_changes)
        self.apply_button.setStyleSheet(
            "QPushButton { background-color: #505954; color: #fff; border: none; border-radius: 5px; padding: 8px; min-width: 50px; } QPushButton:hover { background-color: #303532; }"
        )

        # Night/Day Theme Button
        self.night_day_button = QPushButton("Night")
        self.night_day_button.clicked.connect(self.toggle_night_day_theme)
        self.night_day_button.setStyleSheet(
            "QPushButton { background-color: #A1B3A8; color: #fff; border: none; border-radius: 5px; padding: 8px; min-width: 80px; } QPushButton:hover { background-color: #808f86; }"
        )

        # Crosshair Diameter
        diameter_label = QLabel("Bomba the diameter of the crosshair in pixels:")
        self.diameter_input = QLineEdit(str(self.crosshair.diameter))
        self.diameter_input.setStyleSheet(
            "QLineEdit { background-color: #f0f0f0; color: #333; border: 1px solid #ccc; border-radius: 5px; padding: 5px; }"
        )

        # Vertical Adjust
        vertical_adjust_label = QLabel("Adjust the crosshair position in bomba pixels")
        self.vertical_adjust_input = QLineEdit(str(0))
        self.vertical_adjust_input.setStyleSheet(
            "QLineEdit { background-color: #f0f0f0; color: #333; border: 1px solid #ccc; border-radius: 5px; padding: 5px; }"
        )

        # Transparency Slider
        alpha_label = QLabel("Hide your bomba? (0 to 1)")
        self.alpha_slider = QSlider(Qt.Horizontal)
        self.alpha_slider.setMinimum(0)
        self.alpha_slider.setMaximum(100)
        self.alpha_slider.setValue(int(self.crosshair.alpha * 100))
        self.alpha_slider.valueChanged.connect(self.update_alpha)
        self.alpha_slider.setStyleSheet(
            "QSlider::groove:horizontal { height: 6px; background: #ccc; border-radius: 3px; } QSlider::handle:horizontal { width: 16px; height: 16px; margin: -5px 0; background: #007BFF; border: 2px solid #0056b3; border-radius: 8px; }"
        )

        # Create a horizontal layout for the buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.night_day_button)
        button_layout.addWidget(self.apply_button)

        # Add widgets to the layout
        layout.addLayout(button_layout)
        layout.addWidget(diameter_label)
        layout.addWidget(self.diameter_input)
        layout.addWidget(vertical_adjust_label)
        layout.addWidget(self.vertical_adjust_input)
        layout.addWidget(alpha_label)
        layout.addWidget(self.alpha_slider)
        layout.addStretch()

        self.setLayout(layout)
        self.set_day_theme()  # Start with the day theme

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

    def toggle_night_day_theme(self):
        if self.is_night_theme:
            self.set_day_theme()
        else:
            self.set_night_theme()

    def set_day_theme(self):
        self.setStyleSheet(
            "OptionsMenu { background-color: #f5f5f5; } QLabel, QLineEdit { color: #333; } QPushButton { background-color: #007BFF; color: #fff; }"
        )
        self.night_day_button.setText("Night")
        self.is_night_theme = False

    def set_night_theme(self):
        self.setStyleSheet(
            "OptionsMenu { background-color: #303030; } QLabel, QLineEdit { color: #f0f0f0; } QPushButton { background-color: #212121; color: #fff; }"
        )
        self.night_day_button.setText("Day")
        self.is_night_theme = True
    
def main():
    app = QApplication(sys.argv)

    crosshair_app = CrosshairApp()

    options_menu = OptionsMenu(crosshair_app)
    options_menu.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
