from fastapi import APIRouter
from starlette.responses import Response

router = APIRouter()


@router.get("/health")
async def health() -> Response:
    return Response(status_code=200)


@router.get("/user/{user_id}/sets")
async def get_sets_by_user(user_id: str, allow_substitutions: bool = False) -> Response:
    return Response(status_code=200)
