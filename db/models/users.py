from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from ESMS.db.base import Base

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="SET NULL"), nullable=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_manager = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
