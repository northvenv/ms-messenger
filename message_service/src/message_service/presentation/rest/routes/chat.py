from uuid import UUID
from fastapi import APIRouter, Depends, Request
from dependency_injector.wiring import inject, Provide

from message_service.bootstrap.di import ApplicationContainer

from message_service.domain.entities.chat import Chat

from message_service.application.usecase.create_chat import (
    CreateChat, 
    CreateChatInputDTO
)
from message_service.application.usecase.get_chat import (
    GetChat,
    GetChatInputDTO,
)
from message_service.application.dto.chat import ChatIdDTO, ChatDTO
from message_service.presentation.common.decorators.auth import user_auth
from message_service.presentation.schemas.chat import (
    CreateChatSchema,
    GetChatSchema,
)


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post("/create", response_model=None)
@user_auth
@inject
async def create_chat(
    request: Request,
    data: CreateChatSchema,
    create_chat: CreateChat = Depends(Provide[ApplicationContainer.create_chat]),
    user_id: str = None,
) -> ChatIdDTO:
    chat_id = await create_chat(
        CreateChatInputDTO(
            first_user_id=user_id,
            second_user_id=data.interlocutor_id
        )
    )
    return chat_id


@router.post("/get", response_model=None)
@user_auth
@inject
async def get_chat(
    request: Request,
    data: GetChatSchema,
    get_chat: GetChat = Depends(Provide[ApplicationContainer.get_chat]),
    user_id: str = None,
) -> ChatDTO:
    chat = await get_chat(
        GetChatInputDTO(
            chat_id=data.chat_id,
            user_id=user_id,
        )
    )
    return chat

