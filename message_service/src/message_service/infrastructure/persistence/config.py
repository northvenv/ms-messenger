from dataclasses import dataclass


@dataclass(frozen=True)
class Collections:
    chat: str
    message: str


@dataclass(frozen=True)
class MongoDBConfig:
    host: str
    port: str
    db_name: str
    collections: Collections
    username: str = ""
    password: str = ""

    def get_connection_url(self) -> str:
        if self.username and self.password:
            return f"mongodb://{self.username}:{self.password}@{self.host}:{self.port}/{self.db_name}"
        else:
            return f"mongodb://{self.host}:{self.port}/{self.db_name}"
            

