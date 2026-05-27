
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QDialog, QVBoxLayout, QMessageBox

from utils.paths import ui_path



from services.access_remote_service import AccessRemoteService


class DialogCreateAccessRemote(QDialog):
    def __init__(self, wo_id):
        super(DialogCreateAccessRemote, self).__init__()
        self.wo_id = wo_id
        self.access_remote_service = AccessRemoteService()

        self.load_ui()
        self.setup_connections()



    def load_ui(self):

        loader = QUiLoader()

        file = QFile(ui_path("create_access_remote_dialog.ui"))
        file.open(QFile.ReadOnly)

        self.ui = loader.load(file)
        file.close()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.ui)

    def setup_connections(self):
        pass


    def create_access_remote(self):
        type = self.ui.lineEdit_type.text()
        code = self.ui.lineEdit_code.text()
        password = self.ui.lineEdit_pass.text()

        data = {
            "access_type": type,
            "code": code,
            "password": password
        }


        try:
            res = self.access_remote_service.create_access_remote(data)
            QMessageBox.information(self, "Sucesso", res)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao criar acesso remoto: {e}")
        finally:
            self.close()