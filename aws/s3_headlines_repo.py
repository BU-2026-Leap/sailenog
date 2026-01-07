import boto3
from datetime import datetime

class S3HeadlinesRepository:
    def __init__(self, bucket: str, key: str = "headlines.csv"):
        self.s3 = boto3.client("s3")
        self.bucket = bucket
        self.key = key

    def ensure_exists(self):
        try:
            self.s3.get_object(Bucket=self.bucket, Key=self.key)
        except self.s3.exceptions.NoSuchKey:
            self.s3.put_object(
                Bucket=self.bucket,
                Key=self.key,
                Body="timestamp,headline\n".encode(),
                ContentType="text/csv",
            )

    def append(self, headline: str):
        obj = self.s3.get_object(Bucket=self.bucket, Key=self.key)
        text = obj["Body"].read().decode("utf-8")

        timestamp = datetime.utcnow().isoformat()
        text += f"\"{timestamp}\",\"{headline}\"\n"

        self.s3.put_object(
            Bucket=self.bucket,
            Key=self.key,
            Body=text.encode("utf-8"),
            ContentType="text/csv",
        )
