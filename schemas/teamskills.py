from pydantic import BaseModel,Field
from typing import Optional

class TeamSkillBase(BaseModel):
    team_id: int
    skill_id: int
    is_active: Optional[bool] = True

class TeamSkillCreate(TeamSkillBase):
    pass

class TeamSkillUpdate(TeamSkillBase):
    team_id: Optional[int] = None
    skill_id: Optional[int] = None
    is_active: Optional[bool] = None

class TeamSkill(TeamSkillBase):
    id : int

    class Config:
        orm_mode=True