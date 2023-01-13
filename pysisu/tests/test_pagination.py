from unittest import mock

from pysisu.pysisu_class import PySisu
from pysisu.formats import LatestAnalysisResultsFormats
from pysisu.proto.sisu.v1.api import AnalysisRunResultsResponse
from .helpers_for_tests import SNAPSHOT_DICT


@mock.patch("pysisu.pysisu_class.PySisu.get_results")
def test_pagination_starting_after_gets_updated(
    get_results: mock.MagicMock,
    result_time_compare: AnalysisRunResultsResponse,
    result_has_more: AnalysisRunResultsResponse,
    pysisu_client: PySisu,
):
    get_results.return_value = result_time_compare
    pysisu_client._auto_paginate(1, {}, result_has_more)

    # Make sure limit is truncated at MAX_LIMIT
    assert "limit" not in get_results.call_args.kwargs

    # Make sure the next starting_after was marked at the correct cursor from the pagination hints
    assert (
        get_results.call_args.kwargs["starting_after"]
        == result_has_more.analysis_result.key_driver_analysis_result.segments[
            -1
        ].id
    )


@mock.patch("pysisu.PySisu.get_results")
def test_pagination_limit_works(
    get_results: mock.MagicMock,
    result_time_compare: AnalysisRunResultsResponse,
    result_has_more: AnalysisRunResultsResponse,
    pysisu_client: PySisu,
):
    get_results.return_value = result_time_compare
    pysisu_client._auto_paginate(1, {}, result_has_more, limit=100)

    assert get_results.call_args.kwargs["limit"] == 100 - len(
        result_time_compare.analysis_result.key_driver_analysis_result.segments
    )
    assert (
        get_results.call_args.kwargs["starting_after"]
        == result_time_compare.analysis_result.key_driver_analysis_result.segments[
            -1
        ].id
    )


@mock.patch("pysisu.PySisu.get_results")
def test_pagination_results_make_sense(
    get_results: mock.MagicMock,
    result_time_compare: AnalysisRunResultsResponse,
    result_has_more: AnalysisRunResultsResponse,
    pysisu_client: PySisu,
    pysisu_input_snapshot,
):
    get_results.return_value = result_time_compare
    result = pysisu_client._auto_paginate(1, {}, result_has_more, limit=100)
    pysisu_input_snapshot.assert_match(
        result.to_json(indent=4), SNAPSHOT_DICT["time compare has more"]
    )


@mock.patch("pysisu.PySisu.fetch_sisu_api")
def test_pagination_results_using_customer_facing_functions(
    fetch_sisu_api: mock.MagicMock,
    result_time_compare: AnalysisRunResultsResponse,
    result_has_more: AnalysisRunResultsResponse,
    pysisu_client: PySisu,
    pysisu_input_snapshot,
):
    fetch_sisu_api.side_effect = iter(
        [result_has_more.to_dict(), result_time_compare.to_dict()]
    )
    result = pysisu_client.get_results(
        1, {"limit": 100}, format=LatestAnalysisResultsFormats.PROTO
    )
    pysisu_input_snapshot.assert_match(
        result.to_json(indent=4),
        SNAPSHOT_DICT["time compare has more doubled"],
    )

    assert fetch_sisu_api.call_args.kwargs["limit"] == 100 - len(
        result_time_compare.analysis_result.key_driver_analysis_result.segments
    )
    assert (
        fetch_sisu_api.call_args.kwargs["starting_after"]
        == result_has_more.analysis_result.key_driver_analysis_result.segments[
            -1
        ].id
    )
