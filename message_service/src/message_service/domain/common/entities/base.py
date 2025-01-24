from abc import ABC
from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime



@dataclass
class BaseEntity(ABC):
    created_at: datetime = field(
        default_factory=datetime.now,
        kw_only=True,
    )


