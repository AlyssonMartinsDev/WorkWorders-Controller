# SQLAlchemy imports
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, UTC
from sqlalchemy.orm import relationship

from data.database import Base


class StatusPaymentModel(Base):
    __tablename__ = "status_payments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)

    created_at = Column(
        DateTime(timezone=True),
        default= lambda: datetime.now(UTC)
    )
    updated_at = Column(
        DateTime(timezone=True),
        default= lambda: datetime.now(UTC),
        onupdate= lambda: datetime.now(UTC)
    )

    work_orders = relationship("WorkOrderModel", back_populates="status_payment")