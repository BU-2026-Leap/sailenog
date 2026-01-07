from common.contracts import DataProcessor, ExamScore

class ExamDataProcessor(DataProcessor):
    def compute_number_of_unique_students(self, scores: [ExamScore]) -> int:
        """
        Given a list of ExamScore's, computes the number of unique students in the data set
        """

        # TODO: implement here
        unique_students = {score.student_id for score in scores}
        return len(unique_students)


    def compute_average_final(self, scores: [ExamScore]) -> float:
        """
        Given a list of ExamScore's, computes the average of all final scores
        """

        # TODO: implement here
        final_scores = [score.score for score in scores if score.exam_name == "final"]

        if final_scores:
            return sum(final_scores) / len(final_scores)
        else:
            return 0