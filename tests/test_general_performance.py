import os
import json
from unittest import mock
from pysisu import PySisu

CURR_PATH = os.path.dirname(os.path.abspath(__file__))
INPUT_SNAPSHOT_DIR = os.path.join(CURR_PATH, 'input_snapshots')
OUTPUT_SNAPSHOT_DIR = os.path.join(CURR_PATH, 'output_snapshots')


def load_snapshot(snapshot_file_name: str) -> dict:
    snapshot = os.path.join(INPUT_SNAPSHOT_DIR, snapshot_file_name)
    with open(snapshot, 'r') as file:
        return json.loads(file.read())

@mock.patch("pysisu.PySisu.fetch_sisu_api")
def test_general_perf(mock_pysisu, snapshot):
    mock_pysisu.return_value = load_snapshot('api__endpoint_handlers__test__generate_latest_workflow_results_snapshot.json')
    pysisu = PySisu('API_KEY', "URL")
    snapshot.snapshot_dir = OUTPUT_SNAPSHOT_DIR
    snapshot.assert_match(pysisu.get_results(1).to_csv(), 'general_performance_table.csv')
