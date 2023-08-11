from PyQt5.QtWidgets import QFormLayout, QDialog, QLabel, QComboBox, QVBoxLayout, QPushButton, QGraphicsOpacityEffect
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtCore import Qt, QParallelAnimationGroup, QRect, QSequentialAnimationGroup

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
        form_layout.addRow(color_label, self.color_input)

        shape_label = QLabel("Crosshair Shape:")
        self.shape_input = QComboBox()
        self.populate_shape_options()
        form_layout.addRow(shape_label, self.shape_input)

        layout.addLayout(form_layout)

        self.outline_border_button = QPushButton("Add Outline Border")
        self.outline_border_button.clicked.connect(self.toggle_outline_border)
        layout.addWidget(self.outline_border_button)

        apply_button = QPushButton("Apply")
        apply_button.clicked.connect(self.apply_changes)
        layout.addWidget(apply_button)

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
            QComboBox, QPushButton {
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
        colors = ["#ff5555", "#444444", "#555555", "#666666", "#777777", "#888888", "#999999"]
        for color in colors:
            self.color_input.addItem(color)

    def populate_shape_options(self):
        for i in range(1, 11):
            self.shape_input.addItem(str(i))

    def apply_changes(self):
        color = self.color_input.currentText()
        shape = self.shape_input.currentText()

        self.crosshair.set_crosshair_color(color)
        self.crosshair.set_crosshair_shape(shape)

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
