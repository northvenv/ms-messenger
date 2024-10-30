from uuid import UUID
from dataclasses import dataclass

from access_service.domain.entities.verification_token import VerificationToken
from access_service.domain.common.entities.config import VerificationTokenConfig

from access_service.application.common.gateway.verification_token import VerificationTokenGateway
from access_service.application.common.usecase.interactor import Interactor


@dataclass 
class SendVerificationTokenInputDTO:
    user_id: UUID


class SendVerificationToken(Interactor[SendVerificationTokenInputDTO, None]):
    def __init__(
        self,
        verification_token_gateway: VerificationTokenGateway,
        verification_token_config: VerificationTokenConfig
    ):
        self.verification_token_gateway: VerificationTokenGateway = verification_token_gateway
        self.verification_token_config: VerificationTokenConfig = verification_token_config

    async def __call__(self, data: SendVerificationTokenInputDTO) -> None:
        verification_token = VerificationToken.create_verification_token(
            user_id=data.user_id,
            expires_after=self.verification_token_config.expires_after,
        )

        await self.verification_token_gateway.produce_verification_token(
            data=verification_token,
        )

        await self.verification_token_gateway.save_verification_token(
            data=verification_token,
        )


