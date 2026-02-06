from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ESMS.core.dependencies import get_current_user, get_db

from ESMS.schemas.teams import Team, TeamCreate, TeamUpdate
from ESMS.services.team_service import create_team, get_team_by_id, update_team, delete_team
from ESMS.services.employee_services import get_all_employees
from ESMS.services.teamskill_service import get_team_skill_by_id, get_team_skill_by_id
from ESMS.services.teamskill_service import get_team_skill_by_id
from ESMS.db.models.teamskills import TeamSkills
from sqlalchemy import select
from typing import List
from ESMS.schemas.employees import Employee
from ESMS.schemas.teamskills import TeamSkill

router=APIRouter(prefix="/teams",tags=["Teams"])

@router.post("/", response_model=Team,status_code=status.HTTP_201_CREATED,summary="Create a new team")
async def create_team_endpoint(team: TeamCreate, db: AsyncSession = Depends(get_db),current_user = Depends(get_current_user)):
    if not current_user.is_manager:
        raise HTTPException(status_code=403, detail="Managers only")
    return await create_team(db=db, name=team.name)

@router.get("/{team_id}", response_model=Team,summary="Get team details by ID")
async def get_team_endpoint(team_id: int, db: AsyncSession = Depends(get_db)):
    team = await get_team_by_id(db, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team

@router.patch("/{team_id}", response_model=Team,summary="Update team details by ID")
async def update_team_endpoint(team_id: int, team_update: TeamUpdate, db: AsyncSession = Depends(get_db),current_user = Depends(get_current_user)):
    if not current_user.is_manager:
        raise HTTPException(status_code=403, detail="Managers only")
    updated_team = await update_team(db, team_id, **team_update.dict(exclude_unset=True))
    if not updated_team:
        raise HTTPException(status_code=404, detail="Team not found")
    return updated_team

@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT,summary="Delete a team by ID")
async def delete_team_endpoint(team_id: int, db: AsyncSession = Depends(get_db),current_user = Depends(get_current_user)):
    if not current_user.is_manager:
        raise HTTPException(status_code=403, detail="Managers only")
    success = await delete_team(db, team_id)
    if not success:
        raise HTTPException(status_code=404, detail="Team not found")
    return None


@router.get("/{team_id}/members", response_model=List[Employee], summary="List team members")
async def list_team_members(team_id: int, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    # only manager of this team may view members
    # check manager relationship via employees table
    from ESMS.db.models.employees import Employees
    result = await db.execute(select(Employees).where((Employees.team_id == team_id) & (Employees.manager_id == current_user.employee_id)))
    rows = result.scalars().all()
    if not current_user.is_manager or not rows:
        raise HTTPException(status_code=403, detail='Managers only or not manager of this team')
    # return all members of team
    result_all = await db.execute(select(Employees).where(Employees.team_id == team_id))
    members = result_all.scalars().all()
    return members


@router.get("/{team_id}/skills", response_model=List[TeamSkill], summary="List skills for a team")
async def list_team_skills(team_id: int, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    # manager-only
    if not current_user.is_manager:
        raise HTTPException(status_code=403, detail='Managers only')
    from ESMS.services.teamskill_service import get_team_skill_by_id
    from ESMS.db.models.teamskills import TeamSkills
    result = await db.execute(select(TeamSkills).where(TeamSkills.team_id == team_id))
    rows = result.scalars().all()
    return rows