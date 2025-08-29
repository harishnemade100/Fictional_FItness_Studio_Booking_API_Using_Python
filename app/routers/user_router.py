from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.services.database import get_db
from app.models.user import User
from app.schemas.user import UserRegister, UserLogin, UserResponse
from app.services.user_auth_service import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(
    user_data: UserRegister,
    db: Session = Depends(get_db)
) -> UserResponse:
    """
    Register a new user.

    Args:
        user_data (UserRegister): Request body with user details
        db (Session, optional): SQLAlchemy session (injected).

    Raises:
        HTTPException: If the email is already registered.

    Returns:
        UserResponse: The created user, containing:
            - id (int): User ID
            - name (str): User's name
            - email (EmailStr): User's email
    """
    user = db.query(User).filter(User.email == user_data.email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password_hash=hash_password(user_data.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login", status_code=status.HTTP_200_OK)
def login(
    user_data: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Authenticate a user and return a JWT access token.

    Args:
        user_data (UserLogin): Request body with login credentials
        db (Session, optional): SQLAlchemy session (injected).

    Raises:
        HTTPException: If email is not found or password is invalid.
    """
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    token = create_access_token(data={"sub": user.email})

    return dict(
        access_token=token,
        token_type="bearer"
    )
