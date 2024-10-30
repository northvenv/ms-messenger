from dataclasses import dataclass

from access_service.domain.common.values.base import BaseValueObject


@dataclass(frozen=True)
class VerificationTokenCode(BaseValueObject[int]): ...