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

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Type
import requests
import urllib
from pysisu.sisu.v1.api import Factor, FactorValue, KeyDriverAnalysisResultGroupComparison, KeyDriverAnalysisResultSubgroup, KeyDriverAnalysisResultTimeComparison, LatestAnalysisResultResponse
import datetime


class safelist(list):
    # taken from https://stackoverflow.com/questions/5125619/why-doesnt-list-have-safe-get-method-like-dictionary
    def get(self, index, default=None):
        try:
            return self.__getitem__(index)
        except IndexError:
            return default


@dataclass
class Table:
    header: List["HeaderColumn"]
    rows: List["Row"]


@dataclass
class HeaderColumn:
    column_name: str
    column_type: Type


@dataclass
class Row:
    subgroup_id: int
    is_top_driver: bool
    factor_0_dimension: str
    factor_0_value: str
    factor_1_dimension: str
    factor_1_value: str
    factor_2_dimension: str
    factor_2_value: str

    def __str__(self):
        variables = []
        for x in vars(self).values():
            if isinstance(x, (int, float)):
                variables.append(x)
            else:
                variables.append(f"'{x}'")
        return ','.join([str(x) for x in variables])


@dataclass
class TimeCompareRow(Row):
    previous_period_size: float
    recent_period_size: float
    previous_period_value: float
    recent_period_value: float
    previous_period_start: datetime.datetime
    previous_period_end: datetime.datetime
    recent_period_start: datetime.datetime
    recent_period_end: datetime.datetime


@dataclass
class GroupCompareRow(Row):
    group_a_size: float
    group_b_size: float
    group_a_value: float
    group_b_value: float
    group_a_name: str
    group_b_name: str


@dataclass
class GeneralPerformanceRow(Row):
    size: float
    value: float


def build_url(base_url, path, args_dict):
    url_parts = list(urllib.parse.urlparse(base_url))
    url_parts[2] = path
    url_parts[4] = urllib.parse.urlencode(args_dict)
    return urllib.parse.urlunparse(url_parts)


def get_factor_value(factor: Factor) -> str:
    value: FactorValue = factor.value
    val = (
        value.boolean_value or
        value.float_value or
        value.integer_value or
        value.string_value or
        value.timestamp_value
    )
    return str(val)


@dataclass
class FactorDimVal:
    dimension: Optional[str]
    value: Optional[any]


def get_factor(dimension: str, factor: Factor) -> FactorDimVal:
    if factor.bin:
        return FactorDimVal(dimension, f'{factor.bin.lower_bound_percentile} to {factor.bin.upper_bound_percentile}')
    elif factor.value is not None:
        return FactorDimVal(dimension, get_factor_value(factor))
    elif factor.keyword:
        return FactorDimVal(dimension, factor.keyword.keyword)
    else:
        raise ValueError("invalid factor")


def get_factors(factors: Dict[str, Factor]) -> Tuple[FactorDimVal, FactorDimVal, FactorDimVal]:
    converted_factors = safelist([get_factor(dim, fact)
                                  for dim, fact in factors.items()])

    empty_factor = FactorDimVal(None, None)
    return converted_factors.get(0), converted_factors.get(1, empty_factor), converted_factors.get(2, empty_factor)


def build_header_from_row(rows: List[Row]) -> List[HeaderColumn]:
    if not rows:
        return []
    row = rows[0]
    return [HeaderColumn(
            var,
            type(getattr(row, var))
            ) for var in vars(row).keys()]


def get_table_time_comparision(
    subgroups: List[KeyDriverAnalysisResultSubgroup],
    time_comparision: KeyDriverAnalysisResultTimeComparison
) -> Table:
    rows = []
    for subgroup in subgroups:
        factor_0, factor_1, factor_2 = get_factors(subgroup.factors)

        r = TimeCompareRow(
            subgroup_id=subgroup.id,
            is_top_driver=bool(subgroup.is_top_driver),
            factor_0_dimension=factor_0.dimension,
            factor_0_value=factor_0.value,
            factor_1_dimension=factor_1.dimension,
            factor_1_value=factor_1.value,
            factor_2_dimension=factor_2.dimension,
            factor_2_value=factor_2.value,
            previous_period_size=subgroup.time_comparison.previous_period_size,
            recent_period_size=subgroup.time_comparison.recent_period_size,
            previous_period_value=subgroup.time_comparison.previous_period_value,
            recent_period_value=subgroup.time_comparison.recent_period_value,
            previous_period_start=time_comparision.previous_period.start,
            previous_period_end=time_comparision.previous_period.end,
            recent_period_start=time_comparision.recent_period.start,
            recent_period_end=time_comparision.recent_period.end,
        )
        rows.append(r)

    return Table(
        build_header_from_row(rows),
        rows
    )


def get_table_group_comparision(
    subgroups: List[KeyDriverAnalysisResultSubgroup],
    group_comparision: KeyDriverAnalysisResultGroupComparison
) -> Table:
    rows = []
    for subgroup in subgroups:
        factor_0, factor_1, factor_2 = get_factors(subgroup.factors)

        r = GroupCompareRow(
            subgroup_id=subgroup.id,
            is_top_driver=bool(subgroup.is_top_driver),
            factor_0_dimension=factor_0.dimension,
            factor_0_value=factor_0.value,
            factor_1_dimension=factor_1.dimension,
            factor_1_value=factor_1.value,
            factor_2_dimension=factor_2.dimension,
            factor_2_value=factor_2.value,
            group_a_size=subgroup.group_comparison.group_a_size,
            group_b_size=subgroup.group_comparison.group_b_size,
            group_a_value=subgroup.group_comparison.group_a_value,
            group_b_value=subgroup.group_comparison.group_b_value,
            group_a_name=group_comparision.group_a.name,
            group_b_name=group_comparision.group_b.name,
        )
        rows.append(r)

    return Table(
        build_header_from_row(rows),
        rows
    )


def get_table_general_performance(
    subgroups: List[KeyDriverAnalysisResultSubgroup]
) -> Table:
    rows = []
    for subgroup in subgroups:
        factor_0, factor_1, factor_2 = get_factors(subgroup.factors)

        r = GeneralPerformanceRow(
            subgroup_id=subgroup.id,
            is_top_driver=bool(subgroup.is_top_driver),
            factor_0_dimension=factor_0.dimension,
            factor_0_value=factor_0.value,
            factor_1_dimension=factor_1.dimension,
            factor_1_value=factor_1.value,
            factor_2_dimension=factor_2.dimension,
            factor_2_value=factor_2.value,
            size=subgroup.general_performance.size,
            value=subgroup.general_performance.value,
        )
        rows.append(r)

    return Table(
        build_header_from_row(rows),
        rows
    )


def pathjoin(*args) -> str:
    return '/'.join(s.strip('/') for s in args)


def _get_table(url: str, static_analysis_id: int, auth_key: str, params: dict = {}) -> Table:
    path = ['api/v1/analyses/', str(static_analysis_id), 'runs/latest']

    url_path = build_url(url,  pathjoin(*path), params)
    
    headers = headers = {"Authorization": auth_key}

    r = requests.get(url_path, headers=headers)
    if(r.status_code != 200):
        raise Exception("Result did not complete", r)
    
    latest_analysis_response: LatestAnalysisResultResponse = LatestAnalysisResultResponse().from_dict(r.json())
    key_driver_analysis_result = latest_analysis_response.analysis_result.key_driver_analysis_result

    subgroups = key_driver_analysis_result.subgroups
    if key_driver_analysis_result.time_comparison:
        return get_table_time_comparision(subgroups, key_driver_analysis_result.time_comparison)
    elif key_driver_analysis_result.group_comparison:
        return get_table_group_comparision(subgroups, key_driver_analysis_result.group_comparison)
    elif key_driver_analysis_result.general_performance._serialized_on_wire:
        return get_table_general_performance(subgroups)
    else:
        raise ValueError("Invalid analysis_result")


def get_results(analysis_id: int, auth_key: str, params: dict = {}, auto_paginate: bool = True, url: str = 'https://vip.sisudata.com') -> Table:
    table = _get_table(url, analysis_id, auth_key, params)
    if auto_paginate:
        if not table.rows:
            return table
        if params.get('limit'):
            params['limit'] -= len(table.rows)
        if params.get('limit', 0) < 0:
            return table
        params['starting_after'] = table.rows[-1].subgroup_id

        rest_of_table = get_results(analysis_id, auth_key, params, auto_paginate, url)

        table.rows = table.rows + rest_of_table.rows
        return table
    else:
        return table
