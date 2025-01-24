from dataclasses import dataclass
from uuid import UUID

from message_service.domain.entities.chat import Chat

from message_service.application.common.usecase.interactor import Interactor
from message_service.application.common.repositories.chat import ChatRepository
from message_service.application.exceptions.chat import (
    ChatAccessDenied,
    ChatNotFound,
)
from message_service.domain.values.chat import UserId
from message_service.application.common.repositories.message import MessageRepository
from message_service.application.dto.chat import ChatDTO

@dataclass
class GetChatInputDTO:
    chat_id: str
    user_id: str


class GetChat(Interactor[GetChatInputDTO, ChatDTO]):
    def __init__(
        self, 
        chat_repository: ChatRepository,
        message_repository: MessageRepository
    ):
        self.chat_repository: ChatRepository = chat_repository
        self.message_repository: MessageRepository = message_repository

    async def __call__(self, data: GetChatInputDTO) -> ChatDTO:
        chat = await self.chat_repository.get_chat_by_oid(oid=data.chat_id)

        if not chat:
            raise ChatNotFound
        
        if UserId(data.user_id) not in chat.participants:
            raise ChatAccessDenied
        
        chat_messages = await self.message_repository.get_all_chat_messages(chat_id=data.chat_id)

        return ChatDTO(
            chat_info=chat,
            chat_messages=chat_messages
        )