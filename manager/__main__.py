import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from .app import BookApp
from .styles import STYLESHEET

def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLESHEET)

    # App-level font
    font = QFont("Segoe UI", 10)
    app.setFont(font)

    window = BookApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
