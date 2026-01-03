from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.users.models import User


class UserRepository:
    async def get_all_users_by_company(
        self, db: AsyncSession, company_name: str
    ) -> list[User]:
        result = await db.execute(select(User).where(User.company == company_name))
        return list(result.scalars().all())

    async def get_by_id(self, db: AsyncSession, user_id) -> User | None:
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def create(self, db: AsyncSession, user: User) -> User:
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
