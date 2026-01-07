from dataclasses import dataclass

@dataclass
class ExamScore:
    student_id: str
    exam_name: str
    score: float

@dataclass
class ExamStats:
    average_final: float
    unique_students: int

    def to_dictionary(self):
        return {
            "average_final": self.average_final,
            "unique_students": self.unique_students
        }

class DataFetcher:
    def fetch(self) -> [ExamScore]:
        raise NotImplementedError

class DataProcessor:
    def compute_average_final(self, scores: [ExamScore]) -> float:
        raise NotImplementedError

    def compute_number_of_unique_students(self, scores: [ExamScore]) -> int:
        raise NotImplementedError

def read_and_compute(data_fetcher: DataFetcher, data_processor: DataProcessor) -> ExamStats:
    data = data_fetcher.fetch()
    return ExamStats(
        average_final= data_processor.compute_average_final(data),
        unique_students=data_processor.compute_number_of_unique_students(data)
    )