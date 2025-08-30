from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.services.database import get_db
from app.services.booking_service import BookingService
from app.schemas.booking import BookingRequest, BookingResponse, BookingInfo

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post("/", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def book_class(
    booking_data: BookingRequest,
    db: Session = Depends(get_db)
) -> BookingResponse:
    """
    Create a booking for a fitness class.

    Args:
        booking (BookingRequest): Booking data containing.
        db (Session, optional): SQLAlchemy database session (injected).

    Raises:
        HTTPException: If the class is not found or no slots are available.

    Returns:
        BookingResponse: The newly created booking with:
            - id (int): Booking ID
            - class_id (int): ID of the booked class
            - user_id (int): ID of the user
            - booked_at (datetime): Timestamp of booking
    """
    try:
        service = BookingService(db)
        return service.create_booking(booking_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=List[BookingInfo])
def list_bookings(
    email: str,
    db: Session = Depends(get_db)
) -> List[BookingResponse]:
    """
    Retrieve all bookings for a given user.

    Args:
        email (str): Email address of the user.
        db (Session, optional): SQLAlchemy database session (injected).

    Returns:
        List[BookingResponse]: List of bookings for the user, each with:
            - id (int): Booking ID
            - class_id (int): ID of the booked class
            - user_id (int): ID of the user
            - booked_at (datetime): Timestamp of booking
    """
    try:
        service = BookingService(db)
        return service.get_bookings_by_email(email)
    except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

