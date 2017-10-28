import feedparser
from flask import render_template
from flask import Flask
from flask import request
import json
import requests
from requests.utils import quote

app = Flask(__name__)

RSS_FEEDS = {
        'eltiempo': 'http://www.eltiempo.com/rss/tecnosfera.xml',
        'wwwhatsnew': 'https://wwwhatsnew.com/feed/',
        'granmisterio': 'https://granmisterio.org/feed/'
        }
DEFAULTS = {
        'publication': 'eltiempo',
        'city': 'Cali,CO'
        }
WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&lang=es&appid=d781b17b4dacdcb45df7a576e25924d1'


@app.route("/")
def home():
    # get customized headlines, based on user input or default
    publication = request.args.get('publication')
    if not publication:
        publication = DEFAULTS['publication']
    articles = get_news(publication)

    # get customized weather based on user input or default
    city = request.args.get('city')
    if not city:
        city = DEFAULTS['city']
    weather = get_weather(city)
    return render_template('home.html', articles=articles, weather=weather)


def get_news(query):
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS['publication']
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed['entries']

def get_weather(query):
    query = quote(query)
    url = WEATHER_URL.format(query)
    data = requests.get(url)
    parsed = json.loads(data.text)
    weather = None
    if parsed.get('weather'):
        weather = {
                'description': parsed['weather'][0]['description'],
                'temperature': parsed['main']['temp'],
                'city': parsed['name'],
                'country': parsed['sys']['country']
                }
        return weather


if __name__=='__main__':
    app.run(port=5000, debug=True)
