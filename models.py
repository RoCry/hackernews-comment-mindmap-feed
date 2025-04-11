import json
import asyncio
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, HttpUrl, Field, field_serializer

# https://www.jsonfeed.org/version/1.1/


class FeedItem(BaseModel):
    id: str
    url: Optional[str] = None
    title: str
    content_html: str
    date_published: datetime
    external_url: Optional[str] = None
    image: Optional[HttpUrl] = None
    
    @field_serializer('date_published')
    def serialize_dt(self, dt: datetime):
        return dt.isoformat()
    
class JSONFeed(BaseModel):
    version: str = "https://jsonfeed.org/version/1.1"
    title: str
    home_page_url: Optional[str] = None
    feed_url: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[HttpUrl] = None
    favicon: Optional[HttpUrl] = None
    items: List[FeedItem] = Field(default_factory=list)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    @field_serializer('updated_at')
    def serialize_dt(self, dt: datetime):
        return dt.isoformat()
    
    def save_to_json(self, filepath: str) -> None:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(self.model_dump_json(indent=2))

    @classmethod
    def load_from_json(cls, filepath: str) -> "JSONFeed":
        with open(filepath, "r", encoding="utf-8") as f:
            return cls.model_validate_json(f.read())
