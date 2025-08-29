from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.services.database import Base


class Class(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)   # ✅ length added
    datetime = Column(DateTime, nullable=False)  # stored in UTC
    instructor_id = Column(Integer, ForeignKey("users.id"))
    total_slots = Column(Integer, nullable=False)
    available_slots = Column(Integer, nullable=False)

    instructor = relationship("User", back_populates="classes")
    bookings = relationship("Booking", back_populates="fitness_class")