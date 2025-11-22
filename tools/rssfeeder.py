from tools.webscraper import fetch_news_content

import feedparser

from datetime import datetime
import email.utils

# transform datetime in rss publish date to ISO 8601 string (text storage).
def transform_date_to_text(date: str) -> str:
    dt = email.utils.parsedate_to_datetime(data=date)
    
    return dt.isoformat()


# fetch the rss feed from url.
def load_rss_feed(rss_url: str) -> list[dict]:
    feed_dicts = []
   
    feed = feedparser.parse(rss_url)
    
    # filter some of the entry from each feeds.
    for entry in feed.entries:
        dict = {
            "Id": entry.id,
            "Content": fetch_news_content(news_url=entry.link),
            "metadata": {
                "Title": entry.title,
                "Link": entry.link,
                "Publish_date": entry.published,
                "Publish_date_text": transform_date_to_text(date=entry.published)
            }
        }
        feed_dicts.append(dict)
    
    return feed_dicts
    
