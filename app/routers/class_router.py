from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.services.database import get_db
from app.services.class_service import ClassService
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
    try:
        service = ClassService(db)
        return service.get_upcoming_classes(db, target_tz="Asia/Kolkata")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
