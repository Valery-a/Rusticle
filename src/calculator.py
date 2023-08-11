from PyQt5.QtWidgets import (
    QLabel, QFrame, QLineEdit, QPushButton, QVBoxLayout, QComboBox, QGridLayout, QDialog, QScrollArea
)
from PyQt5.QtCore import Qt


class CalculatorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Rust Raid Cost Calculator")
        self.setGeometry(0, 0, 500, 400)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

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
    QLineEdit {
                background-color: #444444;
                color: white;
                border: 1px solid #ff5555;
                border-radius: 5px;
                width: 100%;
                padding: 10px;
                font-size: 14px;
            }
    QComboBox:hover, QPushButton:hover {
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

        grid_layout = QGridLayout()
        grid_layout.setVerticalSpacing(10)

        self.tool_type_combo = QComboBox()
        self.tool_type_combo.addItems(["C4", "Rocket"])
        self.quantity_input = QLineEdit("")
        self.calculate_tool_button = QPushButton("Calculate Tool Cost")

        self.wall_type_combo = QComboBox()
        self.wall_type_combo.addItems([
            "Twig Wall", "Wooden Wall", "Stone Wall", "Metal Wall", "Armored Wall"
        ])
        self.calculate_wall_button = QPushButton("Calculate Wall Info")

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.result_label = QLabel()
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.result_label.setStyleSheet('''
            font-size: 16px;
            color: #ffffff;
            background-color: #1f2630; /* Dark Rust Blue */
        ''')
        self.scroll_area.setWidget(self.result_label)

        # Set the scroll bar style for both vertical and horizontal
        scroll_bar_style = '''
            QScrollBar:vertical, QScrollBar:horizontal {
                border: none;
                background: #34495e; /* Darker Rust Blue */
                width: 8px;
                height: 8px;
                margin: 0px 0px 0px 0px;
            }
            
            QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
                background: #95a5a6; /* Light Grey */
                border-radius: 4px;
            }

            QScrollBar::handle:vertical:hover, QScrollBar::handle:horizontal:hover {
                background: #7f8c8d; /* Slightly Darker Light Grey */
            }
        '''
        self.scroll_area.verticalScrollBar().setStyleSheet(scroll_bar_style)
        self.scroll_area.horizontalScrollBar().setStyleSheet(scroll_bar_style)

        self.calculate_tool_button.clicked.connect(self.calculate_tool_cost)
        self.calculate_wall_button.clicked.connect(self.calculate_wall_info)

        grid_layout.addWidget(QLabel("Select a tool:"), 0, 0)
        grid_layout.addWidget(self.tool_type_combo, 0, 1)
        grid_layout.addWidget(QLabel("Enter the quantity:"), 1, 0)
        grid_layout.addWidget(self.quantity_input, 1, 1)
        grid_layout.addWidget(self.calculate_tool_button, 2, 0, 1, 2)

        separator_line = QFrame()
        separator_line.setFrameShape(QFrame.HLine)
        separator_line.setFrameShadow(QFrame.Sunken)
        grid_layout.addWidget(separator_line, 3, 0, 1, 2)

        grid_layout.addWidget(QLabel("Select a wall:"), 4, 0)
        grid_layout.addWidget(self.wall_type_combo, 4, 1)
        grid_layout.addWidget(self.calculate_wall_button, 5, 0, 1, 2)

        separator_line2 = QFrame()
        separator_line2.setFrameShape(QFrame.HLine)
        separator_line2.setFrameShadow(QFrame.Sunken)
        grid_layout.addWidget(separator_line2, 6, 0, 1, 2)

        grid_layout.addWidget(self.scroll_area, 7, 0, 1, 2)

        layout.addLayout(grid_layout)
        self.setLayout(layout)

    def calculate_tool_cost(self):
        selected_tool = self.tool_type_combo.currentText()
        quantity_text = self.quantity_input.text()

        if not quantity_text.isdigit():
            self.result_label.setText("Please enter a valid quantity.")
            return

        quantity = int(quantity_text)
        tools_info = {
            "C4": {"sulfur": 2200, "charcoal": 3000},
            "Rocket": {"sulfur": 1400, "charcoal": 1950},
        }

        if selected_tool in tools_info:
            sulfur_cost = tools_info[selected_tool]["sulfur"] * quantity
            charcoal_cost = tools_info[selected_tool]["charcoal"] * quantity

            sulfur_nodes, sulfur_remainder = divmod(sulfur_cost, 300)

            if sulfur_remainder > 0:
                sulfur_nodes += 1

            result_text = (
                f"{selected_tool} x {quantity}:\n"
                f"Sulfur Cost: {sulfur_cost} ({sulfur_nodes} sulfur nodes)\n"
                f"Charcoal Cost: {charcoal_cost}"
            )
            self.result_label.setText(result_text)
        else:
            self.result_label.setText("Invalid tool selection.")

    def calculate_wall_info(self):
        selected_wall = self.wall_type_combo.currentText()

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

            result_text = (
                f"{selected_wall}:\n"
                f"HP: {wall_hp}\n"
                f"Cost: {wall_cost}\n\n"
                f"Destroying Costs:\n{destroying_costs}"
            )
            self.result_label.setText(result_text)
        else:
            self.result_label.setText("Invalid wall type.")
