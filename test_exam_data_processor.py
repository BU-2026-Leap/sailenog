import pytest
from contracts import ExamScore
from exam_data_processor import ExamDataProcessor

@pytest.fixture
def processor():
    return ExamDataProcessor()

def test_compute_average_final_good_data(processor):
    input = [
        ExamScore(
            student_id="U123",
            exam_name="final",
            score=75
        ),
        ExamScore(
            student_id="U124",
            exam_name="midterm",
            score=80
        ),
        ExamScore(
            student_id="U125",
            exam_name="final",
            score=85
        )
    ]

    actual = processor.compute_average_final(input)

    assert 80 == actual

def test_compute_average_final_empty_input(processor):
    actual = processor.compute_average_final([])

    assert 0 == actual

def test_compute_average_final_no_finals_in_input(processor):
    input = [
        ExamScore(
            student_id="U123",
            exam_name="exam",
            score=75
        ),
        ExamScore(
            student_id="U124",
            exam_name="midterm",
            score=80
        )
    ]

    actual = processor.compute_average_final(input)

    assert 0 == actual

def test_compute_unique_students_good_data(processor):
    input = [
        ExamScore(
            student_id="U123",
            exam_name="exam",
            score=75
        ),
        ExamScore(
            student_id="U124",
            exam_name="midterm",
            score=80
        ),
        ExamScore(
            student_id="U123",
            exam_name="midterm",
            score=80
        )
    ]

    actual = processor.compute_number_of_unique_students(input)

    assert 2 == actual

def test_compute_unique_students_empty_input(processor):
    assert 0 == processor.compute_number_of_unique_students([])