from enum import Enum
from dataclasses import dataclass
from access_service.domain.exceptions.user import (
    InvalidPasswordError,
    InvalidPhoneNumberError,
    InvalidUsernameError,
)
from access_service.domain.exceptions.access_token import (
    AccessTokenIsExpiredError,
    UnauthorizedError,
)
from access_service.domain.exceptions.refresh_token import (
    RefreshTokenIsExpiredError
)
from access_service.application.exceptions.user import (
    UserIsNotExistsError,
    InvalidCredentialsError,
)


class ErrorEnum(Enum):
    INVALID_PASSWORD = InvalidPasswordError
    INVALID_PHONE_NUMBER = InvalidPhoneNumberError
    INVALID_USERNAME = InvalidUsernameError
    INVALID_CREDENTIALS = InvalidCredentialsError
    USER_NOT_EXISTS = UserIsNotExistsError
    ACCESS_TOKEN_EXPIRED = AccessTokenIsExpiredError
    REFRESH_TOKEN_EXPIRED = RefreshTokenIsExpiredError
    UNAUTHORIZED = UnauthorizedError


@dataclass
class ErrorContent:
    error_code: int
    message: str


@dataclass
class ErrorInfo:
    status_code: int
    content: ErrorContent


@dataclass
class HTTP_ERRORS:
    INVALID_PASSWORD = ErrorInfo(
        status_code=400, 
        content=ErrorContent(
            error_code=400, 
            message=""
        )
    )








