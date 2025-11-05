from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import os

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict, expires_delta: int = 60):
    secret = os.getenv('SECRET_KEY', 'dev-secret')
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    to_encode = data.copy()
    to_encode.update({'exp': expire})
    encoded = jwt.encode(to_encode, secret, algorithm='HS256')
    return encoded
