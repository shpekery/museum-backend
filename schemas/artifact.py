import datetime

from pydantic import BaseModel, Field

from typing import List, BinaryIO


class ArtifactBase(BaseModel):
    photo: str = Field(description="Фото в формате base64")


class Artifact(ArtifactBase):
    description: str = Field(description="Описание предмета", default=None)
    categories: List[str] = []
    id: int


class ArtifactSearchCreate(BaseModel):
    photo: bytes
    is_search: bool
    is_categorize: bool
    is_generate_description: bool


class ArtifactSearch(Artifact):
    search_results: List[Artifact] = []


class ArtifactSearchHistory(ArtifactBase):
    time_created: datetime.datetime
    id: int

    class Config:
        from_attributes = True
