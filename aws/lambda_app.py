from aws.s3_data_fetcher import S3DataFetcher
from common.exam_data_processor import ExamDataProcessor
from common.contracts import read_and_compute

import boto3
import os
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

s3 = boto3.client("s3")

BUCKET = os.environ["BUCKET_NAME"]
FILE_KEY = "headlines.csv"

def ensure_csv_exists():
    try:
        s3.get_object(Bucket=BUCKET, Key=FILE_KEY)
    except s3.exceptions.NoSuchKey:
        s3.put_object(
            Bucket=BUCKET,
            Key=FILE_KEY,
            Body="timestamp,headline\n".encode("utf-8"),
            ContentType="text/csv"
        )
        print("Created headlines.csv")

def get_top_headline():
    with urllib.request.urlopen("https://rss.cnn.com/rss/edition.rss") as response:
        xml_data = response.read()

    root = ET.fromstring(xml_data)

    for item in root.iter("item"):
        return item.find("title").text

def lambda_handler(event, context):
    # NEW: make sure file exists
    ensure_csv_exists()

    # Read existing file
    obj = s3.get_object(Bucket=BUCKET, Key=FILE_KEY)
    text = obj["Body"].read().decode("utf-8")

    # Get headline + time
    headline = get_top_headline()
    timestamp = datetime.utcnow().isoformat()

    # Append new row
    new_line = f"\"{timestamp}\",\"{headline}\"\n"
    text = text + new_line

    # Save back to S3
    s3.put_object(
        Bucket=BUCKET,
        Key=FILE_KEY,
        Body=text.encode("utf-8"),
        ContentType="text/csv"
    )

    print("Added headline:", headline)
