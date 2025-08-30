from sqlalchemy.orm import Session
from typing import List
from app.models.classes import Class
from app.schemas.classes import ClassBase
from app.utils.timezone import convert_to_timezone


class ClassService:
    """
    Service layer for handling class-related operations.
    """

    def __init__(self, db: Session):
        self.db = db

    def get_upcoming_classes(self, db: Session, *, target_tz: str = "Asia/Kolkata") -> List[ClassBase]:
        """
        Fetch all upcoming classes, converting datetime to the target timezone.
        Args:
            target_tz (str): Timezone to convert class datetimes to. Default is 'Asia/Kolkata'.
        
        Returns:
            List[ClassBase]: List of upcoming classes with converted datetimes.
        """
        classes = self.db.query(Class).all()
        results: List[ClassBase] = []

        for cls in classes:
            results.append(
                ClassBase(
                    id=cls.id,
                    name=cls.name,
                    datetime=convert_to_timezone(cls.datetime, target_tz),
                    instructor=cls.instructor,
                    total_slots=cls.total_slots,
                    available_slots=cls.available_slots,
                )
            )
        return results
    

