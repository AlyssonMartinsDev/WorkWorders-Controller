from PySide6.QtWidgets import QMainWindow
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

from utils.paths import resources_path

from utils.paths import ui_path

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()


        self.load_ui()
        self.setup_connections()



    def load_ui(self):

        loader = QUiLoader()

        file = QFile(ui_path("main_window.ui"))
        file.open(QFile.ReadOnly)

        self.ui = loader.load(file)
        file.close()

        self.setCentralWidget(self.ui)
    

    def setup_connections(self):
        pass

