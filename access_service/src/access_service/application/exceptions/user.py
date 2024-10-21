from access_service.application.common.exceptions.base import ApplicationError


class UserIsNotExistsError(ApplicationError): ...


class InvalidCredentialsError(ApplicationError): ...


class UserAlreadyExistsError(ApplicationError): ...