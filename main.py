from fastapi import FastAPI,HTTPException,Depends, status
from ESMS.db.base import Base
from ESMS.db.models.employees import Employees
from ESMS.db.models.teams import Teams
from ESMS.db.models.skills import Skills
from ESMS.db.models.skillexpectations import SkillExpectations
from ESMS.db.models.skillratings import SkillRatings
from ESMS.db.models.users import Users
from ESMS.db.session import SessionLocal,engine
from ESMS.core.dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated,List

from ESMS.api.employees import router as employee_router
from ESMS.api.auth import router as auth_router
from ESMS.api.teams import router as team_router
from ESMS.api.skills import router as skill_router
from ESMS.api.skillexpectations import router as skill_expectation_router
from ESMS.api.skillratings import router as skill_rating_router
from ESMS.api.teamskills import router as team_skill_router



app=FastAPI()
app.include_router(auth_router)
app.include_router(employee_router)
app.include_router(team_router)
app.include_router(skill_router)
app.include_router(skill_expectation_router)
app.include_router(skill_rating_router)
app.include_router(team_skill_router)


models=[Employees,Teams,Skills,SkillExpectations,SkillRatings,Users]

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

db_dependency=Annotated[AsyncSession,Depends(get_db)]





