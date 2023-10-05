from unittest import TestCase

from model.collection import CollectionEntry, MappedCollection, PartVariantEntry


def _create_collection_entry(
    count: int, piece_id: str, material: int
) -> CollectionEntry:
    part_variant_entry = PartVariantEntry.model_validate(
        {"color": material, "count": count}
    )
    collection_entry = CollectionEntry.model_validate(
        {"pieceId": piece_id, "variants": [part_variant_entry]}
    )
    return collection_entry


class TestCollection(TestCase):
    _collection_entries: list[CollectionEntry]
    _collection: MappedCollection

    def setUp(self) -> None:
        self._collection_entries = [
            _create_collection_entry(10, "4x2", 1),
            _create_collection_entry(20, "4x2", 2),
            _create_collection_entry(30, "4x4", 3),
        ]
        self._collection = MappedCollection.from_collection_entries(
            self._collection_entries
        )

    def test_from_collection_entry_list(self) -> None:
        collection = MappedCollection.from_collection_entries(self._collection_entries)
        assert len(collection.entries) == 2
        assert collection.entries.get("4x2").get(1) == 10
        assert collection.entries.get("4x2").get(2) == 20
        assert collection.entries.get("4x4").get(3) == 30

    def test_add_collections(self) -> None:
        extra_collection_entries = [
            _create_collection_entry(10, "3x2", 1),
            _create_collection_entry(20, "3x2", 2),
            _create_collection_entry(30, "4x4", 3),
        ]
        extra_collection = MappedCollection.from_collection_entries(
            extra_collection_entries
        )
        assert extra_collection.entries.get("3x2").get(1) == 10
        assert extra_collection.entries.get("3x2").get(2) == 20
        assert extra_collection.entries.get("4x4").get(3) == 30

        merged_collection = self._collection + extra_collection
        assert merged_collection.entries.get("4x2").get(1) == 10
        assert merged_collection.entries.get("4x2").get(2) == 20
        assert merged_collection.entries.get("4x4").get(3) == 60
