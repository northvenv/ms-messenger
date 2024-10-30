import random
from uuid import UUID, uuid4
from dataclasses import dataclass
from datetime import datetime, UTC, timedelta

from access_service.domain.common.entities.timed_token import TimedToken, TimedTokenMetadata
from access_service.domain.common.values.timed_token import ExpiresIn, TimedTokenId

from access_service.domain.values.user import UserID
from access_service.domain.values.verification_token import VerificationTokenCode
from access_service.domain.values.verification_token import VerificationTokenCode

from access_service.domain.exceptions.verification_code import VerificationCodeIsExpiredError


@dataclass(frozen=True)
class VerificationTokenMetadata(TimedTokenMetadata):
    code: VerificationTokenCode


@dataclass(frozen=True)
class VerificationToken(TimedToken):
    metadata: VerificationTokenMetadata

    @classmethod
    def create_verification_token(
        cls,
        user_id: UUID,
        expires_after: timedelta,
    ) -> "VerificationToken":
        token_id = TimedTokenId(uuid4())
        uid = UserID(user_id)

        four_digit_code = random.randint(1000, 9999)
        code = VerificationTokenCode(four_digit_code)

        now = datetime.now(tz=UTC)
        expires_in = ExpiresIn(now + expires_after)

        metadata = VerificationTokenMetadata(
            uid=uid,
            expires_in=expires_in,
            code=code,
        )
        return cls(
            metadata=metadata,
            token_id=token_id,
        )

    def verify(self) -> None:
        if self.expires_in.is_expired:
            raise VerificationCodeIsExpiredError
    
