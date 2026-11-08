import enum
from datetime import datetime

from pydantic import BaseModel


class Role(enum.StrEnum):
    USER = "user"
    ADMIN = "admin"


class AdminCounter(BaseModel):
    value: int


class UserLoginRequest(BaseModel):
    name: str
    pwd: str


class UserLoginResponse(BaseModel):
    jwt_token: str
    jwt_eat: datetime


class UserRegisterRequest(UserLoginRequest): ...


class UserResponse(BaseModel):
    id: int
    name: str
    pwd: str | None
    role: Role


class InputDataONNX(BaseModel):
    Pregnancies: int  # (количество беременностей)
    Glucose: float  # (уровень глюкозы)
    BMI: float  # (индекс массы тела)
    Age: float  # (возраст)


class OutputDataONNX(BaseModel):
    _predication: list = []

    def __init__(self, predication: list):
        self._predication = 1 if predication[0] > 0.5 else 0

    def get_value(self):
        return self._predication
