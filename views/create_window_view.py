
from PySide6.QtWidgets import  QDialog, QMessageBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile


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
        







    
        
        
















