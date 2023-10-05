from typing import Any

from pydantic import BaseModel

from model.part import Part


class SetCompletableResponse(BaseModel):
    completable: bool
    missing_parts: list[tuple[Part, int]] | None

    def __init__(
        self,
        completable: bool,
        missing_parts: list[tuple[Part, int]] | None,
        **data: Any,
    ):
        super().__init__(**data)
        self.completable = completable
        self.missing_parts = missing_parts


class CompletableSetsResponse(BaseModel):
    completable_sets: list[dict[str, str]]

    def __init__(self, completable_sets: list[dict[str, str]], **data: Any):
        super().__init__(**data)
        self.completable_sets = completable_sets
