from fastapi import APIRouter, HTTPException, status

from app.core.logging import get_logger
from app.core.time import now_formatted
from app.users import service
from app.users.dependencies import CurrentUser, SessionDep
from app.users.schemas import UserProfile, UserRead

router = APIRouter(prefix="/users", tags=["users"])
logger = get_logger(__name__)


@router.get("/{user_id}")
async def get_user(user_id: int, current_user: CurrentUser, session: SessionDep) -> UserProfile:
    if user_id != current_user.id:
        logger.warning("user_access_denied", user_id=user_id, requested_by=current_user.id)
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="No puedes consultar otro usuario")

    try:
        user = await service.get_user(session, user_id)
    except Exception:
        logger.exception("user_fetch_failed", user_id=user_id)
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, detail="No fue posible obtener el usuario")

    if user is None:
        logger.warning("user_not_found", user_id=user_id)
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

    user_data = UserRead.model_validate(user).model_dump()
    return UserProfile(**user_data, generated_at=now_formatted())
