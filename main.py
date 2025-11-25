from tools.rssfeeder import load_rss_feed
from tools.ChromaDBHandler import ChromaDBHandler
from tools.save_to_text import write_rss_to_file
from tools.chat_with_rss_news import run_chat_loop
# from tools.sqliteDBHandler import SQLiteDBHandler


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
    # initiate sqliteDBHandler object.
    # sqliteDB = SQLiteDBHandler(
    #     db_path=SQLITE_DB_PATH,
    #     db_filename=SQLITE_DB_FILE
    #     )
    
    # ChromaDB configurations.
    # OLLAMA_EMBEDDING_MODEL = os.getenv("OLLAMA_EMBEDDING_MODEL")
    HUGGINGFACE_EMBEDDING_MODEL = os.getenv("HUGGINGFACE_EMBEDDING_MODEL")
    PERSIST_DIRECTORY = os.getenv("CHROMADB_PATH")
    
    # rss news feed links (EN: English, ZN: Chinese)
    RSS_FEED_URL_EN = os.getenv("RSS_FEED_URL_EN")
    RSS_FEED_URL_ZN = os.getenv("RSS_FEED_URL_ZN")
    
    # fetch rss feed from url.
    feeds = load_rss_feed(rss_url=RSS_FEED_URL_EN)
    # for item in feeds:
    #     # save rss item into sqliteDB.
    #     sqliteDB.add_rss_item(item=item)
    
    # save rss feeds into text file for checking.
    write_rss_to_file(feeds=feeds)
    
    # write feeds to chromaDB.
    # initiate ChromaDB object.
    chromaDB = ChromaDBHandler(
        persist_directory=PERSIST_DIRECTORY,
        embedding_model=HUGGINGFACE_EMBEDDING_MODEL
        )
    
    # load rss feeds into chromaDB.
    chromaDB.add_feeds_to_chromadb(feeds=feeds)
    
    # # run chat loop
    run_chat_loop(
        ChromaDB=chromaDB,
        ollama_model=OLLAMA_MODEL
    )
    
    return



# main program entry point.
if __name__ == "__main__":
    main()
