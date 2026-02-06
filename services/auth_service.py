from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from ESMS.db.models.users import Users
from ESMS.utils.security import get_password_hash, verify_password


async def create_user(db: AsyncSession, email: str, password: str, employee_id: int | None = None, is_manager: bool = False):
    try:
        hashed = get_password_hash(password)
        user = Users(email=email, password_hash=hashed, employee_id=employee_id, is_manager=is_manager)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
    except SQLAlchemyError as e:
        await db.rollback()
        raise e


async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(Users).where(Users.email == email))
    return result.scalars().first()


async def authenticate_user(db: AsyncSession, email: str, password: str):
    user = await get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user
