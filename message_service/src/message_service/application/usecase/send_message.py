from dataclasses import dataclass
from uuid import UUID, uuid4

from message_service.domain.entities.chat import (
    Chat,
    Message,
)
from message_service.domain.values.chat import (
    UserId, 
    MessageBody, 
    ChatId,
)
from message_service.application.common.usecase.interactor import Interactor
from message_service.application.common.repositories.message import MessageRepository
from message_service.application.common.repositories.chat import ChatRepository
from message_service.application.exceptions.chat import (
    ChatAccessDenied,
    ChatNotFound,
)


@dataclass
class SendMessageInputDTO:
    chat_id: str
    sender_id: str
    message_body: str


class SendMessage(Interactor[SendMessageInputDTO, Message]):
    def __init__(
        self,
        message_repository: MessageRepository,
        chat_repository: ChatRepository,
    ):
        self.message_repository: MessageRepository = message_repository
        self.chat_repository: ChatRepository = chat_repository


    async def __call__(self, data: SendMessageInputDTO) -> Message:
        chat = await self.chat_repository.get_chat_by_oid(oid=data.chat_id)

        if not chat:
            raise ChatNotFound
        
        if UserId(data.sender_id) not in chat.participants:
            raise ChatAccessDenied

        message = Message.create_message(
            chat_id=ChatId(data.chat_id),
            sender_id=UserId(data.sender_id),
            body=MessageBody(data.message_body),
        )
        await self.message_repository.add_message(
            message=message,
        )
        return message
