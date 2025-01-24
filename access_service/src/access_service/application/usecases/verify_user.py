from dataclasses import dataclass
from access_service.application.common.usecase.interactor import Interactor
from uuid import UUID
from access_service.application.common.gateway.verification_token import VerificationTokenGateway
from access_service.application.common.gateway.user import UserGateway
from access_service.domain.values.user import UserID
from access_service.application.exceptions.user import (
    UserIsNotExistsError,
)


@dataclass
class VerificationInputDTO:
    uid: UUID
    code: int


class VerifyUser(Interactor[VerificationInputDTO, None]):
    def __init__(
        self,
        user_gateway: UserGateway,
        verification_token_gateway: VerificationTokenGateway 
    ):
        self.user_gateway: UserGateway = user_gateway
        self.verification_token_gateway: VerificationTokenGateway = verification_token_gateway

    async def __call__(self, data: VerificationInputDTO):
        user = await self.user_gateway.get_by_uid(
            uid=UserID(data.uid)
        )
        if not user:
            raise UserIsNotExistsError
        
        verification_token_dto = await self.verification_token_gateway.get_verification_token(
            uid=str(data.uid)
        )
        if not verification_token_dto:
            raise Exception
        
        if verification_token_dto.code != data.code:
            raise Exception
        
        await self.user_gateway.activate_user(uid=user.user_id)
        





        