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
        'city': 'Cali,CO',
        'currency_from': 'COP',
        'currency_to': 'USD'
        }

WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&lang=es&appid=d781b17b4dacdcb45df7a576e25924d1'

CURRENCY_URL = 'https://openexchangerates.org/api/latest.json?app_id=e0c958dbc8bf4084bf8bf26abdc72cc1'

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

    # get customized currency based on user input or default
    currency_from = request.args.get('currency_from')
    if not currency_from:
        currency_from = DEFAULTS['currency_from']
    currency_to = request.args.get('currency_to')
    if not currency_to:
        currency_to = DEFAULTS['currency_to']
    rate, currencies = get_rate(currency_from, currency_to)

    return render_template('home.html', articles=articles, weather=weather, currency_from=currency_from, currency_to=currency_to, rate=rate, currencies=sorted(currencies))


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

def get_rate(frm, to):
    all_currency = requests.get(CURRENCY_URL)
    parsed = json.loads(all_currency.text).get('rates')
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())
    return (to_rate/frm_rate, parsed.keys())


if __name__=='__main__':
    app.run(port=5000, debug=True)
