import requests
import os
import math
from newspaper import Article


NEWS_API_SEARCH_URL = "https://newsapi.org/v2/everything?q={}&apiKey={}&language={}&sortBy=relevancy&page={}&pageSize={}"
PAGE_SIZE = 10


def search_articles(keyword,
        article_count,
        language='en'):
    api_key = os.environ['NEWS_API_KEY']
    pages = math.ceil(article_count / PAGE_SIZE)
    articles = []
    for page in range(1, pages+1):
        response = requests.get(NEWS_API_SEARCH_URL.format(keyword, api_key, language, page, PAGE_SIZE)).json()
        remaining = article_count - len(articles)
        if remaining > PAGE_SIZE:
            articles += response['articles'][0:remaining]
        else:
            articles += response['articles']
    return articles


def get_article(url):
    article = Article(url)
    article.download()
    article.parse()
    return article

articles = search_articles("florida", 100)
print(articles)
print("!@#")
print(articles[0]['content'])
print(len(articles[0]['content']))
print(get_article(articles[0]['url']))
