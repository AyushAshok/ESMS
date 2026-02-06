from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ESMS.db.models.skillexpectations import SkillExpectations
from ESMS.enums.ratings import Ratings
from ESMS.enums.employee_designation import Designation

async def create_skill_expectation(db:AsyncSession, description:str, skill_id:int, team_id:int, current_level:Designation = Designation.LEVEL_4, expected_rating:Ratings = Ratings.ZERO):
    try:
        new_expectation = SkillExpectations(description=description, skill_id=skill_id, team_id=team_id, current_level=current_level, expected_rating=expected_rating)
        db.add(new_expectation)
        await db.commit()
        await db.refresh(new_expectation)
        return new_expectation
    except SQLAlchemyError as e:
        await db.rollback()
        raise e
    
async def get_skill_expectation_by_id(db:AsyncSession, expectation_id:int):
    try:
        result = await db.execute(select(SkillExpectations).where(SkillExpectations.id == expectation_id))
        return result.scalars().first()
    except SQLAlchemyError as e:
        raise e
    
async def update_skill_expectation(db:AsyncSession, expectation_id:int, description:str | None=None, skill_id:int | None=None, team_id:int | None=None, current_level:Designation | None=None, expected_rating:Ratings | None=None):
    expectation = await get_skill_expectation_by_id(db, expectation_id)
    if not expectation:
        return None
    if description is not None:
        expectation.description = description
    if skill_id is not None:
        expectation.skill_id = skill_id
    if team_id is not None:
        expectation.team_id = team_id
    if current_level is not None:
        expectation.current_level = current_level
    if expected_rating is not None:
        expectation.expected_rating = expected_rating

    try:
        await db.commit()
        await db.refresh(expectation)
        return expectation
    except SQLAlchemyError as e:
        await db.rollback()
        raise e
    
async def delete_skill_expectation(db:AsyncSession, expectation_id:int):
    expectation = await get_skill_expectation_by_id(db, expectation_id)
    if not expectation:
        return None
    
    try:
        await db.delete(expectation)
        await db.commit()
        return True
    except SQLAlchemyError as e:
        await db.rollback()
        raise e
