from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt
from pydantic import BaseModel, Field
from datetime import datetime, timedelta, timezone
import os
from app.db.database import get_db
from app.db.models import User
from email_validator import validate_email, EmailNotValidError

router = APIRouter()

# Load environment variables
SECRET_KEY = os.getenv("SECRET_KEY", "notsecret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class UserCreate(BaseModel):
    user_name: str = Field(default="username")
    user_email: str = Field(default="user@example.com")
    user_password: str = Field(min_length=5)

    @classmethod
    def validate_email(cls, value: str):
        try:
            validate_email(value)
        except EmailNotValidError:
            raise ValueError("Invalid email format")
        return value


class UserResponse(BaseModel):
    user_id: int
    user_name: str
    user_email: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int | None = None
    user_name: str | None = None


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    with get_db() as db:
        user = db.query(User).filter(User.user_id == token_data.user_id).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
        return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    return current_user


@router.post(
    "/users",
    response_model=UserCreate,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    tags=["user_management"],
)
async def create_user(user: UserCreate):
    hashed_password = get_password_hash(user.user_password)
    with get_db() as db:
        db_user = User(
            user_name=user.user_name,
            user_email=user.user_email,
            user_password=hashed_password,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user


@router.post(
    "/token",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary="Login to obtain an access token",
    tags=["user_management"],
)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    with get_db() as db:
        user = (
            db.query(User)
            .filter(
                (User.user_name == form_data.username)
                | (User.user_email == form_data.username)
            )
            .first()
        )
        if not user or not verify_password(form_data.password, user.user_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.user_name, "user_id": user.user_id},
            expires_delta=access_token_expires,
        )
        return {"access_token": access_token, "token_type": "bearer"}


@router.get(
    "/users/me/",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get current user information",
    tags=["user_management"],
)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.get(
    "/protected-endpoint/",
    status_code=status.HTTP_200_OK,
    summary="Access a protected endpoint",
    tags=["user_management"],
)
async def read_protected_data(current_user: User = Depends(get_current_active_user)):
    return {"message": "This is a protected endpoint", "user": current_user.user_name}
