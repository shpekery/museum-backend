import base64
import random
import time
import os

from fastapi import APIRouter, UploadFile, Depends, Request
from sqlalchemy.orm import Session

from schemas.artifact import Artifact, ArtifactSearchHistory, ArtifactSearchCreate, ArtifactSearch, Category
from db.methods import get_artifacts_search, create_artifact_search, get_artifact_search_by_id
from db.core import get_db

from utils import ml_api

from typing import List, Union

router = APIRouter(prefix='/search_artifact')


def get_file_base64(file_path):
    with open(file_path, 'rb') as f:
        return blob_to_base64(f.read())


def blob_to_base64(blob):
    return "data:image/png;base64," + base64.b64encode(blob).decode('utf-8')


@router.post("",
             name="Загрузка фото для поиска",
             description="Фото загружается на сервер, получает свой айди, который возвращается."
                         " В дальнейшем по айди можно запросить результаты поиска.")
async def upload_artifact_search(
        user_session: str,
        file: UploadFile, db: Session = Depends(get_db),
        is_search_and_categorize: Union[bool, None] = False,
        is_generate_description: Union[bool, None] = False,
) -> int:
    photo_content = await file.read()
    artifact_search = create_artifact_search(db, ArtifactSearchCreate(photo=photo_content,
                                                                      is_search_and_categorize=is_search_and_categorize,
                                                                      is_generate_description=is_generate_description,
                                                                      user_session=user_session))
    return artifact_search.id


@router.get("/history")
def get_search_history(user_session: str,
                       db: Session = Depends(get_db)) -> List[ArtifactSearchHistory]:
    response = []
    for artifact_search in get_artifacts_search(db, user_session, limit=10):
        artifact_search.photo = blob_to_base64(artifact_search.photo)
        response.append(ArtifactSearchHistory.from_orm(artifact_search))
    return response[::-1]


@router.get("/{artifact_search_id}")
async def get_artifact_search_info(artifact_search_id: int,
                             db: Session = Depends(get_db)) -> ArtifactSearch:
    artifact_search = get_artifact_search_by_id(db, artifact_search_id)
    is_search_and_categorize = artifact_search.is_search_and_categorize
    is_generate_description = artifact_search.is_generate_description

    response = ArtifactSearch(photo=blob_to_base64(artifact_search.photo), id=artifact_search.id)

    data = ml_api.search_and_get_category_by_image(artifact_search.photo)

    if is_search_and_categorize:
        categories = []
        search_results = []

        for category in data['class']:
            categories.append(Category(name=category[0], accuracy=category[1]))

        for result in data['similar_images']:
            photo_name = result[0]
            title = result[1]
            description = result[2]
            category = Category(name=result[3], accuracy=1)
            accuracy = float(result[4])

            photo_data = ml_api.get_photo_by_name(photo_name)
            search_results.append(Artifact(
                id=int(photo_name.split('.')[0]),
                description=description,
                title=title,
                categories=[category],
                photo=blob_to_base64(photo_data),
                accuracy=accuracy
            ))
        response.search_results = search_results
        response.categories = categories
    if is_generate_description:
        response.description = description

    return response
