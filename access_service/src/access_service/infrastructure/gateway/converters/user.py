from access_service.domain.entities.user import User
from access_service.infrastructure.persistence.models.user import DBUser
from access_service.application.dto.user import UserDTO
from uuid import UUID
from access_service.domain.values.user import (
    UserID,
    UserName,
    UserPhoneNumber,
    UserHashedPassword
)


def convert_user_entity_to_db_user(user: User) -> DBUser:
    return DBUser(
        user_id=user.user_id.to_raw(),
        username=user.username.to_raw(),
        phone_number=user.phone_number.to_raw(),
        hashed_password=user.hashed_password.to_raw(),
    )


def convert_db_user_to_user_entity(db_user: DBUser) -> User:
    return User(
        user_id=UserID(db_user.user_id),
        username=UserName(db_user.username),
        phone_number=UserPhoneNumber(db_user.phone_number),
        hashed_password=UserHashedPassword(db_user.hashed_password),
    )


def convert_db_user_to_dto(db_user: DBUser) -> UserDTO:
    return UserDTO(
        user_id=UUID(str(db_user.user_id)),
        phone_number=db_user.phone_number
    )




