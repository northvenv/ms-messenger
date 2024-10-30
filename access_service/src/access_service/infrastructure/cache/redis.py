from typing import AsyncGenerator
from redis.asyncio import Redis, ConnectionPool

from access_service.infrastructure.cache.config import RedisConfig


def get_redis_pool(settings: RedisConfig) -> ConnectionPool:
    pool = ConnectionPool.from_url(settings.get_connection_url())
    return pool


async def get_redis_session(pool: ConnectionPool) -> AsyncGenerator[Redis, None]:
    session = Redis.from_pool(pool)

    yield session

    await session.aclose()




