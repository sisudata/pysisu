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

import re
import urllib
from typing import Tuple


def pathjoin(*args) -> str:
    return '/'.join(s.strip('/') for s in args)


def build_url(base_url, path, args_dict):
    url_parts = list(urllib.parse.urlparse(base_url))
    url_parts[2] = path
    url_parts[4] = urllib.parse.urlencode(args_dict)
    return urllib.parse.urlunparse(url_parts)


def semver_parse(version: str) -> Tuple[int, int, int]:
    pattern = r"([1-9]\d*|0)\.([1-9]\d*|0)\.([1-9]\d*|0)"
    match = re.compile(pattern).match(version)
    if match is None:
        raise SyntaxError(
            f"{version} is not a valid semantic version"
        )
    return tuple(int(x) for x in match.groups())
