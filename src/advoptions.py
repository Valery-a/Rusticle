from PyQt5.QtWidgets import QFormLayout, QDialog, QLabel, QLineEdit, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt

class AdvancedOptionsDialog(QDialog):
    def __init__(self, crosshair):
        super().__init__()
        self.crosshair = crosshair
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Advanced Options")
        self.setGeometry(200, 200, 300, 200)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setFixedSize(300, 300)

        layout = QVBoxLayout()

        form_layout = QFormLayout()

        color_label = QLabel("Crosshair Color:")
        self.color_input = QLineEdit("#ffffff")
        form_layout.addRow(color_label, self.color_input)

        shape_label = QLabel("Crosshair Shape:")
        self.shape_input = QLineEdit("1-10") 
        form_layout.addRow(shape_label, self.shape_input)

        layout.addLayout(form_layout)

        self.outline_border_button = QPushButton("Add Outline Border")
        self.outline_border_button.clicked.connect(self.toggle_outline_border)
        layout.addWidget(self.outline_border_button)

        apply_button = QPushButton("Apply")
        apply_button.clicked.connect(self.apply_changes)
        layout.addWidget(apply_button)

        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)

        self.setLayout(layout)

        self.setStyleSheet(
            """
            QDialog {
                background-color: #282c34;
                color: white;
                font-size: 14px;
                border-radius: 10px;  /* Rounded borders */
            }
            QLabel {
                color: #66d9ef;
            }
            QLineEdit, QPushButton {
                background-color: #44475a;
                color: white;
                border: 1px solid #66d9ef;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #66d9ef;
                color: #282c34;
            }
            """
        )

    def apply_changes(self):
        color = self.color_input.text()
        shape = self.shape_input.text()

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
