from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ESMS.core.dependencies import get_current_user, get_db

from ESMS.schemas.skills import Skill, SkillCreate, SkillUpdate
from ESMS.services.skill_service import create_skill, get_skill_by_id, update_skill, delete_skill, get_all_skills

router=APIRouter(prefix="/skills",tags=["Skills"])


@router.get("/", response_model=List[Skill], summary="List skills")
async def list_skills(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    if not current_user.is_manager:
        raise HTTPException(status_code=403, detail="Managers only")
    return await get_all_skills(db)

@router.post("/", response_model=Skill,status_code=status.HTTP_201_CREATED,summary="Create a new skill")
async def create_skill_endpoint(skill: SkillCreate, db: AsyncSession = Depends(get_db),current_user = Depends(get_current_user)):
    if not current_user.is_manager:
        raise HTTPException(status_code=403, detail="Managers only")
    return await create_skill(db=db, name=skill.name,category=skill.category, description=skill.description,is_organizationwide=skill.is_organizationwide)

@router.get("/{skill_id}", response_model=Skill,summary="Get skill details by ID")
async def get_skill_endpoint(skill_id: int, db: AsyncSession = Depends(get_db)):
    skill = await get_skill_by_id(db, skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill

@router.patch("/{skill_id}", response_model=Skill,summary="Update skill details by ID")
async def update_skill_endpoint(skill_id: int, skill_update: SkillUpdate, db: AsyncSession = Depends(get_db),current_user = Depends(get_current_user)):
    if not current_user.is_manager:
        raise HTTPException(status_code=403, detail="Managers only")
    updated_skill = await update_skill(db, skill_id, **skill_update.dict(exclude_unset=True))
    if not updated_skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return updated_skill

@router.delete("/{skill_id}", status_code=status.HTTP_204_NO_CONTENT,summary="Delete a skill by ID")
async def delete_skill_endpoint(skill_id: int, db: AsyncSession = Depends(get_db),current_user = Depends(get_current_user)):
    if not current_user.is_manager:
        raise HTTPException(status_code=403, detail="Managers only")
    success = await delete_skill(db, skill_id)
    if not success:
        raise HTTPException(status_code=404, detail="Skill not found")
    return None

