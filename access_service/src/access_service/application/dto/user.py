from uuid import UUID
from dataclasses import dataclass


@dataclass(frozen=True)
class UserDTO():
    user_id: UUID
    phone_number: int





