import os
from datetime import datetime as dt
from datetime import timedelta as td

import bcrypt
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.app.common_entities import Role, UserResponse
from src.app.logger_app.app_logger import logger as to_log

security = HTTPBearer()

"""Параметры безопасности задаются через переменные окружения"""
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "sEcReT_kEy")
JWT_ALG = os.environ.get("JWT_ALG", "HS256")
JWT_EXP_TIME = os.environ.get("JWT_EXP_TIME", "30")


"""Функция хэширования пароля"""


def pwd_hashing(pwd: str) -> str:
    b_pwd = pwd.encode("utf-8")
    salt = bcrypt.gensalt()
    hash_pwd = bcrypt.hashpw(b_pwd, salt)
    return hash_pwd


"""Функция сравнения паролей"""


def pwd_compare(pwd: str, hash_pwd: str) -> bool:
    is_valid = bcrypt.checkpw(pwd.encode("utf-8"), hash_pwd.encode("utf-8"))
    return is_valid


"""Создание JWT-токена"""


def create_jwt(data: dict) -> tuple[str, dt]:
    payload = data.copy()
    exp_time = dt.now() + td(minutes=int(JWT_EXP_TIME))
    payload["exp"] = exp_time
    new_jwt = jwt.encode(payload, JWT_SECRET_KEY, JWT_ALG)
    return new_jwt, exp_time


"""Декодирование JWT-токена"""


def decode_jwt(token: str):
    return jwt.decode(
        jwt=token, key=JWT_SECRET_KEY, algorithms=JWT_ALG, options={"verify_sub": False}
    )


"""Функция получения текущего пользователя"""


def get_current_user(
    auth_crederials: HTTPAuthorizationCredentials = Depends(security),
) -> UserResponse:
    from src.app.database.db import get_user_by_id

    try:
        auth_token = auth_crederials.credentials
        jwt_payload = decode_jwt(auth_token)
        id_user = jwt_payload.get("sub", None)
        if id_user is None:
            to_log.error(f"Данные для авторизации не валидны")
            raise ValueError("Authorization credentials is not valid")
    except:
        raise HTTPException(status_code=401, detail="Invalid JWT token")

    return get_user_by_id(id_user)


"""Проверка на вхождение в назначенные роли"""


class RoleChacker:
    def __init__(self, permitted_roles=list[Role]):
        self.permitted_roles = permitted_roles

    def __call__(self, user: UserResponse = Depends(get_current_user)) -> UserResponse:
        if user.role not in self.permitted_roles:
            to_log.warning(
                f"Пользователь с ID={user.id} не имеет требуемой роли доступа к ресурсу"
            )
            raise HTTPException(status_code=403, detail="FORBIDDEN")
        return user
