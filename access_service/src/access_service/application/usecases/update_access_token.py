from datetime import datetime, UTC
from access_service.domain.common.values.timed_token import ExpiresIn

from access_service.application.common.usecase.interactor import Interactor
from access_service.application.dto.refresh_token import RefreshTokenDTO
from access_service.application.dto.access_token import AccessTokenDTO
from access_service.domain.common.entities.config import (
    AccessTokenConfig,
)



class UpdateAccessToken(Interactor[RefreshTokenDTO, AccessTokenDTO]):
    def __init__(
        self,
        access_token_config: AccessTokenConfig,
    ):
        self.access_token_config = access_token_config

    async def __call__(self, data: RefreshTokenDTO) -> AccessTokenDTO:
        now = datetime.now(tz=UTC)
        expires_in = ExpiresIn(now + self.access_token_config.expires_after)

        return AccessTokenDTO(
            uid=data.uid,
            expires_in=expires_in.to_raw(),
            token_id=data.token_id,
        )
        
