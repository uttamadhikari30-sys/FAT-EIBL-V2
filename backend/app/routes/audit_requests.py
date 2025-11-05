from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from ..database import SessionLocal
from .. import crud, schemas
from ..auth_utils import get_current_user
from ..audit import record_audit
import os

router = APIRouter(prefix='/audit', tags=['audit'])

@router.post('/', response_model=schemas.AuditRequestOut)
def create_request(req: schemas.AuditRequestCreate, attachment: UploadFile | None = File(None), user = Depends(get_current_user)):
    db = SessionLocal()
    try:
        filename = None
        if attachment:
            UPLOAD_DIR = os.getenv('UPLOAD_DIR', '/app/uploads')
            os.makedirs(UPLOAD_DIR, exist_ok=True)
            filename = f"{int(__import__('time').time())}_{attachment.filename}"
            path = os.path.join(UPLOAD_DIR, filename)
            with open(path, 'wb') as f:
                f.write(attachment.file.read())
        db_req = crud.create_audit_request(db, req, filename)
        record_audit(actor=getattr(user,'username','unknown'), action='CREATE', resource=f'AuditRequest:{db_req.id}', summary=db_req.title, payload={'id': db_req.id})
        return db_req
    finally:
        db.close()

@router.get('/', response_model=list[schemas.AuditRequestOut])
def list_requests(user = Depends(get_current_user)):
    db = SessionLocal()
    try:
        return crud.list_audit_requests(db)
    finally:
        db.close()
