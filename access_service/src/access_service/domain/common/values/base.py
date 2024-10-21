from abc import ABC
from dataclasses import dataclass


@dataclass(frozen=True)
class BaseValueObject[T](ABC):
    value: T

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None: ...
    
    def to_raw(self) -> T:
        return self.value
