from message_service.presentation.schemas.chat import (
    GetChatSchema,
)
from message_service.presentation.schemas.message import (
    SendMessageSchema
)


def validate_chat_dict(data_dict: dict):
    chat_data = GetChatSchema(**data_dict)
    return chat_data


def validate_message_dict(data_dict: dict):
    message_data = SendMessageSchema(**data_dict)
    return message_data