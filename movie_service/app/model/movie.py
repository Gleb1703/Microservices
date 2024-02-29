from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID
from typing import Optional


class Movie(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int]
    movie_name: str
    creation_date: Optional[datetime] = datetime.now()
    genre: str
    director: str