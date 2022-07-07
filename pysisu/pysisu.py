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

from io import UnsupportedOperation
from typing import Union
from urllib import request
from pysisu.formats import LatestAnalysisFormats
from pysisu.query_helpers import build_url, pathjoin
from pysisu.sisu.v1.api import LatestAnalysisResultResponse


class Table:
    # TODO move over from query_wrapper
    pass


class PySisu:
    '''
    Allows the ability to fetch/send commands to the sisu_api
    '''

    _url: str
    _api_key: str

    def __init__(self, api_key: str, url: str = 'https://vip.sisudata.com') -> None:
        self._url = url
        self._api_key = api_key

    def set_url(self, url: str) -> "PySisu":
        self._url = url
        return self

    def set_api_key(self, api_key: str) -> "PySisu":
        self._api_key = api_key
        return self

    def get_results(
        self,
        analysis_id: int,
        params: dict = {},
        auto_paginate: bool = True,
        format: LatestAnalysisFormats = LatestAnalysisFormats.CSV,
    ) -> Union[LatestAnalysisResultResponse, Table]:

        if auto_paginate:
            raise UnsupportedOperation("This will be supported soon")
        path = ['api/v1/analyses/', str(analysis_id), 'runs/latest']

        url_path = build_url(self._url,  pathjoin(*path), params)

        headers = headers = {"Authorization": self._api_key}

        r = request.get(url_path, headers=headers)
        if(r.status_code != 200):
            raise Exception("Result did not complete", r)

        return LatestAnalysisResultResponse().from_dict(r.json())
