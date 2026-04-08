from PySide6.QtWidgets import  QDialog
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtCore import QDate

from services.work_order_service import WorkOrderService

from utils.paths import ui_path


class CreateWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.load_ui()
        self.setup_connections()
        self.set_current_date()
        self.accept()

        self.work_order_service = WorkOrderService()


    def load_ui(self):
        loader = QUiLoader()
        file = QFile(str(ui_path("create_window.ui")))
        file.open(QFile.ReadOnly)
        self.ui = loader.load(file)
        file.close()
        self.setLayout(self.ui.layout())

    def set_current_date(self):
        self.ui.dateEdit.setDate(QDate.currentDate())



    def setup_connections(self):
        self.ui.btn_create.clicked.connect(self.create_new_work_order)




    def create_new_work_order(self):
        

        data = {
            "name": self.ui.lineEdit_name.text(),
            "phone": self.ui.lineEdit_phone.text(),
            "idAccessRemote": self.ui.lineEdit_idAccessRemote.text(),
            "description": self.ui.textEdit.toPlainText(),
            "date": self.ui.dateEdit.date().toString("dd/MM/yyyy"),
            "price": self.ui.lineEdit_price.text(),
            "statusPayment": self.ui.comboBox_statusPayment.currentText(),
            "statusService": self.ui.comboBox_statusService.currentText(),
        }

        self.work_order_service.create_work_order(data)
        self.accept()
    