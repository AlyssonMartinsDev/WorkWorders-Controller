
from PySide6.QtWidgets import  QDialog, QMessageBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtCore import QDate
from sqlalchemy import true

from services.status_payment_service import StatusServiceService
from services.status_service_service import StatusPaymentService
from services.work_order_service import WorkOrderService
from services.clients_service import ClientsService

from utils.paths import ui_path
from views.lookup_window_view import LookupWindowDialog


class CreateWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.load_ui()
        self.selected_id = None

        # Services
        self.status_payment_service = StatusPaymentService()
        self.status_service_service = StatusServiceService()
        self.work_order_service = WorkOrderService()
        self.clients_service = ClientsService()

        self.load_combobox_data()

        self.setup_connections()
        self.accept()




    def load_ui(self):
        loader = QUiLoader()
        file = QFile(str(ui_path("create_window.ui")))
        file.open(QFile.ReadOnly)
        self.ui = loader.load(file)
        file.close()
        self.setLayout(self.ui.layout())
        self.ui.button_clear.setDisabled(True)

    def setup_connections(self):
        self.ui.btn_create.clicked.connect(self.create_new_work_order)
        self.ui.lookupButton.clicked.connect(self.open_lookup)
        self.ui.button_clear.clicked.connect(self.clear_fields)

    def load_combobox_data(self):
        # Status de pagamento
        status_payment = self.status_payment_service.get_all_status_payments()
        self.ui.comboBox_statusPayment.clear()
        for status in status_payment:
            self.ui.comboBox_statusPayment.addItem(status.name, status.id)

        status_service = self.status_service_service.get_all_status_service()
        self.ui.comboBox_statusService.clear()
        for status_se in status_service:
            self.ui.comboBox_statusService.addItem(status_se.name, status_se.id)



    def create_new_work_order(self):
        
        data = {}

        if self.selected_id:
            data["client_id"] = self.selected_id
        else:

            if not self.ui.lineEdit_name.text() or not self.ui.lineEdit_phone.text():
                QMessageBox.critical(self, "Erro", "Os campos nome e contato são obrigatórios!")
                return


            data["client_data"] = {
                "name": self.ui.lineEdit_name.text(),
                "phone": self.ui.lineEdit_phone.text(),
                "email": self.ui.lineEdit_email.text(),
                "notes": self.ui.lineEdit_notes.text()
            }
            
        if self.ui.lineEdit_type.text() or  self.ui.lineEdit_code.text() or self.ui.lineEdit_password.text():

            if not self.ui.lineEdit_type.text() or not self.ui.lineEdit_code.text() or not self.ui.lineEdit_password.text():
                QMessageBox.critical(self, "Erro", "Todos os campos da area acesso remoto deve ser preenchidos")
                return

            data["access_remote_data"] = {
                "type": self.ui.lineEdit_type.text(),
                "code": self.ui.lineEdit_code.text(),
                "password": self.ui.lineEdit_password.text()
            }


        if not self.ui.textEdit.toPlainText():
            QMessageBox.critical(self, "Erro", "O campo descrição é obrigatório!")
            return
        

        data["order_data"] = {
            "description": self.ui.textEdit.toPlainText(),
            "price": self.ui.lineEdit_price.text(),
            "status_service": self.ui.comboBox_statusService.currentData(),
            "status_payment": self.ui.comboBox_statusPayment.currentData()
        }
        
        try:
            message = self.work_order_service.create_work_order(data)

            QMessageBox.information(self,"SUCESSO", message)

            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"{e}")
        
        


    def open_lookup(self):

        headers = ["ID", "Nome", "Telefone"]

        rows = []

        clients = self.clients_service.get_all_clients()
        for client in clients:
            rows.append([client.id, client.name, client.phone])

        try:
            dialog = LookupWindowDialog(headers=headers, rows=rows)

            if dialog.exec():
                selected_id = dialog.selected_id

                client = self.clients_service.get_client_by_id(selected_id)

                if client:
                    self.fill_clients_fields(client)

        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))
            
    def fill_clients_fields(self, data):

        self.selected_id = data.id

        self.ui.lineEdit_name.setText(data.name)
        self.ui.lineEdit_phone.setText(data.phone)

        if data.email:
            self.ui.lineEdit_email.setText(data.email)
        
        if data.notes:
            self.ui.lineEdit_notes.setText(data.notes)

        self.ui.lineEdit_name.setReadOnly(True)
        self.ui.lineEdit_phone.setReadOnly(True)
        self.ui.lineEdit_email.setReadOnly(True)
        self.ui.lineEdit_notes.setReadOnly(True)
        self.ui.lookupButton.setDisabled(True)
        self.ui.button_clear.setDisabled(False)

    def clear_fields(self):

        self.ui.lineEdit_name.setReadOnly(False)
        self.ui.lineEdit_name.clear()
        self.ui.lineEdit_phone.setReadOnly(False)
        self.ui.lineEdit_phone.clear()
        self.ui.lineEdit_email.setReadOnly(False)
        self.ui.lineEdit_email.clear()
        self.ui.lineEdit_notes.setReadOnly(False)
        self.ui.lineEdit_notes.clear()
        self.ui.lookupButton.setDisabled(False)
        self.ui.button_clear.setDisabled(True)














