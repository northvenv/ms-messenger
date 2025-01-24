from uuid import UUID
from datetime import datetime
from dataclasses import dataclass



@dataclass(frozen=True)
class VerificationTokenDTO:
    uid: str
    expires_in: datetime
    code: int
    token_id: str