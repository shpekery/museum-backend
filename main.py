import os.path

import uvicorn

from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from db import models, database

from routers import artifact_search

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Пыоиска по фото среди музейных экспонатов")

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(artifact_search.router)

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=5000)
