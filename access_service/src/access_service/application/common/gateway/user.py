from abc import abstractmethod
from typing import Protocol

from access_service.domain.entities.user import User
from access_service.domain.values.user import (
    UserPhoneNumber,
    UserID
)

from access_service.application.dto.user import UserDTO


class UserGateway(Protocol):
    @abstractmethod
    async def save(self, user: User) -> UserDTO:
        ...

    @abstractmethod
    async def get_with_phone_number(self, phone_number: UserPhoneNumber) -> User | None:
        ...

    @abstractmethod
    async def get_by_uid(self, uid: UserID) -> User | None:
        ...

    @abstractmethod
    async def activate_user(self, uid: UserID) -> User | None:
        ...