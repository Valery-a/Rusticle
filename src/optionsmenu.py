from PyQt5.QtWidgets import (QSlider, QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFrame)
from PyQt5.QtCore import (Qt, QPoint)
import os, json, webbrowser

from advoptions import AdvancedOptionsDialog
from bar import TitleBar
from calculator import CalculatorDialog

class OptionsMenu(QFrame):
    def __init__(self, crosshair):
        super().__init__()
        self.crosshair = crosshair
        self.is_night_theme = False
        self.initUI()
        self.load_settings()

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        self.setWindowTitle("WILDOracle++")
        self.setGeometry(666, 666, 666, 666)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        self.title_bar = TitleBar(self)
        layout.addWidget(self.title_bar)

        self.config_save_button = QPushButton("╚═ Save Config ═╝")
        self.config_save_button.clicked.connect(self.save_settings)
        self.config_save_button.setStyleSheet(
            "QPushButton { background-color: #FF9900; color: #000000; border: none; border-radius: 50px; padding: 10px; min-width: 150px; } QPushButton:hover { background-color: #FF6600; }"
        )
        layout.addWidget(self.config_save_button)

        self.apply_button = QPushButton("╚═ Apply Changes ═╝")
        self.apply_button.clicked.connect(self.apply_changes)
        self.apply_button.setStyleSheet(
            "QPushButton { background-color: #FFA500; color: #000000; border: none; border-radius: 50px; padding: 10px; min-width: 100px; } QPushButton:hover { background-color: #FF6600; }"
        )

        self.night_day_button = QPushButton("☾☼ NIGHT ☼☽")
        self.night_day_button.clicked.connect(self.toggle_night_day_theme)
        self.night_day_button.setStyleSheet(
            "QPushButton { background-color: #808f86; color: #000000; border: none; border-radius: 50px; padding: 10px; min-width: 130px; } QPushButton:hover { background-color: #707d75; }"
        )

        diameter_label = QLabel("Δ Change crosshair diameter (in pixels): Δ")
        self.diameter_input = QLineEdit(str(0))
        self.diameter_input.setStyleSheet(
            "QLineEdit { background-color: #f0f0f0; color: #333; border: 2px solid #ccc; background: #a5aad9; border-radius: 10px; padding: 15px; }"
        )

        self.advanced_options_button = QPushButton("➤ Advanced Options ➤")
        self.advanced_options_button.clicked.connect(self.open_advanced_options)
        self.advanced_options_button.setStyleSheet(
            "QPushButton { background-color: #707d75; color: #000000; border: none; border-radius: 50px; padding: 20px; min-width: 200px; } QPushButton:hover { background-color: #606b64; }"
        )

        vertical_adjust_label = QLabel("♨ Adjust vertical position (in pixels) ♨")
        self.vertical_adjust_input = QLineEdit(str(0))
        self.vertical_adjust_input.setStyleSheet(
            "QLineEdit { background-color: #f0f0f0; color: #333; border: 2px solid #ccc; background: #a5aad9; border-radius: 10px; padding: 15px; }"
        )
        layout.addWidget(vertical_adjust_label)
        layout.addWidget(self.vertical_adjust_input)

        alpha_label = QLabel("▤ Adjust crosshair transparency (0 to 1) ▤")
        self.alpha_slider = QSlider(Qt.Horizontal)
        self.alpha_slider.setMinimum(0)
        self.alpha_slider.setMaximum(100)
        self.alpha_slider.setValue(int(self.crosshair.alpha * 100))
        self.alpha_slider.valueChanged.connect(self.update_alpha)
        self.alpha_slider.setStyleSheet(
            "QSlider::groove:horizontal { height: 15px; background: #ccc; border-radius: 7px; } QSlider::handle:horizontal { width: 30px; height: 30px; margin: -5px 0; background: #a5aad9; border: 5px solid #a5aad9; border-radius: 20px; }"
        )

        self.calculator_button = QPushButton("♢ CALCULATOR ♢")
        self.calculator_button.clicked.connect(self.open_calculator)
        self.calculator_button.setStyleSheet(
            "QPushButton { background-color: #70ad47; color: #000000; border: none; border-radius: 50px; padding: 20px; min-width: 200px; } QPushButton:hover { background-color: #548235; }"
        )

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.night_day_button)
        button_layout.addWidget(self.apply_button)

        layout.addWidget(self.advanced_options_button)
        layout.addLayout(button_layout)
        layout.addWidget(diameter_label)
        layout.addWidget(self.diameter_input)
        layout.addWidget(vertical_adjust_label)
        layout.addWidget(self.vertical_adjust_input)
        layout.addWidget(alpha_label)
        layout.addWidget(self.alpha_slider)
        layout.addWidget(self.calculator_button)
        layout.addStretch()

        self.setLayout(layout)

        self.setStyleSheet(
            """
            OptionsMenu {
                background-color: #f5f5f5;
                border: 3px solid #ccc;
            }
            QLabel, QLineEdit {
                color: #333;
            }
            QPushButton {
                background-color: #007BFF;
                color: #fff;
            }
            """
        )
        
        self.set_day_theme()

    def open_calculator(self):
        calculator_dialog = CalculatorDialog(self)
        calculator_dialog.setModal(True)
        calculator_dialog.exec_()

    def save_settings(self):
        # Save the settings to a configuration file (e.g., config.json)
        settings = {
            "diameter": self.crosshair.diameter,
            "alpha": self.crosshair.alpha,
            "crosshair_color": self.crosshair.crosshair_color.name(),
            "crosshair_shape": self.crosshair.crosshair_shape,
            "is_outline_border": self.crosshair.is_outline_border,
            "night_theme": self.is_night_theme,
            "vertical_adjust_input": int(self.vertical_adjust_input.text()),
        }

        config_folder = "c0nF1g"
        os.makedirs(config_folder, exist_ok=True)
        config_path = os.path.join(config_folder, "s3cr3t_c0nF1g.json")

        with open(config_path, "w") as config_file:
            json.dump(settings, config_file, indent=2)

        webbrowser.open_new_tab("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    def load_settings(self):
        # Load settings from the configuration file (if available)
        config_folder = "c0nF1g"
        config_path = os.path.join(config_folder, "s3cr3t_c0nF1g.json")

        try:
            with open(config_path, "r") as config_file:
                settings = json.load(config_file)

            # Apply the loaded settings to the crosshair app
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

            # Load the theme setting and apply it
            self.is_night_theme = settings.get("night_theme", False)
            if self.is_night_theme:
                self.set_night_theme()
            else:
                self.set_day_theme()

        except (FileNotFoundError, json.JSONDecodeError):
            # The config file doesn't exist or is corrupted, do nothing
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
    
    def open_advanced_options(self):
        dialog = AdvancedOptionsDialog(self.crosshair)
        options_menu_position = self.mapToGlobal(QPoint(0, 0))
        x_offset = self.width() + 100
        y_offset = 100

        # Calculate the top-left position of the screen
        screen_top_left = QApplication.desktop().availableGeometry().topLeft()

        # Calculate the desired position for the dialog
        desired_position = options_menu_position + QPoint(x_offset, y_offset)

        # Ensure the dialog is within the top-left area of the screen
        if desired_position.x() < screen_top_left.x():
            desired_position.setX(screen_top_left.x())
        if desired_position.y() < screen_top_left.y():
            desired_position.setY(screen_top_left.y())

        dialog.move(desired_position)
        dialog.setModal(True)
        dialog.exec_()
    
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
        self.night_day_button.setText("☾☼ NIGHT ☼☽")
        self.is_night_theme = False

    def set_night_theme(self):
        self.setStyleSheet(
            "OptionsMenu { background-color: #303030; } QLabel, QLineEdit { color: #f0f0f0; } QPushButton { background-color: #212121; color: #fff; }"
        )
        self.night_day_button.setText("☼☾ DAY ☾☼")
        self.is_night_theme = True
