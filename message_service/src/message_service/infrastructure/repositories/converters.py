from message_service.domain.entities.chat import (
    Chat,
    Message,
)
from message_service.domain.values.chat import (
    ChatId,
    UserId, 
    MessageBody,
    MessageId
)


def convert_chat_entity_to_document(chat: Chat) -> dict:
    participants = [participant.to_raw() for participant in chat.participants]
    return {
        "oid": chat.chat_id.to_raw(),
        "participants": participants,
        "created_at": chat.created_at
    }

def convert_chat_document_to_entity(data: dict) -> Chat:
    if not data:
        return None
    
    return Chat(
        chat_id=ChatId(data["oid"]),
        participants=[
            UserId(data["participants"][0]),
            UserId(data["participants"][1])
        ],
        created_at=data["created_at"]
    )

def convert_message_entity_to_document(message: Message) -> dict:
    return {
        "oid": message.message_id.to_raw(),
        "chat_id": message.chat_id.to_raw(),
        "sender_id": message.sender_id.to_raw(),
        "body": message.body.to_raw(),
        "created_at": message.created_at
    }

def convert_message_document_to_entity(data: dict) -> Message:
    return Message(
        message_id=MessageId(data["oid"]),
        chat_id=ChatId(data["chat_id"]),
        sender_id=UserId(data["sender_id"]),
        body=MessageBody(data["body"]),
        created_at=data["created_at"]
    )

