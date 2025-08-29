from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.database import get_db
from app.services.class_service import get_upcoming_classes

router = APIRouter(prefix="/classes", tags=["Classes"])


@router.get("/")
def list_classes(db: Session = Depends(get_db)):
    return get_upcoming_classes(db)
