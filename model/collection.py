from pydantic import BaseModel


class VariantEntry(BaseModel):
    color: int  # Note: pydantic supports automatic conversion from int to str, i.e. "123" -> 123
    count: int


class CollectionEntry(BaseModel):
    pieceId: str
    variants: list[VariantEntry]


class MappedCollection:
    entries: dict[str, dict[int, int]]

    def __init__(self, collection_entries: list[CollectionEntry]):
        for collection_entry in collection_entries:
            design_entry = self.entries.setdefault(collection_entry.pieceId, {})
            # A conscious decision was made here to support multiple entries with the same pieceId.
            for variant_entry in collection_entry.variants:
                design_entry.setdefault(variant_entry.color, 0)
                design_entry[variant_entry.color] += variant_entry.count
            self.entries[collection_entry.pieceId] = design_entry
