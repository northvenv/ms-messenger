from access_service.domain.exceptions.base import DomainError


class InvalidUsernameError(DomainError): ...


class InvalidPasswordError(DomainError): ...


class InvalidPhoneNumberError(DomainError): ...