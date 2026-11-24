from collections import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
import config
from models import Base


class DbHelper:
    def __init__(self, database_url: str, echo: bool = False):
        self.engine = create_async_engine(
            url=database_url,
            echo=echo,
        )
        self.session = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            expire_on_commit=False,
        )

    async def get_db(self) -> AsyncGenerator[AsyncSession]:
        async with self.session() as db:
            yield db

    async def create_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


db_helper = DbHelper(
    database_url=config.settings.database_async_url,
    echo=True,
)
