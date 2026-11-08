from fastapi import APIRouter, Depends

from src.app.common_entities import UserResponse
from src.app.endpoints.auth.logic import get_current_user

router = APIRouter(prefix="/me", tags=["me"])


@router.get("", response_model=UserResponse, response_model_exclude_none=True)
def me(user: UserResponse = Depends(get_current_user)) -> UserResponse:
    return user
