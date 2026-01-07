import os
from rss_headlines.s3_headlines_repo import S3HeadlinesRepository
from rss_headlines.rss_client import get_top_headline

def lambda_handler(event, context):
    bucket = os.environ.get("BUCKET_NAME")
    if not bucket:
        raise RuntimeError("BUCKET_NAME environment variable not set")

    repo = S3HeadlinesRepository(bucket)
    repo.ensure_exists()

    headline = get_top_headline()
    repo.append(headline)

    return {
        "statusCode": 200,
        "body": f"Added headline: {headline}"
    }
