from PySide6.QtCore import QFile
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QAbstractItemView, QDialog, QMessageBox, QPushButton, QVBoxLayout

from utils.paths import ui_path


class LookupWindowDialog(QDialog):
    def __init__(self, headers, rows, title="Lookup"):
        super().__init__()
        self.load_ui()
        self.setup_connections()
        self.headers = headers
        self.rows = rows
        self.title = title

        self.selected_id = None

        self.load_table_data()

    def load_ui(self):
        loader = QUiLoader()
        file = QFile(str(ui_path("lookupDialog.ui")))

        if not file.open(QFile.ReadOnly):
            raise RuntimeError("Could not open lookupDialog.ui")

        self.ui = loader.load(file)
        file.close()

        if self.ui is None:
            raise RuntimeError("Could not load lookupDialog.ui")

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.ui)
        self.setLayout(layout)

        self.setWindowTitle(self.ui.windowTitle())
        self.resize(self.ui.size())

    def setup_connections(self):
        btn_ok = self.findChild(QPushButton, "btn_ok")
        btn_cancel = self.findChild(QPushButton, "btn_cancel")

        if btn_ok:
            btn_ok.clicked.connect(self.confirm_selection)

        if btn_cancel:
            btn_cancel.clicked.connect(self.reject)

        self.ui.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tableView.setSelectionMode(QAbstractItemView.SingleSelection)

        self.ui.tableView.clicked.connect(self.on_row_clicked)

    def load_table_data(self):
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(self.headers)

        for row_data in self.rows:
            row_items = [QStandardItem(str(value)) for value in row_data]
            self.model.appendRow(row_items)

        self.ui.tableView.setModel(self.model)
        self.ui.tableView.verticalHeader().setVisible(False)
        self.ui.tableView.resizeColumnsToContents()
    
    
    def confirm_selection(self):

        if not self.selected_id:
            QMessageBox.critical(self, "Erro", "Nenhum dado selecionado")

        self.accept()

            
    def on_row_clicked(self, index):
        row = index.row()
        
        item = self.model.item(row, 0)
        self.selected_id = int(item.text())




