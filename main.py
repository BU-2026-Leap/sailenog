from contracts import DataFetcher
from contracts import DataProcessor
from contracts import ExamStats
from local_csv_data_fetcher import LocalCSVDataFetcher
from exam_data_processor import ExamDataProcessor

import os
import json

def read_and_compute(data_fetcher: DataFetcher, data_processor: DataProcessor) -> ExamStats:
    data = data_fetcher.fetch()
    return ExamStats(
        average_final= data_processor.compute_average_final(data),
        unique_students=data_processor.compute_number_of_unique_students(data)
    )

INPUT_FILENAME = "test_scores.csv"
OUTPUT_FILENAME = "output.json"

if os.path.exists(OUTPUT_FILENAME):
    os.remove(OUTPUT_FILENAME)

result = read_and_compute(
    LocalCSVDataFetcher(INPUT_FILENAME),
    ExamDataProcessor()
)

with open(OUTPUT_FILENAME, "w") as out:
    json.dump(result.to_dictionary(), out, indent=2)