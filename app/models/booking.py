
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base



class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("classes.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    booked_at = Column(DateTime, default=datetime.utcnow)

    fitness_class = relationship("Class", back_populates="bookings")
    user = relationship("User", back_populates="bookings")