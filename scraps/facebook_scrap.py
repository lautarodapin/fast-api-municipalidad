import asyncio
from typing import List
from facebook_scraper import get_posts
from schemas import FacebookPost

HCD_FACEBOOK_USERNAME: str = 'hcdvillamercde'
DATE_REGEX = r'(\d{1,2})[-/](\d{1,2})[/-](\d{1,4})'

async def get_hcd_posts(page_limit: int = 1) -> List[FacebookPost]:
    posts: List[FacebookPost] = []
    for post in get_posts(HCD_FACEBOOK_USERNAME, pages=page_limit):
        post = FacebookPost(**post)
        posts.append(post)
    return posts