import requests
import os

# ML_URI_API = os.getenv("ML_URI_API")
# ML_URI_API = "https://e1ff-217-197-8-73.ngrok-free.app"
ML_URI_API = ""
test_file_name = 'test_response.jpg'


def search_and_get_category_by_image(binary_image):
    if ML_URI_API:
        files = {'file': binary_image}
        return requests.post(ML_URI_API + '/predict', files=files).json()
    else:
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
                 'Печатная продукция', '0.6389663219451904', False]
            ]
        }


def get_photo_by_name(name):
    if ML_URI_API:
        fold, img = name.split('.')[:2]
        return requests.get(f"{ML_URI_API}/images/?fold={fold}&img={img}").content
    else:
        with open(test_file_name, 'rb') as f:
            return f.read()
