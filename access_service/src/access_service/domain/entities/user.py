from dataclasses import dataclass

from access_service.domain.values.user import (
    UserID,
    UserName,
    UserHashedPassword,
    UserPhoneNumber,
)
from access_service.domain.exceptions.user import UserIsNotActiveError


@dataclass
class User:
    user_id: UserID
    username: UserName
    hashed_password: UserHashedPassword
    phone_number: UserPhoneNumber
    is_active: bool = False

    @classmethod
    def create_user(cls):
        return cls()
    
    def verify_is_active(self) -> None:
        if not self.is_active:
            raise UserIsNotActiveError
    
    def _activate(self) -> None:
        self.is_active = True
    
    def __str__(self) -> str:
        return self.user_id
    
    

