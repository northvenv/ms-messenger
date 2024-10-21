from dataclasses import dataclass


@dataclass
class JWTConfig:
    key: str
    algorithm: str