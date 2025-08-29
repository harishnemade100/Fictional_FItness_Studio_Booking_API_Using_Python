from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    """
    Schema for user registration request.
    """
    name: str
    email: EmailStr
    password: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "password": "strongpassword123",
            }
        }
    }


class UserLogin(BaseModel):
    """
    Schema for user login request.
    """
    email: EmailStr
    password: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "john.doe@example.com",
                "password": "strongpassword123",
            }
        }
    }


class UserResponse(BaseModel):
    """
    Schema for user response (returned after registration/login).
    """
    id: int
    name: str
    email: EmailStr

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 42,
                "name": "John Doe",
                "email": "john.doe@example.com",
            }
        }
    }