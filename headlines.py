import feedparser
from flask import render_template
from flask import Flask
app = Flask(__name__)

RSS_FEEDS = {
        'eltiempo': 'http://www.eltiempo.com/rss/tecnosfera.xml',
        'wwwhatsnew': 'https://wwwhatsnew.com/feed/',
        'granmisterio': 'https://granmisterio.org/feed/'
        }

@app.route("/")
@app.route("/<seccion>")
def get_news(seccion='eltiempo'):
    feed = feedparser.parse(RSS_FEEDS[seccion])
    return render_template('home.html', articles=feed['entries'])

if __name__=='__main__':
    app.run(port=5000, debug=True)
