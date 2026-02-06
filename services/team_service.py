from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from ESMS.db.models.teams import Teams

async def create_team(db:AsyncSession, name:str):
    try:
        new_team = Teams(name=name)
        db.add(new_team)
        await db.commit()
        await db.refresh(new_team)
        return new_team
    except SQLAlchemyError as e:
        await db.rollback()
        raise e
    
async def get_team_by_id(db:AsyncSession, team_id:int):
    try:
        result = await db.execute(select(Teams).where(Teams.id == team_id))
        return result.scalars().first()
    except SQLAlchemyError as e:
        raise e
    
async def update_team(db:AsyncSession, team_id:int, name:str | None=None):
    team = await get_team_by_id(db, team_id)
    if not team:
        return None
    if name is not None:
        team.name = name

    try:
        await db.commit()
        await db.refresh(team)
        return team
    except SQLAlchemyError as e:
        await db.rollback()
        raise e
    
async def delete_team(db:AsyncSession, team_id:int):
    team=await get_team_by_id(db,team_id)
    if not team:
        return None
    try:
        await db.delete(team)
        await db.commit()
        return True
    except SQLAlchemyError as e:
        await db.rollback()
        raise e