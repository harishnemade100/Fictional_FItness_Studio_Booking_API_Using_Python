from app.services.database import engine, Base, get_db
from fastapi import FastAPI, Depends
from app.models import user, classes  , booking  # Ensure models are imported for metadata
from app.routers import booking_router, class_router, user_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fitness Booking API")

app.include_router(user_router.router)
app.include_router(class_router.router)
app.include_router(booking_router.router)


@app.get("/")
def root():
    return {"message": "Welcome to Fitness Booking API 🚀"}
