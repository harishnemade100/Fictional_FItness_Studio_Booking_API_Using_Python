import jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Any, Dict

from app.services.database import get_db, load_config
from app.models.user import User


# Load JWT config
auth_conf = load_config("JWT_TOKEN")

SECRET_KEY: str = auth_conf["SECRET_KEY"]
ALGORITHM: str = auth_conf["ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES: int = auth_conf["ACCESS_TOKEN_EXPIRE_MINUTES"]

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme (FastAPI dependency)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def hash_password(password: str) -> str:
    """
    Hash a plain text password using bcrypt.

    Args:
        password (str): Plain text password.

    Returns:
        str: Hashed password.
    """
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    """
    Verify if a plain text password matches a hashed password.

    Args:
        password (str): Plain text password.
        hashed (str): Hashed password from the database.

    Returns:
        bool: True if valid, False otherwise.
    """
    return pwd_context.verify(password, hashed)


def create_access_token(data: Dict[str, Any]) -> str:
    """
    Create a JWT access token.

    Args:
        data (Dict[str, Any]): Payload data (e.g., {"sub": user_email}).

    Returns:
        str: Encoded JWT access token.
    """
    to_encode = data.copy()
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
