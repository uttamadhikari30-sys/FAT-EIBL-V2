from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import SessionLocal
from ..security import create_access_token

router = APIRouter(prefix='/auth', tags=['auth'])

@router.post('/signup', response_model=schemas.UserOut)
def signup(user: schemas.UserCreate):
    db = SessionLocal()
    try:
        return crud.create_user(db, user)
    finally:
        db.close()

@router.post('/token', response_model=schemas.Token)
def login_for_token(form_data: schemas.Login):
    db = SessionLocal()
    try:
        user = crud.authenticate_user(db, form_data.username, form_data.password)
        if not user:
            raise HTTPException(status_code=400, detail='Incorrect username or password')
        token = create_access_token({'sub': user.username}, expires_delta=60)
        return {'access_token': token, 'token_type': 'bearer'}
    finally:
        db.close()
