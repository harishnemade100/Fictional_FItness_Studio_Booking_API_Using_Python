from pydantic import BaseModel
from datetime import datetime

class ClassBase(BaseModel):
    name: str
    datetime: datetime
    instructor: str
    total_slots: int
    available_slots: int