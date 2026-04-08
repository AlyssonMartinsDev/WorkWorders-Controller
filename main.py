import sys
from PySide6.QtWidgets import QApplication

# Database
from data.init_db import init_db

# local imports
from views.main_window_view import MainWindow


def main():
    init_db()
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()