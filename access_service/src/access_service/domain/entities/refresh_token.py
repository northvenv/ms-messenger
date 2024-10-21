from dataclasses import dataclass

from access_service.domain.common.entities.timed_token import TimedToken
from access_service.domain.exceptions.refresh_token import RefreshTokenIsExpiredError


@dataclass(frozen=True)
class RefreshToken(TimedToken):
    revoked: bool = False
    
    def verify(self) -> None:
        if self.expires_in.is_expired or self.revoked:
            raise RefreshTokenIsExpiredError
        

