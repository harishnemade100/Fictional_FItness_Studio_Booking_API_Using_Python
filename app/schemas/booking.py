from pydantic import BaseModel, EmailStr
from datetime import datetime


class BookingRequest(BaseModel):
    """
    Schema for creating a new booking request.
    Sent by the client when booking a class.
    """
    class_id: int
    client_name: str
    client_email: EmailStr

    """Sample Request Body"""
    model_config = {
        "json_schema_extra": {
            "example": {
                "class_id": 1,
                "client_name": "John Doe",
                "client_email": "john.doe@example.com",
            }
        }
    }


class BookingResponse(BaseModel):
    """
    Schema for booking response.
    Returned by the API after a successful booking.
    """
    message: str
    booking_id: int
    class_id: int
    class_name: str
    datetime: datetime
    instructor: str
    client_name: str
    client_email: str

    """Sample Response Body"""
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 101,
                "class_id": 1,
                "user_id": 42,
                "booked_at": "2025-08-29T10:30:00Z",
            }
        }
    }


class BookingInfo(BaseModel):
    """
    Schema for detailed booking information.
    Used internally or for admin views.
    """

    booking_id: int
    user_id: int
    client_email: str
    class_id: int
    class_name: str
    class_datetime: datetime
    instructor: str
