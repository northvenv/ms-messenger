from dataclasses import dataclass

from access_service.domain.values.user import (
    UserID,
    UserName,
    UserHashedPassword,
    UserPhoneNumber,
)


@dataclass
class User:
    user_id: UserID
    username: UserName
    hashed_password: UserHashedPassword
    phone_number: UserPhoneNumber

    @classmethod
    def create_user(
        cls,
        user_id: UserID,
        username: UserName,
        phone_number: UserPhoneNumber,
        hashed_password: UserHashedPassword,
    ) -> "User":
        return cls(
            user_id=user_id, 
            username=username, 
            phone_number=phone_number,
            hashed_password=hashed_password, 
        )
    
    def __str__(self) -> str:
        return self.user_id
    
    

