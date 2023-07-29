from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QColor

class TitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setAutoFillBackground(True)

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.title_label = QLabel("RustOracle", self)
        self.title_label.setStyleSheet("background-color: gray; color: black; font-size: 18px; padding-left: 10px;")

        self.close_button = QPushButton("×", self)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: black;
                font-size: 20px;
                width: 25px;
                height: 25px;
                border: none;
                margin: 0;
            }
            QPushButton:hover {
                border: 1px solid #ccc; 
                border-radius: 5px;
                background-color: #dc3545;
            }
        """)
        self.close_button.clicked.connect(self.parent().closeEvent)

        self.minimize_button = QPushButton("–", self)
        self.minimize_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: black;
                font-size: 20px;
                width: 25px;
                height: 25px;
                border: none;
                margin: 0;
            }
            QPushButton:hover {
                border: 1px solid #ccc; 
                border-radius: 5px;
                background-color: #Ffa500;
            }
        """)
        self.minimize_button.clicked.connect(self.parent().showMinimized)

        self.layout.addWidget(self.title_label, 1, Qt.AlignLeft)
        self.layout.addWidget(self.minimize_button, 0, Qt.AlignRight)
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
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(QColor(64, 64, 64), 1))  # Set the pen color to dark gray
        painter.drawRect(0, 0, self.width() - 1, self.height() - 1)
        painter.end()
