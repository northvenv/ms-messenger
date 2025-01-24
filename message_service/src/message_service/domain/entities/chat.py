from uuid import uuid4
from dataclasses import dataclass, field

from message_service.domain.values.chat import (
    MessageId,
    MessageBody,
    ChatId,
    UserId
)
from message_service.domain.common.entities.base import BaseEntity
from message_service.domain.entities.message import Message


@dataclass
class Chat(BaseEntity):
    chat_id: ChatId = field(
        default_factory=lambda: ChatId(str(uuid4())),
        kw_only=True,
    )
    participants: list[UserId, UserId]
    # messages: set[Message] = field(
    #     default_factory=set,
    #     kw_only=True,
    # )

    @classmethod
    def create_chat(cls, participants: list[UserId, UserId]) -> "Chat":
        return cls(
            participants=participants
        )

