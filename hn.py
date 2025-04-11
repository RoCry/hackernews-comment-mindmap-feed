from typing import List

from hackernews import HackerNewsClient, Story


# fetch hackernews comments and returns markdown for llm
async def fetch_top_stories(
    top_n: int = 3, comment_levels_count: int = 1
) -> List[Story]:
    async with HackerNewsClient(cache_db_path="cache/hn.sqlite") as client:
        # Get top story IDs
        resp = await client.fetch_top_stories(
            top_n=top_n, fetch_comment_levels_count=comment_levels_count
        )
        return resp.stories
