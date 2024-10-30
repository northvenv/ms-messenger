from dataclasses import dataclass

@dataclass
class BaseRedisConfig:
    host: str
    port: int
    # db_name: int
    # user: str
    # password: str

    def get_connection_url(self) -> str:
        return f"redis://{self.host}:{self.port}"
        # return f"redis://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"


@dataclass
class RedisConfig(BaseRedisConfig): ...