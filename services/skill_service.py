from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from ESMS.enums.skill_category import SkillCategory
from ESMS.db.models.skills import Skills

async def create_skill(db:AsyncSession, name:str, category:SkillCategory=SkillCategory.OTHER, description:str | None=None, is_organizationwide:bool=False):
    try:
        new_skill = Skills(name=name, category=category, description=description, is_organizationwide=is_organizationwide)
        db.add(new_skill)
        await db.commit()
        await db.refresh(new_skill)
        return new_skill
    except SQLAlchemyError as e:
        await db.rollback()
        raise e

async def get_skill_by_id(db:AsyncSession, skill_id:int):
    try:
        result = await db.execute(select(Skills).where(Skills.id == skill_id))
        return result.scalars().first()
    except SQLAlchemyError as e:
        raise e
    
async def update_skill(db:AsyncSession,skill_id:int,name:str | None=None,category:SkillCategory|None=None,description:str | None=None,is_organizationwide:bool | None=None):
    skill = await get_skill_by_id(db, skill_id)
    if not skill:
        return None
    if name is not None:
        skill.name = name
    if category is not None:
        skill.category = category
    if description is not None:
        skill.description = description
    if is_organizationwide is not None:
        skill.is_organizationwide = is_organizationwide

    try:
        await db.commit()
        await db.refresh(skill)
        return skill
    except SQLAlchemyError as e:
        await db.rollback()
        raise e
    
async def delete_skill(db:AsyncSession,skill_id:int):
    skill=await get_skill_by_id(db,skill_id)

    try:
        if not skill:
            return None
        await db.delete(skill)
        await db.commit()
        return True
    except SQLAlchemyError as e:
        await db.rollback()
        raise e