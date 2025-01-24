from motor.motor_asyncio import AsyncIOMotorClient

from message_service.infrastructure.persistence.config import MongoDBConfig


def get_mongo_client(settings: MongoDBConfig) -> AsyncIOMotorClient:
    return AsyncIOMotorClient(
        settings.get_connection_url(),
        uuidRepresentation="standard"
    )


