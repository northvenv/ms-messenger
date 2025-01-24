from uuid import uuid4
from dataclasses import dataclass, field

from message_service.domain.values.chat import (
    MessageId,
    MessageBody,
    ChatId,
    UserId,
)
from message_service.domain.common.entities.base import BaseEntity


@dataclass
class Message(BaseEntity):
    chat_id: ChatId
    message_id: MessageId = field(
        default_factory=lambda: MessageId(str(uuid4())),
        kw_only=True,
    )
    sender_id: UserId
    body: MessageBody 

    @classmethod
    def create_message(
        cls, 
        chat_id: ChatId,
        sender_id: UserId, 
        body: MessageBody
    ) -> "Message":
        return cls(
            chat_id=chat_id,
            sender_id=sender_id,
            body=body,
        )