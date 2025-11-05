from pydantic import BaseModel
from typing import Optional, List, Any, Dict

class UserCreate(BaseModel):
    username: str
    password: str
    role: Optional[str] = 'finance'

class UserOut(BaseModel):
    id: int
    username: str
    role: str
    active: bool
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class Login(BaseModel):
    username: str
    password: str

class AuditRequestCreate(BaseModel):
    title: str
    description: Optional[str] = None
    owner: Optional[str] = None
    due_date: Optional[str] = None

class AuditRequestOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    owner: Optional[str]
    status: str
    due_date: Optional[str]
    attachment: Optional[str]
    class Config:
        orm_mode = True

class ComplianceCreate(BaseModel):
    company_id: int
    name: str
    regulation: Optional[str]
    filing_frequency: Optional[str]
    last_filed_on: Optional[str]
    filing_status: Optional[str]
    due_date: Optional[str]
    iridai_license_no: Optional[str]
    solvency_ratio: Optional[str]

class ComplianceOut(BaseModel):
    id: int
    name: str
    filing_status: Optional[str]
    due_date: Optional[str]
    class Config:
        orm_mode = True
