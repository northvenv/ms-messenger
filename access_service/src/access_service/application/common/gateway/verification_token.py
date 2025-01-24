from typing import Protocol
from abc import abstractmethod

from access_service.domain.entities.verification_token import VerificationToken
from access_service.application.dto.verification_token import VerificationTokenDTO


class VerificationTokenGateway(Protocol):

    @abstractmethod
    async def save_verification_token(self, verification_token_dto: VerificationTokenDTO) -> None:
        ...

    @abstractmethod
    async def get_verification_token(self, uid: str) -> VerificationTokenDTO:
        ...