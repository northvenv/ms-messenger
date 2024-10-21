import re
from uuid import UUID
from dataclasses import dataclass

from access_service.domain.common.values.base import BaseValueObject
from access_service.domain.exceptions.user import (
    InvalidPasswordError,
    InvalidPhoneNumberError, 
    InvalidUsernameError
)


@dataclass(frozen=True)
class UserID(BaseValueObject[UUID]): ...


@dataclass(frozen=True)
class UserName(BaseValueObject[str]):
    _PATTERN = r'^[a-zA-Z][a-zA-Z0-9._]{3,31}$' 

    def _validate(self):
        if not re.fullmatch(pattern=self._PATTERN, string=self.value):
            raise InvalidUsernameError


@dataclass(frozen=True)
class UserRawPassword(BaseValueObject[str]):
    _PATTERN = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    
    def _validate(self):
        if not re.fullmatch(pattern=self._PATTERN, string=self.value):
            raise InvalidPasswordError
        
        
@dataclass(frozen=True)
class UserHashedPassword(BaseValueObject[str]): ...


@dataclass(frozen=True)
class UserPhoneNumber(BaseValueObject[int]): 
    _PATTERN = r'^7\d{10}$'

    def _validate(self):
        if not re.fullmatch(pattern=self._PATTERN, string=str(self.value)):
            raise InvalidPhoneNumberError