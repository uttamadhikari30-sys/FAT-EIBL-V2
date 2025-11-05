from fastapi import APIRouter
from ..database import SessionLocal, engine, Base
from .. import models
from ..security import hash_password

router = APIRouter(prefix='/seed', tags=['seed'])

@router.post('/')
def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    admin_email = 'uttam.singh@edmeinsurance.com'
    admin_password = '123'
    try:
        if not db.query(models.User).filter(models.User.username==admin_email).first():
            user = models.User(username=admin_email, hashed_password=hash_password(admin_password), role='admin')
            db.add(user)
        for role_name in ['admin','audit_manager','auditor','finance','viewer']:
            if not db.query(models.Role).filter(models.Role.name==role_name).first():
                db.add(models.Role(name=role_name, description=role_name + ' role'))
        if not db.query(models.Company).filter(models.Company.name=='Edme Insurance Brokers Limited').first():
            c = models.Company(name='Edme Insurance Brokers Limited')
            db.add(c); db.flush()
            comp = models.Compliance(company_id=c.id, name='Annual IRDAI Filing', due_date='2025-12-31', regulation='IRDAI Act', filing_frequency='Annual', filing_status='Pending')
            db.add(comp)
        db.commit()
        return {'status':'seeded'}
    finally:
        db.close()
