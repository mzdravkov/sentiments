from flask import Flask
from flask import render_template
from flask import request

import concurrent.futures
import statistics

import news
import sentiment

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search-news', methods=['POST'])
def search_news():
    print(request.form)
    query = request.form.get('query')
    articles_list = news.search_articles(query, 100)

    articles = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []

        for article_summary in articles_list:
            futures.append(executor.submit(news.get_article, article_summary['url']))

        for future in concurrent.futures.as_completed(futures):
            try:
                article = future.result()
                articles.append(article)
            except:
                # TODO
                pass

    sentiment_scores = {a.url: sentiment.vader_sentiment(a.text) for a in articles}

    mean_score = statistics.mean(sentiment_scores.values())
    median_score = statistics.median(sentiment_scores.values())
    std_dev = statistics.stdev(sentiment_scores.values())

    return render_template('index.html',
            articles=articles,
            query=query,
            sentiment_scores=sentiment_scores,
            mean_sentiment_score=mean_score,
            median_sentiment_score=median_score,
            std_dev_sentiment_scores=std_dev
            )


if __name__ == '__main__':
    app.run(debug=True)
