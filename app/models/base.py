from sqlalchemy import Column, Integer, DateTime
from sqlalchemy import func
from ..core.database import Base

class TimeStampedBase(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())