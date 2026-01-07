from common.contracts import DataFetcher, ExamScore

import boto3
import csv
import io

class S3DataFetcher(DataFetcher):
    def __init__(self, bucket: str, key: str):
        self._s3 = boto3.client("s3")
        self.bucket = bucket
        self.key = key

    def fetch(self) -> [ExamScore]:
        print("Fetching from S3!")

        obj = self._s3.get_object(Bucket=self.bucket, Key=self.key)
        contents = obj["Body"]

        text_stream = io.TextIOWrapper(contents, encoding="utf-8")
        reader = csv.DictReader(text_stream)

        scores = []
        for row in reader:
            scores.append(
                ExamScore(
                    student_id=row["student_id"],
                    exam_name=row["exam_name"],
                    score=float(row["score"])
                )
            )

        return scores