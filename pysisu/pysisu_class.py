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

import warnings
from datetime import timedelta
from http import HTTPStatus
from typing import Optional, Union

import requests
import requests_cache

from pysisu.formats import LatestAnalysisResultsFormats, Table
from pysisu.latest_analysis_result import to_table
from pysisu.proto.sisu.v1.api import (AnalysesListResponse,
                                      AnalysisRunResultsResponse,
                                      DataSetsResponse, DataSourceListResponse,
                                      DuplicateAnalysisResponse,
                                      GetAnalysisFiltersResponse,
                                      MetricsListResponse,
                                      SetAnalysisFiltersRequest,
                                      GetSegmentDataResponse,
                                      )
from pysisu.query_helpers import build_url, pathjoin, semver_parse
from pysisu.version import __version__ as PYSISU_VERSION


class PySisuBaseException(Exception):
    pass


class PySisuInvalidReturnedPaginationHintsFromServer(PySisuBaseException):
    pass


class PySisuInvalidResponseFromServer(PySisuBaseException):
    pass


class PySisuDeprecatedVersionException(PySisuBaseException):
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
        self.session = requests_cache.CachedSession(
            cache_name="pysisu_cache",
            use_cache_dir=True,
            expire_after=timedelta(days=1),
        )
        self._check_compatibility()
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
        **kwargs
    ) -> AnalysisRunResultsResponse:
        """
        Fetches the rest of the results if there is more results to fetch.

        Respects the limit parameter and only fetches a maximum of params['limit'] that is left.
        """
        if not result.pagination_hints.has_more:
            return result

        kda_result = result.analysis_result.key_driver_analysis_result
        subgroups = kda_result.segments

        kwargs = {**params, **kwargs}  # fold together so we just use 1 dict
        if kwargs.get("limit"):
            kwargs["limit"] -= len(subgroups)

        if kwargs.get("limit", 1) <= 0 or len(subgroups) == 0:
            return result

        next_cursor = int(subgroups[-1].id)
        if result.pagination_hints.has_more:
            if result.pagination_hints.next_starting_cursor is None:
                raise PySisuInvalidReturnedPaginationHintsFromServer(
                    "There is more to fetch, however the next_starting cursor is none."
                )

        kwargs["starting_after"] = next_cursor

        next_page = self.get_results(
            analysis_id,
            format=LatestAnalysisResultsFormats.PROTO,
            **kwargs
        )
        kda_result.segments = (
            subgroups
            + next_page.analysis_result.key_driver_analysis_result.segments
        )
        return result

    def _call_sisu_api(self, url_path: int, request_method="get", json=None) -> dict:
        headers = {
            "Authorization": self._api_key,
            "User-Agent": f"PySisu/{PYSISU_VERSION}",
        }
        # don't cache API responses, we don't want to return stale responses
        # or cache in-flight status
        with self.session.cache_disabled():
            r = self.session.request(
                request_method, url_path, headers=headers, json=json
            )
        if r.status_code != HTTPStatus.OK:
            raise PySisuInvalidResponseFromServer(
                "Result did not complete", r.content
            )
        return r.json()

    def _check_compatibility(self):
        r = self.session.get("https://pypi.python.org/pypi/pysisu/json")
        try:
            latest_version = r.json()["info"]["version"]
        except (requests.RequestException, KeyError):
            warnings.warn(
                "Unable to verify current pysisu version with PyPI; get "
                "latest version with 'pip install -U pysisu'"
            )
            return

        local_major, local_minor, local_patch = semver_parse(PYSISU_VERSION)
        latest_major, latest_minor, latest_patch = semver_parse(latest_version)

        if (local_major < latest_major
                or (local_major == 0 and local_minor < latest_minor)):
            raise PySisuDeprecatedVersionException(
                "Pysisu has been updated with breaking changes from "
                f"{PYSISU_VERSION} to {latest_version}; get latest version "
                "with 'pip install -U pysisu'"
            )
        if (local_minor, local_patch) < (latest_minor, latest_patch):
            warnings.warn(
                f"Pysisu has been updated from {PYSISU_VERSION} to "
                f"{latest_version}; get latest version with 'pip install -U "
                "pysisu'"
            )

    def fetch_sisu_api(self, analysis_id: int, params: dict = {}, **kwargs) -> dict:
        path = ["api/v1/analyses/", str(analysis_id), "runs/latest"]
        url_path = build_url(self._url, pathjoin(*path), {**params, **kwargs})
        return self._call_sisu_api(url_path)

    def run(self, analysis_id: int, **kwargs):
        path = ["api/v1/analyses/", str(analysis_id), "run"]
        url_path = build_url(self._url, pathjoin(*path), kwargs)
        self._call_sisu_api(url_path, request_method="POST")

    def analyses(self, **kwargs) -> AnalysesListResponse:
        path = ["api/v1/analyses"]
        url_path = build_url(self._url, pathjoin(*path), kwargs)
        return AnalysesListResponse().from_dict(self._call_sisu_api(url_path))

    def get_results(
        self,
        analysis_id: int,
        params: dict = {"confidence_gte": "LOW"},
        auto_paginate: bool = True,
        format: LatestAnalysisResultsFormats = LatestAnalysisResultsFormats.TABLE,
        **kwargs
    ) -> Union[AnalysisRunResultsResponse, Table]:
        assert type(params) is dict
        assert type(kwargs) is dict
        kwargs = {**params, **kwargs}

        result = AnalysisRunResultsResponse().from_dict(
            self.fetch_sisu_api(analysis_id, **kwargs)
        )
        if auto_paginate:
            result = self._auto_paginate(analysis_id, kwargs, result)

        if format == LatestAnalysisResultsFormats.TABLE:
            return to_table(result)
        else:
            return result

    def metrics(self, **kwargs) -> MetricsListResponse:
        path = ["api/v1/metrics"]
        url_path = build_url(self._url, pathjoin(*path), kwargs)
        return MetricsListResponse().from_dict(self._call_sisu_api(url_path))

    def data_sources(self, **kwargs) -> DataSourceListResponse:
        path = ["api/v1/data_sources"]
        url_path = build_url(self._url, pathjoin(*path), kwargs)
        return DataSourceListResponse().from_dict(
            self._call_sisu_api(url_path)
        )

    def datasets(self, **kwargs) -> DataSetsResponse:
        path = ["api/v1/datasets"]
        url_path = build_url(self._url, pathjoin(*path), kwargs)
        return DataSetsResponse().from_dict(self._call_sisu_api(url_path))

    def get_filters(self, analysis_id: int, **kwargs) -> GetAnalysisFiltersResponse:
        path = [f"api/v1/analyses/{analysis_id}/filters"]
        url_path = build_url(self._url, pathjoin(*path), kwargs)
        return GetAnalysisFiltersResponse().from_dict(self._call_sisu_api(url_path))

    def set_filters(self, analysis_id: int, expr: SetAnalysisFiltersRequest, **kwargs):
        path = [f"api/v1/analyses/{analysis_id}/filters"]
        url_path = build_url(self._url, pathjoin(*path), kwargs)
        expr = expr.to_dict() if isinstance(expr, SetAnalysisFiltersRequest) else expr
        return self._call_sisu_api(url_path, request_method="PUT", json=expr)

    def duplicate_analysis(
        self,
        analysis_id: int,
        name: Optional[str] = None,
        **kwargs
    ) -> DuplicateAnalysisResponse:
        path = [f"api/v1/analyses/{analysis_id}/duplicate"]
        url_path = build_url(self._url, pathjoin(*path), kwargs)
        json = {"name": name} if name else None
        return DuplicateAnalysisResponse().from_dict(
            self._call_sisu_api(url_path, request_method="POST", json=json)
        )

    def get_factor_data(self, segment_id: int) -> GetSegmentDataResponse:
        path = [f"api/v1/segments/{segment_id}/data_query"]
        url_path = build_url(self._url, pathjoin(*path), {})
        return GetSegmentDataResponse().from_dict(self._call_sisu_api(url_path, request_method="GET"))
