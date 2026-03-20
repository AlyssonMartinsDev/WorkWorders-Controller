import sys
from PySide6.QtWidgets import QApplication

# local imports
from views.main_window_view import MainWindow


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()