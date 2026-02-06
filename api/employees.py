from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
# from ESMS.db.models.employees import Employees

from ESMS.core.dependencies import get_current_user, get_db

from ESMS.schemas.employees import Employee,EmployeeCreate,EmployeeUpdate
from ESMS.services.employee_services import create_employee, get_employee_by_id, update_employee, delete_employee


router=APIRouter(prefix="/employees",tags=["Employees"])

@router.post("/", response_model=Employee,status_code=status.HTTP_201_CREATED,summary="Create a new employee")
async def create_employee_endpoint(employee: EmployeeCreate, db: AsyncSession = Depends(get_db)):
    return await create_employee(db=db, name=employee.name, email=employee.email, team_id=employee.team_id, manager_id=employee.manager_id, designation_level=employee.designation_level)

@router.get("/{employee_id}", response_model=Employee,summary="Get employee details by ID")
async def get_employee_endpoint(employee_id: int, db: AsyncSession = Depends(get_db),current_user = Depends(get_current_user)):
    employee = await get_employee_by_id(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    if (current_user.employee_id == employee.id or (current_user.is_manager and employee.manager_id == current_user.employee_id)):
        return employee
    raise HTTPException(status_code=403, detail="Not authorized")

@router.patch("/{employee_id}", response_model=Employee,summary="Update employee details by ID")
async def update_employee_endpoint(employee_id: int, employee_update: EmployeeUpdate, db: AsyncSession = Depends(get_db),current_user = Depends(get_current_user)):
    employee = await get_employee_by_id(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    if not (current_user.employee_id == employee.id or (current_user.is_manager and employee.manager_id == current_user.employee_id)):
        raise HTTPException(status_code=403, detail='Not authorized')
    updated_employee = await update_employee(db, employee_id, **employee_update.dict(exclude_unset=True))
    if not updated_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return updated_employee

@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT,summary="Delete an employee by ID")
async def delete_employee_endpoint(employee_id: int, db: AsyncSession = Depends(get_db),current_user = Depends(get_current_user)):
    if not current_user.is_manager:
        raise HTTPException(status_code=403, detail="Managers only")
    success = await delete_employee(db, employee_id)
    if not success:
        raise HTTPException(status_code=404, detail="Employee not found")
    return None