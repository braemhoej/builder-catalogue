from pydantic import BaseModel


class PartVariantEntry(BaseModel):
    color: int  # Note: pydantic supports automatic conversion from int to str, i.e. "123" -> 123
    count: int


class CollectionEntry(BaseModel):
    pieceId: str
    variants: list[PartVariantEntry]


class MappedCollection:
    entries: dict[str, dict[int, int]]

    def __init__(self, entries: dict[str, dict[int, int]]):
        self.entries = entries

    @staticmethod
    def from_collection_entries(
        collection_entries: list[CollectionEntry],
    ) -> "MappedCollection":
        entries: dict[str, dict[int, int]] = {}
        for collection_entry in collection_entries:
            design_entry = entries.setdefault(collection_entry.pieceId, {})
            # A conscious decision was made here to support multiple entries with the same pieceId.
            for variant_entry in collection_entry.variants:
                design_entry.setdefault(variant_entry.color, 0)
                design_entry[variant_entry.color] += variant_entry.count
        return MappedCollection(entries)

    def __add__(self, other: "MappedCollection") -> "MappedCollection":
        entries_copy = self.entries.copy()
        for design_id, design_entry_other in other.entries.items():
            design_entry_self = entries_copy.setdefault(design_id, {})
            for color, count in design_entry_other.items():
                design_entry_self.setdefault(color, 0)
                design_entry_self[color] += count
        return MappedCollection(entries_copy)

    def __copy__(self) -> "MappedCollection":
        entries_copy = self.entries.copy()
        return MappedCollection(entries_copy)

    def copy(self) -> "MappedCollection":
        return self.__copy__()
