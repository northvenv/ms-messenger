from uuid import uuid4
from datetime import datetime, UTC
from dataclasses import dataclass

from access_service.application.common.usecase.interactor import Interactor
from access_service.application.common.repository.user import UserRepository
from access_service.application.common.services.password_hasher import PasswordHasher

from access_service.domain.entities.access_token import AccessToken
from access_service.domain.entities.refresh_token import RefreshToken
from access_service.domain.common.entities.config import (
    AccessTokenConfig,
    RefreshTokenConfig,
)

from access_service.domain.common.entities.timed_token import TimedTokenMetadata

from access_service.domain.common.values.timed_token import (
    TimedTokenId,
    ExpiresIn,
)
from access_service.domain.values.user import (
    UserHashedPassword,
    UserPhoneNumber,
    UserRawPassword,
)
from access_service.application.dto.access_token import AccessTokenDTO
from access_service.application.dto.refresh_token import RefreshTokenDTO

from access_service.application.exceptions.password_hasher import PasswordMismatchError
from access_service.application.exceptions.user import (
    UserIsNotExistsError,
    InvalidCredentialsError,
)


@dataclass(frozen=True)
class AuthorizeInputDTO():
    phone_number: int
    password: str


@dataclass(frozen=True)
class TokensDTO():
    access_token: AccessTokenDTO
    refresh_token: RefreshTokenDTO


class Authorize(Interactor[AuthorizeInputDTO, TokensDTO]):
    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
        access_token_config: AccessTokenConfig,
        refresh_token_config: RefreshTokenConfig
    ):
        self.user_repository: UserRepository = user_repository
        self.password_hasher: PasswordHasher[UserRawPassword, UserHashedPassword] = password_hasher
        self.access_token_config: AccessTokenConfig = access_token_config
        self.refresh_token_config: RefreshTokenConfig = refresh_token_config
    
    async def __call__(self, data: AuthorizeInputDTO) -> TokensDTO:
        user = await self.user_repository.get_with_phone_number(UserPhoneNumber(data.phone_number))

        if not user:
            raise UserIsNotExistsError

        try:
            self.password_hasher.verify_password(UserRawPassword(data.password), user.hashed_password)
        except PasswordMismatchError as exc:
            raise InvalidCredentialsError from exc
        
        now = datetime.now(tz=UTC)
        access_token_expires_in = ExpiresIn(now + self.access_token_config.expires_after)
        refresh_token_expires_in = ExpiresIn(now + self.refresh_token_config.expires_after)

        access_token_metadata = TimedTokenMetadata(uid=user.user_id, expires_in=access_token_expires_in)
        refresh_token_metadata = TimedTokenMetadata(uid=user.user_id, expires_in=refresh_token_expires_in)
        token_id = TimedTokenId(uuid4())

        access_token = AccessToken(metadata=access_token_metadata, token_id=token_id)
        refresh_token = RefreshToken(metadata=refresh_token_metadata, token_id=token_id)

        return TokensDTO(
            access_token=AccessTokenDTO(
                uid=access_token.uid.to_raw(),
                expires_in=access_token.expires_in.to_raw(),
                token_id=access_token.token_id.to_raw(),
            ),
            refresh_token=RefreshTokenDTO(
                uid=refresh_token.uid.to_raw(),
                expires_in=refresh_token.expires_in.to_raw(),
                token_id=refresh_token.token_id.to_raw(),
            )
        )
        

