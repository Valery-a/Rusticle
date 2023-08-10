from PyQt5.QtWidgets import QLabel, QFrame, QLineEdit, QPushButton, QVBoxLayout, QComboBox, QGridLayout, QDialog
from PyQt5.QtCore import Qt

class CalculatorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Rust Raid Cost Calculator")
        self.setGeometry(0, 0, 500, 200)  # Adjust size if needed

        layout = QVBoxLayout(self)
        self.setLayout(layout)
        layout.setContentsMargins(20, 20, 20, 20)

        grid_layout = QGridLayout()
        grid_layout.setVerticalSpacing(10)

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

        # Separator Line
        separator_line = QFrame()
        separator_line.setFrameShape(QFrame.HLine)
        separator_line.setFrameShadow(QFrame.Sunken)
        grid_layout.addWidget(separator_line, 3, 0, 1, 2)  # Span 2 columns

        # Wall Selection Section
        grid_layout.addWidget(QLabel("Select a wall:"), 4, 0)
        self.wall_type_combo = QComboBox()
        self.wall_type_combo.addItems([
            "Twig Wall", "Wooden Wall", "Stone Wall", "Metal Wall", "Armored Wall"
        ])  # Add more walls if needed
        grid_layout.addWidget(self.wall_type_combo, 4, 1)

        calculate_wall_button = QPushButton("Calculate Wall Info")
        calculate_wall_button.clicked.connect(self.calculate_wall_info)
        grid_layout.addWidget(calculate_wall_button, 5, 0, 1, 2)  # Span 2 columns

        # Separator Line
        separator_line2 = QFrame()
        separator_line2.setFrameShape(QFrame.HLine)
        separator_line2.setFrameShadow(QFrame.Sunken)
        grid_layout.addWidget(separator_line2, 6, 0, 1, 2)  # Span 2 columns

        # New Result Label
        self.result_label = QLabel()
        self.result_label.setAlignment(Qt.AlignCenter)
        grid_layout.addWidget(self.result_label, 7, 1)

        layout.addLayout(grid_layout)

        self.setStyleSheet('''
            QDialog {
                background-color: #2c3e50; /* Dark Blue */
            }
            QLabel {
                font-size: 18px;
                color: #ffffff; /* White */
            }
            QComboBox, QLineEdit {
                font-size: 18px;
                color: #000000; /* Black */
                background-color: #ecf0f1; /* Light Grey */
                border: 1px solid #34495e; /* Darker Blue */
                border-radius: 5px;
            }
            QPushButton {
                font-size: 18px;
                color: #ffffff; /* White */
                background-color: #3498db; /* Light Blue */
                border: 2px solid #2980b9; /* Slightly Darker Blue */
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #2980b9; /* Slightly Darker Blue */
            }
            QFrame {
                color: #b2b2b2; /* Lighter Grey */
            }
        ''')

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

            sulfur_nodes, sulfur_remainder = divmod(sulfur_cost, 300)  # Each node gives 300 sulfur

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
