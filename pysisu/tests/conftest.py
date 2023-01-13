from unittest import mock

from pysisu.pysisu_class import PySisu
from pysisu.proto.sisu.v1.api import (
    AnalysisRunResultsResponse,
    AnalysesListResponse,
    DataSetsResponse,
    DataSourceListResponse,
    GetAnalysisFiltersResponse,
    GetProjectsAnalysesListResponse,
    GetProjectsListResponseListProjectResponse,
    MetricsListResponse,
    PaginationHints,
)
from pytest import fixture

from pysisu.tests.helpers_for_tests import (
    INPUT_SNAPSHOT_DIR,
    OUTPUT_SNAPSHOT_DIR,
    load_snapshot,
    pyapp_api_snapshots_to_pysisu,
)


def pytest_collection_finish(session):
    # ensure we have latest API response snapshots from the pyapp
    # do after collection so this step happens even if run from root pysisu directory
    pyapp_api_snapshots_to_pysisu()


@fixture
def pysisu_input_snapshot(snapshot):
    snapshot.snapshot_dir = INPUT_SNAPSHOT_DIR
    return snapshot


@fixture
def pysisu_output_snapshot(snapshot):
    snapshot.snapshot_dir = OUTPUT_SNAPSHOT_DIR
    return snapshot


@fixture
@mock.patch.object(PySisu, "_check_compatibility", lambda x: None)
def pysisu_client():
    pysisu = PySisu("API_KEY", "URL")
    return pysisu


@fixture
def result_time_compare() -> AnalysisRunResultsResponse:
    return AnalysisRunResultsResponse().from_dict(
        load_snapshot("time compare")
    )


@fixture
def result_group_compare() -> AnalysisRunResultsResponse:
    return AnalysisRunResultsResponse().from_dict(
        load_snapshot("group compare")
    )


@fixture
def result_general_performance() -> AnalysisRunResultsResponse:
    return AnalysisRunResultsResponse().from_dict(
        load_snapshot("general performance")
    )


@fixture
def result_trend() -> AnalysisRunResultsResponse:
    return AnalysisRunResultsResponse().from_dict(load_snapshot("trend"))


@fixture
def result_has_more(result_time_compare) -> AnalysisRunResultsResponse:
    # make a copy of result_time_compare
    result = AnalysisRunResultsResponse().from_dict(
        result_time_compare.to_dict()
    )
    result.pagination_hints = PaginationHints(
        has_more=True, next_starting_cursor=1
    )
    return result


@fixture
def analyses_list() -> AnalysesListResponse:
    return AnalysesListResponse().from_dict(load_snapshot("list analyses"))


@fixture
def metrics_list() -> MetricsListResponse:
    return MetricsListResponse().from_dict(load_snapshot("list metrics"))


@fixture
def data_sources_list() -> DataSourceListResponse:
    return DataSourceListResponse().from_dict(
        load_snapshot("list data sources")
    )


@fixture
def datasets_list() -> DataSetsResponse:
    return DataSetsResponse().from_dict(load_snapshot("list datasets"))


@fixture
def analysis_filter() -> GetAnalysisFiltersResponse:
    return GetAnalysisFiltersResponse().from_dict(
        load_snapshot("get analysis filters")
    )


@fixture
def projects_list() -> GetProjectsListResponseListProjectResponse:
    return GetProjectsListResponseListProjectResponse().from_dict(
        load_snapshot("list projects")
    )


@fixture
def project_analyses_list() -> GetProjectsAnalysesListResponse:
    return GetProjectsAnalysesListResponse().from_dict(
        load_snapshot("list project analyses")
    )
