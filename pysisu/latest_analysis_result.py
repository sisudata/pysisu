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
from typing import Dict, List, Optional, Tuple, Union
from pysisu.formats import HeaderColumn, Row as FormatRow, Table
from pysisu.sisu.v1.api import AnalysisRunResultsResponse
from pysisu.sisu.v1.api import Factor, FactorValue, KeyDriverAnalysisResultGroupComparison, KeyDriverAnalysisResultSubgroup, KeyDriverAnalysisResultTimeComparison
import datetime
import betterproto


@dataclass
class LatestAnalysisResultTable(Table):
    pass


@dataclass
class Row(FormatRow):
    subgroup_id: int
    is_top_driver: bool
    factor_0_dimension: str
    factor_0_value: any
    factor_1_dimension: str
    factor_1_value: any
    factor_2_dimension: str
    factor_2_value: any

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


class safelist(list):
    # taken from https://stackoverflow.com/questions/5125619/why-doesnt-list-have-safe-get-method-like-dictionary
    def get(self, index, default=None):
        try:
            return self.__getitem__(index)
        except IndexError:
            return default


def get_factor_value(factor_value: FactorValue) -> Union[str, int, float, bool, datetime.datetime]:
    _val_type, value = betterproto.which_one_of(factor_value, "value_type")
    return value


@dataclass
class FactorDimVal:
    dimension: Optional[str]
    value: Optional[any]


def get_factor(dimension: str, factor: Factor) -> FactorDimVal:
    factor_type, _factor_data = betterproto.which_one_of(factor, "factor_type")
    if factor_type == "value":
        return FactorDimVal(dimension, get_factor_value(factor.value))
    elif factor_type == "bin":
        return FactorDimVal(dimension, f'{factor.bin.lower_bound_percentile} to {factor.bin.upper_bound_percentile}')
    elif factor_type == "keyword":
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
            str if getattr(row, var) is None else type(getattr(row, var))
            ) for var in vars(row).keys()]


def get_rows_time_comparision(
    subgroups: List[KeyDriverAnalysisResultSubgroup],
    time_comparision: KeyDriverAnalysisResultTimeComparison
) -> List[Row]:
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

    return rows


def get_rows_group_comparision(
    subgroups: List[KeyDriverAnalysisResultSubgroup],
    group_comparision: KeyDriverAnalysisResultGroupComparison
) -> List[Row]:
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

    return rows


def get_rows_general_performance(
    subgroups: List[KeyDriverAnalysisResultSubgroup]
) -> List[Row]:
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

    return rows


def _get_rows(result: AnalysisRunResultsResponse) -> LatestAnalysisResultTable:
    key_driver_analysis_result = result.analysis_result.key_driver_analysis_result

    subgroups = key_driver_analysis_result.subgroups
    if key_driver_analysis_result.time_comparison:
        return get_rows_time_comparision(subgroups, key_driver_analysis_result.time_comparison)
    elif key_driver_analysis_result.group_comparison:
        return get_rows_group_comparision(subgroups, key_driver_analysis_result.group_comparison)
    elif key_driver_analysis_result.general_performance._serialized_on_wire:
        return get_rows_general_performance(subgroups)
    else:
        raise ValueError("Invalid analysis_result")


def to_table(result: AnalysisRunResultsResponse, force_factor_value_to_str: bool = True) -> LatestAnalysisResultTable:
    rows = _get_rows(result)
    if force_factor_value_to_str:
        for i, row in enumerate(rows):
            row: Row = row
            rows[i].factor_0_value = str(row.factor_0_value)
            rows[i].factor_1_value = str(row.factor_1_value)
            rows[i].factor_2_value = str(row.factor_2_value)
    return LatestAnalysisResultTable(
        build_header_from_row(rows),
        rows
    )
