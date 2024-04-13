from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, BLOB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from db.database import Base


class ArtifactSearch(Base):
    __tablename__ = "artifact_search"

    id = Column(Integer, primary_key=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    photo = Column(BLOB)
