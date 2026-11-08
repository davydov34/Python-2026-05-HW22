from fastapi import APIRouter, HTTPException

from src.app.common_entities import (UserLoginRequest, UserLoginResponse,
                                     UserRegisterRequest)
from src.app.database.db import (create_user, get_user_by_id,
                                 get_user_id_by_name)
from src.app.endpoints.auth.logic import create_jwt, pwd_compare
from src.app.logger_app.app_logger import logger as to_log

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
def register(request: UserRegisterRequest) -> bool:
    create_user(name=request.name, pwd=request.pwd)
    return True


@router.post("/login")
def login(request: UserLoginRequest) -> UserLoginResponse:
    id_user = get_user_id_by_name(request.name)
    print(f"GOT ID: {id_user}")
    if not id_user:
        raise HTTPException(status_code=401, detail="Incorrect auth data")

    user = get_user_by_id(id_user)

    if not user.pwd or not pwd_compare(request.pwd, user.pwd):
        raise HTTPException(status_code=401, detail="Incorrect auth data")

    jwt_token, jwt_exp_time = create_jwt(
        {"sub": user.id, "name": user.name, "role": user.role}
    )
    return UserLoginResponse(jwt_token=jwt_token, jwt_eat=jwt_exp_time)
