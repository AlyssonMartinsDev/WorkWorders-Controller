from PySide6.QtCore import QFile, Qt
from PySide6.QtGui import QColor, QStandardItem, QStandardItemModel
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QHeaderView, QWidget, QVBoxLayout

from services.work_order_service import WorkOrderService
from utils.formatters import format_currency
from utils.paths import ui_path


class DashboardView(QWidget):
    def __init__(self):
        super().__init__()

        self.work_order_service = WorkOrderService()


        self.load_ui()
        self.load_finished_orders()
        self.load_pending_orders()

    def load_ui(self):
        loader = QUiLoader()

        file = QFile(str(ui_path("dashboard.ui")))
        file.open(QFile.ReadOnly)

        self.ui = loader.load(file)
        file.close()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.ui)

    def load_work_orders_by_status(self, table, allowed_status):
        work_orders = self.work_order_service.get_all_work_orders()

        model = QStandardItemModel()
        model.setHorizontalHeaderLabels([
            "ID",
            "Cliente",
            "WPP numero",
            "Acesso Remoto",
            "Descrição",
            "Data",
            "Status Serviço",
            "Valor",
            "Status Pagamento"
        ])

        for order in work_orders:
            status = order.status_service.name.strip().upper()

            if status not in allowed_status:
                continue

            row_items = [
                QStandardItem(str(order.id)),
                QStandardItem(str(order.client.name)),
                QStandardItem(str(order.client.phone)),
                QStandardItem(str(order.remote_access.code if order.remote_access else "")),
                QStandardItem(str(order.description)),
                QStandardItem(str(order.created_at.date())),
                QStandardItem(str(order.status_service.name)),
                QStandardItem(format_currency(order.price)),
                QStandardItem(str(order.status_payment.name))
            ]
            self.apply_status_style(row_items, order)
            model.appendRow(row_items)

        table.setModel(model)
        table.verticalHeader().setVisible(False)

        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.Stretch)
        table.resizeColumnsToContents()


    def load_pending_orders(self):
        self.load_work_orders_by_status(
            self.ui.table_pending,
            ["EM ANDAMENTO", "AGUARDANDO CLIENTE", "ATRASADO"]
        )

    def load_finished_orders(self):
        self.load_work_orders_by_status(
            self.ui.table_finished,
            ["FINALIZADO", "REJEITADO"]
        )

    def apply_status_style(self, row_items, order):

        # STATUS SERVICE
        status = order.status_service.name.strip().upper()

        status_item = row_items[6]

        font = status_item.font()
        font.setBold(True)

        status_item.setFont(font)

        if status == "FINALIZADO":
            status_item.setForeground(QColor("#4CAF50"))

        elif status == "EM ANDAMENTO":
            status_item.setForeground(QColor("#03A9F4"))

        elif status == "ATRASADO":
            status_item.setForeground(QColor("#9E9E9E"))

        elif status == "AGUARDANDO CLIENTE":
            status_item.setForeground(QColor("#FFC107"))

        elif status == "REJEITADO":
            status_item.setForeground(QColor("#F44336"))

        # STATUS PAYMENT
        payment = order.status_payment.name.strip().upper()

        payment_item = row_items[8]

        payment_font = payment_item.font()
        payment_font.setBold(True)

        payment_item.setFont(payment_font)

        if payment == "PAGO":
            payment_item.setForeground(QColor("#4CAF50"))

        elif payment == "PENDENTE":
            payment_item.setForeground(QColor("#FFC107"))

        elif payment == "DEVENDO":
            payment_item.setForeground(QColor("#F44336"))




