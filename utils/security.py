from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from typing import Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "replace-this-secret"  # set via env in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(subject: str, data: Optional[dict] = None, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = {"sub": str(subject)}
    if data:
        to_encode.update(data)
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise
