import os
import re
import requests
import subprocess
import sys
from packaging.version import parse

PYSISU_ROOT = os.path.abspath(
    os.path.join(__file__, os.pardir, os.pardir, os.pardir)
)

def main() -> int:
    most_recent_common_ancestor = (
        subprocess.run(
            ["git", "merge-base", "HEAD", "master"],
            capture_output=True,
            check=True,
        )
        .stdout.decode("utf-8")
        .rstrip("\n")
    )

    pysisu_diff = subprocess.run(
        ["git", "diff", "--quiet", most_recent_common_ancestor, "./pysisu"]
    ).returncode

    if not pysisu_diff:
        return 0

    current_master_commit = (
        subprocess.run(
            ["git", "rev-parse", "master"], capture_output=True, check=True
        )
        .stdout.decode("utf-8")
        .rstrip("\n")
    )

    master_pysisu_version = subprocess.run(
        ["git", "show", f"{current_master_commit}:./pysisu/version.py"],
        capture_output=True,
        check=True,
    ).stdout.decode("utf-8")

    local_pysisu_version = subprocess.run(
        ["cat", os.path.join(PYSISU_ROOT, "pysisu", "version.py")],
        capture_output=True,
        check=True,
    ).stdout.decode("utf-8")

    pypi_latest_version = requests.get(
        "https://pypi.org/pypi/pysisu/json", headers={"Connection": "close"}
    ).json()["info"]["version"]

    # find version between quotes from: __version__ = "0.13.2"
    version_regex = '"([^"]*)"'

    master_version_matches = re.findall(version_regex, master_pysisu_version)
    local_version_matches = re.findall(version_regex, local_pysisu_version)

    if len(local_version_matches) != 1:
        raise SyntaxError(
            "Local core/pysisu/pysisu/version.py file contains invalid semantic version."
        )

    if len(master_version_matches) != 1:
        raise SyntaxError(
            "Master core/pysisu/pysisu/version.py file contains invalid semantic version."
        )

    local_version_match = local_version_matches[0]
    master_version_match = master_version_matches[0]

    if parse(local_version_match) <= parse(pypi_latest_version):
        print("Pysisu version must be greater than latest version on PyPI.")
        return 1
    if parse(local_version_match) < parse(master_version_match):
        print(
            "Pysisu version should not be lower than current master version. "
            "Please merge or rebase master and update version if necessary."
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
