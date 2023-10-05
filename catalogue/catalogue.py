from api.async_api_client import AsyncApiClient
from model.collection import MappedCollection
from model.part import Part
from model.set import Set
from model.user import User


def compute_missing_parts(
    set: Set, collection: MappedCollection
) -> list[tuple[Part, int]]:
    missing_parts = []
    for part_entry in set.pieces:
        design_id = part_entry.part.designID
        colour_code = part_entry.part.material
        required_quantity = part_entry.quantity

        part_variants = collection.entries.get(design_id, {})
        quantity_in_collection = part_variants.get(colour_code, 0)
        if quantity_in_collection < required_quantity:
            missing_parts.append(
                (part_entry.part, required_quantity - quantity_in_collection)
            )

    return missing_parts if len(missing_parts) != 0 else None


def completable(set: Set, collection: MappedCollection) -> bool:
    missing_parts = compute_missing_parts(set, collection)
    return missing_parts is None


class Catalogue:
    _client: AsyncApiClient

    def __init__(self, client: AsyncApiClient):
        self._client = client

    async def find_collaborators_for_user(
        self, set_id: str, user_id: str
    ) -> list[User]:
        set = await self._client.get_set(set_id)
        user = await self._client.get_user_by_id(user_id)
        user_collection = user.get_mapped_collection()

        potential_collaborators: list[User] = []
        collaborators = filter(
            lambda usr: usr.id != user_id, await self._client.get_users()
        )

        for collaborator in collaborators:
            collaborator_collection = collaborator.get_mapped_collection()
            combined_collection = user_collection + collaborator_collection
            if completable(set, combined_collection):
                potential_collaborators.append(collaborator)

        return potential_collaborators

    async def get_missing_parts_from_set_by_user(
        self, set_id: str, user_id: str, collaborator_ids: list[str] | None = None
    ) -> list[tuple[Part, int]]:
        set = await self._client.get_set(set_id)
        user = await self._client.get_user_by_id(user_id)
        collection = user.get_mapped_collection()

        if collaborator_ids is not None:
            collection = await self._compute_combined_collection(
                collection, collaborator_ids
            )

        return compute_missing_parts(set, collection)

    async def get_completable_sets_by_user(
        self, user_id: str, collaborator_ids: list[str] | None = None
    ) -> list[dict[str, str]]:
        sets = await self._client.get_sets()
        user = await self._client.get_user_by_id(user_id)
        collection = user.get_mapped_collection()

        if collaborator_ids is not None:
            collection = await self._compute_combined_collection(
                collection, collaborator_ids
            )

        completable_sets = []
        for set in sets:
            if completable(set, collection):
                completable_sets.append(
                    {"name": set.name, "setNumber": set.setNumber, "id": set.id}
                )

        return completable_sets

    async def _compute_combined_collection(
        self, collection: MappedCollection, collaborator_ids: list[str]
    ) -> MappedCollection:
        total_collection = collection.copy()
        collaborators = await self._client.get_users_by_ids(collaborator_ids)
        for collaborator in collaborators:
            collaborator_collection = collaborator.get_mapped_collection()
            total_collection += collaborator_collection
        return total_collection
