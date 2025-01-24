from uuid import UUID
from typing import Protocol, Any
from abc import abstractmethod

from message_service.domain.entities.chat import Chat
from message_service.application.dto.chat import ChatIdDTO, ChatDTO


class ChatRepository(Protocol):
    @abstractmethod
    async def add_chat(self, chat: Chat) -> ChatIdDTO:
        raise NotImplementedError
    
    @abstractmethod
    async def get_chat_by_oid(self, oid: str) -> ChatDTO:
        raise NotImplementedError
    
    @abstractmethod
    async def get_chat_by_participants(self, first_user_id: str, second_user_id: str) -> Chat:
        raise NotImplementedError