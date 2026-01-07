import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

RSS_URL = "https://news.google.com/rss/search?q=site:cnn.com&hl=en-US&gl=US&ceid=US:en"

# ---- In-memory cache (persists across warm invocations) ----
HEADLINE_CACHE = []
LAST_UPDATED = None
UPDATE_INTERVAL = timedelta(minutes=5)
MAX_HEADLINES = 10


def fetch_headline() -> str:
    with urllib.request.urlopen(RSS_URL) as response:
        xml_data = response.read()

    root = ET.fromstring(xml_data)
    first_title = root.find("channel").find("item")[0]
    return first_title.text


def get_top_headline(event, context):
    global LAST_UPDATED, HEADLINE_CACHE

    now = datetime.utcnow()

    # Update only every 5 minutes
    if LAST_UPDATED is None or (now - LAST_UPDATED) >= UPDATE_INTERVAL:
        headline = fetch_headline()
        timestamp = now.strftime("%H:%M:%S UTC")

        HEADLINE_CACHE.insert(0, f"{timestamp} — {headline}")
        HEADLINE_CACHE = HEADLINE_CACHE[:MAX_HEADLINES]

        LAST_UPDATED = now
    else:
        headline = HEADLINE_CACHE[0].split(" — ", 1)[1]

    # Build HTML list
    headlines_html = "".join(
        f"<li>{item}</li>" for item in HEADLINE_CACHE
    )

    html = f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>Latest CNN Headlines</title>
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
        color: #444;
      }}
      .timestamp {{
        color: #777;
        font-size: 13px;
      }}
    </style>
  </head>
  <body>
    <div class="container">
      <h1>{headline}</h1>
      <p class="timestamp">Last refreshed at {LAST_UPDATED.strftime("%H:%M:%S UTC")}</p>

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
