from uuid import UUID
from dataclasses import dataclass
from message_service.domain.entities.chat import Chat
from message_service.domain.entities.message import Message


@dataclass
class ChatIdDTO:
    chat_id: str

@dataclass
class ChatDTO:
    chat_info: Chat
    chat_messages: list[Message]
