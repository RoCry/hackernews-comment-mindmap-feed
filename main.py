import asyncio

from hn import fetch_top_stories
from ai import generate_social_comments_markdown_summary

async def main():
    # TODO:
    # fetch the top story and related comments from hackernews
    stories = await fetch_top_stories(top_n=1, comment_levels_count=3)

    for story in stories:
        # Flatten the nested lists returned by format_tree
        comments_lines = [line for comment in story.comments for line in comment.format_tree(max_length=0)]
        comments_str = "\n".join(comments_lines)
        resp = await generate_social_comments_markdown_summary(story.title, comments_str)
        print(resp)

    # generate toc for each story.comments
    # generate mindmap for each story
    # generate a feed of mindmaps
    pass


if __name__ == "__main__":
    asyncio.run(main())
