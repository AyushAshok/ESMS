from fastapi import FastAPI,HTTPException,Depends, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic  import BaseModel
from ESMS.db.base import Base
from ESMS.db.models.employees import Employees
from ESMS.db.models.teams import Teams
from ESMS.db.models.skills import Skills
from ESMS.db.models.skillexpectations import SkillExpectations
from ESMS.db.models.skillratings import SkillRatings
from ESMS.db.models.users import Users
from ESMS.db.session import SessionLocal,engine
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated,List

from ESMS.services.auth_service import create_user, authenticate_user, get_user_by_email
from ESMS.utils.security import create_access_token, decode_access_token
from ESMS.schemas.users import UserCreate, UserOut, Token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

app=FastAPI()
models=[Employees,Teams,Skills,SkillExpectations,SkillRatings,Users]

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    async with SessionLocal() as session:
        yield session

db_dependency=Annotated[AsyncSession,Depends(get_db)]


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    try:
        payload = decode_access_token(token)
        user_id = int(payload.get("sub"))
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    result = await db.execute(Users.__table__.select().where(Users.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


@app.post("/auth/register", response_model=UserOut)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    existing = await get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = await create_user(db, email=user_in.email, password=user_in.password, employee_id=user_in.employee_id, is_manager=user_in.is_manager)
    return user


@app.post("/auth/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    token = create_access_token(subject=str(user.id), data={"is_manager": user.is_manager, "employee_id": user.employee_id})
    return {"access_token": token, "token_type": "bearer"}


@app.get('/employees/{employee_id}', response_model=dict)
async def read_employee(employee_id: int, current_user = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    # permission: owner or manager of that employee
    result = await db.execute(Employees.__table__.select().where(Employees.id == employee_id))
    employee = result.scalars().first()
    if not employee:
        raise HTTPException(status_code=404, detail='Employee not found')
    # owner
    if current_user.employee_id == employee.id:
        return {"id": employee.id, "name": employee.name, "email": employee.email, "team_id": employee.team_id, "manager_id": employee.manager_id, "designation_level": employee.designation_level}
    # manager: check if employee.manager_id matches current_user.employee_id
    if current_user.is_manager and employee.manager_id == current_user.employee_id:
        return {"id": employee.id, "name": employee.name, "email": employee.email, "team_id": employee.team_id, "manager_id": employee.manager_id, "designation_level": employee.designation_level}
    raise HTTPException(status_code=403, detail='Not authorized')


@app.put('/employees/{employee_id}', response_model=dict)
async def update_employee(employee_id: int, payload: dict, current_user = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(Employees.__table__.select().where(Employees.id == employee_id))
    employee = result.scalars().first()
    if not employee:
        raise HTTPException(status_code=404, detail='Employee not found')
    if not (current_user.employee_id == employee.id or (current_user.is_manager and employee.manager_id == current_user.employee_id)):
        raise HTTPException(status_code=403, detail='Not authorized')
    # apply updates (only allow certain fields)
    allowed = {'name', 'email', 'team_id', 'manager_id', 'designation_level'}
    for k, v in payload.items():
        if k in allowed:
            setattr(employee, k, v)
    db.add(employee)
    await db.commit()
    await db.refresh(employee)
    return {"id": employee.id, "name": employee.name, "email": employee.email, "team_id": employee.team_id, "manager_id": employee.manager_id, "designation_level": employee.designation_level}