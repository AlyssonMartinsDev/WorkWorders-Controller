from PySide6.QtCore import QFile, Qt
from PySide6.QtGui import QColor, QStandardItem, QStandardItemModel
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import (
    QHeaderView,
    QComboBox,
    QWidget,
    QVBoxLayout,
)

from services.work_order_service import WorkOrderService
from utils.formatters import format_currency
from utils.paths import ui_path
from views.dialog_WO_options import Dialog_WO_options


class DashboardView(QWidget):
    def __init__(self):
        super().__init__()

        self.work_order_service = WorkOrderService()

        self.load_ui()
        self.setup_connections()
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

    def setup_connections(self):
        self.ui.table_pending.doubleClicked.connect(self.on_row_double_clicked)
        self.ui.table_finished.doubleClicked.connect(self.on_row_double_clicked)

    def load_work_orders_by_status(self, table, allowed_status):
        work_orders = self.work_order_service.get_all_work_orders()

        model = QStandardItemModel()
        model.setHorizontalHeaderLabels([
            "ID",
            "Cliente",
            "WPP número",
            "Acesso Remoto",
            "Descrição",
            "Data",
            "Status Serviço",
            "Valor",
            "Status Pagamento"
        ])

        filtered_orders = []

        for order in work_orders:
            status = order.status_service.name.strip().upper()

            if status not in allowed_status:
                continue

            filtered_orders.append(order)

            row_items = [
                QStandardItem(str(order.id)),
                QStandardItem(str(order.client.name)),
                QStandardItem(str(order.client.phone)),
                QStandardItem(""),
                QStandardItem(str(order.description)),
                QStandardItem(str(order.created_at.date())),
                QStandardItem(str(order.status_service.name)),
                QStandardItem(format_currency(order.price)),
                QStandardItem(str(order.status_payment.name))
            ]

            self.apply_status_style(row_items, order)
            model.appendRow(row_items)

        table.setModel(model)

        self.add_remote_access_comboboxes(table, model, filtered_orders)


        table.setSelectionBehavior(table.SelectionBehavior.SelectRows)
        table.setSelectionMode(table.SelectionMode.SingleSelection)
        table.setEditTriggers(table.EditTrigger.NoEditTriggers)

        table.verticalHeader().setVisible(False)

        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.Stretch)

    def add_remote_access_comboboxes(self, table, model, orders):
        for row, order in enumerate(orders):
            combo = QComboBox()

            if order.remote_accesses:
                for access in order.remote_accesses:
                    access_type = access.type or "Acesso"
                    combo.addItem(
                        f"{access_type} - {access.code}",
                        access.id
                    )
            else:
                combo.addItem("Sem acesso remoto", None)
                combo.setEnabled(False)

            table.setIndexWidget(
                model.index(row, 3),
                combo
            )

    def on_row_double_clicked(self, index):
        if not index.isValid():
            return

        table = self.sender()
        model = table.model()

        row = index.row()

        order_id = int(model.item(row, 0).text())
        wo_status_service = model.item(row, 6).text()
        wo_status_payment = model.item(row, 8).text()

        dialog = Dialog_WO_options(
            order_id,
            wo_status_service,
            wo_status_payment
        )

        dialog.work_order_updated.connect(self.reload_tables)
        dialog.exec()

    def reload_tables(self):
        self.load_pending_orders()
        self.load_finished_orders()

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
        status = order.status_service.name.strip().upper()
        status_item = row_items[6]

        font = status_item.font()
        font.setBold(True)
        status_item.setFont(font)

        if status == "FINALIZADO":
            status_item.setForeground(QColor("#4CAF50"))
        elif status == "EM ANDAMENTO":
            status_item.setForeground(QColor("#9E9E9E"))
        elif status == "AGUARDANDO CLIENTE":
            status_item.setForeground(QColor("#FFC107"))
        elif status == "ATRASADO":
            status_item.setForeground(QColor("#FF9800"))
        elif status == "REJEITADO":
            status_item.setForeground(QColor("#F44336"))

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