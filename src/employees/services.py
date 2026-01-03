from uuid import uuid4

from src.employees.models import Employee
from src.employees.repo import EmployeeRepository
from src.employees.schemas import EmployeeCreate, EmployeeUpdate

# from src.employees.exceptions import EmployeeAlreadyExistsError
from src.users.services import UserService

repo = EmployeeRepository()
user_service = UserService()


class EmployeeService:
    async def create_employee(self, db, data: EmployeeCreate):
        # Create user
        user = await user_service.create_user(db, data.user)

        # existing = await repo.get_by_user_id(db, user.id)
        # if existing:
        #     raise EmployeeAlreadyExistsError()

        employee = Employee(
            id=uuid4(),
            user_id=user.id,
            job_title=data.job_title,
            department=data.department,
            address=data.address,
            date_of_joining=data.date_of_joining,
            profile_picture_url=data.profile_picture_url,
            check_in_time=data.check_in_time,
            check_out_time=data.check_out_time,
        )

        return await repo.create(db, employee)

    async def get_employee_by_id(self, db, employee_id):
        return await repo.get_by_id(db, employee_id)

    async def update_profile(self, db, employee: Employee, data: EmployeeUpdate):
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(employee, field, value)

        await db.commit()
        await db.refresh(employee)
        return employee
