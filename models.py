import json
from datetime import datetime
from typing import Any, Dict, List

from pydantic import BaseModel, HttpUrl

# https://www.jsonfeed.org/version/1.1/


class FeedItem(BaseModel):
    id: str
    url: HttpUrl
    title: str
    content_html: str
    image: HttpUrl
    date_published: datetime
    date_modified: datetime
    _social_mindmap: Dict[str, Any]


class Feed(BaseModel):
    version: str = "https://jsonfeed.org/version/1.1"
    title: str
    home_page_url: HttpUrl
    feed_url: HttpUrl
    description: str
    items: List[FeedItem] = []

    def save_to_json(self, filepath: str) -> None:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(
                self.model_dump(exclude_none=True), f, ensure_ascii=False, indent=2
            )

    @classmethod
    def load_from_json(cls, filepath: str) -> "Feed":
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            return cls.model_validate(data)
