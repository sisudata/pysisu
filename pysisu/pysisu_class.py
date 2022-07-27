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
import requests
from pysisu.formats import LatestAnalysisResultsFormats, Table
from pysisu.latest_analysis_result import to_table
from pysisu.query_helpers import build_url, pathjoin
from pysisu.sisu.v1.api import AnalysisRunResultsResponse

RECURSION_MAX = 1000
RESPONSE_MAX = 100
MAX_LIMIT = RECURSION_MAX * RESPONSE_MAX


class PySisu:
    '''
    Allows the ability to fetch/send commands to the sisu_api.
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

    def auto_paginate(
        self,
        analysis_id: int,
        params: dict,
        result: AnalysisRunResultsResponse,
    ) -> None:
        '''
        Appends the rest of the subgroups to `result`. 

        MUTATES: result
        '''
        if not result.pagination_hints.has_more:
            return result
        if params.get('limit', MAX_LIMIT) >= MAX_LIMIT:
            params['limit'] = MAX_LIMIT

        kda_result = result.analysis_result.key_driver_analysis_result
        subgroups = kda_result.subgroups
        if params.get('limit'):
            params['limit'] -= len(subgroups)

        if params.get('limit', 1) <= 0 or len(subgroups) == 0:
            return result

        next_page = self.get_results(
            analysis_id, params, True, format=LatestAnalysisResultsFormats.PROTO)
        kda_result.subgroups = subgroups + \
            next_page.analysis_result.key_driver_analysis_result.subgroups
        return result

    def get_results(
        self,
        analysis_id: int,
        params: dict = {"top_drivers": "True"},
        auto_paginate: bool = True,
        format: LatestAnalysisResultsFormats = LatestAnalysisResultsFormats.TABLE,
    ) -> Union[AnalysisRunResultsResponse, Table]:
        path = ['api/v1/analyses/', str(analysis_id), 'runs/latest']

        url_path = build_url(self._url,  pathjoin(*path), params)

        headers = headers = {"Authorization": self._api_key}

        r = requests.get(url_path, headers=headers)
        if(r.status_code != 200):
            raise Exception("Result did not complete", r)

        result = AnalysisRunResultsResponse().from_dict(r.json())
        if auto_paginate:
            result = self.auto_paginate(analysis_id, params, result)

        if format == LatestAnalysisResultsFormats.TABLE:
            return to_table(result)
        else:
            return result
