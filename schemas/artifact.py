import datetime

from pydantic import BaseModel, Field

from typing import List, BinaryIO


class Category(BaseModel):
    name: str
    accuracy: float


class ArtifactBase(BaseModel):
    photo: str = Field(description="Фото в формате base64")


class Artifact(ArtifactBase):
    title: str = Field(description="Название", default=None)
    description: str = Field(description="Описание предмета", default=None)
    categories: List[Category] = []
    id: int
    accuracy: float = None


class ArtifactSearchCreate(BaseModel):
    photo: bytes
    is_search_and_categorize: bool
    is_generate_description: bool
    user_session: str


class ArtifactSearch(Artifact):
    search_results: List[Artifact] = []


class ArtifactSearchHistory(ArtifactBase):
    time_created: datetime.datetime
    id: int

    class Config:
        from_attributes = True
