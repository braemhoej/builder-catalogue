from unittest import TestCase

from api.api_endpoint_config import ROOT_URL
from api.async_api_client import AsyncApiClient
from model.set import Set, SetDescription
from model.user import UserDescription
from util.async_util import run_async


class TestAsyncApiClient(TestCase):
    _client: AsyncApiClient

    @classmethod
    def setUpClass(cls) -> None:
        cls._client = AsyncApiClient(ROOT_URL)

    def test_get_users(self):
        users = run_async(self._client.get_users())
        assert len(users) > 0
        for user in users:
            assert isinstance(user, UserDescription)
            assert isinstance(user.username, str)
            assert isinstance(user.id, str)
            assert isinstance(user.location, str)
            assert isinstance(user.brickCount, int)

    def test_get_user(self):
        user = run_async(self._client.get_user_by_username("brickfan35"))
        assert isinstance(user, UserDescription)
        assert user.username == "brickfan35"
        assert user.id == "6d6bc9f2-a762-4a30-8d9a-52cf8d8373fc"
        assert user.brickCount == 1413
        assert user.location == "UKY"

    def test_get_set_summaries(self):
        sets = run_async(self._client.get_set_descriptions())
        assert len(sets) > 0
        for s in sets:
            assert isinstance(s, SetDescription)
            assert s.name is not None
            assert isinstance(s.name, str)
            assert isinstance(s.id, str)
            assert isinstance(s.setNumber, str)
            assert isinstance(s.totalPieces, int)

    def test_get_set_summary(self):
        s = run_async(self._client.get_set_description("alien-spaceship"))
        assert isinstance(s, SetDescription)
        assert s.name == "alien-spaceship"
        assert s.id == "040f11ab-e301-4724-bacd-50841816e06b"
        assert s.setNumber == "497XX"
        assert s.totalPieces == 1050

    def test_get_set(self):
        s = run_async(self._client.get_set("040f11ab-e301-4724-bacd-50841816e06b"))
        assert isinstance(s, Set)
        assert s.id == "040f11ab-e301-4724-bacd-50841816e06b"
        assert s.totalPieces == 1050
        assert s.setNumber == "497XX"
        assert len(s.pieces) > 0
        for part_count in s.pieces:
            part = part_count.part
            count = part_count.quantity
            assert part is not None
            assert count > 0

