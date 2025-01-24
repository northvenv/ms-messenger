from message_service.presentation.schemas.base import Base


class SendMessageSchema(Base):
    chat_id: str
    message_body: str