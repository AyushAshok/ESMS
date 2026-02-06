from sqlalchemy import Boolean,Column,ForeignKey,Integer,String,Enum,DateTime
from sqlalchemy.sql import func
from ESMS.db.base import Base
from datetime import datetime

from ESMS.enums.ratings import Ratings
#from ESMS.enums.employee_designation import Designation

class SkillRatings(Base):
    __tablename__="skillratings"

    id=Column(Integer,primary_key=True,index=True)
    emp_id=Column(Integer,ForeignKey("employees.id",ondelete="CASCADE"),nullable=False,index=True)
    skill_id=Column(Integer,ForeignKey("skills.id",ondelete="CASCADE"),nullable=False,index=True)
    last_rated_by=Column(Integer,ForeignKey("employees.id",ondelete="CASCADE"),nullable=False,index=True)
    manager_rating=Column(Enum(Ratings),nullable=False)
    manager_rated_date=Column(DateTime,server_default=func.now())
    self_rating=Column(Enum(Ratings),nullable=False)
    self_rated_date=Column(DateTime,server_default=func.now())
    comments=Column(String)
