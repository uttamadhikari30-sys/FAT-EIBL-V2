from fastapi import APIRouter, Depends
from ..database import SessionLocal
from .. import models
from ..auth_utils import require_roles

router = APIRouter(prefix='/roles', tags=['roles'])

@router.get('/')
def list_roles(user = Depends(require_roles('admin'))):
    db = SessionLocal()
    try:
        return db.query(models.Role).all()
    finally:
        db.close()
