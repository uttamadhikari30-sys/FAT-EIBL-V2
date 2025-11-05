from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import os
from .database import SessionLocal
from . import models

security = HTTPBearer()

def get_current_username_from_token(token: str):
    secret = os.getenv('SECRET_KEY', 'dev-secret')
    try:
        payload = jwt.decode(token, secret, algorithms=['HS256'])
        return payload.get('sub')
    except JWTError:
        return None

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    username = get_current_username_from_token(token)
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    db = SessionLocal()
    user = db.query(models.User).filter(models.User.username == username).first()
    db.close()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

def require_roles(*roles):
    def _require(user = Depends(get_current_user)):
        user_roles = [r.name for r in getattr(user, 'roles', [])]
        for r in roles:
            if r in user_roles:
                return user
        raise HTTPException(status_code=403, detail="Insufficient role")
    return _require
