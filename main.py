from flask import Flask
from flask import render_template
from flask import request

import concurrent.futures
import statistics

import news
import sentiment

import time

app = Flask(__name__)


def get_article_with_score(url):
    article = news.get_article(url)
    score = sentiment.vader_sentiment(article.text)
    return (article, score)


@app.route('/')
def index():
    return render_template('index.html',
            search_type='twitter')


@app.route('/search-news', methods=['POST'])
def search_news():
    print(request.form)
    query = request.form.get('query')
    from_date = request.form.get('start_date')
    to_date = request.form.get('end_date')
    articles_list = news.search_articles(
            query,
            100,
            from_date=from_date,
            to_date=to_date)

    articles = []
    sentiment_scores = {}

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []

        for article_summary in articles_list:
            futures.append(executor.submit(get_article_with_score, article_summary['url']))

        for future in concurrent.futures.as_completed(futures):
            try:
                article, score = future.result()
                articles.append(article)
                sentiment_scores[article.url] = score
            except:
                # TODO
                pass

    mean_score = statistics.mean(sentiment_scores.values())
    median_score = statistics.median(sentiment_scores.values())
    std_dev = statistics.stdev(sentiment_scores.values())

    return render_template('index.html',
            search_type='news',
            articles=articles,
            form=request.form,
            sentiment_scores=sentiment_scores,
            mean_sentiment_score=mean_score,
            median_sentiment_score=median_score,
            std_dev_sentiment_scores=std_dev
            )


if __name__ == '__main__':
    app.run(debug=True)
