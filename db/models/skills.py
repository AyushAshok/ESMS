from sqlalchemy import Boolean,Column,ForeignKey,Integer,String,Enum
from sqlalchemy.sql import func
from ESMS.db.base import Base
from datetime import datetime

from ESMS.enums.skill_category import SkillCategory

class Skills(Base):
    __tablename__='skills'

    id=Column(Integer,primary_key=True,index=True,unique=True)
    name=Column(String,unique=True,index=True)
    category=Column(Enum(SkillCategory),index=True,nullable=False)
    description=Column(String)
    is_organizationwide=Column(Boolean)
    date_created=Column(datetime,server_default=func.now())
