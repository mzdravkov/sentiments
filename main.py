from flask import Flask
from flask import render_template
from flask import request

import news

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search-news', methods=['POST'])
def search_news():
    print(request.form)
    query = request.form.get('query')
    articles_list = news.search_articles(query, 20)
    print('articles list')
    print(articles_list)
    articles = []
    for article_summary in articles_list:
        try:
            article = news.get_article(article_summary['url'])
            articles.append(article)
        except:
            # TODO
            pass
    return render_template('index.html', articles=articles, query=query)


if __name__ == '__main__':
    app.run(debug=True)
