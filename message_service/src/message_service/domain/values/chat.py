from dataclasses import dataclass


from message_service.domain.common.values.base import BaseValueObject


@dataclass(frozen=True)
class MessageId(BaseValueObject[str]): ...


@dataclass(frozen=True)
class MessageBody(BaseValueObject[str]): ...


@dataclass(frozen=True)
class ChatId(BaseValueObject[str]): ...


@dataclass(frozen=True)
class UserId(BaseValueObject[str]): ...

