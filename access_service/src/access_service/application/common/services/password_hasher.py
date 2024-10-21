from abc import abstractmethod
from typing import Protocol


class PasswordHasher[RawPassword, HashedPassword](Protocol):
    @abstractmethod
    def hash_password(self, password: RawPassword) -> HashedPassword: ...

    @abstractmethod
    def verify_password(
        self,
        raw_password: RawPassword,
        hashed_password: HashedPassword,
    ) -> None: ...
        