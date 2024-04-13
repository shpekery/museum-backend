from sqlalchemy.orm import Session

from db import models
from schemas import artifact as artifact_schemas
from typing import List


def get_artifacts_search(db: Session, skip: int = 0, limit: int = 100) -> List[models.ArtifactSearch]:
    return db.query(models.ArtifactSearch).offset(skip).limit(limit).all()


def get_artifact_search_by_id(db: Session, object_id: int) -> models.ArtifactSearch:
    return db.query(models.ArtifactSearch).get(object_id)


def create_artifact_search(db: Session,
                           artifact_search: artifact_schemas.ArtifactSearchCreate) -> models.ArtifactSearch:
    db_artifact_search = models.ArtifactSearch(photo=artifact_search.photo,
                                               is_search=artifact_search.is_search,
                                               is_categorize=artifact_search.is_categorize,
                                               is_generate_description=artifact_search.is_generate_description)
    db.add(db_artifact_search)
    db.commit()
    db.refresh(db_artifact_search)
    return db_artifact_search
