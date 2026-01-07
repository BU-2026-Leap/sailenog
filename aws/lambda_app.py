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

    print("Added headline:", headline)

    return {
        "statusCode": 200,
        "body": headline,
    }
