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

from typing import Union

import requests

from pysisu.formats import LatestAnalysisResultsFormats, Table
from pysisu.latest_analysis_result import to_table
from pysisu.proto.sisu.v1.api import (AnalysesListResponse,
                                      AnalysisRunResultsResponse,
                                      DataSetsResponse, DataSourceListResponse,
                                      DuplicateAnalysisResponse,
                                      GetAnalysisFiltersResponse,
                                      MetricsListResponse,
                                      SetAnalysisFiltersRequest)
from pysisu.query_helpers import build_url, pathjoin


class PySisuBaseException(Exception):
    pass


class PySisuInvalidReturnedPaginationHintsFromServer(PySisuBaseException):
    pass


class PySisuInvalidResponseFromServer(PySisuBaseException):
    pass


class PySisu:
    """
    Allows the ability to fetch/send commands to the sisu_api.
    """

    _url: str
    _api_key: str

    def __init__(
        self, api_key: str, url: str = "https://vip.sisudata.com"
    ) -> None:
        self._url = url
        self._api_key = api_key

    def set_url(self, url: str) -> "PySisu":
        self._url = url
        return self

    def set_api_key(self, api_key: str) -> "PySisu":
        self._api_key = api_key
        return self

    def _auto_paginate(
        self,
        analysis_id: int,
        params: dict,
        result: AnalysisRunResultsResponse,
    ) -> AnalysisRunResultsResponse:
        """
        Fetches the rest of the results if there is more results to fetch.

        Respects the limit parameter and only fetches a maximum of params['limit'] that is left.
        """
        if not result.pagination_hints.has_more:
            return result

        kda_result = result.analysis_result.key_driver_analysis_result
        subgroups = kda_result.segments

        if params.get("limit"):
            params["limit"] -= len(subgroups)

        if params.get("limit", 1) <= 0 or len(subgroups) == 0:
            return result

        next_cursor = int(subgroups[-1].id)
        if result.pagination_hints.has_more:
            if result.pagination_hints.next_starting_cursor is None:
                raise PySisuInvalidReturnedPaginationHintsFromServer(
                    "There is more to fetch, however the next_starting cursor is none."
                )

        params["starting_after"] = next_cursor

        next_page = self.get_results(
            analysis_id,
            params,
            True,
            format=LatestAnalysisResultsFormats.PROTO,
        )
        kda_result.segments = (
            subgroups
            + next_page.analysis_result.key_driver_analysis_result.segments
        )
        return result

    def _call_sisu_api(self, url_path: int, request_method="get", json=None) -> dict:
        headers = headers = {"Authorization": self._api_key, "User-Agent": "PySisu"}
        r = requests.request(request_method, url_path, headers=headers, json=json)
        if r.status_code != 200:
            raise PySisuInvalidResponseFromServer(
                "Result did not complete", r.content
            )
        return r.json()

    def fetch_sisu_api(self, analysis_id: int, params: dict) -> dict:
        path = ["api/v1/analyses/", str(analysis_id), "runs/latest"]
        url_path = build_url(self._url, pathjoin(*path), params)
        return self._call_sisu_api(url_path)

    def run(self, analysis_id: int):
        path = ["api/v1/analyses/", str(analysis_id), "run"]
        url_path = build_url(self._url, pathjoin(*path), {})
        self._call_sisu_api(url_path, request_method="POST")

    def analyses(self) -> AnalysesListResponse:
        path = ["api/v1/analyses"]
        url_path = build_url(self._url, pathjoin(*path), {})
        return AnalysesListResponse().from_dict(self._call_sisu_api(url_path))

    def get_results(
        self,
        analysis_id: int,
        params: dict = {"top_drivers": "False"},
        auto_paginate: bool = True,
        format: LatestAnalysisResultsFormats = LatestAnalysisResultsFormats.TABLE,
    ) -> Union[AnalysisRunResultsResponse, Table]:
        result = AnalysisRunResultsResponse().from_dict(
            self.fetch_sisu_api(analysis_id, params)
        )
        if auto_paginate:
            result = self._auto_paginate(analysis_id, params, result)

        if format == LatestAnalysisResultsFormats.TABLE:
            return to_table(result)
        else:
            return result

    def metrics(self) -> MetricsListResponse:
        path = ["api/v1/metrics"]
        url_path = build_url(self._url, pathjoin(*path), {})
        return MetricsListResponse().from_dict(self._call_sisu_api(url_path))

    def data_sources(self) -> DataSourceListResponse:
        path = ["api/v1/data_sources"]
        url_path = build_url(self._url, pathjoin(*path), {})
        return DataSourceListResponse().from_dict(
            self._call_sisu_api(url_path)
        )

    def datasets(self) -> DataSetsResponse:
        path = ["api/v1/datasets"]
        url_path = build_url(self._url, pathjoin(*path), {})
        return DataSetsResponse().from_dict(self._call_sisu_api(url_path))

    def get_filters(self, analysis_id: int) -> GetAnalysisFiltersResponse:
        path = [f"api/v1/analyses/{analysis_id}/filters"]
        url_path = build_url(self._url, pathjoin(*path), {})
        return GetAnalysisFiltersResponse().from_dict(self._call_sisu_api(url_path))

    def set_filters(self, analysis_id: int , expr: SetAnalysisFiltersRequest):
        path = [f"api/v1/analyses/{analysis_id}/filters"]
        url_path = build_url(self._url, pathjoin(*path), {})
        expr = expr.to_dict() if isinstance(expr, SetAnalysisFiltersRequest) else expr
        return self._call_sisu_api(url_path, request_method="PUT", json=expr)

    def duplicate_analysis(self, analysis_id: int) -> DuplicateAnalysisResponse:
        path = [f"api/v1/analyses/{analysis_id}/duplicate"]
        url_path = build_url(self._url, pathjoin(*path), {})
        return DuplicateAnalysisResponse().from_dict(self._call_sisu_api(url_path, request_method="POST"))
