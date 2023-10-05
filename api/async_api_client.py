import asyncio
from typing import Any, Mapping, Sequence, TypeAlias, TypeVar

import httpx as httpx
from httpx import QueryParams, Response
from pydantic import BaseModel

from api.api_endpoint_config import (
    GET_SET_BY_ID,
    GET_SET_BY_NAME,
    GET_SETS,
    GET_USER_BY_ID,
    GET_USER_BY_USERNAME,
    GET_USERS,
)
from api.exceptions import ApiException
from model.set import Set, SetDescription, SetDescriptionList
from model.user import User, UserDescription, UserDescriptionList

RequestParameters: TypeAlias = (
    QueryParams
    | Mapping[
        str,
        str | int | float | bool | None | Sequence[str | int | float | bool | None],
    ]
    | list[tuple[str, str | int | float | bool | None]]
    | tuple[tuple[str, str | int | float | bool | None], ...]
    | str
    | bytes
    | None
)


class AsyncApiClient:
    _root_url: str
    _client: httpx.AsyncClient

    def __init__(self, root_url: str) -> None:
        self._root_url = root_url
        self._client = httpx.AsyncClient(base_url=self._root_url)

    async def get_user_by_username(self, username: str) -> UserDescription:
        request_url = _construct_request_url(
            self._root_url, GET_USER_BY_USERNAME, username
        )
        return await self._get_and_validate(request_url, UserDescription)

    async def get_user_by_id(self, user_id: str) -> User:
        request_url = _construct_request_url(self._root_url, GET_USER_BY_ID, user_id)
        return await self._get_and_validate(request_url, User)

    async def get_users(self) -> list[User]:
        user_descriptions = await self.get_user_descriptions()
        user_ids = map(lambda user_description: user_description.id, user_descriptions)
        get_user_coroutines = list(
            map(lambda set_id: self.get_user_by_id(set_id), user_ids)
        )
        return await asyncio.gather(*get_user_coroutines)

    async def get_user_descriptions(self) -> list[UserDescription]:
        request_url = _construct_request_url(self._root_url, GET_USERS)
        return (await self._get_and_validate(request_url, UserDescriptionList)).Users

    async def get_users_by_ids(self, ids: list[str]) -> list[User]:
        get_user_coroutines = map(lambda user_id: self.get_user_by_id(user_id), ids)
        return await asyncio.gather(*get_user_coroutines)

    async def get_set_descriptions(self) -> list[SetDescription]:
        request_url = _construct_request_url(self._root_url, GET_SETS)
        return (await self._get_and_validate(request_url, SetDescriptionList)).Sets

    async def get_set_description(self, name: str) -> SetDescription:
        request_url = _construct_request_url(self._root_url, GET_SET_BY_NAME, name)
        return await self._get_and_validate(request_url, SetDescription)

    async def get_set(self, set_id: str) -> Set:
        request_url = _construct_request_url(self._root_url, GET_SET_BY_ID, set_id)
        return await self._get_and_validate(request_url, Set)

    async def get_sets(self) -> list[Set]:
        set_descriptions = await self.get_set_descriptions()
        set_ids = map(lambda set_description: set_description.id, set_descriptions)
        get_set_coroutines = list(map(lambda set_id: self.get_set(set_id), set_ids))
        return await asyncio.gather(*get_set_coroutines)

    T = TypeVar("T", bound=BaseModel)

    async def _get_and_validate(self, url: str, clss: type[T]) -> T:
        response = (await self._request("GET", url)).json()
        return clss.model_validate(response)

    async def _request(
        self,
        request_type: str,
        url: str,
        params: RequestParameters = None,
        json: Any | None = None,
    ) -> Response:
        response = await self._client.request(
            request_type, url, params=params, json=json
        )
        if response.is_error:
            _handle_error_response(response)
        return response


def _handle_error_response(response: Response) -> None:
    response_bytes = b"".join(c for c in response.iter_bytes())
    raise ApiException(response.status_code, response_bytes)


def _construct_request_url(*path: str) -> str:
    return "/".join(path)
