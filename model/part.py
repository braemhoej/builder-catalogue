from pydantic import BaseModel


class Part(BaseModel):
    designID: str
    material: int


class PartEntry(BaseModel):
    part: Part
    quantity: int
