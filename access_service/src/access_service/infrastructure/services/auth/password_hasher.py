import argon2

from access_service.domain.values.user import (
    UserHashedPassword,
    UserRawPassword,
)

from access_service.application.common.services.password_hasher import PasswordHasher
from access_service.application.exceptions.password_hasher import PasswordMismatchError


class PasswordHasherImpl(PasswordHasher[UserRawPassword, UserHashedPassword]):
    def __init__(self, password_hasher: argon2.PasswordHasher):
        self.ph = password_hasher

    def hash_password(self, password: UserRawPassword) -> UserHashedPassword:
        return UserHashedPassword(self.ph.hash(password.value))

    def verify_password(
        self,
        raw_password: UserRawPassword,
        hashed_password: UserHashedPassword,
    ) -> None:
        try:
            self.ph.verify(hashed_password.value, raw_password.value)
        except argon2.exceptions.VerifyMismatchError as exc:
            raise PasswordMismatchError from exc