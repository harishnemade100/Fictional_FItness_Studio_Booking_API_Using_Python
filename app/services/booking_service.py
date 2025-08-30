from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import List, Optional
from fastapi import HTTPException

from app.models.booking import Booking
from app.models.user import User
from app.models.classes import Class
from app.schemas.booking import BookingRequest, BookingResponse, BookingInfo


class BookingService:
    """
    Service layer for handling booking-related operations.
    """

    def __init__(self, db: Session):
        self.db = db

    def create_booking(self, booking_data: BookingRequest) -> BookingResponse:
        """
        Create a booking for a given class if slots are available.
        Prevents duplicate bookings by the same user for the same class.

        Args:
            booking_data (BookingRequest): Data required to create a booking.
        
        Returns:
            BookingResponse: Details of the created booking.
        """

        # Check if the class exists
        fitness_class = self.db.query(Class).filter(Class.id == booking_data.class_id).first()
        if not fitness_class:
            raise ValueError("Class not found")

        # Check if slots are available
        if fitness_class.available_slots <= 0:
            raise ValueError("No slots available for this class")
        
        # Check if the user exists
        user = self.db.query(User).filter(User.email == booking_data.client_email).first()
        if user is None:
            raise HTTPException(
                status_code=400,
                detail="Please register before booking a class."
            )
        
        # Check if the user already booked this class
        existing_booking = (
            self.db.query(Booking)
            .filter(Booking.class_id == fitness_class.id, Booking.user_id == user.id)
            .first()
        )
        if existing_booking:
            return BookingResponse(
                message="You have already booked this class.",
                booking_id=existing_booking.id,
                class_id=fitness_class.id,
                class_name=fitness_class.name,
                datetime=fitness_class.datetime,
                instructor=fitness_class.instructor,
                client_name=user.name,
                client_email=user.email,
            )

        # Create the booking
        booking = Booking(
            class_id=fitness_class.id,
            user_id=user.id,
            booked_at=datetime.now(timezone.utc)
        )
        self.db.add(booking)

        # Decrement available slots
        fitness_class.available_slots -= 1
        self.db.commit()
        self.db.refresh(booking)

        return BookingResponse(
            message="Booking successful!",
            class_id=fitness_class.id,
            booking_id=booking.id,
            class_name=fitness_class.name,
            datetime=fitness_class.datetime,
            instructor=fitness_class.instructor,
            client_name=user.name,
            client_email=user.email,
        )

    def get_bookings_by_email(self, email: str) -> List[BookingInfo]:
        """
        Retrieve all bookings associated with a user's email,
        including user ID, client email, class ID, and class datetime.
        
        Args:
            email (str): Email address of the user.

        Returns:
            List[BookingInfo]: List of bookings for the user.
        """

        user: Optional[User] = self.db.query(User).filter(User.email == email).first()
        if user is None:
            raise HTTPException(
                status_code=400,
                detail="Please register before booking a class."
            )
        
        bookings = self.db.query(Booking).filter(Booking.user_id == user.id).all()
        if not bookings:
            raise HTTPException(
                status_code=404,
                detail="No bookings found for this email."
            )
        
        all_bookings = []
        for booking in bookings:
            fitness_class = self.db.query(Class).filter(Class.id == booking.class_id).first()
            if fitness_class:
                booking_info = BookingInfo(
                    booking_id=booking.id,
                    user_id=user.id,
                    client_email=user.email,
                    class_id=fitness_class.id,
                    class_name=fitness_class.name,
                    class_datetime=fitness_class.datetime,
                    instructor=fitness_class.instructor,
                    booked_at=booking.booked_at
                )
                all_bookings.append(booking_info)

        return all_bookings
