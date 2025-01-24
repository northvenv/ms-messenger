from uuid import UUID
from typing import Protocol
from abc import abstractmethod

from message_service.domain.entities.chat import Message


class MessageRepository(Protocol):
    @abstractmethod
    async def add_message(self, message: Message) -> None:
        raise NotImplementedError
    
    @abstractmethod
    async def get_all_chat_messages(self, chat_id: str) -> list[Message]:
        raise NotImplementedError