from pydantic import BaseModel

from model.part import PartEntry


class SetDescription(BaseModel):
    # Further validation could be imposed on both the id and setNumber fields.
    id: str
    name: str
    setNumber: str
    totalPieces: int


class Set(SetDescription):
    pieces: list[PartEntry]


class SetDescriptionList(BaseModel):
    Sets: list[SetDescription]
