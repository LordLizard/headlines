import feedparser
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
    first_article = feed['entries'][0]
    return """
    <html>
    <body>
        <h1>Noticias</h1>
        <b>{0}</b> <br/>
        <i>{1}</i> <br/>
        <p>{2}</p> <br/>
    </body>
    </html>""".format(first_article.get('title'), first_article.get('published'), first_article.get('summary'))

if __name__=='__main__':
    app.run(port=5000, debug=True)
