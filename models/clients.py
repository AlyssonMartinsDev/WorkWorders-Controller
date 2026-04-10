# SQLAlchemy imports
from sqlalchemy import Column, Integer, String, Text, null, DateTime
from datetime import datetime, UTC
from sqlalchemy.orm import relationship

from data.database import Base


class ClientsModel(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=True)
    notes = Column(Text, nullable=True)


    created_at = Column(
        DateTime(timezone=True),
        default= lambda: datetime.now(UTC)
    )
    updated_at = Column(
        DateTime(timezone=True),
        default= lambda: datetime.now(UTC),
        onupdate= lambda: datetime.now(UTC)
    )

    work_orders = relationship("WorkOrderModel", back_populates="client")