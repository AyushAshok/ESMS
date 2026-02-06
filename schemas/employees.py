from pydantic import BaseModel,Field
from typing import Optional

from ESMS.enums.employee_designation import Designation

class EmployeeBase(BaseModel):
    name: str
    email: str
    team_id: int
    manager_id: int
    designation_level: Designation

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(EmployeeBase):
    name: Optional[str] = Field(default=None, min_length=1)
    email: Optional[str] = Field(default=None, min_length=1)
    team_id: Optional[int] = None
    manager_id: Optional[int] = None
    designation_level: Optional[Designation] = None

class Employee(EmployeeBase):
    id: int

    class Config:
        orm_mode = True