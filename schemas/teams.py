from pydantic import BaseModel,Field
from typing import Optional

class TeamBase(BaseModel):
    name: str

class TeamCreate(TeamBase):
    pass

class TeamUpdate(TeamBase):
    name: Optional[str] = Field(default=None, min_length=1)

class Team(TeamBase):
    id: int

    class Config:
        orm_mode = True




