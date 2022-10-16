"""
Описание моделей данных (DTO).
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class NewsItemDTO(BaseModel):
    """
    Модель данных для представления новости.
    """

    source: str
    author: Optional[str]
    title: str
    description: Optional[str]
    url: Optional[str]
    published_at: datetime
