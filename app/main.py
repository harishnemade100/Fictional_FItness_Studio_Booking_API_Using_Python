from app.services.database import engine, Base
from fastapi import FastAPI
from app.models import user, classes  , booking
from app.routers import booking_router, class_router, user_router
from app.sample_dataset import run_seed 

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fitness Booking API")

app.include_router(user_router.router)
app.include_router(class_router.router)
app.include_router(booking_router.router)


@app.get("/")
def root():
    return {"message": "Welcome to Fitness Booking API 🚀"}


@app.on_event("startup")
def startup_event():
    # Run seeding automatically on startup
    run_seed()
