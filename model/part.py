from enum import Enum

from pydantic import BaseModel


class PartType(str, Enum):
    rigid = "rigid"
    # ... and all other enum variations.


class Part(BaseModel):
    designID: str
    material: int
    partType: PartType


class PartEntry(BaseModel):
    part: Part
    quantity: int
