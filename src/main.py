import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTabWidget
from crosshair import CrosshairApp
from optionsmenu import OptionsMenu
import sys
from advoptions import AdvancedOptionsDialog
from bar import TitleBar
from calculator import CalculatorDialog

class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.crosshair = CrosshairApp()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("RustOracle")
        self.setGeometry(100, 100, 800, 600)

        self.title_bar = TitleBar(self)
        self.setMenuWidget(self.title_bar)

        tab_widget = QTabWidget()
        self.setCentralWidget(tab_widget)

        # Create instances of your menu classes
        advanced_options_menu = AdvancedOptionsDialog(self.crosshair)
        calculator_menu = CalculatorDialog(self)
        options_menu = OptionsMenu(self.crosshair)

        # Set the menus as the tab content
        tab_widget.addTab(advanced_options_menu, "Advanced Options")
        tab_widget.addTab(calculator_menu, "Calculator")
        tab_widget.addTab(options_menu, "Options Menu")

def main():
    app = QApplication(sys.argv)
    main_menu = MainMenu()
    main_menu.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()