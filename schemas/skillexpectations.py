from pydantic import BaseModel
from typing import Optional

from ESMS.enums.ratings import Ratings
from ESMS.enums.employee_designation import Designation

class SkillExpectationBase(BaseModel):
    description: str
    skill_id : int
    team_id : int
    current_level: Designation
    expected_rating: Ratings

class SkillExpectationCreate(SkillExpectationBase):
    pass

class SkillExpectationUpdate(SkillExpectationBase):
    description: Optional[str] = None
    skill_id : Optional[int] = None
    team_id : Optional[int] = None
    current_level: Optional[Designation] = None
    expected_rating: Optional[Ratings] = None

class SkillExpectation(SkillExpectationBase):
    id : int

    class Config:
        orm_mode=True