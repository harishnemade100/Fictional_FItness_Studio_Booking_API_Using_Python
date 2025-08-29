from sqlalchemy.orm import Session
from app.models.booking import Booking
from app.models.user import User
from app.models import classes

from app.schemas.booking import BookingRequest
from datetime import datetime


def create_booking(db: Session, booking_data: BookingRequest):
    """Create a booking if slots are available."""

    fitness_class = db.query(classes.Class).filter(classes.Class.id == booking_data.class_id).first()
    if not fitness_class:
        raise ValueError("Class not found")

    if fitness_class.available_slots <= 0:
        raise ValueError("No slots available for this class")

    # Ensure user exists or create new
    user = db.query(User).filter(User.email == booking_data.client_email).first()
    if not user:
        user = User(
            name=booking_data.client_name,
            email=booking_data.client_email,
            password_hash="N/A"  # not required here
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    # Create booking
    booking = Booking(
        class_id=fitness_class.id,
        user_id=user.id,
        booked_at=datetime.utcnow()
    )
    db.add(booking)

    # Update slots
    fitness_class.available_slots -= 1
    db.commit()
    db.refresh(booking)

    return booking


def get_bookings_by_email(db: Session, email: str):
    """Return all bookings for a given client email."""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return []

    return db.query(Booking).filter(Booking.user_id == user.id).all()
