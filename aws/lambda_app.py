import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

RSS_URL = "https://news.google.com/rss/search?q=site:cnn.com&hl=en-US&gl=US&ceid=US:en"

# ---- In-memory cache (persists across warm invocations) ----
HEADLINE_CACHE = []
LAST_UPDATED = None
LAST_HEADLINE_TEXT = None

UPDATE_INTERVAL = timedelta(minutes=5)
MAX_HEADLINES = 10
ET_ZONE = ZoneInfo("America/New_York")


def fetch_headlines(limit=5):
    with urllib.request.urlopen(RSS_URL) as response:
        xml_data = response.read()

    root = ET.fromstring(xml_data)
    items = root.find("channel").findall("item")

    headlines = []
    for item in items[:limit]:
        headlines.append(
            (
                item.find("title").text,
                item.find("link").text,
            )
        )

    return headlines



def get_top_headline(event, context):
    global LAST_UPDATED, HEADLINE_CACHE, LAST_HEADLINE_TEXT

    now = datetime.now(ET_ZONE)

    underline = False

    # Update only every 5 minutes
    if LAST_UPDATED is None or (now - LAST_UPDATED) >= UPDATE_INTERVAL:
        title, link = fetch_headline()
        timestamp = now.strftime("%I:%M:%S %p ET")

        if LAST_HEADLINE_TEXT and title != LAST_HEADLINE_TEXT:
            underline = True

        LAST_HEADLINE_TEXT = title

        HEADLINE_CACHE.insert(
            0,
            {
                "title": title,
                "link": link,
                "timestamp": timestamp,
            },
        )

        HEADLINE_CACHE = HEADLINE_CACHE[:MAX_HEADLINES]
        LAST_UPDATED = now
    else:
        title = HEADLINE_CACHE[0]["title"]
        link = HEADLINE_CACHE[0]["link"]
        timestamp = HEADLINE_CACHE[0]["timestamp"]

    # Build HTML list
    headlines_html = "".join(
        f'<li><a href="{h["link"]}" target="_blank">{h["timestamp"]} — {h["title"]}</a></li>'
        for h in HEADLINE_CACHE
    )

    headline_style = "color:red;"
    if underline:
        headline_style += " text-decoration: underline;"

    html = f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>CNN Headline Tracker</title>
    <style>
      body {{
        font-family: Arial, sans-serif;
        background-color: #f4f4f4;
        padding: 40px;
      }}
      .container {{
        max-width: 700px;
        margin: auto;
        background: white;
        padding: 25px;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
      }}
      h1 {{
        font-size: 22px;
        margin-bottom: 10px;
      }}
      ul {{
        margin-top: 20px;
        padding-left: 20px;
      }}
      li {{
        margin-bottom: 8px;
        color: black;
      }}
      a {{
        color: black;
        text-decoration: none;
      }}
      a:hover {{
        text-decoration: underline;
      }}
      .timestamp {{
        color: #777;
        font-size: 13px;
      }}
    </style>
  </head>
  <body>
    <div class="container">
      <h1 style="{headline_style}">
        <a href="{link}" target="_blank" style="color:red;">
          {title}
        </a>
      </h1>
      <p class="timestamp">Last refreshed at {LAST_UPDATED.strftime("%I:%M:%S %p ET")}</p>

      <h3>Recent Headlines</h3>
      <ul>
        {headlines_html}
      </ul>
    </div>
  </body>
</html>
"""

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "text/html"
        },
        "body": html
    }
