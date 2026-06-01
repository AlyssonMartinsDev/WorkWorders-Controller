from data.database import engine, Base

# IMPORTANTE: importar todos os models
from models.clients import ClientsModel
from models.work_orders import WorkOrderModel
from models.status_services import StatusServiceModel
from models.status_payments import StatusPaymentModel
from models.remote_access import RemoteAccess
from data.seed import seed_database


def init_db():
    Base.metadata.create_all(bind=engine)
    seed_database()