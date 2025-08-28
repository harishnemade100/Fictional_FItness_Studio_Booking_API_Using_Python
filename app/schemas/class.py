from pydantic import BaseModel, EmailStr
from datetime import datetime

class ClassBase(BaseModel):
    name: str
    datetime: datetime
    total_slots: int

class ClassCreate(ClassBase):
    pass

class ClassOut(ClassBase):
    id: int
    instructor_id: int
    available_slots: int

    class Config:
        orm_mode = True
