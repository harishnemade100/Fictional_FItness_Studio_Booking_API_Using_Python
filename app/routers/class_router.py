from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.services.database import get_db
from app.services.class_service import get_upcoming_classes
from app.schemas.classes import ClassBase

router = APIRouter(prefix="/classes", tags=["Classes"])


@router.get("/", response_model=List[ClassBase])
def list_classes(
    db: Session = Depends(get_db)
) -> List[ClassBase]:
    """
    Retrieve all upcoming fitness classes.

    Args:
        db (Session, optional): SQLAlchemy database session (injected automatically).

    Returns:
        List[ClassBase]: A list of upcoming fitness classes, where each class contains:
            - name (str): Name of the class
            - datetime (datetime): Scheduled class datetime (converted to timezone)
            - instructor (str): Name of the instructor
            - total_slots (int): Total number of slots for the class
            - available_slots (int): Number of slots still available
    """
    return get_upcoming_classes(db)
