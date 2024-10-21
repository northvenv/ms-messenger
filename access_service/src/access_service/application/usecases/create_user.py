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
from access_service.application.common.repository.user import UserRepository
from access_service.application.common.services.password_hasher import PasswordHasher


@dataclass(frozen=True)
class CreateUserInputDTO(): 
    username: str
    phone_number: str
    password: str


class CreateUser(Interactor[CreateUserInputDTO, UserDTO]):
    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher
    ): 
        self.user_repository: UserRepository = user_repository
        self.password_hasher: PasswordHasher[UserRawPassword, UserHashedPassword] = password_hasher

    async def __call__(self, data: CreateUserInputDTO) -> UserDTO:
        user_id = UserID(uuid4())
        username = UserName(data.username)
        phone_number = UserPhoneNumber(data.phone_number)
        hashed_password = self.password_hasher.hash_password(
            UserRawPassword(data.password)
        )

        user = User.create_user(
            user_id=user_id,
            username=username,
            phone_number=phone_number,
            hashed_password=hashed_password,
        )

        user_dto = await self.user_repository.save(user)
        
        return user_dto






