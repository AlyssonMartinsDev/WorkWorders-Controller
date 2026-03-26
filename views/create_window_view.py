from PySide6.QtWidgets import  QDialog
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

from utils.paths import ui_path


class CreateWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.load_ui()
        self.setup_connections()

    def load_ui(self):
        loader = QUiLoader()
        file = QFile(str(ui_path("create_window.ui")))
        file.open(QFile.ReadOnly)
        self.ui = loader.load(file)
        file.close()
        self.setLayout(self.ui.layout())

        print("UI carregado")



    def setup_connections(self):
        pass