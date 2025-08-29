from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.services.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)  # ✅ length added
    email = Column(String(255), unique=True, index=True, nullable=False)  # ✅ length added
    password_hash = Column(String(255), nullable=False)  # ✅ length added
    role = Column(String(50), default="client")   # ✅ safe length
    created_at = Column(DateTime, default=datetime.utcnow)

    classes = relationship("Class", back_populates="instructor")
    bookings = relationship("Booking", back_populates="user")
