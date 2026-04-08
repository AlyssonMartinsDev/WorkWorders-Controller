from sqlalchemy import Column, Integer, String, Text, null

from data.database import Base


class WorkOrder(Base):
    __tablename__ = "work_orders"

    id= Column(Integer, primary_key=True, autoincrement=True)
    client_name= Column[str](String, nullable=False)
    phone= Column[str](String, nullable=False)
    access_remote= Column[str](String, nullable=False)
    description= Column[str](Text, nullable=False)
    date= Column[str](String, nullable=False)
    status_service = Column[str](String, nullable=False)
    price = Column[str](String, nullable=False)
    status_payment = Column[str](String, nullable=False)