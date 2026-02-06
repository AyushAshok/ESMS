from pydantic import BaseModel
from typing import Optional

from ESMS.enums.ratings import Ratings

class SkillRatingsBase(BaseModel):
    emp_id : int
    skill_id : int
    last_rated_by : int
    manager_rating : Ratings
    self_rating : Ratings
    comments : Optional[str] = None

class SkillRatingsCreate(SkillRatingsBase):
    pass

class SkillRatingsUpdate(SkillRatingsBase):
    emp_id : Optional[int] = None
    skill_id : Optional[int] = None
    last_rated_by : Optional[int] = None
    manager_rating : Optional[Ratings] = None
    self_rating : Optional[Ratings] = None
    comments : Optional[str] = None

class SkillRatings(SkillRatingsBase):
    id : int

    class Config:
        orm_mode=True


class SkillAssign(BaseModel):
    skill_id: int
    manager_rating: Ratings | None = None
    self_rating: Ratings | None = None
    comments: str | None = None
