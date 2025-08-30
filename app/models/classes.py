from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.services.database import Base


class Class(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)   # Yoga, Zumba, HIIT
    datetime = Column(DateTime, nullable=False, default=datetime.utcnow)  # stored in UTC
    instructor = Column(String(100), nullable=False)  # direct string field instead of foreign key
    total_slots = Column(Integer, nullable=False)
    available_slots = Column(Integer, nullable=False)

    # Relationships
    bookings = relationship("Booking",  back_populates="fitness_class", cascade="all, delete-orphan")