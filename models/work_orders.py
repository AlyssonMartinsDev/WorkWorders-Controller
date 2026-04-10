from sqlalchemy import Column, Integer, String, Text, null, ForeignKey, DateTime, Float
from datetime import datetime, UTC
from sqlalchemy.orm import relationship

from data.database import Base


class WorkOrderModel(Base):
    __tablename__ = "work_orders"

    id= Column(Integer, primary_key=True, autoincrement=True)

    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)

    remote_access_id = Column(Integer, ForeignKey("remote_access.id"), nullable=True)

    description= Column(Text, nullable=False)

    status_service_id = Column(Integer, ForeignKey("status_services.id"), nullable=False, default=1)

    price = Column(Float, nullable=False)

    status_payment_id = Column(Integer, ForeignKey("status_payments.id"), nullable=False, default=1)

    created_at = Column(
        DateTime(timezone=True),
        default= lambda: datetime.now(UTC)
    )
    updated_at = Column(
        DateTime(timezone=True),
        default= lambda: datetime.now(UTC),
        onupdate= lambda: datetime.now(UTC)
    )


    client = relationship("ClientsModel", back_populates="work_orders")
    remote_access = relationship("RemoteAccess", back_populates="work_orders")
    status_service = relationship("StatusServiceModel", back_populates="work_orders")
    status_payment = relationship("StatusPaymentModel", back_populates="work_orders")