from dataclasses import dataclass
from uuid import UUID, uuid4

from message_service.domain.entities.chat import Chat
from message_service.domain.values.chat import (
    ChatId,
    UserId
)
from message_service.application.common.usecase.interactor import Interactor
from message_service.application.common.repositories.chat import ChatRepository
from message_service.application.dto.chat import ChatIdDTO

from message_service.application.exceptions.chat import ChatAlreadyExists


@dataclass
class CreateChatInputDTO:
    first_user_id: str
    second_user_id: str


class CreateChat(Interactor[CreateChatInputDTO, ChatIdDTO]):
    def __init__(
        self,
        chat_repository: ChatRepository
    ):
        self.chat_repository: ChatRepository = chat_repository

    async def __call__(self, data: CreateChatInputDTO) -> ChatIdDTO:
        chat = await self.chat_repository.get_chat_by_participants(
            first_user_id=data.first_user_id,
            second_user_id=data.second_user_id,
        )
        if chat: 
            raise ChatAlreadyExists
        
        chat = Chat.create_chat(
            participants=(
                UserId(data.first_user_id),
                UserId(data.second_user_id),
            )
        )
        chat_data = await self.chat_repository.add_chat(chat)
        return chat_data
