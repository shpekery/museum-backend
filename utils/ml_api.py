import requests
import os

ML_URI_API = os.getenv("ML_URI_API")
if ML_URI_API is None:
    ML_URI_API = "https://0880-217-197-8-73.ngrok-free.app"
TEST_PHOTO_NAME = os.getenv("TEST_PHOTO_NAME")
if TEST_PHOTO_NAME is None:
    TEST_PHOTO_NAME = 'test_response.jpg'

print(ML_URI_API, TEST_PHOTO_NAME)


def search_and_get_category_by_image(binary_image, description=False):
    if ML_URI_API:
        files = {'file': binary_image}
        return requests.post(ML_URI_API + f'/predict?description={description}', files=files).json()
    else:
        description_dict = {}
        if description:
            description_dict = {
                "caption_1": "Музейная фотография молодого человека с очень короткой стрижкой",
                "caption_2": "человек, который родился с очень серьезным лицом"
            }

        return {
            "class": [
                [
                    "Редкие книги",
                    0.6986414790153503
                ],
                [
                    "ДПИ",
                    0.19446881115436554
                ],
                [
                    "Скульптура",
                    0.06164960190653801
                ],
            ],
            "similar_images": [
                ['19941100.20647862.jpg', 'Открытка поздравительная',
                 'рисунок В.Киреева, оборотная сторона без надписей, издательство "Плакат", Москва, 1978 год',
                 'Печатная продукция', '0.6389663219451904', False] for i in range(10)
            ],
            "description": description_dict
        }


def get_photo_by_name(name):
    if ML_URI_API:
        fold, img = name.split('.')[:2]
        return requests.get(f"{ML_URI_API}/images/?fold={fold}&img={img}").content
    else:
        if TEST_PHOTO_NAME:
            with open(TEST_PHOTO_NAME, 'rb') as f:
                return f.read()
        else:
            raise ValueError("Не указано тестовое фото")
