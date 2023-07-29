import sys
import json
import os
from PyQt5.QtWidgets import QApplication, QGridLayout, QComboBox, QFormLayout, QDialog, QFrame, QWidget, QLabel, QLineEdit, QSlider, QVBoxLayout, QHBoxLayout, QMainWindow, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal, QPoint, QRect
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
            gap_size = self.diameter // 4
            painter.drawLine(center_x - half_line, center_y, center_x - gap_size, center_y)
            painter.drawLine(center_x + gap_size, center_y, center_x + half_line, center_y)
            painter.drawLine(center_x, center_y - half_line, center_x, center_y - gap_size)
            painter.drawLine(center_x, center_y + gap_size, center_x, center_y + half_line)
        elif self.crosshair_shape == "5":  # cross_in_circle
            painter.drawEllipse(center_x - half_line, center_y - half_line, self.diameter, self.diameter)
            gap_size = self.diameter // 4
            painter.drawLine(center_x - gap_size, center_y, center_x + gap_size, center_y)
            painter.drawLine(center_x, center_y - gap_size, center_x, center_y + gap_size)
        elif self.crosshair_shape == "6":  # custom
            painter.drawLine(center_x - half_line, center_y - half_line, center_x + half_line, center_y + half_line)
        elif self.crosshair_shape == "7":  # dot
            painter.drawEllipse(center_x, center_y, 1, 1)
        elif self.crosshair_shape == "8":  # diamond
            painter.drawLine(center_x, center_y - half_line, center_x + half_line, center_y)
            painter.drawLine(center_x + half_line, center_y, center_x, center_y + half_line)
            painter.drawLine(center_x, center_y + half_line, center_x - half_line, center_y)
            painter.drawLine(center_x - half_line, center_y, center_x, center_y - half_line)
        elif self.crosshair_shape == "9":  # arrow
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

class OptionsMenu(QFrame):
    def __init__(self, crosshair):
        super().__init__()
        self.crosshair = crosshair
        self.is_night_theme = False
        self.initUI()
        self.load_settings()

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(2, 2, 2, 2)

        self.setWindowTitle("RustOracle")
        self.setGeometry(100, 100, 300, 200)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        self.title_bar = TitleBar(self)
        layout.addWidget(self.title_bar)

        self.config_save_button = QPushButton("Config Save")
        self.config_save_button.clicked.connect(self.save_settings)
        self.config_save_button.setStyleSheet(
            "QPushButton { background-color: #FF9900; color: #000000; border: none; border-radius: 5px; padding: 8px; min-width: 100px; } QPushButton:hover { background-color: #FF6600; }"
        )
        layout.addWidget(self.config_save_button)

        self.apply_button = QPushButton("Apply")
        self.apply_button.clicked.connect(self.apply_changes)
        self.apply_button.setStyleSheet(
            "QPushButton { background-color: #FFA500; color: #000000; border: none; border-radius: 5px; padding: 8px; min-width: 50px; } QPushButton:hover { background-color: #FF6600; }"
        )

        self.night_day_button = QPushButton("Night")
        self.night_day_button.clicked.connect(self.toggle_night_day_theme)
        self.night_day_button.setStyleSheet(
            "QPushButton { background-color: #A1B3A8; color: #000000; border: none; border-radius: 5px; padding: 8px; min-width: 80px; } QPushButton:hover { background-color: #808f86; }"
        )

        diameter_label = QLabel("Change the diameter of the crosshair in pixels:")
        self.diameter_input = QLineEdit(str(self.crosshair.diameter))
        self.diameter_input.setStyleSheet(
            "QLineEdit { background-color: #f0f0f0; color: #333; border: 1px solid #ccc; border-radius: 5px; padding: 5px; }"
        )

        self.advanced_options_button = QPushButton("Advanced Options")
        self.advanced_options_button.clicked.connect(self.open_advanced_options)
        self.advanced_options_button.setStyleSheet(
            "QPushButton { background-color: #707d75; color: #000000; border: none; border-radius: 5px; padding: 8px; min-width: 100px; } QPushButton:hover { background-color: #606b64; }"
        )

        vertical_adjust_label = QLabel("Adjust the crosshair position in pixels")
        self.vertical_adjust_input = QLineEdit(str(0))
        self.vertical_adjust_input.setStyleSheet(
            "QLineEdit { background-color: #f0f0f0; color: #333; border: 1px solid #ccc; border-radius: 5px; padding: 5px; }"
        )
        layout.addWidget(vertical_adjust_label)
        layout.addWidget(self.vertical_adjust_input)

        alpha_label = QLabel("Adjust the transparency of the crosshair: (0 to 1)")
        self.alpha_slider = QSlider(Qt.Horizontal)
        self.alpha_slider.setMinimum(0)
        self.alpha_slider.setMaximum(100)
        self.alpha_slider.setValue(int(self.crosshair.alpha * 100))
        self.alpha_slider.valueChanged.connect(self.update_alpha)
        self.alpha_slider.setStyleSheet(
            "QSlider::groove:horizontal { height: 6px; background: #ccc; border-radius: 3px; } QSlider::handle:horizontal { width: 16px; height: 16px; margin: -5px 0; background: #a5aad9; border: 2px solid #a5aad9; border-radius: 8px; }"
        )

        self.calculator_button = QPushButton("CALCULATOR")
        self.calculator_button.clicked.connect(self.open_calculator)
        self.calculator_button.setStyleSheet(
            "QPushButton { background-color: #70ad47; color: #000000; border: none; border-radius: 5px; padding: 8px; min-width: 100px; } QPushButton:hover { background-color: #548235; }"
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
                border: 1px solid #ccc;
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
        # Gather the settings to save
        settings = {
            "diameter": self.crosshair.diameter,
            "alpha": self.crosshair.alpha,
            "crosshair_color": self.crosshair.crosshair_color.name(),
            "crosshair_shape": self.crosshair.crosshair_shape,
            "is_outline_border": self.crosshair.is_outline_border,
            "night_theme": self.is_night_theme,  # Save the current theme state
            "vertical_adjust_input": int(self.vertical_adjust_input.text()),  # Save the vertical adjust value
        }

        # Save the settings to a configuration file (e.g., config.json)
        config_folder = "config"
        os.makedirs(config_folder, exist_ok=True)  # Create the config folder if it doesn't exist
        config_path = os.path.join(config_folder, "config.json")

        with open(config_path, "w") as config_file:
            json.dump(settings, config_file)

    def load_settings(self):
        # Load settings from the configuration file (if available)
        config_folder = "config"
        config_path = os.path.join(config_folder, "config.json")

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
            self.crosshair.new_window_y += settings.get("vertical_adjust_input", 0)  # Apply vertical adjust value
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
        x_offset = self.width() + 10
        y_offset = 0

        dialog.move(options_menu_position + QPoint(x_offset, y_offset))
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
        self.night_day_button.setText("Night")
        self.is_night_theme = False

    def set_night_theme(self):
        self.setStyleSheet(
            "OptionsMenu { background-color: #303030; } QLabel, QLineEdit { color: #f0f0f0; } QPushButton { background-color: #212121; color: #fff; }"
        )
        self.night_day_button.setText("Day")
        self.is_night_theme = True

class CalculatorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Rust Raid Cost Calculator")
        self.setGeometry(0, 0, 400, 150)  # Adjust size if needed

        layout = QVBoxLayout()
        self.setLayout(layout)

        grid_layout = QGridLayout()

        # Tool Selection Section
        grid_layout.addWidget(QLabel("Select a tool:"), 0, 0)
        self.tool_type_combo = QComboBox()
        self.tool_type_combo.addItems(["C4", "Rocket"])  # Add more tools if needed
        grid_layout.addWidget(self.tool_type_combo, 0, 1)

        grid_layout.addWidget(QLabel("Enter the quantity:"), 1, 0)
        self.quantity_input = QLineEdit("1")
        grid_layout.addWidget(self.quantity_input, 1, 1)

        calculate_tool_button = QPushButton("Calculate Tool Cost")
        calculate_tool_button.clicked.connect(self.calculate_tool_cost)
        grid_layout.addWidget(calculate_tool_button, 2, 0, 1, 2)  # Span 2 columns

        # Wall Selection Section
        grid_layout.addWidget(QLabel("Select a wall:"), 3, 0)
        self.wall_type_combo = QComboBox()
        self.wall_type_combo.addItems([
            "Twig Wall", "Wooden Wall", "Stone Wall", "Metal Wall", "Armored Wall"
        ])  # Add more walls if needed
        grid_layout.addWidget(self.wall_type_combo, 3, 1)

        calculate_wall_button = QPushButton("Calculate Wall Info")
        calculate_wall_button.clicked.connect(self.calculate_wall_info)
        grid_layout.addWidget(calculate_wall_button, 4, 0, 1, 2)  # Span 2 columns

        # New Result Label
        grid_layout.addWidget(QLabel("Result:"), 5, 0)
        self.result_label = QLabel()
        grid_layout.addWidget(self.result_label, 5, 1)

        layout.addLayout(grid_layout)

    def calculate_tool_cost(self):
        selected_tool = self.tool_type_combo.currentText()
        quantity = int(self.quantity_input.text())

        # Dictionary containing information about each tool
        tools_info = {
            "C4": {"sulfur": 2200, "charcoal": 3000},
            "Rocket": {"sulfur": 1400, "charcoal": 1950},
            # Add more tools if needed
        }

        if selected_tool in tools_info:
            sulfur_cost = tools_info[selected_tool]["sulfur"] * quantity
            charcoal_cost = tools_info[selected_tool]["charcoal"] * quantity

            result_text = (
                f"{selected_tool} x {quantity}:\n"
                f"Sulfur Cost: {sulfur_cost}\n"
                f"Charcoal Cost: {charcoal_cost}"
            )
            self.result_label.setText(result_text)
        else:
            self.result_label.setText("Invalid tool selection.")

    def calculate_wall_info(self):
        selected_wall = self.wall_type_combo.currentText()

        # Dictionary containing information about each wall type
        walls_info = {
            "Twig Wall": {
                "HP": 10,
                "Cost": "Wood×10 (10)",
                "Destroying Costs": "Explosive 5.56 Rifle Ammo×2 (1 sec, Sulfur Amount×50)\nF1 Grenade×1 (4 sec, Sulfur Amount×60)\nBeancan Grenade×1 (6 sec, Sulfur Amount×120)\nHigh Velocity Rocket×1 (1 sec, Sulfur Amount×200)\nSatchel Charge×1 (9 sec, Sulfur Amount×480)\nIncendiary Rocket×1 (1 sec, Sulfur Amount×610)\nRocket×1 (1 sec, Sulfur Amount×1,400)\nTimed Explosive Charge×1 (10 sec, Sulfur Amount×2,200)"
            },
            "Wooden Wall": {
                "HP": 250,
                "Cost": "Wood×200 (250)",
                "Destroying Costs": "Incendiary Rocket×1 (20 sec, Sulfur Amount×253)\nExplosive 5.56 Rifle Ammo×1 (21 sec, Sulfur Amount×1,225)\nSatchel Charge×3 (12 sec, Sulfur Amount×1,440)\nBeancan Grenade×1 (51 sec, Sulfur Amount×1,560)\nHigh Velocity Rocket×9 (48 sec, Sulfur Amount×1,800)\nTimed Explosive Charge×1 (10 sec, Sulfur Amount×2,200)\nRocket×2 (6 sec, Sulfur Amount×2,800)\nF1 Grenade×1 (2 min 29 sec, Sulfur Amount×3,540)\nFlame Thrower×~ 206 (44 sec, Fuel Amount×206)\nMolotov Cocktail×~ 4 (21 sec, Fuel Amount×200)"
            },
            "Stone Wall": {
                "HP": 500,
                "Cost": "Stones×300 (500)",
                "Destroying Costs": "Timed Explosive Charge×2 (11 sec, Sulfur Amount×4,400)\nExplosive 5.56 Rifle Ammo×1 (1 min 18 sec, Sulfur Amount×4,625)\nSatchel Charge×10 (22 sec, Sulfur Amount×4,800)\nBeancan Grenade×1 (2 min 55 sec, Sulfur Amount×5,520)\nRocket×4 (18 sec, Sulfur Amount×5,600)\nHigh Velocity Rocket×32 (3 min 6 sec, Sulfur Amount×6,400)\nF1 Grenade×1 (7 min 36 sec, Sulfur Amount×10,920)"
            },
            "Metal Wall": {
                "HP": 1000,
                "Cost": "Metal Fragments×200 (1000)",
                "Destroying Costs": "Timed Explosive Charge×4 (14 sec, Sulfur Amount×8,800)\nExplosive 5.56 Rifle Ammo×1 (2 min 51 sec, Sulfur Amount×10,000)\nSatchel Charge×23 (42 sec, Sulfur Amount×11,040)\nRocket×8 (42 sec, Sulfur Amount×11,200)\nHigh Velocity Rocket×67 (6 min 36 sec, Sulfur Amount×13,400)\nBeancan Grenade×1 (7 min 2 sec, Sulfur Amount×13,440)\nF1 Grenade×1 (41 min 24 sec, Sulfur Amount×59,580)"
            },
            "Armored Wall": {
                "HP": 2000,
                "Cost": "High Quality Metal×25 (2000)",
                "Destroying Costs": "Timed Explosive Charge×8 (20 sec, Sulfur Amount×17,600)\nExplosive 5.56 Rifle Ammo×799 (5 min 46 sec, Sulfur Amount×19,975)\nRocket×15 (1 min 24 sec, Sulfur Amount×21,000)\nSatchel Charge×46 (1 min 16 sec, Sulfur Amount×22,080)\nBeancan Grenade×223 (13 min 58 sec, Sulfur Amount×26,760)\nHigh Velocity Rocket×134 (13 min 18 sec, Sulfur Amount×26,800)\nF1 Grenade×1,986 (1 hour 22 min 46 sec, Sulfur Amount×119,160)"
            }
        }
        if selected_wall in walls_info:
            wall_hp = walls_info[selected_wall]["HP"]
            wall_cost = walls_info[selected_wall]["Cost"]
            destroying_costs = walls_info[selected_wall]["Destroying Costs"]

            result_text = f"{selected_wall}:\nHP: {wall_hp}\nCost: {wall_cost}\n\nDestroying Costs:\n{destroying_costs}"
            self.result_label.setText(result_text)
        else:
            self.result_label.setText("Invalid wall type.")



class TitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setAutoFillBackground(True)

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.title_label = QLabel("RustOracle", self)
        self.title_label.setStyleSheet("color: black; font-size: 18px; padding-left: 10px;")

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
                background-color: #Ffa500
;
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
        painter.setPen(QPen(Qt.black, 1))
        painter.drawRect(0, 0, self.width() - 1, self.height() - 1)
        painter.end()

class AdvancedOptionsDialog(QDialog):
    def __init__(self, crosshair):
        super().__init__()
        self.crosshair = crosshair
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Advanced Options")
        self.setGeometry(200, 200, 300, 200)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()

        form_layout = QFormLayout()

        color_label = QLabel("Crosshair Color:")
        self.color_input = QLineEdit("#ffffff")
        form_layout.addRow(color_label, self.color_input)

        shape_label = QLabel("Crosshair Shape:")
        self.shape_input = QLineEdit("1-9") 
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

def main():
    app = QApplication(sys.argv)
    crosshair_app = CrosshairApp()
    options_menu = OptionsMenu(crosshair_app)
    options_menu.show()
    crosshair_app.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()