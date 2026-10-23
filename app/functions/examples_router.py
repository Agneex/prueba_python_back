from fastapi import APIRouter, HTTPException, status

from app.core.logging import get_logger
from app.functions import service
from app.functions.examples import EXAMPLES, EXAMPLES_BY_SLUG, Example
from app.functions.schemas import FunctionRead
from app.users.dependencies import CurrentUser, SessionDep

router = APIRouter(prefix="/functions/examples", tags=["examples"])
logger = get_logger(__name__)


@router.get("")
async def list_examples() -> list[Example]:
    return EXAMPLES


@router.post("/{slug}", status_code=status.HTTP_201_CREATED)
async def add_example(slug: str, current_user: CurrentUser, session: SessionDep) -> FunctionRead:
    example = EXAMPLES_BY_SLUG.get(slug)
    if example is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Ejemplo no encontrado")

    function = await service.create_function(session, current_user.id, example.function)
    logger.info("example_added", slug=slug, function_id=function.id, user_id=current_user.id)
    return FunctionRead.model_validate(function)
