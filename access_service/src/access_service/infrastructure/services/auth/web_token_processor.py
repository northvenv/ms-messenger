from uuid import UUID
from datetime import datetime, UTC

from access_service.infrastructure.web_token.jwt_processor import (
    JWTProcessor,
    JWTToken,
)
from access_service.infrastructure.web_token.exceptions import (
    JWTDecodeError,
    JWTExpiredError,
)
from access_service.domain.exceptions.access_token import (
    UnauthorizedError,
    AccessTokenIsExpiredError,
)
from access_service.domain.exceptions.refresh_token import (
    RefreshTokenIsExpiredError,
)

from access_service.application.dto.access_token import AccessTokenDTO
from access_service.application.dto.refresh_token import RefreshTokenDTO


AccessTokenType = type
RefreshTokenType = type


class WebTokenProcessor:
    def __init__(
        self,
        jwt_processor: JWTProcessor,
    ): 
        self.jwt_processor = jwt_processor

    def encode(self, token_data: AccessTokenDTO | RefreshTokenDTO) -> JWTToken:
        jwt_token_payload = {
            "sub": str(token_data.uid),
            "token_id": str(token_data.token_id),
            "exp": token_data.expires_in,
        }
        jwt_token = self.jwt_processor.encode(jwt_token_payload)

        return jwt_token
    
    def decode(
        self, 
        token: JWTToken, 
        token_type: AccessTokenType | RefreshTokenType
    ) -> AccessTokenDTO | RefreshTokenDTO:
        try:
            payload = self.jwt_processor.decode(token)

            uid = UUID(payload["sub"])
            token_id = UUID(payload["token_id"])
            expires_in = datetime.fromtimestamp(float(payload["exp"]), UTC)
            
            if token_type == AccessTokenType:
                return AccessTokenDTO(
                    uid=uid,
                    expires_in=expires_in,
                    token_id=token_id,
            )
            elif token_type == RefreshTokenType:
                return RefreshTokenDTO(
                    uid=uid,
                    expires_in=expires_in,
                    token_id=token_id,
            )
        except JWTExpiredError as exc:
            if token_type == AccessTokenType:
                raise AccessTokenIsExpiredError from exc
            elif token_type == RefreshTokenType:
                raise RefreshTokenIsExpiredError from exc
        except (JWTDecodeError, ValueError, TypeError, KeyError) as exc:
            raise UnauthorizedError from exc