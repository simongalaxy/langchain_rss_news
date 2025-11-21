import requests
from bs4 import BeautifulSoup


# fetch news content from url.
def fetch_news_content(news_url: str) -> str:
    
    # fetch news html from url.
    response = requests.get(url=news_url)
    response.encoding = response.apparent_encoding
    
    # parse the main news content.
    soup = BeautifulSoup(response.content, "html.parser")
    article = soup.find("span", id="pressrelease")
    if article:
        return article.get_text(separator="\n", strip=True)
    else:
        return f"Main content not found from {news_url}"
    
    
    #contentBody