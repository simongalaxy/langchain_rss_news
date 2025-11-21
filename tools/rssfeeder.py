import feedparser

from tools.webscraper import fetch_news_content


# fetch the rss feed from url.
def load_rss_feed(rss_url: str) -> list[dict]:
    feed_dicts = []
   
    feed = feedparser.parse(rss_url)
    
    # filter some of the entry from each feeds.
    for entry in feed.entries:
        dict = {
            "Id": entry.id,
            "Title": entry.title,
            "Link": entry.link,
            "Publish_date": entry.published,
            "Content": fetch_news_content(news_url=entry.link)   
        }
        feed_dicts.append(dict)
    
    return feed_dicts
    
