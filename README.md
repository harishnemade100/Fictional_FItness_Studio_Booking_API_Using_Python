# 🏋️ Fictional Fitness Studio Booking API

A **FastAPI-based Booking API** for a fictional fitness studio.  
This project demonstrates **backend development skills** including API design, database integration, JWT authentication, and input validation.

---

## 🎯 Objective
Build a **Booking API** for a fitness studio that offers classes such as Yoga, Zumba, and HIIT.  
Clients should be able to:
- View available upcoming classes
- Book a spot in a class (if slots are available)
- Retrieve all their bookings by email  
The system should also handle **authentication & authorization** using JWT.

---

## 📌 Requirements Implemented
✔️ **POST /users/register** → Register a new user  
✔️ **POST /users/login** → Authenticate a user and return a **JWT token**  
✔️ **GET /classes** → List all upcoming classes (name, date/time, instructor, available slots)  
✔️ **POST /book** → Create a booking request (validates slot availability & reduces slots)  
✔️ **GET /bookings** → Get all bookings made by a client email  

---

## 🚀 Features
- **JWT authentication** for secure booking
- **SQLAlchemy ORM** with relationships (Users, Classes, Bookings)
- **MySQL/SQLite** support
- **Seed data** for demo classes
- **Automatic docs** via FastAPI (`/docs`)

---

## 📦 Tech Stack
- **FastAPI** (Python 3.11+)
- **SQLAlchemy + Alembic**
- **Pydantic v2**
- **MySQL** (with fallback to SQLite)
- **Docker + Docker Compose**

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repo
```bash
git clone https://github.com/YOUR_USERNAME/fitness-api.git
cd fitness-api

Run Locally (No Docker)

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate     # Mac/Linux
venv\Scripts\activate        # Windows

# Install dependencies
pip install pipenv

pipenv install

# Run FastAPI app
uvicorn app.main:app --reload


📘 API Endpoints

👤 Users
Register

POST /users/register
Request:

{
  "name": "Alice Johnson",
  "email": "alice@example.com",
  "password": "password123"
}

Login (JWT Token)

POST /users/login
Response:

{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}

🏋️ Classes
Get All Upcoming Classes

GET /classes
Response:

[
  {
    "id": 1,
    "name": "Morning Yoga",
    "datetime": "2025-09-01T07:00:00Z",
    "instructor": "Alice Johnson",
    "total_slots": 20,
    "available_slots": 15
  }
]

📅 Bookings
Create Booking (JWT Required)

POST /book
Headers:

Authorization: Bearer <JWT_TOKEN>


Request:

{
  "class_id": 1,
  "client_name": "Alice Johnson",
  "client_email": "alice@example.com"
}


Response:

{
  "id": 10,
  "class_id": 1,
  "client_name": "Alice Johnson",
  "client_email": "alice@example.com",
  "status": "confirmed"
}

Get Bookings by Email

GET /bookings?email=alice@example.com
Response:

[
  {
    "id": 10,
    "class_id": 1,
    "client_name": "Alice Johnson",
    "client_email": "alice@example.com",
    "status": "confirmed"
  }
]
