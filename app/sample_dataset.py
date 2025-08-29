from sqlalchemy.orm import Session
from app.services.database import SessionLocal, engine, Base
from app.models.classes import Class
from datetime import datetime, timedelta

# Create all tables
Base.metadata.create_all(bind=engine)

# Open DB session
db: Session = SessionLocal()

# Clear existing data (optional, for a clean seed)
db.query(Class).delete()

# Add sample classes
sample_classes = [
    Class(
        name="Morning Yoga",
        datetime=datetime.utcnow() + timedelta(days=1, hours=7),
        instructor="Alice Johnson",
        total_slots=20,
        available_slots=20,
    ),
    Class(
        name="Evening Zumba",
        datetime=datetime.utcnow() + timedelta(days=1, hours=18),
        instructor="Bob Smith",
        total_slots=25,
        available_slots=25,
    ),
    Class(
        name="HIIT Blast",
        datetime=datetime.utcnow() + timedelta(days=2, hours=6),
        instructor="Charlie Brown",
        total_slots=15,
        available_slots=15,
    ),
]

db.add_all(sample_classes)
db.commit()

print("✅ Seed data inserted successfully!")
