from uuid import uuid4
from dataclasses import dataclass

from access_service.domain.entities.user import User
from access_service.domain.values.user import (
    UserID,
    UserName,
    UserHashedPassword,
    UserPhoneNumber,
    UserRawPassword,
)
from access_service.application.dto.user import (
    UserDTO,
)
from access_service.application.common.usecase.interactor import Interactor
from access_service.application.common.gateway.user import UserGateway
from access_service.application.common.services.password_hasher import PasswordHasher


@dataclass(frozen=True)
class CreateUserInputDTO(): 
    username: str
    phone_number: int
    password: str


class CreateUser(Interactor[CreateUserInputDTO, UserDTO]):
    def __init__(
        self,
        user_gateway: UserGateway,
        password_hasher: PasswordHasher,
    ): 
        self.user_gateway: UserGateway = user_gateway
        self.password_hasher: PasswordHasher[UserRawPassword, UserHashedPassword] = password_hasher
    
    async def __call__(self, data: CreateUserInputDTO) -> UserDTO:
        user_id = UserID(uuid4())
        username = UserName(data.username)
        phone_number = UserPhoneNumber(data.phone_number)
        hashed_password = self.password_hasher.hash_password(
            UserRawPassword(data.password)
        )

        user = User(
            user_id=user_id,
            username=username,
            phone_number=phone_number,
            hashed_password=hashed_password,
        )

        user_dto = await self.user_gateway.save(user)

        return user_dto







