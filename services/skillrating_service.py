from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ESMS.db.models.skillratings import SkillRatings
from ESMS.enums.ratings import Ratings

async def create_skill_rating(db:AsyncSession,employee_id:int,skill_id:int,last_rated_by:int | None=None,manager_rating:Ratings | None=None,self_rating:Ratings | None=None,comments:str | None=None):
    try:
        new_rating = SkillRatings(emp_id=employee_id, skill_id=skill_id, last_rated_by=last_rated_by, manager_rating=manager_rating, self_rating=self_rating, comments=comments)
        db.add(new_rating)
        await db.commit()
        await db.refresh(new_rating)
        return new_rating
    except SQLAlchemyError as e:
        await db.rollback()
        raise e
    
async def get_skill_rating_by_id(db:AsyncSession, rating_id:int):
    try:
        result = await db.execute(select(SkillRatings).where(SkillRatings.id == rating_id))
        return result.scalars().first()
    except SQLAlchemyError as e:
        raise e
    
async def update_skill_rating(db:AsyncSession, rating_id:int, employee_id:int | None=None, skill_id:int | None=None, last_rated_by:int | None=None, manager_rating:Ratings | None=None, self_rating:Ratings | None=None, comments:str | None=None):
    rating = await get_skill_rating_by_id(db, rating_id)
    if not rating:
        return None
    if employee_id is not None:
        rating.emp_id = employee_id
    if skill_id is not None:
        rating.skill_id = skill_id
    if last_rated_by is not None:
        rating.last_rated_by = last_rated_by
    if manager_rating is not None:
        rating.manager_rating = manager_rating
    if self_rating is not None:
        rating.self_rating = self_rating
    if comments is not None:
        rating.comments = comments

    try:
        await db.commit()
        await db.refresh(rating)
        return rating
    except SQLAlchemyError as e:
        await db.rollback()
        raise e
    
async def delete_skill_rating(db:AsyncSession, rating_id:int):
    rating=await get_skill_rating_by_id(db, rating_id)
    if not rating:
        return None
    try:
        db.delete(rating)
        await db.commit()
        return True
    except SQLAlchemyError as e:
        await db.rollback()
        raise e