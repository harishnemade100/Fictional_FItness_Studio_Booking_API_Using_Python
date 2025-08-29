from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.database import get_db
from app.services.booking_service import create_booking, get_bookings_by_email
from app.schemas.booking import BookingRequest

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post("/")
def book_class(booking: BookingRequest, db: Session = Depends(get_db)):
    try:
        booking_obj = create_booking(db, booking)
        return {"message": "Booking successful", "booking_id": booking_obj.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/")
def list_bookings(email: str, db: Session = Depends(get_db)):
    return get_bookings_by_email(db, email)
