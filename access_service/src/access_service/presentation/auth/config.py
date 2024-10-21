from dataclasses import dataclass

@dataclass
class TokenAuthConfig:
    access_token_cookie_key: str
    refresh_token_cookie_key: str
