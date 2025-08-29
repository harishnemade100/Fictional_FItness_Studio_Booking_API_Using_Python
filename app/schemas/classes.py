from pydantic import BaseModel
from datetime import datetime

class ClassBase(BaseModel):
    """
    Base schema for a fitness class.
    """
    id: int
    name: str
    datetime: datetime
    instructor: str
    total_slots: int
    available_slots: int

    """Sample Class Data"""

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "Morning Yoga",
                "datetime": "2025-09-01T07:00:00+05:30",
                "instructor": "Alice Johnson",
                "total_slots": 20,
                "available_slots": 15,
            }
        }
    }
