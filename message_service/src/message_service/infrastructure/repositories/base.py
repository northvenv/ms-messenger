from abc import ABC

from motor.motor_asyncio import AsyncIOMotorClient
from message_service.infrastructure.persistence.config import MongoDBConfig


class BaseMongoDBRepository(ABC):
    def __init__(
        self, 
        mongo_client: AsyncIOMotorClient,
        config: MongoDBConfig,
    ):
        self.mongo_client: AsyncIOMotorClient = mongo_client
        self.config: MongoDBConfig = config

    @property
    def _db(self):
        return self.mongo_client[self.config.db_name]