import asyncio
from uuid import UUID
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import DuplicateKeyError
from typing import Any

from message_service.domain.entities.chat import Chat

from message_service.infrastructure.repositories.base import BaseMongoDBRepository
from message_service.infrastructure.repositories.converters import (
    convert_chat_entity_to_document,
    convert_chat_document_to_entity,
)
from message_service.infrastructure.persistence.config import MongoDBConfig
from message_service.application.dto.chat import ChatIdDTO

import pymongo




class ChatRepositoryImpl(BaseMongoDBRepository):
    def __init__(
        self,
        mongo_client: AsyncIOMotorClient,
        config: MongoDBConfig,
    ):
        super().__init__(
            mongo_client,
            config,
        )
    

    async def add_chat(self, chat: Chat) -> ChatIdDTO:
        chat_document = convert_chat_entity_to_document(chat)
        await self._collection.insert_one(chat_document)
        chat_id = chat_document["oid"]

        return ChatIdDTO(chat_id=str(chat_id))
       
        
    async def get_chat_by_oid(self, oid: str) -> Chat | None:
        chat_document = await self._collection.find_one(
            filter={
                'oid': oid
            }
        )

        if not chat_document:
            return None
    
        return convert_chat_document_to_entity(chat_document)
    
    async def get_chat_by_participants(self, first_user_id: str, second_user_id: str) -> Chat:
        chat_document = await self._collection.find_one(
            filter={
                "participants": {"$all": [first_user_id, second_user_id]}
            }
        )
        return convert_chat_document_to_entity(chat_document)
        
    async def get_all_user_chats(self, user_id: str) -> list[Chat]:
        query = {"participants": {"$in": [user_id]}}
        cursor = self._collection.find(query)

        chats = [
            convert_chat_document_to_entity(chat_document)
            async for chat_document in cursor
        ]
 
        return chats 
        
    @property
    def _collection(self):
        return self._db[self.config.collections.chat]