from uuid import UUID
from datetime import datetime
from dataclasses import dataclass


@dataclass(frozen=True)
class VerificationTokenDTO:
    uid: UUID
    expires_in: datetime
    code: int
    token_id: UUID