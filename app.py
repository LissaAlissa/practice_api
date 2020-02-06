from flask import Flask, request, jsonify, make_response, abort, url_for
from sitescraper import SiteScraperFactory
import json

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False

@app.route('/')
def hello():
    return "Все последние новости:'/news'. Наши информационные рксурсы: '/news/tut.by', '/news/rbc.ru', '/news/mk.ru'"


@app.route("/news", methods=['GET'])
def get_news():
    news = SiteScraperFactory().get_all_news()
    return jsonify({'news':news})

@app.route("/news/<site>", methods=['GET'])
def get_news_site(site):
    news_site = SiteScraperFactory().get_site(site)
    if len(news_site) == 0:
        abort(404)
    return jsonify({'news': news_site})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)