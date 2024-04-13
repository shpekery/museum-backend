import base64
import random
import time
import os

from fastapi import APIRouter, UploadFile, Depends
from sqlalchemy.orm import Session

from schemas.artifact import Artifact, ArtifactSearchHistory, ArtifactSearchCreate, ArtifactSearch
from db.methods import get_artifacts_search, create_artifact_search, get_artifact_search_by_id
from db.core import get_db

from typing import List, Union

router = APIRouter(prefix='/search_artifact')

# TODO в конфиг вынести
test_file_name = 'test_response.jpg'


def get_file_base64(file_path):
    with open(file_path, 'rb') as f:
        return blob_to_base64(f.read())


def blob_to_base64(blob):
    return base64.b64encode(blob).decode('utf-8')


def generate_test_search_results():
    search_results = []
    test_file_base64 = get_file_base64(test_file_name)
    for i in range(10):
        search_results.append(Artifact(
            id=random.randint(1, 1000),
            description="Шашка драгунская офицерская обр. 1881 г.",
            photo=test_file_base64
        ))

    return search_results


def generate_test_search_history():
    search_history = []
    for i in range(5):
        search_history.append(ArtifactSearchHistory(
            timestamp=time.time() - 86400 * i,
            photo=get_file_base64(test_file_name),
            results=generate_test_search_results()
        ))
    return search_history


@router.post("",
             name="Загрузка фото для поиска",
             description="Фото загружается на сервер, получает свой айди, который возвращается."
                         " В дальнейшем по айди можно запросить результаты поиска.")
async def upload_artifact_search(
        file: UploadFile, db: Session = Depends(get_db),
        is_search: Union[bool, None] = False,
        is_categorize: Union[bool, None] = False,
        is_generate_description: Union[bool, None] = False,

) -> int:
    photo_content = await file.read()
    artifact_search = create_artifact_search(db, ArtifactSearchCreate(photo=photo_content,
                                                                      is_search=is_search,
                                                                      is_categorize=is_categorize,
                                                                      is_generate_description=is_generate_description))
    return artifact_search.id


@router.get("/history")
def get_search_history(db: Session = Depends(get_db)) -> List[ArtifactSearchHistory]:
    response = []
    for artifact_search in get_artifacts_search(db, limit=10):
        artifact_search.photo = blob_to_base64(artifact_search.photo)
        response.append(ArtifactSearchHistory.from_orm(artifact_search))
    return response


@router.get("/{artifact_search_id}")
def get_artifact_search_info(artifact_search_id: int,
                             db: Session = Depends(get_db)) -> ArtifactSearch:
    artifact_search = get_artifact_search_by_id(db, artifact_search_id)
    is_search = artifact_search.is_search
    is_categorize = artifact_search.is_categorize
    is_generate_description = artifact_search.is_generate_description

    response = ArtifactSearch(photo=blob_to_base64(artifact_search.photo), id=artifact_search.id)
    search_results = generate_test_search_results()
    description = "Красивый меч цвета BMW M8 Competition"
    categories = ["Оружие"]

    if is_search:
        response.search_results = search_results
    if is_categorize:
        response.description = description
    if is_generate_description:
        response.categories = categories

    return response
