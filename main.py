from tools.rssfeeder import load_rss_feed


import os
from dotenv import load_dotenv
from pprint import pprint


# load .env file
load_dotenv()

# main program
def main():
    
    # configurations.
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
    OLLAMA_EMBEDDING_MODEL = os.getenv("OLLAMA_EMBEDDING_MODEL")
    PRESIST_DIRECTORY = os.getenv("CHROMADB_PATH")
    
    # rss news feed links (EN: English, ZN: Chinese)
    RSS_FEED_URL_EN = os.getenv("RSS_FEED_URL_EN")
    RSS_FEED_URL_ZN = os.getenv("RSS_FEED_URL_ZN")
    
    # fetch rss feed from url.
    feed_dicts = load_rss_feed(rss_url=RSS_FEED_URL_ZN)
    # print(f"Total no of feeds: {len(feed_dicts)}\n")
    # print(f"Sample feed dict:")
    # pprint(feed_dicts[0])
    
    # 
    
    
    return



# main program entry point.
if __name__ == "__main__":
    main()
