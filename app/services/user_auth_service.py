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

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


class AuthService:
    """
    Authentication & User security service:
    - Password hashing/verification
    - JWT token generation & validation
    """

    def __init__(self, db: Session):
        self.db = db

    def hash_password(self, password: str) -> str:
        """
        Hash a plaintext password.
        
        Args:
            password (str): The plaintext password to hash.
            
        Returns:
            str: The hashed password.
        """
        return pwd_context.hash(password)

    def verify_password(self, password: str, hashed: str) -> bool:
        """
        Verify a plaintext password against a hashed password.

        Args:
            password (str): The plaintext password to verify.
            hashed (str): The hashed password to compare against.
        Returns:
            bool: True if the password matches the hash, False otherwise.
        """

        return pwd_context.verify(password, hashed)

    def create_access_token(self, data: Dict[str, Any]) -> str:

        """
        Create a JWT access token.
        Args:
            data (Dict[str, Any]): Data to encode in the token.
        Returns:
            str: The encoded JWT token.
        """

        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    def authenticate_user(self, email: str, password: str) -> User:
        """
        Check if user exists and password is valid.

        Args:
            email (str): User's email.
            password (str): User's plaintext password.

        Returns:
            User: The authenticated user object.
        """
        user = self.db.query(User).filter(User.email == email).first()
        if not user or not self.verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
