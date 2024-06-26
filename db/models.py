from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from db.database import Base


class ArtifactSearch(Base):
    __tablename__ = "artifact_search"

    id = Column(Integer, primary_key=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    photo = Column(BYTEA, nullable=False)
    is_search_and_categorize = Column(Boolean, default=False)
    is_generate_description = Column(Boolean, default=False)
    user_session = Column(String, nullable=False)
