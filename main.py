import time
import threading
import feedparser
import requests
from flask import Flask, render_template

app = Flask(__name__)

# List of subreddits and websites to fetch top posts from
subreddits_and_sites = {
    "technology": "https://www.reddit.com/r/technology/top/.rss?t=week",
    "nba": "https://www.reddit.com/r/nba/top/.rss?t=week",
    "news": "https://www.reddit.com/r/news/top/.rss?t=week",
    "unusual_whales": "https://www.reddit.com/r/unusual_whales/top/.rss?t=week",
    "PanIslamistPosting": "https://www.reddit.com/r/PanIslamistPosting/top/.rss?t=week",
    "Futurology": "https://www.reddit.com/r/Futurology/top/.rss?t=week",
    "geopolitics": "https://www.reddit.com/r/geopolitics/top/.rss?t=week",
    "bestof": "https://www.reddit.com/r/bestof/top/.rss?t=week",
    "truereddit": "https://www.reddit.com/r/truereddit/top/.rss?t=week",
    "thenation": "https://www.thenation.com/feed/?post_type=article&subject=politics",
    "muslimskeptic": "https://muslimskeptic.com/feed/",
    "theintercept": "https://theintercept.com/feed/",
    "slashdot": "http://rss.slashdot.org/Slashdot/slashdotMain",
    "aljazeera": "https://www.aljazeera.com/xml/rss/all.xml"
}

# Store the latest posts globally
latest_posts = {}

def fetch_posts(feed_url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(feed_url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch {feed_url}: {e}")
        return []

    feed = feedparser.parse(response.content)
    return [{"title": entry.title, "link": entry.link} for entry in feed.entries[:5]]

def update_posts():
    global latest_posts
    while True:
        print("Fetching latest posts...")
        latest_posts = {name: fetch_posts(url) for name, url in subreddits_and_sites.items()}
        time.sleep(3600)  # Refresh every 1 hour

@app.route('/')
def index():
    if not latest_posts:
        return "No posts available yet. Try again later."
    
    html_content = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #000;
                color: #fff;
                text-align: center;
                padding: 20px;
            }}
            .container {{
                background-color: #1e1e1e;
                padding: 20px;
                border-radius: 8px;
                width: 80%;
                max-width: 800px;
                margin: auto;
            }}
            h1 {{ color: #ffcc00; }}
            h2 {{ color: #ffcc00; }}
            a {{ color: #00FF00; text-decoration: none; }}
            a:hover {{ text-decoration: underline; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Top Posts of the Week</h1>
    """

    for site, posts in latest_posts.items():
        html_content += f"<h2>{site}</h2>"
        for post in posts:
            html_content += f'<p><a href="{post["link"]}" target="_blank">{post["title"]}</a></p>'

    html_content += "</div></body></html>"
    return html_content

if __name__ == '__main__':
    # Start background thread for fetching posts
    thread = threading.Thread(target=update_posts, daemon=True)
    thread.start()
    
    app.run(host='0.0.0.0', port=10000)
