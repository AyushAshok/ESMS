from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from ESMS.enums.employee_designation import Designation

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    employee_id: Optional[int] = None
    is_manager: Optional[bool] = False

class UserOut(BaseModel):
    id: int
    email: EmailStr
    employee_id: Optional[int] = None
    is_manager: bool
    is_active: bool

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
