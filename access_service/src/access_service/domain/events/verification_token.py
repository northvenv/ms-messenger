from dataclasses import dataclass
from access_service.domain.common.events.base import BaseEvent
from access_service.domain.entities.verification_token import VerificationToken
from typing import ClassVar


@dataclass
class VerificationTokenCreatedEvent(BaseEvent):
    event_title: ClassVar[str] = "Verification Token Created"

    verification_token: VerificationToken
