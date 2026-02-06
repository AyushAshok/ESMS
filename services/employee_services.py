from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from ESMS.db.models.employees import Employees
from ESMS.enums.employee_designation import Designation


async def create_employee(db:AsyncSession, name:str, email:str, team_id:int, manager_id:int, designation_level:Designation = Designation.LEVEL_4):
    try:
        new_employee = Employees(name=name, email=email, team_id=team_id, manager_id=manager_id, designation_level=designation_level)
        db.add(new_employee)
        await db.commit()
        await db.refresh(new_employee)
        return new_employee
    except SQLAlchemyError as e:
        await db.rollback()
        raise e

async def get_employee_by_id(db:AsyncSession, employee_id:int):
    try:
        result = await db.execute(select(Employees).where(Employees.id == employee_id))
        return result.scalars().first()
    except SQLAlchemyError as e:
        raise e

async def update_employee(db:AsyncSession, employee_id:int, name:str | None=None, email:str | None=None, team_id:int | None=None, manager_id:int | None=None, designation_level:Designation | None=None):
    employee = await get_employee_by_id(db, employee_id)
    if not employee:
        return None
    if name is not None:
        employee.name = name
    if email is not None:
        employee.email = email
    if team_id is not None:
        employee.team_id = team_id
    if manager_id is not None:
        employee.manager_id = manager_id
    if designation_level is not None:
        employee.designation_level = designation_level

    try:
        await db.commit()
        await db.refresh(employee)
        return employee
    except SQLAlchemyError as e:
        await db.rollback()
        raise e

async def delete_employee(db:AsyncSession, employee_id:int):
    employee = await get_employee_by_id(db, employee_id)
    if not employee:
        return None
    
    try:
        await db.delete(employee)
        await db.commit()
        return True
    except SQLAlchemyError as e:
        await db.rollback()
        raise e