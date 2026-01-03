from datetime import date

from src.users.models import User
from src.users.repo import UserRepository
from src.users.schemas import UserCreate
from src.users.utils import get_largest_serial_number_from_ids
from src.core.security import hash_password

repo = UserRepository()


class UserService:
    async def create_user(self, db, data: UserCreate):
        company_users = await repo.get_all_users_by_company(db, data.company)
        company_user_ids = [user.id for user in company_users]
        next_serial_num = get_largest_serial_number_from_ids(company_user_ids) + 1
        serial_str = str(next_serial_num).zfill(4)
        current_year = date.today().year
        company_abbr = ""
        if data.company.__contains__(" "):
            company_abbr = "".join(
                [word[0] for word in data.company.split(" ")]
            ).upper()
        else:
            company_abbr = data.company[:2].upper()

        first_name_two_initial = data.full_name[:2].upper()
        last_name_two_initial = ""
        if data.full_name.__contains__(" "):
            last_name_two_initial = "".join(
                [word[0] for word in data.full_name.split(" ")[1:3]]
            ).upper()
        else:
            last_name_two_initial = data.full_name[-2:].upper()

        new_user_id = f"{company_abbr}{first_name_two_initial}{last_name_two_initial}{current_year}{serial_str}"

        user_existing = await repo.get_by_id(db, new_user_id)
        if user_existing:
            raise Exception("User with generated ID already exists. Try again.")

        password_hash = hash_password(data.password)

        user = User(
            id=new_user_id,
            full_name=data.full_name,
            email=data.email,
            password_hash=password_hash,
            role=data.role,
            company=data.company,
            phone=data.phone,
        )

        return await repo.create(db, user)

    # async def update_profile(self, db, employee: Employee, data: EmployeeUpdate):
    #     for field, value in data.model_dump(exclude_unset=True).items():
    #         setattr(employee, field, value)

    #     await db.commit()
    #     await db.refresh(employee)
    #     return employee
