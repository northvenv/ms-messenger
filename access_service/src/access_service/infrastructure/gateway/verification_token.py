import orjson
from uuid import UUID
from redis.asyncio import Redis, ConnectionPool
from typing import NoReturn
from typing import AsyncGenerator

from access_service.domain.entities.verification_token import VerificationToken

from access_service.infrastructure.gateway.converters.user import (
    convert_user_entity_to_db_user,
    convert_db_user_to_user_entity,
    convert_db_user_to_dto,
)
from access_service.infrastructure.persistence.models.user import DBUser
from access_service.infrastructure.gateway.converters.verification_token import (
    convert_verification_token_dto_to_bytes,
)
from access_service.application.dto.verification_token import VerificationTokenDTO



class VerificationTokenGatewayImpl:
    def __init__(
        self,
        session: AsyncGenerator[Redis, None]
    ):
        self.session = session

    async def save_verification_token(self, verification_token_dto: VerificationTokenDTO):
        async for session in self.session:
            await session.set(
                name=verification_token_dto.uid,
                value=convert_verification_token_dto_to_bytes(verification_token_dto)
            )

    async def get_verification_token(self, uid: str) -> VerificationTokenDTO:
        async for session in self.session:
            verification_token = await session.get(name=uid)
            data = orjson.loads(verification_token)

            verification_token_dto = VerificationTokenDTO(
                uid=data["uid"],
                expires_in=data["expires_in"],
                code=data["code"],
                token_id=data["token_id"]
            )
            return verification_token_dto

            