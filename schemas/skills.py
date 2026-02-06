from pydantic import BaseModel,Field
from typing import Optional
from ESMS.enums.skill_category import SkillCategory

class SkillBase(BaseModel):
    name: str
    category: SkillCategory
    description: Optional[str] = Field(default=None, min_length=1)
    is_organizationwide: bool

class SkillCreate(SkillBase):
    pass

class SkillUpdate(SkillBase):
    name: Optional[str] = Field(default=None, min_length=1)
    category: Optional[SkillCategory] = None
    description: Optional[str] = Field(default=None, min_length=1)
    is_organizationwide: Optional[bool] = None

class Skill(SkillBase):
    id: int

    class Config:
        orm_mode = True