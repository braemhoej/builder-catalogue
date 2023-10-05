import datetime
import threading
from typing import Any

from fastapi import APIRouter
from starlette.responses import Response

from api.api_endpoint_config import ROOT_URL
from api.async_api_client import AsyncApiClient
from catalogue.catalogue import Catalogue

router = APIRouter()

_CLIENT = AsyncApiClient(ROOT_URL)
_CATALOGUE = Catalogue(_CLIENT)


@router.get("/health")
async def health() -> Response:
    return Response(status_code=200)


@router.get("/api/catalogue/sets/{set_id}/completable-by/user_id/{user_id}")
async def get_sets_completable_by_user_id(
    set_id: str, user_id: str, collaborator_ids: list[str] | None = None
) -> dict[str, Any]:
    info(
        "set_completable_by_user_received",
        {"set_id": set_id, "user_id": user_id, "collaborator_ids": collaborator_ids},
    )
    missing_parts = await _CATALOGUE.get_missing_parts_from_set_by_user(
        set_id, user_id, collaborator_ids
    )
    completable = missing_parts is None
    return {"completable": completable, "missing_parts": missing_parts}


@router.get("/api/catalogue/sets/{set_id}/find_collaborators_for/user_id/{user_id}")
async def get_sets_find_collaborators(set_id: str, user_id: str) -> dict[str, Any]:
    info(
        "find_collaborator_received",
        {"set_id": set_id, "user_id": user_id},
    )
    collaborators = await _CATALOGUE.find_collaborators_for_user(set_id, user_id)
    projected_collaborators = map(
        lambda user: {
            "username": user.username,
            "id": user.id,
            "location": user.location,
        },
        collaborators,
    )
    return {"collaborators": projected_collaborators}


@router.get("/api/catalogue/sets/completable-by/user_id/{user_id}")
async def get_completable_sets_by_user(
    user_id: str, collaborator_ids: list[str] | None = None
) -> list[dict[str, str]]:
    info(
        "completable_sets_by_user_received",
        {"user_id": user_id, "collaborator_ids": collaborator_ids},
    )
    return await _CATALOGUE.get_completable_sets_by_user(user_id, collaborator_ids)


def info(event: str, details: dict[str, Any]) -> None:
    log(event, "info", details)


def log(event: str, level: str, details: dict[str, Any]) -> None:
    now = datetime.datetime.now()
    thread = threading.get_ident()
    print(f"[{now}] [{thread}] [{level}] [{event}] {details}")
