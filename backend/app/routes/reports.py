from fastapi import APIRouter, Depends, Response
from ..database import SessionLocal
from .. import models
from ..auth_utils import get_current_user, require_roles
from sqlalchemy import func
import csv, io
from ..audit import record_audit

router = APIRouter(prefix='/reports', tags=['reports'])

@router.get('/compliance-status')
def compliance_status(format: str = 'json', user = Depends(get_current_user)):
    db = SessionLocal()
    try:
        q = db.query(models.Compliance.filing_status, func.count(models.Compliance.id)).group_by(models.Compliance.filing_status).all()
        data = {status: count for status, count in q}
        if format == 'csv':
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(['filing_status','count'])
            for k, v in data.items():
                writer.writerow([k, v])
            return Response(content=output.getvalue(), media_type='text/csv')
        return data
    finally:
        db.close()

def generate_weekly_report():
    db = SessionLocal()
    try:
        total = db.query(models.AuditRequest).count()
        open_count = db.query(models.AuditRequest).filter(models.AuditRequest.status=='Open').count()
        overdue = db.query(models.AuditRequest).filter(models.AuditRequest.status=='Open').filter(models.AuditRequest.due_date < func.now()).count()
        summary = {'total': total, 'open': open_count, 'overdue': overdue}
        record_audit(actor='system', action='WEEKLY_REPORT', resource='weekly_report', summary=str(summary))
        return summary
    finally:
        db.close()

def send_due_reminders():
    db = SessionLocal()
    try:
        record_audit(actor='system', action='REMINDER', resource='reminder', summary='daily reminders executed')
        return {'status':'ok'}
    finally:
        db.close()
