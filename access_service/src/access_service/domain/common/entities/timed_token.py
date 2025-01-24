from uuid import uuid4
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

from access_service.domain.values.user import UserID
from access_service.domain.common.values.timed_token import (
    ExpiresIn,
    TimedTokenId,
)


@dataclass(frozen=True)
class TimedTokenMetadata:
    uid: UserID
    expires_in: ExpiresIn


@dataclass(frozen=True)
class TimedToken(ABC):
    metadata: TimedTokenMetadata
    token_id: TimedTokenId = field(
        default_factory=lambda: TimedTokenId(uuid4()),
        kw_only=True,
    )

    @property
    def uid(self) -> UserID:
        return self.metadata.uid
    
    @property
    def expires_in(self) -> ExpiresIn:
        return self.metadata.expires_in
    
    @abstractmethod
    def verify(self) -> None: ...