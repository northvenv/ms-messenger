from access_service.presentation.schemas.base import Base



class CreateUserSchema(Base):
    username: str
    phone_number: str
    password: str


class LoginSchema(Base):
    phone_number: str
    password: str
