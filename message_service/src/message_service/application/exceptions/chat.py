from message_service.application.common.exceptions.application import ApplicationError


class ChatAccessDenied(ApplicationError): ...


class ChatNotFound(ApplicationError): ...


class ChatAlreadyExists(ApplicationError): ...