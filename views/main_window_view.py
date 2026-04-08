from PySide6.QtWidgets import QMainWindow, QHeaderView
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, Qt
from PySide6.QtGui import QStandardItem, QStandardItemModel, QColor

from views.create_window_view import CreateWindow

from services.work_order_service import WorkOrderService

from utils.formatters import format_currency

from utils.paths import ui_path

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.service = WorkOrderService()
        self.center_window()


        self.load_ui()
        self.setup_connections()
        self.load_work_orders()




    def load_ui(self):

        loader = QUiLoader()

        file = QFile(ui_path("main_window.ui"))
        file.open(QFile.ReadOnly)

        self.ui = loader.load(file)
        file.close()

        self.setCentralWidget(self.ui)
    def load_work_orders(self):
        work_orders = self.service.get_all_work_orders()



        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels([
            "ID",
            "Cliente",
            "WPP numero",
            "Acesso Remoto",
            "Descrião",
            "Data",
            "Status Serviço",
            "Valor",
            "Status Pagamento"
        ])

        for order in work_orders:
            row_items = [
                QStandardItem(str(order.id)),
                QStandardItem(str(order.client_name)),
                QStandardItem(str(order.phone)),
                QStandardItem(str(order.access_remote)),
                QStandardItem(str(order.description)),
                QStandardItem(str(order.date)),
                QStandardItem(str(order.status_service)),  # 👈 índice 6
                QStandardItem(format_currency(order.price)),
                QStandardItem(str(order.status_payment))
            ]

            status = order.status_service.strip().upper()

            if status == "FINALIZADO":
                color = QColor("#C8E6C9")  # verde
            elif status == "EM ANDAMENTO":
                color = QColor("#B3E5FC")  # azul claro
            elif status == "REJEITADA":
                color = QColor("#BBDEFB")  # azul
            else:
                color = None

            # 🎯 aplica só na célula do status (índice 6)
            if color:
                status_item = row_items[6]
                status_item.setBackground(color)
                status_item.setForeground(QColor("black"))  # texto preto

            status_payment = order.status_payment.strip().upper()

            if status_payment == "PAGO":
                color = QColor("#C8E6C9")  # verde
            elif status_payment == "PENDENTE":
                color = QColor("#FFF9C4")  # amarelo claro
            else:
                color = None

            if color:
                item = row_items[8]
                item.setBackground(color)
                item.setForeground(QColor("black"))
                item.setTextAlignment(Qt.AlignCenter)

            self.model.appendRow(row_items)


        self.ui.tableView.setModel(self.model)

        self.ui.tableView.verticalHeader().setVisible(False)


        header = self.ui.tableView.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.Stretch)
        self.ui.tableView.resizeColumnsToContents()
    def setup_connections(self):
        self.ui.btn_create.clicked.connect(self.create_window)

    def create_window(self):
        
        dialog = CreateWindow()
        if dialog.exec():
            self.load_work_orders()

    def center_window(self):
        frame = self.frameGeometry()
        screen = self.screen().availableGeometry().center()
        frame.moveCenter(screen)
        self.move(frame.topLeft())

    def showEvent(self, event):
        super().showEvent(event)
        self.center_window()
        

