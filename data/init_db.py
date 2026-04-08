from data.database import engine, Base

# importa o model para registrar a tabela
from models.work_orders import WorkOrder


def init_db():
    Base.metadata.create_all(bind=engine)