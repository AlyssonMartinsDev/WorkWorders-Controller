from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, UTC
from sqlalchemy.orm import relationship

from data.database import Base


class RemoteAccess(Base):
    __tablename__ = "remote_access"

    id = Column(Integer, primary_key=True, autoincrement=True)

    code = Column(String, nullable=False)
    password = Column(String, nullable=True)
    type = Column(String, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC)
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC)
    )

    work_orders = relationship("WorkOrderModel", back_populates="remote_access")