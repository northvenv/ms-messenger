import jwt
from abc import abstractmethod, ABC
from typing import Any

from access_service.infrastructure.services.web_token.config import JWTConfig
from access_service.infrastructure.services.web_token.exceptions import (
    JWTDecodeError,
    JWTExpiredError,
)


JWTPayload = dict[str, Any]
JWTToken = str


class JWTProcessor(ABC):
    @abstractmethod
    def encode(self, payload: JWTPayload) -> JWTToken: ...

    @abstractmethod
    def decode(self, token: JWTToken) -> JWTPayload: ...


class JWTProcessorImpl(JWTProcessor):
    def __init__(self, config: JWTConfig) -> None:
        self.key = config.key
        self.algorithm = config.algorithm

    def encode(self, payload: JWTPayload) -> JWTToken:
        return jwt.encode(payload, self.key, self.algorithm)

    def decode(self, token: JWTToken) -> JWTPayload:
        try:
            return jwt.decode(token, self.key, algorithms=[self.algorithm])
        except jwt.ExpiredSignatureError as exc:
            raise JWTExpiredError from exc
        except jwt.DecodeError as exc:
            raise JWTDecodeError from exc