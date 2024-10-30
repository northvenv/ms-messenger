from typing import Protocol
from abc import abstractmethod

from access_service.domain.entities.verification_token import VerificationToken


class VerificationTokenGateway(Protocol):
    @abstractmethod
    async def produce_verification_token(self, data: VerificationToken) -> None:
        ...

    @abstractmethod
    async def save_verification_token(self, data: VerificationToken) -> None:
        ...