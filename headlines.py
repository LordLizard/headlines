import feedparser
from flask import render_template
from flask import Flask
from flask import request

app = Flask(__name__)

RSS_FEEDS = {
        'eltiempo': 'http://www.eltiempo.com/rss/tecnosfera.xml',
        'wwwhatsnew': 'https://wwwhatsnew.com/feed/',
        'granmisterio': 'https://granmisterio.org/feed/'
        }

@app.route("/")
def get_news():
    query = request.args.get('publication')
    if not query or query.lower() not in RSS_FEEDS:
        publication = 'eltiempo'
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    return render_template('home.html', articles=feed['entries'])

if __name__=='__main__':
    app.run(port=5000, debug=True)
