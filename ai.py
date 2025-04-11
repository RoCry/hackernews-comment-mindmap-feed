from typing import Literal

from smolllm import ask_llm


# returns the markdown file path
async def generate_social_comments_markdown_summary(
    title: str,
    comments: str,
    model: str = "grok/grok-3",
    language: str = "zh",
) -> str:
    prompt = social_comments_to_mindmap_markdown(title, comments, language)
    return await ask_llm(prompt, model=model, remove_backticks=True, timeout=300)


_MINDMAP_MD_RESPONSE_FORMAT_EXAMPLE = """
# Response Format Example
```
# Generate a proper title to summarize the following content

## SUBTITLE HERE
- Point 1
  - Subpoint 1.1
  - Subpoint 1.2
- Point 2

## ANOTHER SUBTITLE HERE
- Point 3
  - Subpoint 3.1
    - Subsubpoint 3.1.1
    - Subsubpoint 3.1.2
- Point 4
```
"""


# convert lang code or name to prompt string
def _lang_to_prompt_str(lang: Literal["en", "zh"] | str | None) -> str:
    if lang is None:
        return ""
    lang = lang.lower()
    if lang == "en" or lang == "english":
        return " in English"
    elif lang == "zh" or lang == "cn" or lang == "chinese":
        return " in Simplified Chinese(but keep names in original language)"
    elif lang == "zh-tw" or lang == "traditional" or lang == "traditional chinese":
        return " in Traditional Chinese(but keep names in original language)"
    else:
        print(f"Unknown language: {lang}, fallback to English")
        return " in English"


def social_comments_to_mindmap_markdown(
    title: str,
    comments: str,
    lang: Literal["en", "zh"] | str | None = "en",
) -> str:
    lang = _lang_to_prompt_str(lang)

    prompt = f"""
Extract the main points{lang} using markdown format from the following user comments:

{_MINDMAP_MD_RESPONSE_FORMAT_EXAMPLE}

# Title about the story
{title}

# Comments
{comments}

# Note
- Only include the table of contents, no other text, no explanation, do not wrap the response in ```
- For each point, do not ends with a period
"""
    return prompt
