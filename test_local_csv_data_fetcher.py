from local_csv_data_fetcher import LocalCSVDataFetcher

def test_local_csv_data_fetcher():
    fetcher = LocalCSVDataFetcher("test_scores.csv")
    result = fetcher.fetch()

    assert len(result) == 8

    assert result[0].student_id == "U123"
    assert result[0].exam_name == "midterm1"
    assert result[0].score == 84
