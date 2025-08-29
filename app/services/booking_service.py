from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional

from app.models.booking import Booking
from app.models.user import User
from app.models.classes import Class
from app.schemas.booking import BookingRequest


def create_booking(db: Session, booking_data: BookingRequest) -> Booking:
    """
    Create a booking for a given class if slots are available.

    Args:
        db (Session): SQLAlchemy database session.
        booking_data (BookingRequest): Data required to create a booking 
            including class ID, client name, and client email.

    Raises:
        ValueError: If the class is not found or if no slots are available.

    Returns:
        Booking: The newly created booking instance.
    """
    # Check if the class exists
    fitness_class = db.query(Class).filter(Class.id == booking_data.class_id).first()
    if not fitness_class:
        raise ValueError("Class not found")

    # Check if slots are available
    if fitness_class.available_slots <= 0:
        raise ValueError("No slots available for this class")

    # Ensure user exists, otherwise create a new one
    user = db.query(User).filter(User.email == booking_data.client_email).first()
    if not user:
        user = User(
            name=booking_data.client_name,
            email=booking_data.client_email,
            password_hash="N/A"  # Placeholder, since no password is provided
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    # Create the booking
    booking = Booking(
        class_id=fitness_class.id,
        user_id=user.id,
        booked_at=datetime.utcnow()
    )
    db.add(booking)

    # Decrement available slots
    fitness_class.available_slots -= 1
    db.commit()
    db.refresh(booking)

    return booking


def get_bookings_by_email(db: Session, email: str) -> List[Booking]:
    """
    Retrieve all bookings associated with a user's email.

    Args:
        db (Session): SQLAlchemy database session.
        email (str): The email address of the user.

    Returns:
        List[Booking]: A list of bookings associated with the given email.
                       Returns an empty list if the user does not exist or 
                       has no bookings.
    """
    # Find the user by email
    user: Optional[User] = db.query(User).filter(User.email == email).first()
    if not user:
        return []

    # Retrieve bookings for the user
    return db.query(Booking).filter(Booking.user_id == user.id).all()
