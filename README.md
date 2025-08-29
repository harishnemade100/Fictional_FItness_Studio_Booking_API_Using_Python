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
2️⃣ Run Locally (No Docker)
bash
Copy code
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate     # Mac/Linux
venv\Scripts\activate        # Windows

# Install dependencies
pip install -r requirements.txt

# Run FastAPI app
uvicorn app.main:app --reload


---


📘 API Endpoints
👤 Users
Register User
POST /users/register

Request:

json
Copy code
{
  "name": "Alice Johnson",
  "email": "alice@example.com",
  "password": "password123"
}
Login (Get JWT Token)
POST /users/login

Response:

json
Copy code
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
🏋️ Classes
Get All Upcoming Classes
GET /classes

Response:

json
Copy code
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

makefile
Copy code
Authorization: Bearer <JWT_TOKEN>
Request:

json
Copy code
{
  "class_id": 1,
  "client_name": "Alice Johnson",
  "client_email": "alice@example.com"
}
Response:

json
Copy code
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

json
Copy code
[
  {
    "id": 10,
    "class_id": 1,
    "client_name": "Alice Johnson",
    "client_email": "alice@example.com",
    "status": "confirmed"
  }
]

--- 


🧪 Testing
You can test the API in multiple ways:

1️⃣ Swagger UI
Open: http://localhost:8000/docs

Interactive documentation with built-in request testing.

2️⃣ ReDoc
Open: http://localhost:8000/redoc

Clean, read-only API reference documentation.

3️⃣ Postman
Import the provided {'postman_collection.json'} file from the project root into Postman.

Contains pre-configured requests for:

User Registration

User Login (JWT Authentication)

Get Upcoming Classes

Create Booking

Get Bookings by Email


---

## 🧪 cURL Examples

You can test the API directly using `cURL` from your terminal.

---

### 👤 Register User
```bash
curl -X POST http://127.0.0.1:8000/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "password": "password123"
  }'
🔑 Login (Get JWT Token)
bash
Copy code
curl -X POST http://127.0.0.1:8000/users/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice@example.com",
    "password": "password123"
  }'
🏋️ Get All Upcoming Classes
bash
Copy code
curl -X GET "http://127.0.0.1:8000/classes/" \
  -H "accept: application/json"
📅 Book a Class (JWT Required)
Replace <JWT_TOKEN> with the token from login.

bash
Copy code
curl -X POST "http://127.0.0.1:8000/bookings/" \
  -H "accept: application/json" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "class_id": 1,
    "client_email": "john.doe@example.com",
    "client_name": "John Doe"
  }'
📋 List Bookings by Email
bash
Copy code
curl -X GET "http://127.0.0.1:8000/bookings/?email=alice@example.com" \
  -H "accept: application/json"