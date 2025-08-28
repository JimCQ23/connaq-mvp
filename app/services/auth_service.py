# services/auth_service.py
import os
import pyodbc
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from app.services.user_service import get_user_by_email
from app.models.user_schema import LoginRequest, TokenResponse
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def authenticate_user(login_data: LoginRequest) -> TokenResponse:
    user = get_user_by_email(login_data.email)
    if not user or not verify_password(login_data.password, user.PASSWORD):
        raise ValueError("Invalid credentials")

    token = create_access_token({"sub": user.EMAIL})
    return TokenResponse(access_token=token)
