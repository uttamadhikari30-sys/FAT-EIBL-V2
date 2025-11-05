from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, Table, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default='finance')
    active = Column(Boolean, default=True)

class Company(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Compliance(Base):
    __tablename__ = 'compliances'
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey('companies.id'))
    name = Column(String, nullable=False)
    regulation = Column(String, nullable=True)
    filing_frequency = Column(String, nullable=True)
    last_filed_on = Column(String, nullable=True)
    filing_status = Column(String, default='Pending')
    due_date = Column(String, nullable=True)
    iridai_license_no = Column(String, nullable=True)
    solvency_ratio = Column(String, nullable=True)
    company = relationship('Company')

class AuditRequest(Base):
    __tablename__ = 'audit_requests'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    owner = Column(String)
    status = Column(String, default='Open')
    due_date = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    attachment = Column(String, nullable=True)

user_roles = Table(
    'user_roles', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE')),
    Column('role_id', Integer, ForeignKey('roles.id', ondelete='CASCADE'))
)

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    permissions = Column(String, nullable=True)
    users = relationship("User", secondary=user_roles, backref='roles')

class AuditLog(Base):
    __tablename__ = 'audit_logs'
    id = Column(Integer, primary_key=True, index=True)
    actor = Column(String, nullable=True)
    action = Column(String, nullable=False)
    resource = Column(String, nullable=True)
    summary = Column(String, nullable=True)
    payload = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
