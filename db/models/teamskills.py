from sqlalchemy import Boolean,Column,ForeignKey,Integer,String
from sqlalchemy.sql import func
from ESMS.db.base import Base
# from ESMS.enums.employee_designation import Designation
from datetime import datetime


class TeamSkills(Base):
    __tablename__="teamskills"

    id=Column(Integer,primary_key=True,index=True,unique=True)
    team_id=Column(Integer,ForeignKey("teams.id",ondelete="CASCADE"),nullable=False,index=True)
    skill_id=Column(Integer,ForeignKey("skills.id",ondelete="CASCADE"),nullable=False,index=True)
    assigned_date=Column(datetime,server_default=func.now())
    is_active=Column(Boolean)
