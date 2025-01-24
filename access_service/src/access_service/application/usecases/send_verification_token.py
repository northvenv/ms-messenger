from uuid import UUID
from dataclasses import dataclass

from access_service.domain.entities.verification_token import VerificationToken
from access_service.domain.common.entities.config import VerificationTokenConfig

from access_service.application.common.usecase.interactor import Interactor
from access_service.application.common.usecase.interactor import Interactor
from access_service.domain.entities.verification_token import VerificationToken
from access_service.domain.common.entities.config import VerificationTokenConfig
from access_service.infrastructure.events.verification_token import VerificationTokenCreatedEventHandler
from access_service.domain.events.verification_token import VerificationTokenCreatedEvent


@dataclass 
class SendVerificationTokenInputDTO:
    user_id: UUID
    phone_number: int


class SendVerificationToken(Interactor[SendVerificationTokenInputDTO, None]):
    def __init__(
        self,
        verification_token_config: VerificationTokenConfig,
        verification_token_created_event_handler: VerificationTokenCreatedEventHandler
    ): 
        self.verification_token_config: VerificationTokenConfig = verification_token_config
        self.verification_token_created_event_handler: VerificationTokenCreatedEventHandler = verification_token_created_event_handler

    async def __call__(self, data: SendVerificationTokenInputDTO):
        verification_token = VerificationToken.create_verification_token(
            user_id=data.user_id,
            phone_number=data.phone_number,
            expires_after=self.verification_token_config.expires_after,
        )
        event = VerificationTokenCreatedEvent(
            verification_token=verification_token
        )
        await self.verification_token_created_event_handler.handle(event=event)


