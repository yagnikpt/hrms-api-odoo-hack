from uuid import uuid4

from src.employees.models import Employee
from src.employees.repo import EmployeeRepository
from src.employees.schemas import EmployeeCreate, EmployeeUpdate
from src.employees.exceptions import EmployeeAlreadyExistsError

repo = EmployeeRepository()


class EmployeeService:
    async def create_employee(self, db, data: EmployeeCreate):
        existing = await repo.get_by_user_id(db, data.user_id)
        if existing:
            raise EmployeeAlreadyExistsError()

        employee = Employee(
            id=uuid4(),
            user_id=data.user_id,
            employee_code=data.employee_code,
            full_name=data.full_name,
            job_title=data.job_title,
            department=data.department,
            phone=data.phone,
            address=data.address,
            date_of_joining=data.date_of_joining,
        )

        return await repo.create(db, employee)

    async def update_profile(self, db, employee: Employee, data: EmployeeUpdate):
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(employee, field, value)

        await db.commit()
        await db.refresh(employee)
        return employee
