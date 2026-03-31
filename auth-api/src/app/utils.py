from datetime import timedelta, datetime, timezone
from typing import Any
from shared.config import settings
from jose import jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['argon2'], deprecated="auto")

def hash_password(plain: str)-> str:
    return pwd_context.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict[str, Any], expires_delta: timedelta | None = None,) -> str:
    to_encode = data.copy()
    if expires_delta is not None:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode["exp"] = expire
    to_encode["iat"] = datetime.now(timezone.utc)
    return jwt.encode(data,algorithm=settings.algorithm, key=settings.secret)

