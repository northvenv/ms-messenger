import asyncpg
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import DBAPIError, IntegrityError

from typing import NoReturn

from access_service.domain.entities.user import User
from access_service.domain.values.user import (
    UserPhoneNumber,
    UserID
)

from access_service.application.dto.user import UserDTO
from access_service.application.exceptions.user import UserAlreadyExistsError
from access_service.application.common.exceptions.repo_error import RepoError

from access_service.infrastructure.gateway.converters.user import (
    convert_user_entity_to_db_user,
    convert_db_user_to_user_entity,
    convert_db_user_to_dto,
)
from access_service.infrastructure.persistence.models.user import DBUser


class UserGatewayImpl:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(
        self, 
        user: User,
    ) -> UserDTO:
        db_user = convert_user_entity_to_db_user(user)
        try: 
            self.session.add(db_user)
            await self.session.commit()
        except IntegrityError as err:
            await self.session.rollback()
            self._process_error(err)
            
        await self.session.refresh(db_user)
        
        return convert_db_user_to_dto(db_user)
    
    async def activate_user(
        self,
        uid: UserID
    ) -> User | None:
        user: DBUser | None = await self._get_by_uid(uid.to_raw())

        if user:
            user.is_active = True

        try:
            await self.session.commit()
        except IntegrityError as err:
            await self.session.rollback()
            self._process_error(err)

        await self.session.refresh(user)

        return convert_db_user_to_user_entity(user)
        
    async def _get_by_uid(
        self, 
        uid: UUID
    ) -> DBUser | None:
        query = select(DBUser).where(DBUser.user_id == uid)

        result = await self.session.execute(query)
        user: DBUser | None = result.scalar()
        
        return user
        

    async def get_by_uid(
        self,
        uid: UserID
    ) -> User | None:
        user = await self._get_by_uid(uid.to_raw())

        if not user:
            return None
        
        return convert_db_user_to_user_entity(user)
    
    async def get_with_phone_number(
        self,
        phone_number: UserPhoneNumber,
    ) -> User | None :
        query = select(DBUser).where(DBUser.phone_number == phone_number.to_raw())

        result = await self.session.execute(query)
        user: DBUser | None = result.scalar()

        if not user: 
            return None
        
        return convert_db_user_to_user_entity(user)

    @staticmethod
    def _process_error(error: DBAPIError) -> NoReturn:
        match error.__cause__.__cause__.constraint_name:
            case "users_phone_number_key":
                raise UserAlreadyExistsError from error
            case "users_username_key":
                raise UserAlreadyExistsError from error
            case _:
                raise RepoError from error
        
    