from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy import Enum as SQLEnum
from ..core.database import Base
from .enums import UserRoleEnum
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(20), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(100))
    role = Column(SQLEnum(UserRoleEnum), nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    otp_code = Column(String(6))
    otp_expires_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    fighter_profile = relationship("Fighter", back_populates="user", uselist=False)
    trainer_profile = relationship("Trainer", back_populates="user", uselist=False)
    manager_profile = relationship("Manager", back_populates="user", uselist=False)