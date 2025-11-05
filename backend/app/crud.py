from sqlalchemy.orm import Session
from . import models, schemas
from .security import hash_password, verify_password

def create_user(db: Session, user: schemas.UserCreate):
    hashed = hash_password(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username==username).first()

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def create_audit_request(db: Session, req: schemas.AuditRequestCreate, filename: str | None = None):
    db_req = models.AuditRequest(
        title=req.title,
        description=req.description,
        owner=req.owner,
        due_date=req.due_date,
        attachment=filename,
    )
    db.add(db_req)
    db.commit()
    db.refresh(db_req)
    return db_req

def list_audit_requests(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.AuditRequest).offset(skip).limit(limit).all()
