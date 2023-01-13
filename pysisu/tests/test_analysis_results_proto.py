from unittest import mock

from .helpers_for_tests import SNAPSHOT_DICT


@mock.patch("pysisu.PySisu.fetch_sisu_api")
def test_time_compare_proto(
    mock_pysisu, result_time_compare, pysisu_client, pysisu_input_snapshot
):
    mock_pysisu.return_value = result_time_compare.to_dict()
    pysisu_input_snapshot.assert_match(
        pysisu_client.get_results(1, format=None).to_json(indent=4),
        SNAPSHOT_DICT["time compare"],
    )


@mock.patch("pysisu.PySisu.fetch_sisu_api")
def test_group_compare_proto(
    mock_pysisu, result_group_compare, pysisu_client, pysisu_input_snapshot
):
    mock_pysisu.return_value = result_group_compare.to_dict()
    pysisu_input_snapshot.assert_match(
        pysisu_client.get_results(1, format=None).to_json(indent=4),
        SNAPSHOT_DICT["group compare"],
    )


@mock.patch("pysisu.PySisu.fetch_sisu_api")
def test_general_performance_proto(
    mock_pysisu,
    result_general_performance,
    pysisu_client,
    pysisu_input_snapshot,
):
    mock_pysisu.return_value = result_general_performance.to_dict()
    pysisu_input_snapshot.assert_match(
        pysisu_client.get_results(1, format=None).to_json(indent=4),
        SNAPSHOT_DICT["general performance"],
    )


@mock.patch("pysisu.PySisu.fetch_sisu_api")
def test_trend_detection_proto(
    mock_fetch, result_trend, pysisu_client, pysisu_input_snapshot
):
    mock_fetch.return_value = result_trend.to_dict()
    pysisu_input_snapshot.assert_match(
        pysisu_client.get_results(1, format=None).to_json(indent=4),
        SNAPSHOT_DICT["trend"],
    )
