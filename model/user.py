from pydantic import BaseModel

from model.collection import CollectionEntry, MappedCollection


class UserDescription(BaseModel):
    id: str
    username: str
    location: str
    brickCount: int


class User(UserDescription):
    collection: list[CollectionEntry]
    _mapped_collection: MappedCollection

    def __init__(self, **kw):
        super().__init__(**kw)
        self._mapped_collection = MappedCollection(self.collection)

    def get_mapped_collection(self) -> MappedCollection:
        return self._mapped_collection


class UserDescriptionList(BaseModel):
    Users: list[UserDescription]
