import dataclasses

from fastapi import HTTPException
from pydantic import BaseModel, Field

from src.app.common_entities import Role, UserResponse


@dataclasses.dataclass
class User:
    name: str
    pwd: str
    role: Role = Field(strict=False)

    def __post_init__(self):
        from src.app.endpoints.auth.logic import pwd_hashing

        self.pwd = pwd_hashing(self.pwd)


http_counter = {"counter": 0}

user_db = {
    1: User(name="user", pwd="qwerty", role=Role.USER),
    2: User(name="admin", pwd="qwerty", role=Role.ADMIN),
}


"""Функция получения пользователя по ID"""


def get_user_by_id(target_id: int) -> UserResponse:
    if target_id not in user_db:
        raise HTTPException(status_code=404, detail="USER_NOT_FOUND")

    found_user = user_db[target_id]

    return UserResponse(
        id=target_id, name=found_user.name, pwd=found_user.pwd, role=found_user.role
    )


"""Функция получения пользователя по USERNAME"""


def get_user_id_by_name(name: str) -> int | None:
    for found_id, user in user_db.items():
        if user.name == name:
            return found_id
    return None


"""Функция создания нового пользователя"""


def create_user(name: str, pwd: str, role: Role = Role.USER):
    check_username = get_user_id_by_name(name=name)
    if check_username:
        raise HTTPException(status_code=409, detail="User already exists")

    new_user = User(name=name, pwd=pwd, role=role)
    new_id = max(user_db) + 1
    user_db[new_id] = new_user

    return new_id


"""Функция получения значения счетчика HTTP запросов"""


def get_http_counter() -> int:
    return http_counter["counter"]


"""Функция увеличения значения счетчика HTTP запросов"""


def increase_http_counter() -> None:
    http_counter["counter"] = http_counter["counter"] + 1
