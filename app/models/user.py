from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datatime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="client")   # client, instructor, admin
    created_at = Column(DateTime, default=datetime.utcnow)

    classes = relationship("Class", back_populates="instructor")
    bookings = relationship("Booking", back_populates="user")