from collections.abc import AsyncGenerator, AsyncIterable

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    AsyncEngine,
)

from access_service.infrastructure.persistence.config import DBConfig


async def get_async_engine(settings: DBConfig) -> AsyncGenerator[AsyncEngine, None]:
    engine = create_async_engine(
        url=settings.get_connection_url()
    )

    yield engine

    await engine.dispose()


async def get_async_sessionmaker(
    async_engine: AsyncEngine
) -> async_sessionmaker[AsyncSession]:
    session_factory = async_sessionmaker(
        async_engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )

    return session_factory

async def get_async_session(
    session_factory: async_sessionmaker[AsyncSession],
) -> AsyncIterable[AsyncSession]:
    async with session_factory() as session:
        yield session

