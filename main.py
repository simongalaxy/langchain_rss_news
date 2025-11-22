from tools.rssfeeder import load_rss_feed
from tools.ChromaDBHandler import ChromaDBHandler


from tools.save_to_text import write_rss_to_file
from tools.chat_with_rss_news import run_chat_loop

import os
from dotenv import load_dotenv

# load .env file
load_dotenv()


# main program.
def main():
    
    # chat model configurations.
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
    
    # sqlite3 database configurations.
    SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH")
    SQLITE_DB_FILE = os.getenv("SQLITE_DB_FILE")
    
    # ChromaDB configurations.
    OLLAMA_EMBEDDING_MODEL = os.getenv("OLLAMA_EMBEDDING_MODEL")
    PERSIST_DIRECTORY = os.getenv("CHROMADB_PATH")
    
    # rss news feed links (EN: English, ZN: Chinese)
    RSS_FEED_URL_EN = os.getenv("RSS_FEED_URL_EN")
    RSS_FEED_URL_ZN = os.getenv("RSS_FEED_URL_ZN")
    
    # fetch rss feed from url.
    feeds = load_rss_feed(rss_url=RSS_FEED_URL_EN)
    
    # save rss feeds into text file for checking.
    write_rss_to_file(feeds=feeds)
    
    # write feeds to chromaDB.
    # initiate ChromaDB object.
    # chromaDB = ChromaDBHandler(
    #     persist_directory=PERSIST_DIRECTORY,
    #     ollama_embedding_model=OLLAMA_EMBEDDING_MODEL
    #     )
    
    # for feed in feeds:
    #     chromaDB.add_text(text=feed["Content"], metadata=feed["metadata"], doc_id=feed["Id"])
    
    # run chat loop
    run_chat_loop(
        persist_directory=PERSIST_DIRECTORY,
        ollama_model=OLLAMA_MODEL,
        ollama_embedding_model=OLLAMA_EMBEDDING_MODEL
    )
    
    return



# main program entry point.
if __name__ == "__main__":
    main()
