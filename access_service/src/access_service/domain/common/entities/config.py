from dataclasses import dataclass
from datetime import timedelta


@dataclass(frozen=True)
class AccessTokenConfig:
    expires_after: timedelta

@dataclass(frozen=True)
class RefreshTokenConfig:
    expires_after: timedelta