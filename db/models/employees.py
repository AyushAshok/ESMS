from sqlalchemy import Boolean,Column,ForeignKey,Integer,String, Enum
# from sqlalchemy.sql import func
from ESMS.db.base import Base
from ESMS.enums.employee_designation import Designation

class Employees(Base):
    __tablename__="employees"

    id=Column(Integer,primary_key=True,index=True,unique=True)
    name=Column(String,index=True)
    email=Column(String,index=True,unique=True)
    team_id=Column(Integer,ForeignKey("teams.id"),nullable=False,index=True)
    manager_id=Column(Integer,ForeignKey("employees.id"),nullable=False,index=True)
    designation_level=Column(Enum(Designation),index=True,nullable=False)



