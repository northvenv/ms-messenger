import random
from uuid import UUID, uuid4
from dataclasses import dataclass, field
from datetime import datetime, UTC, timedelta

from access_service.domain.common.entities.timed_token import TimedToken, TimedTokenMetadata
from access_service.domain.common.values.timed_token import ExpiresIn, TimedTokenId

from access_service.domain.values.user import UserID
from access_service.domain.values.verification_token import VerificationTokenCode
from access_service.domain.values.verification_token import VerificationTokenCode
from access_service.domain.values.user import UserPhoneNumber
from access_service.domain.exceptions.verification_code import VerificationCodeIsExpiredError


@dataclass(frozen=True)
class VerificationTokenMetadata(TimedTokenMetadata):
    code: VerificationTokenCode = field(
        default_factory=lambda: VerificationTokenCode(
            random.randint(1000, 9999)
        ),
        kw_only=True
    )
    phone_number: UserPhoneNumber


@dataclass(frozen=True)
class VerificationToken(TimedToken):
    metadata: VerificationTokenMetadata

    @classmethod
    def create_verification_token(
        cls,
        user_id: UUID,
        phone_number: int,
        expires_after: timedelta,
    ) -> "VerificationToken":
        now = datetime.now(tz=UTC)
        expires_in = ExpiresIn(now + expires_after)

        metadata = VerificationTokenMetadata(
            uid=UserID(user_id),
            phone_number=UserPhoneNumber(phone_number),
            expires_in=expires_in,
        )
        return cls(
            metadata=metadata,
        )

    def verify(self) -> None:
        if self.expires_in.is_expired:
            raise VerificationCodeIsExpiredError
    
