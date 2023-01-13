from unittest import mock


@mock.patch("pysisu.PySisu.fetch_sisu_api")
def test_time_compare_csv(
    mock_pysisu, result_time_compare, pysisu_client, pysisu_output_snapshot
):
    mock_pysisu.return_value = result_time_compare.to_dict()
    pysisu_output_snapshot.assert_match(
        pysisu_client.get_results(1).to_csv(), "time_compare.csv"
    )


@mock.patch("pysisu.PySisu.fetch_sisu_api")
def test_group_compare_csv(
    mock_pysisu, result_group_compare, pysisu_client, pysisu_output_snapshot
):
    mock_pysisu.return_value = result_group_compare.to_dict()
    pysisu_output_snapshot.assert_match(
        pysisu_client.get_results(1).to_csv(), "group_compare.csv"
    )


@mock.patch("pysisu.PySisu.fetch_sisu_api")
def test_general_performance_csv(
    mock_pysisu,
    result_general_performance,
    pysisu_client,
    pysisu_output_snapshot,
):
    mock_pysisu.return_value = result_general_performance.to_dict()
    pysisu_output_snapshot.assert_match(
        pysisu_client.get_results(1).to_csv(), "general_performance.csv"
    )


@mock.patch("pysisu.PySisu.fetch_sisu_api")
def test_trend_detection_csv(
    mock_fetch, result_trend, pysisu_client, pysisu_output_snapshot
):
    mock_fetch.return_value = result_trend.to_dict()
    pysisu_output_snapshot.assert_match(
        pysisu_client.get_results(1).to_csv(), "trend_detection.csv"
    )
