import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTabWidget, QWidget
from PyQt5.QtCore import Qt

from crosshair import CrosshairApp
from optionsmenu import OptionsMenu
from advoptions import AdvancedOptionsDialog
from bar import TitleBar
from calculator import CalculatorDialog

class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__(flags=Qt.FramelessWindowHint | Qt.WindowMinMaxButtonsHint)
        self.crosshair = CrosshairApp()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("RustOracle")
        self.setGeometry(100, 100, 800, 600)
        self.setFixedSize(400, 500)
        self.title_bar = TitleBar(self) 
        self.setMenuWidget(self.title_bar)
        tab_widget = QTabWidget()
        self.setCentralWidget(tab_widget)

        # Apply dynamic stylesheet to the tab widget and its contents
        dynamic_stylesheet = """
            QTabWidget::pane {
                background-color: #2E2E2E;
                border-radius: 10px;
            }
            QTabWidget::tab-bar {
                flex: 1;
                background-color: #2E2E2E;
                border-radius: 10px;
            }
            QTabBar::tab {
                flex: 1;
                background-color: #3E3E3E;
                color: white;
                padding: 8px;
            }
            QTabBar::tab:selected {
                background-color: red;
            }
        """
        tab_widget.setStyleSheet(dynamic_stylesheet)

        advanced_options_menu = AdvancedOptionsDialog(self.crosshair)
        calculator_menu = CalculatorDialog(self)
        options_menu = OptionsMenu(self.crosshair)

        tab_widget.addTab(options_menu, "Options Menu")
        tab_widget.addTab(advanced_options_menu, "Advanced Options")
        tab_widget.addTab(calculator_menu, "Calculator")


def main():
    app = QApplication(sys.argv)
    main_menu = MainMenu()
    main_menu.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()