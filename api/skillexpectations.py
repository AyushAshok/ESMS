from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ESMS.core.dependencies import get_current_user, get_db
from ESMS.schemas.skillexpectations import SkillExpectation, SkillExpectationCreate, SkillExpectationUpdate
from ESMS.services.skillexpectation_service import create_skill_expectation, get_skill_expectation_by_id, update_skill_expectation, delete_skill_expectation

router=APIRouter(prefix="/skill-expectations",tags=["SkillExpectations"])

@router.post("/", response_model=SkillExpectation,status_code=status.HTTP_201_CREATED,summary="Create a new skill expectation")
async def create_skill_expectation_endpoint(skill_expectation: SkillExpectationCreate, db: AsyncSession = Depends(get_db),current_user = Depends(get_current_user)):
    if not current_user.is_manager:
        raise HTTPException(status_code=403, detail="Managers only")
    return await create_skill_expectation(db=db, description=skill_expectation.description, team_id=skill_expectation.team_id, skill_id=skill_expectation.skill_id, current_level=skill_expectation.current_level, expected_rating=skill_expectation.expected_rating)

@router.get("/{skill_expectation_id}", response_model=SkillExpectation,summary="Get skill expectation details by ID")
async def get_skill_expectation_endpoint(skill_expectation_id: int, db: AsyncSession = Depends(get_db)):
    skill_expectation = await get_skill_expectation_by_id(db, skill_expectation_id)
    if not skill_expectation:
        raise HTTPException(status_code=404, detail="Skill expectation not found")
    return skill_expectation

@router.patch("/{skill_expectation_id}", response_model=SkillExpectation,summary="Update skill expectation details by ID")
async def update_skill_expectation_endpoint(skill_expectation_id: int, skill_expectation_update: SkillExpectationUpdate, db: AsyncSession = Depends(get_db),current_user = Depends(get_current_user)):
    if not current_user.is_manager:
        raise HTTPException(status_code=403, detail="Managers only")
    updated_skill_expectation = await update_skill_expectation(db, skill_expectation_id, **skill_expectation_update.dict(exclude_unset=True))
    if not updated_skill_expectation:
        raise HTTPException(status_code=404, detail="Skill expectation not found")
    return updated_skill_expectation

@router.delete("/{skill_expectation_id}", status_code=status.HTTP_204_NO_CONTENT,summary="Delete a skill expectation by ID")
async def delete_skill_expectation_endpoint(skill_expectation_id: int, db: AsyncSession = Depends(get_db),current_user = Depends(get_current_user)):
    if not current_user.is_manager:
        raise HTTPException(status_code=403, detail="Managers only")
    success = await delete_skill_expectation(db, skill_expectation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Skill expectation not found")
    return None

