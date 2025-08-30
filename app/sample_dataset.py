from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.services.database import SessionLocal, engine, Base
from app.models.classes import Class
from app.models.booking import Booking
from app.models.user import User

Base.metadata.create_all(bind=engine)


def run_seed():
    """Insert default classes into the DB with safe cleanup."""

    db: Session = SessionLocal()
    try:
        db.query(Booking).delete()
        db.query(Class).delete()
        db.query(User).delete()

        # Sample classes
        sample_classes = [
            Class(
                name="Morning Yoga",
                datetime=datetime.now(timezone.utc)+ timedelta(days=1, hours=7),
                instructor="Alice Johnson",
                total_slots=20,
                available_slots=20,
            ),
            Class(
                name="Evening Zumba",
                datetime=datetime.now(timezone.utc) + timedelta(days=1, hours=18),
                instructor="Bob Smith",
                total_slots=25,
                available_slots=25,
            ),
            Class(
                name="HIIT Blast",
                datetime=datetime.now(timezone.utc) + timedelta(days=2, hours=6),
                instructor="Charlie Brown",
                total_slots=15,
                available_slots=15,
            ),
        ]

        db.add_all(sample_classes)
        db.commit()
        print("Seed data inserted successfully!")

    except Exception as e:
        db.rollback()
        print(f"Error during seeding: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()
