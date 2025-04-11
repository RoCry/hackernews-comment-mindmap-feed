import asyncio
import os
import json
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path

from hn import fetch_top_stories
from ai import generate_social_comments_markdown_summary
from models import FeedItem, JSONFeed

async def generate_mindmap_html(markdown_content, output_file):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as temp_md:
        temp_md.write(markdown_content)
        temp_md_path = temp_md.name
    
    try:
        # Run markmap-cli to convert markdown to HTML mindmap
        subprocess.run([
            'npx', 'markmap-cli', 
            temp_md_path, 
            '--no-open', 
            '--no-toolbar',
            '-o', output_file
        ], check=True)
        
        # Read the generated HTML content
        with open(output_file, 'r') as f:
            html_content = f.read()
            
        return html_content
    finally:
        # Clean up temporary file
        os.unlink(temp_md_path)

async def main():
    # Create outputs directory if it doesn't exist
    outputs_dir = Path("outputs")
    outputs_dir.mkdir(exist_ok=True)
    
    # fetch the top story and related comments from hackernews
    stories = await fetch_top_stories(top_n=1, comment_levels_count=3)
    
    # Initialize the JSON feed
    feed = JSONFeed(
        title="HackerNews Top Stories Mindmap",
        home_page_url="https://news.ycombinator.com/",
        feed_url="https://raw.githubusercontent.com/username/hackernews-mindmap-feed/main/outputs/feed.json",
        description="Mindmaps of top HackerNews stories and their comments",
        updated_at=datetime.utcnow()
    )
    
    # Generate mindmaps for each story
    for idx, story in enumerate(stories):
        # Format comments into markdown
        comments_lines = [line for comment in story.comments for line in comment.format_tree(max_length=0)]
        comments_markdown = "\n".join(comments_lines)
        
        # Generate AI summary
        markdown_summary = await generate_social_comments_markdown_summary(story.title, comments_markdown)
        
        # Generate mindmap HTML
        mindmap_html_path = outputs_dir / f"mindmap_{story.id}.html"
        html_content = await generate_mindmap_html(markdown_summary, str(mindmap_html_path))
        
        # Create feed item
        feed_item = FeedItem(
            id=str(story.id),
            url=story.url if story.url else f"https://news.ycombinator.com/item?id={story.id}",
            title=story.title,
            content_html=html_content,
            date_published=story.time,
            external_url=f"https://news.ycombinator.com/item?id={story.id}"
        )
        
        feed.items.append(feed_item)
        
        print(f"Generated mindmap for: {story.title}")
    
    # Save feed to JSON file
    feed.save_to_json(outputs_dir / "feed.json")
    
    print(f"Generated JSON feed with {len(feed.items)} items")


if __name__ == "__main__":
    asyncio.run(main())
