#
# Copyright 2022 Sisu Data, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from pathlib import Path

from setuptools import find_packages, setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
pkg_vars = {}

# Doing versions is hard and annoying in python.
# See https://stackoverflow.com/questions/458550/standard-way-to-embed-version-into-python-package
with open("pysisu/version.py") as fp:
    exec(fp.read(), pkg_vars)

setup(
    name="pysisu",
    packages=find_packages(include=["pysisu", "pysisu.*"]),
    install_requires=["betterproto>=2.0.0b4", "requests-cache", "requests"],
    version=pkg_vars['__version__'],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
