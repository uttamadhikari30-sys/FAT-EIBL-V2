from .database import SessionLocal
from .models import AuditLog

def record_audit(actor: str, action: str, resource: str = None, summary: str = None, payload: dict = None):
    db = SessionLocal()
    try:
        log = AuditLog(actor=actor, action=action, resource=resource, summary=summary, payload=payload)
        db.add(log)
        db.commit()
    finally:
        db.close()
