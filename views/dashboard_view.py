from PySide6.QtCore import QFile, Qt, QTimer
from PySide6.QtGui import QColor, QStandardItem, QStandardItemModel
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import (
    QHeaderView,
    QMessageBox,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QHBoxLayout
)

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
            "WPP número",
            "Acesso Remoto",
            "Descrição",
            "Data",
            "Status Serviço",
            "Valor",
            "Status Pagamento",
            "Ações"
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
                QStandardItem(str(order.remote_access.code if order.remote_access else "")),
                QStandardItem(str(order.description)),
                QStandardItem(str(order.created_at.date())),
                QStandardItem(str(order.status_service.name)),
                QStandardItem(format_currency(order.price)),
                QStandardItem(str(order.status_payment.name)),
                QStandardItem("")
            ]

            self.apply_status_style(row_items, order)
            model.appendRow(row_items)

        table.setModel(model)

        self.add_action_buttons(table, filtered_orders)

        table.verticalHeader().setVisible(False)

        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.Stretch)
        header.setSectionResizeMode(9, QHeaderView.Fixed)

        table.setColumnWidth(9, 180)

        
        

    def add_action_buttons(self, table, orders):
        for row, order in enumerate(orders):
            container = QWidget()
            layout = QHBoxLayout(container)
            layout.setContentsMargins(4, 2, 4, 2)
            layout.setSpacing(6)

            btn_finish = QPushButton("Finalizar")
            btn_paid = QPushButton("Pago")

            service_status = order.status_service.name.strip().upper()
            payment_status = order.status_payment.name.strip().upper()

            btn_finish.setStyleSheet("""
                QPushButton {
                    background-color: #1976D2;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 6px 12px;
                    font-weight: bold;
                }

                QPushButton:hover {
                    background-color: #1565C0;
                }

                QPushButton:pressed {
                    background-color: #0D47A1;
                }

                QPushButton:disabled {
                    background-color: #B0BEC5;
                    color: #ECEFF1;
                }
            """)

            btn_paid.setStyleSheet("""
                QPushButton {
                    background-color: #2E7D32;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 6px 12px;
                    font-weight: bold;
                }

                QPushButton:hover {
                    background-color: #1B5E20;
                }

                QPushButton:pressed {
                    background-color: #0D3B12;
                }

                QPushButton:disabled {
                    background-color: #B0BEC5;
                    color: #ECEFF1;
                }
            """)

            if service_status == "FINALIZADO":
                btn_finish.setEnabled(False)

            if payment_status == "PAGO":
                btn_paid.setEnabled(False)

            btn_finish.clicked.connect(
                lambda checked=False, order_id=order.id: self.finish_work_order(order_id)
            )

            btn_paid.clicked.connect(
                lambda checked=False, order_id=order.id: self.mark_work_order_as_paid(order_id)
            )

            layout.addWidget(btn_finish)
            layout.addWidget(btn_paid)

            table.setIndexWidget(
                table.model().index(row, 9),
                container
            )

    def finish_work_order(self, work_order_id):
        try:
            res = self.work_order_service.update_status_service(work_order_id, 2)

            QMessageBox.information(self, "Sucesso", res)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao finalizar ordem de serviço: {e}")
        finally:
            self.reload_tables()


        # depois você chama o service:
        # self.work_order_service.finish_work_order(work_order_id)

        

    def mark_work_order_as_paid(self, work_order_id):
        try:
            res = self.work_order_service.update_status_payment(work_order_id, 2)

            QMessageBox.information(self, "Sucesso", res)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao marcar ordem de serviço como paga: {e}")
        finally:
            self.reload_tables()

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
            status_item.setForeground(QColor("#03A9F4"))
        elif status == "ATRASADO":
            status_item.setForeground(QColor("#9E9E9E"))
        elif status == "AGUARDANDO CLIENTE":
            status_item.setForeground(QColor("#FFC107"))
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