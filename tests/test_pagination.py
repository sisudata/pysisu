import os
import json
from unittest import mock
from pysisu.formats import LatestAnalysisResultsFormats
from pytest import fixture
from pysisu import PySisu
from pysisu.proto.sisu.v1.api import (
    AnalysisRunResultsResponse,
    PaginationHints,
)

CURR_PATH = os.path.dirname(os.path.abspath(__file__))
INPUT_SNAPSHOT_DIR = os.path.join(CURR_PATH, "input_snapshots")
OUTPUT_SNAPSHOT_DIR = os.path.join(CURR_PATH, "output_snapshots")


def load_snapshot(snapshot_file_name: str) -> dict:
    snapshot = os.path.join(INPUT_SNAPSHOT_DIR, snapshot_file_name)
    with open(snapshot, "r") as file:
        return json.loads(file.read())


@fixture
def result_1() -> AnalysisRunResultsResponse:
    return AnalysisRunResultsResponse().from_dict(
        load_snapshot(
            "api__endpoint_handlers__test__generate_latest_workflow_results_snapshot.json"
        )
    )


@fixture
def result_has_more() -> AnalysisRunResultsResponse:
    result = AnalysisRunResultsResponse().from_dict(
        load_snapshot(
            "api__endpoint_handlers__test__generate_latest_workflow_results_snapshot.json"
        )
    )
    result.pagination_hints = PaginationHints(
        has_more=True, next_starting_cursor=1
    )
    return result


@mock.patch("pysisu.PySisu.get_results")
def test_pagination_staring_after_gets_updated(
    get_results: mock.MagicMock,
    result_1: AnalysisRunResultsResponse,
    result_has_more: AnalysisRunResultsResponse,
):
    get_results.return_value = result_1
    pysisu = PySisu("API_KEY", "URL")
    pysisu._auto_paginate(1, {}, result_has_more)

    # Make sure limit is truncated at MAX_LIMIT
    assert "limit" not in get_results.call_args[0][1].keys()

    # Make sure the next starting_after was marked at the correct cursor from the pagination hints
    assert (
        get_results.call_args[0][1]["starting_after"]
        == result_has_more.analysis_result.key_driver_analysis_result.segments[
            -1
        ].id
    )


@mock.patch("pysisu.PySisu.get_results")
def test_pagination_limit_works(
    get_results: mock.MagicMock,
    result_1: AnalysisRunResultsResponse,
    result_has_more: AnalysisRunResultsResponse,
):
    get_results.return_value = result_1
    pysisu = PySisu("API_KEY", "URL")
    pysisu._auto_paginate(1, {"limit": 100}, result_has_more)

    # 98 comes from the 100 - len(result_has_more.subgroups)
    assert get_results.call_args[0][1]["limit"] == 98
    assert (
        get_results.call_args[0][1]["starting_after"]
        == result_has_more.analysis_result.key_driver_analysis_result.segments[
            -1
        ].id
    )


@mock.patch("pysisu.PySisu.get_results")
def test_pagination_results_make_sense(
    get_results: mock.MagicMock,
    result_1: AnalysisRunResultsResponse,
    result_has_more: AnalysisRunResultsResponse,
    snapshot,
):
    get_results.return_value = result_1
    pysisu = PySisu("API_KEY", "URL")
    result = pysisu._auto_paginate(1, {"limit": 100}, result_has_more)
    snapshot.snapshot_dir = OUTPUT_SNAPSHOT_DIR
    snapshot.assert_match(
        result.to_json(indent=4), "subgroups_pagination.json"
    )


@mock.patch("pysisu.PySisu.fetch_sisu_api")
def test_pagination_results_using_customer_facing_functions(
    fetch_sisu_api: mock.MagicMock,
    result_1: AnalysisRunResultsResponse,
    result_has_more: AnalysisRunResultsResponse,
    snapshot,
):
    fetch_sisu_api.side_effect = iter(
        [result_has_more.to_dict(), result_1.to_dict()]
    )
    pysisu = PySisu("API_KEY", "URL")
    result = pysisu.get_results(
        1, {"limit": 100}, format=LatestAnalysisResultsFormats.PROTO
    )
    snapshot.assert_match(
        result.to_json(indent=4), "subgroups_pagination.json"
    )

    # 98 comes from the 100 - len(result_has_more.subgroups)
    assert fetch_sisu_api.call_args[0][1]["limit"] == 98
    assert (
        fetch_sisu_api.call_args[0][1]["starting_after"]
        == result_has_more.analysis_result.key_driver_analysis_result.segments[
            -1
        ].id
    )
