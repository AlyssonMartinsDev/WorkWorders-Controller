from typing import Self
from PySide6.QtWidgets import QMainWindow, QHeaderView, QMessageBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, Qt
from PySide6.QtGui import QStandardItem, QStandardItemModel, QColor

from views.create_window_view import CreateWindow
from views.create_work_order_view import CreateWorkOrderView
from views.dashboard_view import DashboardView

from services.work_order_service import WorkOrderService

from utils.formatters import format_currency

from utils.paths import ui_path


# views
from views.create_client_view import CreateClientView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.service = WorkOrderService()
        
        self.center_window()


        self.load_ui()
        self.setup_connections()
        # self.load_pending_orders()
        # self.load_finished_orders()

        # Carregamento das views
        self.load_pages()





    def load_ui(self):

        loader = QUiLoader()

        file = QFile(ui_path("main_window.ui"))
        file.open(QFile.ReadOnly)

        self.ui = loader.load(file)
        self.ui.menuBar().setNativeMenuBar(False)
        file.close()

        self.setCentralWidget(self.ui)

    def load_pages(self):
        # função responsavel por carregar as paginals e adicionar na stackedwidget
        self.create_client_page = CreateClientView()
        self.dashboard_page = DashboardView()
        self.create_work_order_page = CreateWorkOrderView()

        self.ui.stackedWidget.addWidget(self.dashboard_page)
        self.ui.stackedWidget.addWidget(self.create_client_page)
        self.ui.stackedWidget.addWidget(self.create_work_order_page)


        self.ui.stackedWidget.setCurrentWidget(self.dashboard_page)

    def setup_connections(self):
        # MenuBar connectiojs
        # Clients
        self.ui.action_create_client.triggered.connect(self.open_create_client_page)
        self.ui.action_home.triggered.connect(self.go_to_home)
        self.ui.action_create_work_order.triggered.connect(self.open_create_work_order_page)


    def create_window(self):
        
        dialog = CreateWindow()
        if dialog.exec():
            self.load_pending_orders()
            self.load_finished_orders()

    def center_window(self):
        frame = self.frameGeometry()
        screen = self.screen().availableGeometry().center()
        frame.moveCenter(screen)
        self.move(frame.topLeft())

    def showEvent(self, event):
        super().showEvent(event)
        self.center_window()
        
    def open_create_client_page(self):
        self.ui.stackedWidget.setCurrentWidget(self.create_client_page)

    def open_create_work_order_page(self):
        self.ui.stackedWidget.setCurrentWidget(self.create_work_order_page)

    def go_to_home(self):
        self.ui.stackedWidget.setCurrentWidget(self.dashboard_page)