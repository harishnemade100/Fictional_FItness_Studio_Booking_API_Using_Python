from sqlalchemy.orm import Session
from typing import List
from app.models.classes import Class
from app.schemas.classes import ClassBase
from app.utils.timezone import convert_to_timezone


def get_upcoming_classes(db: Session, target_tz: str = "Asia/Kolkata") -> List[ClassBase]:
    """
    Fetch all upcoming classes, converting datetime to the target timezone.
    """
    classes = db.query(Class).all()
    results: List[ClassBase] = []

    for cls in classes:
        results.append(
            ClassBase(
                id=cls.id,
                name=cls.name,
                datetime=convert_to_timezone(cls.datetime, target_tz),  # keep as datetime
                instructor=cls.instructor,
                total_slots=cls.total_slots,
                available_slots=cls.available_slots,
            )
        )
    return results
