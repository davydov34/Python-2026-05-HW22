from fastapi import APIRouter, Depends

from src.app.common_entities import AdminCounter, Role, UserResponse
from src.app.database.db import get_http_counter
from src.app.endpoints.auth.logic import RoleChacker

admin_permission = RoleChacker([Role.ADMIN])

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/health")
def health(u: UserResponse = Depends(admin_permission)) -> AdminCounter:
    return AdminCounter(value=get_http_counter())
