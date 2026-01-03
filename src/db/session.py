from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")

engine = create_async_engine(
    DATABASE_URL,
    echo=False,  # True only in local dev
    pool_pre_ping=True,  # Detect dead connections
)

async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
