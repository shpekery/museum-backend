import os.path
import time

import uvicorn
import aiofiles
import base64

from uuid import uuid4
from fastapi import FastAPI, UploadFile
from models import Artifact, SearchHistory, ProduceResponse
from typing import List, Union

upload_folder = 'upload'
photo_extension = '.jpg'
test_file_name = 'test_response.jpg'

app = FastAPI()

if upload_folder not in os.listdir():
    os.mkdir(upload_folder)


def get_file_base64(file_path):
    with open(file_path, 'rb') as img:
        # Открываем файл изображения в бинарном режиме
        return base64.b64encode(img.read()).decode('utf-8')


def generate_test_search_results():
    search_results = []
    test_file_base64 = get_file_base64(test_file_name)
    for i in range(10):
        search_results.append(Artifact(
            description="Шашка драгунская офицерская обр. 1881 г.",
            photo=test_file_base64
        ))

    return search_results


def generate_test_search_history():
    search_history = []
    for i in range(5):
        search_history.append(SearchHistory(
            timestamp=time.time() - 86400 * i,
            photo=get_file_base64(test_file_name),
            results=generate_test_search_results()
        ))
    return search_history


@app.post("/produce",
          name="Обработка фото от пользователя",
          description="Обработка фото от пользователя",
          response_model=ProduceResponse)
async def read_item(
        file: UploadFile,
        is_search: Union[bool, None] = False,
        is_categorize: Union[bool, None] = False,
        is_generate_description: Union[bool, None] = False) -> ProduceResponse:
    response = ProduceResponse()

    file_name = str(uuid4()) + '.jpg'
    file_path = os.path.join('./' + upload_folder, file_name)
    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)

    # работа с моделью
    search_results = generate_test_search_results()
    description = "Красивый меч цвета BMW M8 Competition"
    category = "Оружие"

    response.search_results = search_results
    response.description = description
    response.category = category

    return response


@app.get("/search_history")
def get_search_history() -> List[SearchHistory]:
    return generate_test_search_history()


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=5000)
