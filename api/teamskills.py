from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ESMS.core.dependencies import get_current_user, get_db
from ESMS.schemas.teamskills import TeamSkill, TeamSkillCreate, TeamSkillUpdate
from ESMS.services.teamskill_service import create_team_skill, get_team_skill_by_id, update_team_skill, delete_team_skill

router=APIRouter(prefix="/team-skills",tags=["TeamSkills"])

@router.post("/", response_model=TeamSkill,status_code=status.HTTP_201_CREATED,summary="Create a new team skill expectation")
async def create_team_skill_endpoint(team_skill: TeamSkillCreate, db: AsyncSession = Depends(get_db),current_user = Depends(get_current_user)):
    if not current_user.is_manager:
        raise HTTPException(status_code=403, detail="Managers only")
    return await create_team_skill(db=db, team_id=team_skill.team_id, skill_id=team_skill.skill_id, is_active=team_skill.is_active)

@router.get("/{team_skill_id}", response_model=TeamSkill,summary="Get team skill expectation details by ID")
async def get_team_skill_endpoint(team_skill_id: int, db: AsyncSession = Depends(get_db)):
    team_skill = await get_team_skill_by_id(db, team_skill_id)
    if not team_skill:
        raise HTTPException(status_code=404, detail="Team skill expectation not found")
    return team_skill

@router.patch("/{team_skill_id}", response_model=TeamSkill,summary="Update team skill expectation details by ID")
async def update_team_skill_endpoint(team_skill_id: int, team_skill_update: TeamSkillUpdate, db: AsyncSession = Depends(get_db),current_user = Depends(get_current_user)):
    if not current_user.is_manager:
        raise HTTPException(status_code=403, detail="Managers only")
    updated_team_skill = await update_team_skill(db, team_skill_id, **team_skill_update.dict(exclude_unset=True))
    if not updated_team_skill:
        raise HTTPException(status_code=404, detail="Team skill expectation not found")
    return updated_team_skill

@router.delete("/{team_skill_id}", status_code=status.HTTP_204_NO_CONTENT,summary="Delete a team skill expectation by ID")
async def delete_team_skill_endpoint(team_skill_id: int, db: AsyncSession = Depends(get_db),current_user = Depends(get_current_user)):
    if not current_user.is_manager:
        raise HTTPException(status_code=403, detail="Managers only")
    success = await delete_team_skill(db, team_skill_id)
    if not success:
        raise HTTPException(status_code=404, detail="Team skill expectation not found")
    return None

