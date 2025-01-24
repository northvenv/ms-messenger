from message_service.presentation.schemas.base import Base


class CreateChatSchema(Base):
    interlocutor_id: str

class GetChatSchema(Base):
    chat_id: str