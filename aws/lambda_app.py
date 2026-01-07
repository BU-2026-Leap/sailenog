import urllib.request
import xml.etree.ElementTree as ET
import boto3
import os
from datetime import datetime

RSS_URL = "https://news.google.com/rss/search?q=site:cnn.com&hl=en-US&gl=US&ceid=US:en"

s3 = boto3.client("s3")

BUCKET = os.environ.get("BUCKET_NAME")
KEY = "headlines.csv"

def get_top_headline() -> str:
    with urllib.request.urlopen(RSS_URL) as response:
        xml_data = response.read()

    root = ET.fromstring(xml_data)
    first_title = root.find("channel").find("item")[0]
    return first_title.text

def ensure_csv_exists():
    try:
        s3.get_object(Bucket=BUCKET, Key=KEY)
    except s3.exceptions.NoSuchKey:
        s3.put_object(
            Bucket=BUCKET,
            Key=KEY,
            Body="timestamp,headline\n".encode("utf-8"),
            ContentType="text/csv",
        )

def lambda_handler(event, context):
    if not BUCKET:
        raise RuntimeError("BUCKET_NAME environment variable not set")

    ensure_csv_exists()

    obj = s3.get_object(Bucket=BUCKET, Key=KEY)
    text = obj["Body"].read().decode("utf-8")

    headline = get_top_headline()
    timestamp = datetime.utcnow().isoformat()

    text += f"\"{timestamp}\",\"{headline}\"\n"

    s3.put_object(
        Bucket=BUCKET,
        Key=KEY,
        Body=text.encode("utf-8"),
        ContentType="text/csv",
    )

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
