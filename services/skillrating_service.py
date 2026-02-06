from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ESMS.db.models.skillratings import SkillRatings
from ESMS.enums.ratings import Ratings
from ESMS.db.models.employees import Employees
from ESMS.db.models.skills import Skills
from ESMS.db.models.teamskills import TeamSkills
from ESMS.db.models.skillexpectations import SkillExpectations
from sqlalchemy import select

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


async def get_all_skill_ratings(db:AsyncSession):
    try:
        result = await db.execute(select(SkillRatings))
        return result.scalars().all()
    except SQLAlchemyError as e:
        raise e


async def get_employee_skill_overview(db: AsyncSession, employee_id: int):
    """Return a list of skills relevant to the employee's team, with ratings if assigned.
    Each item: { skill_id, skill_name, assigned(bool), manager_rating, self_rating, expected_rating }
    """
    try:      
        res = await db.execute(select(Employees).where(Employees.id == employee_id))
        employee = res.scalars().first()
        if not employee:
            return None

        team_id = employee.team_id

        # skills referenced by team via TeamSkills or SkillExpectations
        result_ts = await db.execute(select(TeamSkills).where(TeamSkills.team_id == team_id))
        team_skill_rows = result_ts.scalars().all()
        team_skill_ids = {r.skill_id for r in team_skill_rows}

        result_se = await db.execute(select(SkillExpectations).where(SkillExpectations.team_id == team_id))
        expectation_rows = result_se.scalars().all()
        expectation_map = {r.skill_id: r.expected_rating for r in expectation_rows}
        expectation_ids = {r.skill_id for r in expectation_rows}

        all_skill_ids = set(team_skill_ids) | set(expectation_ids)

        # load skill records
        if not all_skill_ids:
            return []
        result_sk = await db.execute(select(Skills).where(Skills.id.in_(all_skill_ids)))
        skills = {s.id: s for s in result_sk.scalars().all()}

        # load existing ratings for employee
        result_r = await db.execute(select(SkillRatings).where(SkillRatings.emp_id == employee_id))
        ratings = {r.skill_id: r for r in result_r.scalars().all()}

        overview = []
        for sid in sorted(all_skill_ids):
            sk = skills.get(sid)
            rating = ratings.get(sid)
            overview.append({
                'skill_id': sid,
                'skill_name': getattr(sk, 'name', None),
                'assigned': rating is not None,
                'manager_rating': rating.manager_rating.name if (rating and rating.manager_rating is not None) else None,
                'self_rating': rating.self_rating.name if (rating and rating.self_rating is not None) else None,
                'rating_id': rating.id if rating else None,
                'expected_rating': expectation_map.get(sid, 0),
            })

        return overview
    except SQLAlchemyError as e:
        raise e