from datetime import datetime

from pydantic import BaseModel

# TODO: lets implement the basic models for jsonfeed https://www.jsonfeed.org/version/1.1/
class FeedItem(BaseModel):

# https://www.jsonfeed.org/version/1.1/
class Feed(BaseModel):
    version: str = "https://www.jsonfeed.org/version/1.1"
    items: list[FeedItem]

