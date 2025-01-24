import os
from dataclasses import dataclass


@dataclass
class BaseDBConfig:
    host: str
    port: int
    db_name: str
    user: str
    password: str

    def get_connection_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"
    
    
@dataclass
class DBConfig(BaseDBConfig): ...


@dataclass
class AlembicDBConfig(BaseDBConfig): ...


def load_alembic_config() -> AlembicDBConfig:
    return AlembicDBConfig(
        host=os.environ["POSTGRES_HOST"],
        port=int(os.environ["POSTGRES_PORT"]),
        db_name=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
    )

