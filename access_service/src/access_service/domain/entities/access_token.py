from dataclasses import dataclass

from access_service.domain.common.entities.timed_token import TimedToken
from access_service.domain.exceptions.access_token import AccessTokenIsExpiredError


@dataclass(frozen=True)
class AccessToken(TimedToken):
    revoked: bool = False

    def verify(self) -> None:
        if self.expires_in.is_expired or self.revoked:
            raise AccessTokenIsExpiredError
        