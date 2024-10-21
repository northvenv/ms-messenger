from datetime import datetime, UTC
from uuid import UUID
from dataclasses import dataclass

from access_service.domain.common.values.base import BaseValueObject


@dataclass(frozen=True)
class ExpiresIn(BaseValueObject[datetime]):

    @property
    def is_expired(self) -> bool:
        return self.value < datetime.now(tz=UTC)


@dataclass(frozen=True)
class TimedTokenId(BaseValueObject[UUID]): ...