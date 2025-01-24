from dataclasses import dataclass


@dataclass
class SmsConfig:
    email: str
    api_key: str