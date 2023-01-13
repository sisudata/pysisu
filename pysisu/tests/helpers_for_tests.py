import json
import os


CURR_PATH = os.path.dirname(os.path.abspath(__file__))
INPUT_SNAPSHOT_DIR = os.path.join(CURR_PATH, "input_snapshots")
OUTPUT_SNAPSHOT_DIR = os.path.join(CURR_PATH, "output_snapshots")
SNAPSHOT_DICT = {
    "time compare": "auto_time_compare_kda_result.json",
    "group compare": "auto_group_compare_kda_result.json",
    "general performance": "auto_gen_perf_kda_result.json",
    "trend": "auto_trend_analysis_result.json",
    "time compare has more": "auto_time_compare_kda_result_has_more.json",
    "time compare has more doubled": "auto_time_compare_kda_result_has_more_doubled.json",
    "list analyses": "auto_active_analysis_list.json",
    "list metrics": "auto_active_metrics_list.json",
    "list data sources": "auto_data_source_list.json",
    "list datasets": "auto_dataset_list.json",
    "get analysis filters": "mixed_filter_expression.json",
    "list projects": "auto_project_list.json",
    "list project analyses": "auto_project_analysis_list.json",
}


def load_snapshot(snapshot_name: str) -> dict:
    snapshot = os.path.join(INPUT_SNAPSHOT_DIR, SNAPSHOT_DICT[snapshot_name])
    with open(snapshot, "r") as file:
        return json.loads(file.read())


def pyapp_api_snapshots_to_pysisu() -> None:
    """
    Recursively walks the pyapp API snapshots directory
    to get snapshots, copies them all into pysisu/tests/input_snapshots, and
    removes any pysisu snapshots that don't correspond to a pyapp snapshot.

    If not run from Sisu core repo, do nothing.
    """

    if os.environ.get("SKIP_SNAPSHOT_MIGRATION") == "true":
        return

    try:
        from pysisu.pyapp_snapshot_directory import PYAPP_SNAPSHOT_DIR
    except ModuleNotFoundError:
        return 0

    # keep track of snapshots without a pyapp counterpart
    snapshots_to_keep = {
        "auto_time_compare_kda_result_has_more.json",
        "auto_time_compare_kda_result_has_more_doubled.json",
    }

    # check for existence of pyapp snapshots in the same directory
    if not os.path.isdir(PYAPP_SNAPSHOT_DIR):
        raise FileNotFoundError(
            1,
            f"pyapp api snapshots directory no longer in {PYAPP_SNAPSHOT_DIR}, please update pyapp_snapshot_directory.py with new location",
        )

    # write pyapp snapshots to input_snapshots recursively & flatten dir structure
    for subdir, _, files in os.walk(PYAPP_SNAPSHOT_DIR):
        for file in files:
            snapshots_to_keep.add(file)
            with open(os.path.join(subdir, file), "r") as pyapp_snapshot:
                pyapp_contents = pyapp_snapshot.read()
                if os.path.exists(os.path.join(INPUT_SNAPSHOT_DIR, file)):
                    with open(
                        os.path.join(INPUT_SNAPSHOT_DIR, file), "r"
                    ) as pysisu_snapshot:
                        if pysisu_snapshot.read() == pyapp_contents:
                            continue
                    with open(
                        os.path.join(INPUT_SNAPSHOT_DIR, file), "w"
                    ) as pysisu_snapshot:
                        print(
                            f"Current snapshot {file} needs to be updated. Updating..."
                        )
                        pysisu_snapshot.write(pyapp_contents)
                        continue

                # else file doesn't exist in INPUT_SNAPSHOT_DIR
                with open(
                    os.path.join(INPUT_SNAPSHOT_DIR, file), "w"
                ) as pysisu_snapshot:
                    print(
                        f"Snapshot {file} does not yet exist in pysisu. Writing..."
                    )
                    pysisu_snapshot.write(pyapp_contents)

    for subdir, _, files in os.walk(INPUT_SNAPSHOT_DIR):
        for file in files:
            if file not in snapshots_to_keep:
                print(
                    f"Snapshot {file} no longer exists in pyapp. Deleting..."
                )
                os.remove(os.path.join(INPUT_SNAPSHOT_DIR, file))
