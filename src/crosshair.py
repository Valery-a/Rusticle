from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, pyqtSignal, QRect
from PyQt5.QtGui import QPainter, QPen, QColor

class CrosshairApp(QMainWindow):
    closeRequested = pyqtSignal()
    diameterChanged = pyqtSignal(int)

    def closeEvent(self, event):
        self.closeRequested.emit()
        super().closeEvent(event)

    def __init__(self):
        super().__init__()
        self.diameter = 0
        self.alpha = 1
        self.initUI()
        self.crosshair_color = QColor(Qt.white)
        self.crosshair_shape = "cross"
        self.is_outline_border = False

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

        center_x = self.width() // 2
        center_y = self.height() // 2
        half_line = self.diameter // 2
        bounding_rect = QRect(center_x - half_line, center_y - half_line, self.diameter, self.diameter)

        if self.is_outline_border:
            painter.setPen(QPen(Qt.black, 4))
            painter.drawRect(bounding_rect.adjusted(-2, -2, 2, 2))

        painter.setPen(QPen(self.crosshair_color, 2))

        if self.crosshair_shape == "1":  # circle
            painter.drawEllipse(center_x - half_line, center_y - half_line, self.diameter, self.diameter)
        elif self.crosshair_shape == "2":  # x_mark
            painter.drawLine(center_x - half_line, center_y - half_line, center_x + half_line, center_y + half_line)
            painter.drawLine(center_x - half_line, center_y + half_line, center_x + half_line, center_y - half_line)
        elif self.crosshair_shape == "3":  # plus
            painter.drawLine(center_x, center_y - half_line, center_x, center_y + half_line)
            painter.drawLine(center_x - half_line, center_y, center_x + half_line, center_y)
        elif self.crosshair_shape == "4":  # gap_cross
            gap_size = self.diameter // 3
            painter.drawLine(center_x - half_line, center_y, center_x - gap_size, center_y)
            painter.drawLine(center_x + gap_size, center_y, center_x + half_line, center_y)
            painter.drawLine(center_x, center_y - half_line, center_x, center_y - gap_size)
            painter.drawLine(center_x, center_y + gap_size, center_x, center_y + half_line)
        elif self.crosshair_shape == "8":  # cross_in_circle
            painter.drawEllipse(center_x - half_line, center_y - half_line, self.diameter, self.diameter)
            gap_size = self.diameter // 4
            painter.drawLine(center_x - gap_size, center_y, center_x + gap_size, center_y)
            painter.drawLine(center_x, center_y - gap_size, center_x, center_y + gap_size)
        elif self.crosshair_shape == "7":  # custom
            gap_size = self.diameter // 3
            painter.drawLine(center_x - half_line, center_y - gap_size, center_x - half_line, center_y + gap_size)
            painter.drawLine(center_x + half_line, center_y - gap_size, center_x + half_line, center_y + gap_size)
            painter.drawLine(center_x - gap_size, center_y - half_line, center_x + gap_size, center_y - half_line)
            painter.drawLine(center_x - gap_size, center_y + half_line, center_x + gap_size, center_y + half_line)
        elif self.crosshair_shape == "5":  # cross
            painter.drawEllipse(center_x, center_y, 1, 1)
        elif self.crosshair_shape == "6":  # dot
            gap_size = self.diameter // 4
            painter.drawLine(center_x - half_line, center_y, center_x - gap_size, center_y)
            painter.drawLine(center_x + gap_size, center_y, center_x + half_line, center_y)
            painter.drawLine(center_x, center_y - half_line, center_x, center_y - gap_size)
            painter.drawLine(center_x, center_y + gap_size, center_x, center_y + half_line)
        elif self.crosshair_shape == "9":  # diamond
            painter.drawLine(center_x, center_y - half_line, center_x + half_line, center_y)
            painter.drawLine(center_x + half_line, center_y, center_x, center_y + half_line)
            painter.drawLine(center_x, center_y + half_line, center_x - half_line, center_y)
            painter.drawLine(center_x - half_line, center_y, center_x, center_y - half_line)
        elif self.crosshair_shape == "10":  # arrow
            arrow_size = self.diameter // 4
            painter.drawLine(center_x, center_y - half_line, center_x, center_y + half_line)
            painter.drawLine(center_x - arrow_size, center_y, center_x, center_y - half_line + arrow_size)
            painter.drawLine(center_x + arrow_size, center_y, center_x, center_y - half_line + arrow_size)
        else:
            painter.drawLine(center_x, center_y - half_line, center_x, center_y + half_line)
            painter.drawLine(center_x - half_line, center_y, center_x + half_line, center_y)

        painter.end()

    def set_crosshair_color(self, color):
        self.crosshair_color = QColor(color)
        self.repaint()

    def set_crosshair_shape(self, shape):
        self.crosshair_shape = shape.lower()
        self.repaint()

    def toggle_outline_border(self):
        self.is_outline_border = not self.is_outline_border
        self.repaint()

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