from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from ESMS.core.dependencies import get_db
from ESMS.services.auth_service import create_user, authenticate_user, get_user_by_email
from ESMS.schemas.users import UserCreate, UserOut, Token
from ESMS.core.security import create_access_token, decode_access_token



router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserOut)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    existing = await get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = await create_user(db, email=user_in.email, password=user_in.password, employee_id=user_in.employee_id, is_manager=user_in.is_manager)
    return user


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    token = create_access_token(subject=str(user.id), data={"is_manager": user.is_manager, "employee_id": user.employee_id})
    return {"access_token": token, "token_type": "bearer"}