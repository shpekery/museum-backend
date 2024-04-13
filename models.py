from pydantic import BaseModel, Field

from typing import List


class Artifact(BaseModel):
    description: str = Field(description="Описание предмета")
    photo: str = Field(description="Фото в формате base64")


class SearchHistory(BaseModel):
    timestamp: float
    photo: str = Field(description="Фото в формате base64")
    results: List[Artifact]


class ProduceResponse(BaseModel):
    description: str = None
    category: str = None
    search_results: List[Artifact] = None
