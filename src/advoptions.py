import re
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLabel, QComboBox, QPushButton,
    QLineEdit
)

class AdvancedOptionsDialog(QDialog):
    def __init__(self, crosshair):
        super().__init__()
        self.crosshair = crosshair
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Advanced Options")
        self.setGeometry(200, 200, 300, 200)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)

        layout = QVBoxLayout()

        form_layout = QFormLayout()

        color_label = QLabel("Crosshair Color:")
        self.color_input = QComboBox()
        self.populate_color_palette()
        self.color_input.currentTextChanged.connect(self.update_color)
        form_layout.addRow(color_label, self.color_input)

        self.hex_color_input = QLineEdit()
        self.hex_color_input.textChanged.connect(self.update_color)

        shape_label = QLabel("Crosshair Shape:")
        self.shape_input = QComboBox()
        self.populate_shape_options()
        self.shape_input.currentTextChanged.connect(self.update_shape)
        form_layout.addRow(shape_label, self.shape_input)

        layout.addLayout(form_layout)

        self.outline_border_button = QPushButton("Add Outline Border")
        self.outline_border_button.clicked.connect(self.toggle_outline_border)
        layout.addWidget(self.outline_border_button)

        self.setLayout(layout)

        self.setStyleSheet(
            """
            QDialog {
            background-color: #2b2b2b;
            color: white;
            font-size: 14px;
            }
            QLabel {
                color: #ff5555;
            }
            QComboBox, QPushButton, QLineEdit {
                background-color: #444444;
                color: white;
                border: 1px solid #ff5555;
                border-radius: 5px;
                width: 100%;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #ff5555;
                color: #2b2b2b;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #ff5555;
                background-color: #444444;
                color: white;
                selection-background-color: #ff5555;
            }
            """
        )

    def populate_color_palette(self):
        colors = ["#ff4040", "#89ffa0", "#0000ff", "#777fff", "#777fff", "#a75ad0", "#ffe589"]
        for color in colors:
            self.color_input.addItem(color)
        self.color_input.setEditable(True)

    def populate_shape_options(self):
        for i in range(1, 11):
            self.shape_input.addItem(str(i))

    def update_color(self, value):
        if self.is_valid_hex_color(value):
            self.crosshair.set_crosshair_color(value)

    def update_shape(self, value):
        self.crosshair.set_crosshair_shape(value)

    def is_valid_hex_color(self, color):
        return re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', color)

    def toggle_outline_border(self):
        if self.crosshair.is_outline_border:
            self.crosshair.is_outline_border = False
            self.outline_border_button.setText("Add Outline Border")
        else:
            self.crosshair.is_outline_border = True
            self.outline_border_button.setText("Remove Outline Border")
        self.crosshair.repaint()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor("#444444"))
        painter.drawRect(self.rect())