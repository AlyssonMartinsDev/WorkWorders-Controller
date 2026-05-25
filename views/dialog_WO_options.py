from PySide6.QtWidgets import QDialog, QMessageBox, QVBoxLayout
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, Signal


from services.work_order_service import WorkOrderService
from utils.paths import ui_path

class Dialog_WO_options(QDialog):
    work_order_updated = Signal() # Sinal para indicar que a ordem de serviço foi atualizada
    def __init__(self, wo_id, wo_status_service, wo_status_payment):
        super(Dialog_WO_options, self).__init__()
        self.wo_id = wo_id
        self.wo_status_service = wo_status_service
        self.wo_status_payment = wo_status_payment
        self.work_order_service = WorkOrderService()

        

        self.load_ui()
        self.setup_connections()
        self.check_status()





    def load_ui(self):

        loader = QUiLoader()

        file = QFile(ui_path("WOOptionsDialog.ui"))
        file.open(QFile.ReadOnly)

        self.ui = loader.load(file)
        file.close()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.ui)

    

    def setup_connections(self):
        self.ui.btn_finish.clicked.connect(self.finish_work_order)
        self.ui.btn_mark_paid.clicked.connect(self.mark_work_order_as_paid)


    def finish_work_order(self):

        print(f"Finalizando ordem de serviço com ID: {self.wo_id}")  # Debug: Verificar o ID da ordem de serviço
        try:
            res = self.work_order_service.update_status_service(self.wo_id, 2)

            QMessageBox.information(self, "Sucesso", res)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao finalizar ordem de serviço: {e}")
        finally:
            self.work_order_updated.emit()
            self.close()


            # depois você chama o service:
            # self.work_order_service.finish_work_order(work_order_id)

    def check_status(self):
        # Aqui você pode implementar a lógica para verificar o status da ordem de serviço
        # e habilitar/desabilitar os botões conforme necessário
        if self.wo_status_service == "Finalizado":
            self.ui.btn_finish.setEnabled(False)
            self.ui.btn_vinc_access_remote.setEnabled(False)
        
        if self.wo_status_payment == "Pago":
            self.ui.btn_mark_paid.setEnabled(False)

    def mark_work_order_as_paid(self):
        try:
            res = self.work_order_service.update_status_payment(self.wo_id, 2)

            QMessageBox.information(self, "Sucesso", res)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao marcar ordem de serviço como paga: {e}")
            
        finally:
            self.work_order_updated.emit()
            self.close()

