from pydantic import BaseModel, EmailStr
from datetime import datetime


class BookingRequest(BaseModel):
    class_id: int
    client_name: str
    client_email: EmailStr

class BookingResponse(BaseModel):
    id: int
    class_id: int
    user_id: int
    booked_at: datetime