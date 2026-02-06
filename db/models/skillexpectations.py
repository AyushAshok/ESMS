from sqlalchemy import Boolean,Column, Enum,ForeignKey,Integer,String
#from sqlalchemy.sql import func
from ESMS.db.base import Base
# from datetime import datetime

from ESMS.enums.ratings import Ratings
from ESMS.enums.employee_designation import Designation

class SkillExpectation(Base):
    __tablename__="skillexpectations"

    id=Column(Integer,primary_key=True,index=True)
    description=Column(String)
    skill_id=Column(Integer,ForeignKey("skills.id",ondelete="CASCADE"),nullable=False)
    team_id=Column(Integer,ForeignKey("teams.id",ondelete="CASCADE"),nullable=False)
    current_level=Column(Enum(Designation),index=True,nullable=False)
    expected_rating=Column(Enum(Ratings),index=True,nullable=False)
    