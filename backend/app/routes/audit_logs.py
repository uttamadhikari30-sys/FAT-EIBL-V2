from fastapi import APIRouter, Depends
from ..database import SessionLocal
from .. import models
from ..auth_utils import require_roles

router = APIRouter(prefix='/audit/logs', tags=['audit_logs'])

@router.get('/')
def list_logs(user = Depends(require_roles('admin','audit_manager'))):
    db = SessionLocal()
    try:
        return db.query(models.AuditLog).order_by(models.AuditLog.created_at.desc()).limit(200).all()
    finally:
        db.close()
