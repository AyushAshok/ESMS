from fastapi import FastAPI,HTTPException,Depends
from pydantic  import BaseModel
from ESMS.db.base import Base
from ESMS.db.models.employees import Employees
from ESMS.db.models.teams import Teams
from ESMS.db.models.skills import Skills
from ESMS.db.models.skillexpectations import SkillExpectations
from ESMS.db.models.skillratings import SkillRatings
from ESMS.db.session import SessionLocal,engine
from sqlalchemy.orm import Session
from typing import Annotated,List


app=FastAPI()
models=[Employees,Teams,Skills,SkillExpectations,SkillRatings]
Base.metadata.create_all(bind=engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]