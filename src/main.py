import sys
from PyQt5.QtWidgets import QApplication
from crosshair import CrosshairApp
from optionsmenu import OptionsMenu

def main():
    app = QApplication(sys.argv)
    crosshair_app = CrosshairApp()
    options_menu = OptionsMenu(crosshair_app)
    options_menu.show()
    crosshair_app.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()