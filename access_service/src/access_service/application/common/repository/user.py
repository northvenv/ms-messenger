from abc import abstractmethod
from typing import Protocol

from access_service.domain.entities.user import User
from access_service.domain.values.user import UserPhoneNumber

from access_service.application.dto.user import UserDTO


class UserRepository(Protocol):
    @abstractmethod
    async def save(self, user: User) -> UserDTO:
        ...

    @abstractmethod
    async def get_with_phone_number(self, phone_number: UserPhoneNumber) -> User | None:
        ...