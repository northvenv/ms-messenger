from access_service.presentation.schemas.base import Base



class CreateUserSchema(Base):
    username: str
    phone_number: int
    password: str


class LoginSchema(Base):
    phone_number: int
    password: str
