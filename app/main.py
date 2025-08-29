from app.services.database import engine, Base, get_db
from fastapi import FastAPI, Depends
from app.models import user, classes  , booking  # Ensure models are imported for metadata
from app.routers import booking_router, class_router  # , users

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fitness Booking API", version="1.0.0")

app.include_router(class_router.router)
app.include_router(booking_router.router)

@app.get("/")
def root():
    return {"message": "Welcome to Fitness Booking API 🚀"}

# # Register routers
# app.include_router(users.router, prefix="/users", tags=["Users"])
# app.include_router(classes.router, prefix="/classes", tags=["Classes"])
# app.include_router(bookings.router, prefix="/bookings", tags=["Bookings"])
