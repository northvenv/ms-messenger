from dataclasses import dataclass
from typing import List



@dataclass
class Sms:
    number: int | List[int]
    text: str

@dataclass(frozen=True)
class SmsResult:
    sms_result: dict
    verification_token: dict