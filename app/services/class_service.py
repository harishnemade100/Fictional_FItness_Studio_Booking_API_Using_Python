from sqlalchemy.orm import Session
from app.models.classes import Class
from app.utils.timezone import convert_to_timezone


def get_upcoming_classes(db: Session, target_tz: str = "Asia/Kolkata"):
    """Return all upcoming classes in given timezone (default IST)."""
    classes = db.query(Class).all()
    results = []
    for cls in classes:
        results.append({
            "id": cls.id,
            "name": cls.name,
            "datetime": convert_to_timezone(cls.datetime, target_tz),
            "instructor": cls.instructor.name if cls.instructor else None,
            "available_slots": cls.available_slots,
        })
    return results
