from PySide6.QtCore import QFile, Qt
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QMessageBox, QWidget, QVBoxLayout

from services.clients_service import ClientsService
from utils.paths import ui_path


class CreateClientView(QWidget):
    def __init__(self):
        super().__init__()
        self.load_ui()

        self.client_service = ClientsService()
        self.setup_connections()

    def load_ui(self):
        loader = QUiLoader()

        file = QFile(str(ui_path("create_client.ui")))
        file.open(QFile.ReadOnly)

        self.ui = loader.load(file)
        file.close()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.ui)


    
    def setup_connections(self):
        
        self.ui.btn_create.clicked.connect(self.create_client)


    def create_client(self):

        try:
            data = {
                "name": self.ui.lineEdit_name.text(),
                "phone": self.ui.lineEdit_phone.text(),
                "email": self.ui.lineEdit_email.text(),
                "notes": self.ui.lineEdit_notes.text()
            }


            result = self.client_service.create_client(data)

            QMessageBox.information(self, "Sucesso", "Cliente cadastrado com sucesso")

            self.clear_fields()

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro ao tentar cadastrar um cliente. \n{e}")
        
    def clear_fields(self):
        self.ui.lineEdit_name.clear()
        self.ui.lineEdit_phone.clear()
        self.ui.lineEdit_email.clear()
        self.ui.lineEdit_notes.clear()






