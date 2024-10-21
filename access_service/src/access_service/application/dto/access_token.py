from uuid import UUID
from datetime import datetime
from dataclasses import dataclass


@dataclass(frozen=True)
class AccessTokenDTO:
    uid: UUID
    expires_in: datetime
    token_id: UUID