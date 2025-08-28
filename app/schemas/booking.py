from pydantic import BaseModel, EmailStr
from datetime import datetime

class BookingBase(BaseModel):
    class_id: int

class BookingCreate(BookingBase):
    pass

class BookingOut(BaseModel):
    id: int
    class_id: int
    user_id: int
    booked_at: datetime

    class Config:
        orm_mode = True