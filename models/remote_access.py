from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from datetime import datetime, UTC
from sqlalchemy.orm import relationship

from data.database import Base


class RemoteAccess(Base):
    __tablename__ = "remote_access"

    id = Column(Integer, primary_key=True, autoincrement=True)

    code = Column(String, nullable=False)
    password = Column(String, nullable=True)
    type = Column(String, nullable=True)
    work_order_id = Column(Integer, ForeignKey("work_orders.id"), nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC)
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC)
    )

    work_order = relationship("WorkOrderModel", back_populates="remote_accesses")