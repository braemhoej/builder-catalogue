from pydantic import BaseModel


class VariantEntry(BaseModel):
    # Ideally the type of the 'color' field should be subtype of Enum, either constructed manually, or fetched from
    # another service and constructed dynamically, i.e. material-registry
    color: str
    count: int


class CollectionEntry(BaseModel):
    pieceId: str
    variants: list[VariantEntry]


class MappedCollection:
    entries: dict[str, dict[str, int]]

    def __init__(self, collection_entries: list[CollectionEntry]):
        for collection_entry in collection_entries:
            design_entry = self.entries.setdefault(collection_entry.pieceId, {})
            # A conscious decision was made here to support multiple entries with the same pieceId.
            for variant_entry in collection_entry.variants:
                design_entry.setdefault(variant_entry.color, 0)
                design_entry[variant_entry.color] += variant_entry.count
            self.entries[collection_entry.pieceId] = design_entry

