import urllib.request
import xml.etree.ElementTree as ET
import boto3
import os
from datetime import datetime

RSS_URL = "https://news.google.com/rss/search?q=site:cnn.com&hl=en-US&gl=US&ceid=US:en"


def get_top_headline(event, context) -> str:
    with urllib.request.urlopen(RSS_URL) as response:
        xml_data = response.read()

    root = ET.fromstring(xml_data)
    first_title = root.find("channel").find("item")[0]
    headline = first_title.text

    # Get the current date and time as a datetime object
    now = datetime.now()

    # Format the datetime object into a string (e.g., "HH:MM:SS")
    timestamp = now.strftime("%H:%M:%S")

    html = f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>Latest CNN Headline</title>
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
      p {{
        color: #666;
        font-size: 14px;
      }}
    </style>
  </head>
  <body>
    <div class="container">
      <h1>{headline}</h1>
      <p>Fetched at {timestamp} UTC</p>
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
