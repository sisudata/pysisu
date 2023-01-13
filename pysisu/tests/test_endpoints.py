from unittest import mock

from pysisu.proto.sisu.v1.api import CreateDataSetRequestDataset
from .helpers_for_tests import SNAPSHOT_DICT


def validate_api_call(mock_call_sisu_api, method=None, path=None):
    assert mock_call_sisu_api.call_count == 1
    if method is not None:
        assert mock_call_sisu_api.call_args.kwargs["request_method"] == method
    if path is not None:
        assert mock_call_sisu_api.call_args[0][0] == path


@mock.patch("pysisu.pysisu_class.PySisu._call_sisu_api")
def test_run_analysis(mock_call_sisu_api, pysisu_client):
    pysisu_client.run(1)
    validate_api_call(
        mock_call_sisu_api, method="POST", path="api/v1/analyses/1/run"
    )


@mock.patch("pysisu.pysisu_class.PySisu._call_sisu_api")
def test_list_analyses(
    mock_call_sisu_api, analyses_list, pysisu_client, pysisu_input_snapshot
):
    mock_call_sisu_api.return_value = analyses_list.to_dict()
    pysisu_input_snapshot.assert_match(
        pysisu_client.analyses().to_json(indent=4),
        SNAPSHOT_DICT["list analyses"],
    )
    validate_api_call(mock_call_sisu_api, path="api/v1/analyses")


@mock.patch("pysisu.pysisu_class.PySisu._call_sisu_api")
def test_list_metrics(
    mock_call_sisu_api, metrics_list, pysisu_client, pysisu_input_snapshot
):
    mock_call_sisu_api.return_value = metrics_list.to_dict()
    pysisu_input_snapshot.assert_match(
        pysisu_client.metrics().to_json(indent=4),
        SNAPSHOT_DICT["list metrics"],
    )
    validate_api_call(mock_call_sisu_api, path="api/v1/metrics")


@mock.patch("pysisu.pysisu_class.PySisu._call_sisu_api")
def test_list_data_sources(
    mock_call_sisu_api, data_sources_list, pysisu_client, pysisu_input_snapshot
):
    mock_call_sisu_api.return_value = data_sources_list.to_dict()
    pysisu_input_snapshot.assert_match(
        pysisu_client.data_sources().to_json(indent=4),
        SNAPSHOT_DICT["list data sources"],
    )
    validate_api_call(mock_call_sisu_api, path="api/v1/data_sources")


@mock.patch("pysisu.pysisu_class.PySisu._call_sisu_api")
def test_list_datasets(
    mock_call_sisu_api, datasets_list, pysisu_client, pysisu_input_snapshot
):
    mock_call_sisu_api.return_value = datasets_list.to_dict()
    pysisu_input_snapshot.assert_match(
        pysisu_client.datasets().to_json(indent=4),
        SNAPSHOT_DICT["list datasets"],
    )
    validate_api_call(mock_call_sisu_api, path="api/v1/datasets")


@mock.patch("pysisu.pysisu_class.PySisu._call_sisu_api")
def test_get_analysis_filters(
    mock_call_sisu_api, analysis_filter, pysisu_client, pysisu_input_snapshot
):
    mock_call_sisu_api.return_value = analysis_filter.to_dict()
    pysisu_input_snapshot.assert_match(
        pysisu_client.get_filters(1).to_json(indent=4),
        SNAPSHOT_DICT["get analysis filters"],
    )
    validate_api_call(mock_call_sisu_api, path="api/v1/analyses/1/filters")


@mock.patch("pysisu.pysisu_class.PySisu._call_sisu_api")
def test_list_projects(
    mock_call_sisu_api, projects_list, pysisu_client, pysisu_input_snapshot
):
    mock_call_sisu_api.return_value = projects_list.to_dict()
    pysisu_input_snapshot.assert_match(
        pysisu_client.get_projects().to_json(indent=4),
        SNAPSHOT_DICT["list projects"],
    )
    validate_api_call(mock_call_sisu_api, "GET", "api/v1/projects")


@mock.patch("pysisu.pysisu_class.PySisu._call_sisu_api")
def test_list_project_analyses(
    mock_call_sisu_api,
    project_analyses_list,
    pysisu_client,
    pysisu_input_snapshot,
):
    mock_call_sisu_api.return_value = project_analyses_list.to_dict()
    pysisu_input_snapshot.assert_match(
        pysisu_client.get_project_analyses_list(1).to_json(indent=4),
        SNAPSHOT_DICT["list project analyses"],
    )
    validate_api_call(mock_call_sisu_api, "GET", "api/v1/projects/1/analyses")


@mock.patch("pysisu.pysisu_class.PySisu._call_sisu_api")
def test_set_filters(mock_call_sisu_api, pysisu_client):
    pysisu_client.set_filters(1, expr={})
    validate_api_call(mock_call_sisu_api, "PUT", "api/v1/analyses/1/filters")


@mock.patch("pysisu.pysisu_class.PySisu._call_sisu_api")
def test_duplicate_analysis(mock_call_sisu_api, pysisu_client):
    pysisu_client.duplicate_analysis(1)
    validate_api_call(
        mock_call_sisu_api, "POST", "api/v1/analyses/1/duplicate"
    )


@mock.patch("pysisu.pysisu_class.PySisu._call_sisu_api")
def test_get_factor_data(mock_call_sisu_api, pysisu_client):
    pysisu_client.get_factor_data(1)
    validate_api_call(
        mock_call_sisu_api, "GET", "api/v1/segments/1/data_query"
    )


@mock.patch("pysisu.pysisu_class.PySisu._call_sisu_api")
def test_create_dataset(mock_call_sisu_api, pysisu_client):
    pysisu_client.create_dataset(1, body=CreateDataSetRequestDataset())
    validate_api_call(
        mock_call_sisu_api, "POST", "api/v1/data_sources/1/datasets"
    )
