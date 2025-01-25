from uuid import UUID
from fastapi import APIRouter, Depends, Request
from dependency_injector.wiring import inject, Provide

from message_service.bootstrap.di import ApplicationContainer
from message_service.application.usecase.send_message import (
    SendMessage,
    SendMessageInputDTO
)
from message_service.presentation.common.decorators.auth import user_auth
from message_service.presentation.schemas.message import (
    SendMessageSchema
)


router = APIRouter(
    prefix="/message",
    tags=["Message"],
)


@router.post("/send")
@user_auth
@inject 
async def send_message(
    request: Request,
    data: SendMessageSchema,
    send_message: SendMessage = Depends(Provide[ApplicationContainer.send_message]),
    user_id: str = None,
): 
    message = await send_message(
        SendMessageInputDTO(
            chat_id=data.chat_id,
            sender_id=user_id,
            message_body=data.message_body,
        )
    )
    return message
