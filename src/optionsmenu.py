from PyQt5.QtWidgets import QSlider, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QGroupBox, QCheckBox
from PyQt5.QtCore import Qt, QPoint
import platform
from pynput.mouse import Listener
import os
import json

from advoptions import AdvancedOptionsDialog
from bar import TitleBar
from calculator import CalculatorDialog

class OptionsMenu(QFrame):
    def __init__(self, crosshair):
        super().__init__()
        self.crosshair = crosshair
        self.right_button_enabled = False
        self.listener = None
        self.initUI()
        self.load_settings()

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        self.setGeometry(200, 200, 300, 200)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        checkbox_stylesheet = """
    QCheckBox {
        background-color: #444444;
        color: white;
        border: 1px solid #ff5555;
        border-radius: 5px;
        padding: 8.5px;
        font-size: 14px;
    }
    QCheckBox::indicator {
        width: 20px;
        height: 20px;
        background-color: #444444;
        border: 1px solid #ff5555;
        border-radius: 4px;
    }
    QCheckBox::indicator:checked {
        background-color: red;
    }
    QCheckBox:hover {
        background-color: #ff5555;
        color: #2b2b2b;
    }
"""


        button_stylesheet = """
            QPushButton {
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
        """

        darker_button_stylesheet = """
            QPushButton {
                background-color: #de0d0d;
                color: #FFFFFF;
                border: none;
                border-radius: 5px;
                padding: 8px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #8B0000;
            }
        """
        
        self.config_save_button = QPushButton("Config Save")
        self.config_save_button.clicked.connect(self.save_settings)
        self.config_save_button.setStyleSheet(darker_button_stylesheet)
        layout.addWidget(self.config_save_button)

        settings_group = QGroupBox("(˵ ͡° ͜ʖ ͡°˵)")
        settings_layout = QVBoxLayout()

        diameter_label = QLabel("Change the diameter of the crosshair in pixels:")
        self.diameter_input = QLineEdit(str(0))

        vertical_adjust_label = QLabel("Adjust the crosshair position in pixels")
        self.vertical_adjust_input = QLineEdit(str(0))

        alpha_label = QLabel("Adjust the transparency of the crosshair: (0 to 1)")
        self.alpha_slider = QSlider(Qt.Horizontal)
        self.alpha_slider.setMinimum(0)
        self.alpha_slider.setMaximum(100)
        self.alpha_slider.setValue(int(self.crosshair.alpha * 100))
        self.alpha_slider.valueChanged.connect(self.update_alpha)

        settings_layout.addWidget(diameter_label)
        settings_layout.addWidget(self.diameter_input)
        settings_layout.addWidget(vertical_adjust_label)
        settings_layout.addWidget(self.vertical_adjust_input)
        settings_layout.addWidget(alpha_label)
        settings_layout.addWidget(self.alpha_slider)
        settings_layout.addStretch()

        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)

        button_layout = QHBoxLayout()
        self.apply_button = QPushButton("Apply")
        self.apply_button.clicked.connect(self.apply_changes)
        self.apply_button.setStyleSheet(button_stylesheet)
        button_layout.addWidget(self.apply_button)

        self.hide_crosshair_checkbox = QCheckBox("Hide crosshair on R-click")
        self.hide_crosshair_checkbox.clicked.connect(self.toggle_right_button_functionality)
        self.hide_crosshair_checkbox.setStyleSheet(checkbox_stylesheet)
        button_layout.addWidget(self.hide_crosshair_checkbox)

        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.alpha_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #ff5555;
                background: #444444;
                height: 8px;
                width 90%;
            }

            QSlider::handle:horizontal {
                background: #ff5555;
                border: 1px solid #ff5555;
                width: 16px;
                height: 16px;
                margin: -4px 0;
                border-radius: 2px;
            }
        """)

        self.setStyleSheet(
            """
            QDialog, QGroupBox {
                background-color: #2b2b2b;
                color: white;
                font-size: 14px;
            }
            QLabel {
                color: #ff5555;
            }
            QComboBox, QPushButton, QLineEdit, QCheckBox {
                background-color: #444444;
                color: white;
                border: 1px solid #ff5555;
                padding: 10px;
                font-size: 14px;
            }
            QComboBox:hover, QPushButton:hover, QCheckBox:hover {
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

        

    def save_settings(self):
        settings = {
            "diameter": self.crosshair.diameter,
            "alpha": self.crosshair.alpha,
            "crosshair_color": self.crosshair.crosshair_color.name(),
            "crosshair_shape": self.crosshair.crosshair_shape,
            "is_outline_border": self.crosshair.is_outline_border,
            "vertical_adjust_input": int(self.vertical_adjust_input.text()),
        }

        config_folder = "config"
        os.makedirs(config_folder, exist_ok=True) 
        config_path = os.path.join(config_folder, "config.json")

        with open(config_path, "w") as config_file:
            json.dump(settings, config_file)

    def load_settings(self):
        config_folder = "config"
        config_path = os.path.join(config_folder, "config.json")

        try:
            with open(config_path, "r") as config_file:
                settings = json.load(config_file)

            self.crosshair.update_diameter(settings.get("diameter", self.crosshair.diameter))
            self.crosshair.alpha = settings.get("alpha", self.crosshair.alpha)
            self.crosshair.set_transparency(self.crosshair.alpha)
            self.crosshair.set_crosshair_color(settings.get("crosshair_color", self.crosshair.crosshair_color.name()))
            self.crosshair.set_crosshair_shape(settings.get("crosshair_shape", self.crosshair.crosshair_shape))
            self.crosshair.is_outline_border = settings.get("is_outline_border", self.crosshair.is_outline_border)
            self.crosshair.new_window_y += settings.get("vertical_adjust_input", 0) 
            self.crosshair.setGeometry(self.crosshair.new_window_x, self.crosshair.new_window_y,
                                       self.crosshair.window_width, self.crosshair.window_height)
            self.crosshair.repaint()

        except (FileNotFoundError, json.JSONDecodeError):
            pass

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

    def on_click_windows(self, x, y, button, pressed):
        if button == button.right and pressed and self.right_button_enabled:
            self.crosshair.hide()

        if button == button.right and not pressed:
            self.crosshair.show()

    def on_click_other(self, x, y, button, pressed):
        if button == button.right and not pressed:
            self.crosshair.show()

    def toggle_right_button_functionality(self):
        self.right_button_enabled = not self.right_button_enabled
        if self.right_button_enabled:
            if platform.system() == "Windows":
                self.listener = Listener(on_click=self.on_click_windows)
            else:
                self.listener = Listener(on_click=self.on_click_other)
            self.listener.start()
        else:
            if self.listener is not None:
                self.listener.stop()
                self.listener = None 
