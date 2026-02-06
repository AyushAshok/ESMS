from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ESMS.core.dependencies import get_current_user, get_db
from ESMS.db.models.employees import Employees
from ESMS.schemas.skillratings import SkillRating, SkillRatingCreate, SkillRatingUpdate
from ESMS.services.skillrating_service import create_skill_rating, get_skill_rating_by_id, update_skill_rating, delete_skill_rating

router=APIRouter(prefix="/skill-ratings",tags=["SkillRatings"])

@router.post("/", response_model=SkillRating,status_code=status.HTTP_201_CREATED,summary="Create a new skill rating")
async def create_skill_rating_endpoint(skill_rating: SkillRatingCreate, db: AsyncSession = Depends(get_db),current_user = Depends(get_current_user)):
    if not (current_user.employee_id == skill_rating.emp_id or current_user.is_manager):
        raise HTTPException(status_code=403, detail='Not authorized')
    return await create_skill_rating(db=db, employee_id=skill_rating.emp_id, skill_id=skill_rating.skill_id, last_rated_by=current_user.employee_id, manager_rating=skill_rating.manager_rating, self_rating=skill_rating.self_rating, comments=skill_rating.comments)   

@router.get("/{skill_rating_id}", response_model=SkillRating,summary="Get skill rating details by ID")
async def get_skill_rating_endpoint(skill_rating_id: int, db: AsyncSession = Depends(get_db)):
    skill_rating = await get_skill_rating_by_id(db, skill_rating_id)
    if not skill_rating:
        raise HTTPException(status_code=404, detail="Skill rating not found")
    return skill_rating

@router.patch("/{skill_rating_id}", response_model=SkillRating,summary="Update skill rating details by ID")
async def update_skill_rating_endpoint(skill_rating_id: int, skill_rating_update: SkillRatingUpdate, db: AsyncSession = Depends(get_db),current_user = Depends(get_current_user)):
    skill_rating = await get_skill_rating_by_id(db, skill_rating_id)
    if not skill_rating:
        raise HTTPException(status_code=404, detail="Skill rating not found")
    result = await db.execute(select(Employees).where(Employees.id == skill_rating.emp_id))
    employee = result.scalars().first()
    if not (current_user.employee_id == skill_rating.emp_id or (current_user.is_manager and employee and employee.manager_id == current_user.employee_id)):
        raise HTTPException(status_code=403, detail='Not authorized')
    updated_skill_rating = await update_skill_rating(db, skill_rating_id, **skill_rating_update.dict(exclude_unset=True))
    if not updated_skill_rating:
        raise HTTPException(status_code=404, detail="Skill rating not found")
    return updated_skill_rating

@router.delete("/{skill_rating_id}", status_code=status.HTTP_204_NO_CONTENT,summary="Delete a skill rating by ID")
async def delete_skill_rating_endpoint(skill_rating_id: int, db: AsyncSession = Depends(get_db),current_user = Depends(get_current_user)):
    skill_rating = await get_skill_rating_by_id(db, skill_rating_id)
    if not skill_rating:
        raise HTTPException(status_code=404, detail="Skill rating not found")
    result = await db.execute(select(Employees).where(Employees.id == skill_rating.emp_id))
    employee = result.scalars().first()
    if not (current_user.employee_id == skill_rating.emp_id or (current_user.is_manager and employee and employee.manager_id == current_user.employee_id)):
        raise HTTPException(status_code=403, detail='Not authorized')
    success = await delete_skill_rating(db, skill_rating_id)
    if not success:
        raise HTTPException(status_code=404, detail="Skill rating not found")
    return None