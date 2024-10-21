from access_service.domain.exceptions.base import DomainError


class AccessTokenIsExpiredError(DomainError): ...


class UnauthorizedError(DomainError): ...