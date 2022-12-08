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
from pysisu.formats import HeaderColumn, Row, Table
from pysisu.proto.sisu.v1.api import AnalysisRunResultsResponse
from pysisu.proto.sisu.v1.api import (
    Factor,
    Value,
    KeyDriverAnalysisResultGroupComparison,
    KeyDriverAnalysisResultSegment,
    KeyDriverAnalysisResultTimeComparison,
    TrendAnalysisResultSegment,
    TrendAnalysisResultTrend,
    KeyDriverAnalysisResultSegmentConfidenceLevel
)
import datetime
import betterproto


@dataclass
class LatestAnalysisResultTable(Table):
    pass


@dataclass
class KDARow(Row):
    subgroup_id: int
    confidence: str
    factor_0_dimension: str
    factor_0_value: any
    factor_1_dimension: str
    factor_1_value: any
    factor_2_dimension: str
    factor_2_value: any
    impact: float


@dataclass
class TimeCompareRow(KDARow):
    previous_period_size: float
    recent_period_size: float
    previous_period_value: float
    recent_period_value: float
    previous_period_start: datetime.datetime
    previous_period_end: datetime.datetime
    recent_period_start: datetime.datetime
    recent_period_end: datetime.datetime


@dataclass
class GroupCompareRow(KDARow):
    group_a_size: float
    group_b_size: float
    group_a_value: float
    group_b_value: float
    group_a_name: str
    group_b_name: str


@dataclass
class GeneralPerformanceRow(KDARow):
    size: float
    value: float


@dataclass
class TrendRow(Row):
    subgroup_id: int
    factor_0_dimension: str
    factor_0_value: any
    factor_1_dimension: str
    factor_1_value: any
    factor_2_dimension: str
    factor_2_value: any
    impact: float
    start_dt: datetime.datetime
    end_dt: datetime.datetime
    intercept: Optional[float]
    slope: Optional[float]
    size: Optional[float]


class safelist(list):
    # taken from https://stackoverflow.com/questions/5125619/why-doesnt-list-have-safe-get-method-like-dictionary
    def get(self, index, default=None):
        try:
            return self.__getitem__(index)
        except IndexError:
            return default


def get_factor_value(
    factor_value: Value,
) -> Union[str, int, float, bool, datetime.datetime]:
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
        return FactorDimVal(
            dimension,
            f"{factor.bin.lower_bound}-{factor.bin.upper_bound} ({factor.bin.lower_bound_percentile}-{factor.bin.upper_bound_percentile} percentile)",
        )
    elif factor_type == "keyword":
        return FactorDimVal(dimension, factor.keyword.keyword)
    else:
        raise ValueError("invalid factor")


def get_factors(
    factors: Dict[str, Factor]
) -> Tuple[FactorDimVal, FactorDimVal, FactorDimVal]:
    converted_factors = safelist(
        [get_factor(dim, fact) for dim, fact in factors.items()]
    )

    empty_factor = FactorDimVal(None, None)
    return (
        converted_factors.get(0),
        converted_factors.get(1, empty_factor),
        converted_factors.get(2, empty_factor),
    )


def build_header_from_row(rows: List[Row]) -> List[HeaderColumn]:
    if not rows:
        return []
    row = rows[0]
    return [
        HeaderColumn(
            var, str if getattr(row, var) is None else type(getattr(row, var))
        )
        for var in vars(row).keys()
    ]


def get_rows_time_comparision(
    subgroups: List[KeyDriverAnalysisResultSegment],
    time_comparision: KeyDriverAnalysisResultTimeComparison,
) -> List[Row]:
    rows = []
    for subgroup in subgroups:
        factor_0, factor_1, factor_2 = get_factors(subgroup.factors)

        r = TimeCompareRow(
            subgroup_id=subgroup.id,
            confidence=subgroup.confidence.name,
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
            impact=subgroup.impact,
        )
        rows.append(r)

    return rows


def get_rows_group_comparision(
    subgroups: List[KeyDriverAnalysisResultSegment],
    group_comparision: KeyDriverAnalysisResultGroupComparison,
) -> List[Row]:
    rows = []
    for subgroup in subgroups:
        factor_0, factor_1, factor_2 = get_factors(subgroup.factors)

        r = GroupCompareRow(
            subgroup_id=subgroup.id,
            confidence=subgroup.confidence.name,
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
            impact=subgroup.impact,
        )
        rows.append(r)

    return rows


def get_rows_general_performance(
    subgroups: List[KeyDriverAnalysisResultSegment],
) -> List[Row]:
    rows = []
    for subgroup in subgroups:
        factor_0, factor_1, factor_2 = get_factors(subgroup.factors)

        r = GeneralPerformanceRow(
            subgroup_id=subgroup.id,
            confidence=subgroup.confidence.name,
            factor_0_dimension=factor_0.dimension,
            factor_0_value=factor_0.value,
            factor_1_dimension=factor_1.dimension,
            factor_1_value=factor_1.value,
            factor_2_dimension=factor_2.dimension,
            factor_2_value=factor_2.value,
            size=subgroup.general_performance.size,
            value=subgroup.general_performance.value,
            impact=subgroup.impact,
        )
        rows.append(r)

    return rows


def get_rows_trend(
    subgroups: List[TrendAnalysisResultSegment],
    overall_trends: List[TrendAnalysisResultTrend],
) -> List[Row]:
    rows = []

    for otrend in overall_trends:
        r = TrendRow(
            subgroup_id=None,
            factor_0_dimension=None,
            factor_0_value=None,
            factor_1_dimension=None,
            factor_1_value=None,
            factor_2_dimension=None,
            factor_2_value=None,
            impact=otrend.trend,
            start_dt=otrend.time_range.start,
            end_dt=otrend.time_range.end,
            intercept=otrend.intercept,
            slope=otrend.trend,
            size=otrend.size,
        )
        rows.append(r)

    for subgroup in subgroups:
        factor_0, factor_1, factor_2 = get_factors(subgroup.factors)

        if factor_1.dimension is not None:
            if factor_2.dimension is not None:
                factor_0, factor_1, factor_2 = sorted(
                    (factor_0, factor_1, factor_2),
                    key=lambda factor: factor.dimension,
                )
            else:
                factor_0, factor_1 = sorted(
                    (factor_0, factor_1), key=lambda factor: factor.dimension
                )

        for trend in subgroup.trends:
            r = TrendRow(
                subgroup_id=subgroup.id,
                factor_0_dimension=factor_0.dimension,
                factor_0_value=factor_0.value,
                factor_1_dimension=factor_1.dimension,
                factor_1_value=factor_1.value,
                factor_2_dimension=factor_2.dimension,
                factor_2_value=factor_2.value,
                impact=subgroup.impact,
                start_dt=trend.time_range.start,
                end_dt=trend.time_range.end,
                intercept=trend.intercept,
                slope=trend.trend,
                size=trend.size,
            )
            rows.append(r)

    return rows


def _get_rows(result: AnalysisRunResultsResponse) -> List[Row]:
    # Under the assumption that an analysis can't be
    # more than one of [KDA, TD]
    if result.analysis_result.key_driver_analysis_result:
        analysis_result = result.analysis_result.key_driver_analysis_result
        subgroups = analysis_result.segments

        if analysis_result.time_comparison:
            return get_rows_time_comparision(
                subgroups, analysis_result.time_comparison
            )
        elif analysis_result.group_comparison:
            return get_rows_group_comparision(
                subgroups, analysis_result.group_comparison
            )
        elif analysis_result.general_performance._serialized_on_wire:
            return get_rows_general_performance(subgroups)
        else:
            raise ValueError("Invalid key_driver_analysis_result")

    elif result.analysis_result.trend_analysis_result:
        analysis_result = result.analysis_result.trend_analysis_result
        subgroups = analysis_result.segments

        return get_rows_trend(subgroups, analysis_result.overall_trends)

    else:
        raise ValueError("Invalid analysis_result")


def to_table(result: AnalysisRunResultsResponse) -> LatestAnalysisResultTable:
    rows = _get_rows(result)
    return LatestAnalysisResultTable(build_header_from_row(rows), rows)
