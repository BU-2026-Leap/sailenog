from common.contracts import DataFetcher, ExamScore

import csv

class LocalCSVDataFetcher(DataFetcher):
    def __init__(self, file_path:str):
        self.file_path = file_path

    def fetch(self) -> [ExamScore]:
        scores = []

        with open(self.file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                scores.append(
                    ExamScore(
                        student_id=row["student_id"],
                        exam_name=row["exam_name"],
                        score=int(row["score"])
                    )
                )
        return scores