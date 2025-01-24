from motor.motor_asyncio import AsyncIOMotorClient

from message_service.domain.entities.chat import Chat, Message

from message_service.infrastructure.repositories.base import BaseMongoDBRepository
from message_service.infrastructure.repositories.converters import (
    convert_message_entity_to_document,
    convert_message_document_to_entity
)
from message_service.infrastructure.persistence.config import MongoDBConfig




class MessageRepositoryImpl(BaseMongoDBRepository):
    def __init__(
        self,
        mongo_client: AsyncIOMotorClient,
        config: MongoDBConfig,
    ):
        super().__init__(
            mongo_client,
            config,
        )

    async def add_message(self, message: Message) -> None:
        await self._collection.insert_one(
            document=convert_message_entity_to_document(message),
        )

    async def get_all_chat_messages(self, chat_id: str) -> list[Message]:
        query = {"chat_id": chat_id}
        cursor = self._collection.find(query).sort("created_at", -1)

        messages = [
            convert_message_document_to_entity(message_document)
            async for message_document in cursor
        ]
 
        return messages

    @property
    def _collection(self):
        return self._db[self.config.collections.message]
        