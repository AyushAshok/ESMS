from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select 
from sqlalchemy.exc import SQLAlchemyError

from ESMS.db.models.teamskills import TeamSkills

async def create_team_skill(db:AsyncSession, team_id:int, skill_id:int, is_active:bool=True):
    try:
        new_team_skill = TeamSkills(team_id=team_id, skill_id=skill_id, is_active=is_active)
        db.add(new_team_skill)
        await db.commit()
        await db.refresh(new_team_skill)
        return new_team_skill
    except SQLAlchemyError as e:
        await db.rollback()
        raise e
    
async def get_team_skill_by_id(db:AsyncSession,team_skill_id:int):
    try:
        result = await db.execute(select(TeamSkills).where(TeamSkills.id==team_skill_id))
        return result.scalars().first()
    except SQLAlchemyError as e:
        raise e
    
async def update_team_skill(db:AsyncSession,team_skill_id:int,team_id:int | None=None,skill_id:int | None=None,is_active:bool | None=None):
    team_skill=await get_team_skill_by_id(db,team_skill_id)
    if not team_skill:
        return None
    if team_id is not None:
        team_skill.team_id=team_id
    if skill_id is not None:
        team_skill.skill_id=skill_id
    if is_active is not None:
        team_skill.is_active=is_active

    try:
        await db.commit()
        await db.refresh(team_skill)
        return team_skill
    except SQLAlchemyError as e:
        await db.rollback()
        raise e
    
async def delete_team_skill(db:AsyncSession,team_skill_id:int):
    team_skill=await get_team_skill_by_id(db,team_skill_id)
    if not team_skill:
        return None
    try:
        db.delete(team_skill)
        await db.commit()
        return True
    except SQLAlchemyError as e:
        await db.rollback()
        raise e