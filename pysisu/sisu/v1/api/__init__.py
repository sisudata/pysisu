# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: api.proto
# plugin: python-betterproto
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional

import betterproto
from betterproto.grpc.grpclib_server import ServiceBase


class AnalysisType(betterproto.Enum):
    """Type of Analysis eg. KEY_DRIVER."""

    ANALYSIS_TYPE_UNKNOWN = 0
    ANALYSIS_TYPE_KEY_DRIVER = 1
    ANALYSIS_TYPE_TREND = 2


class AnalysisResultRunStatus(betterproto.Enum):
    RUN_STATUS_UNKNOWN = 0
    RUN_STATUS_IN_FLIGHT = 1
    RUN_STATUS_FAILED = 2
    RUN_STATUS_COMPLETED = 3


class AnalysisResultRunType(betterproto.Enum):
    RUN_TYPE_UNKNOWN = 0
    RUN_TYPE_SCHEDULED = 1
    RUN_TYPE_MANUAL = 2


@dataclass(eq=False, repr=False)
class AnalysesResultRequest(betterproto.Message):
    """Request parameters for get analysis results."""

    # A limit on the number of objects to be returned, between 1 and 100. Default
    # value is 100.
    limit: Optional[int] = betterproto.message_field(1, wraps=betterproto.TYPE_UINT64)
    # starting_after is an object ID that defines your place in the list. For
    # instance, if you make a analysis list request and receive 100, ending with
    # id = 89, your subsequent call can include starting_after=89 in order to
    # fetch the next page of the list.
    starting_after: Optional[int] = betterproto.message_field(
        2, wraps=betterproto.TYPE_INT64
    )
    # Formats the return as a csv.
    csv: Optional[bool] = betterproto.message_field(3, wraps=betterproto.TYPE_BOOL)
    # filter by only top driver results
    top_drivers: Optional[str] = betterproto.message_field(
        4, wraps=betterproto.TYPE_STRING
    )


@dataclass(eq=False, repr=False)
class ListAnalysesRequest(betterproto.Message):
    """Request parameters for get analysis list."""

    # What type of analyses to include in the results. If not set all types will
    # be returned.
    analysis_type: "AnalysisType" = betterproto.enum_field(1)
    # A limit on the number of objects to be returned, between 1 and 100. Default
    # value is 100.
    limit: Optional[int] = betterproto.message_field(2, wraps=betterproto.TYPE_UINT64)
    # starting_after is an object ID that defines your place in the list. For
    # instance, if you make a analysis list request and receive 100, ending with
    # id = 89, your subsequent call can include starting_after=89 in order to
    # fetch the next page of the list.
    starting_after: Optional[int] = betterproto.message_field(
        3, wraps=betterproto.TYPE_INT64
    )


@dataclass(eq=False, repr=False)
class ListAnalysesResponse(betterproto.Message):
    """ListAnalysesResponse provides list of Analyses."""

    # List of analyses.
    analyses: List["Analysis"] = betterproto.message_field(1)
    pagination_hints: "PaginationHints" = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class Analysis(betterproto.Message):
    """Provides detailed information about an analysis."""

    # Analysis id.
    id: int = betterproto.int64_field(1)
    # Analysis name.
    name: str = betterproto.string_field(2)
    # Type of Analysis eg. TYPE_KEY_DRIVER.
    type: "AnalysisType" = betterproto.enum_field(3)
    # Timestamp when the analysis was created.
    created_at: datetime = betterproto.message_field(4)


@dataclass(eq=False, repr=False)
class RunAnalysisRequest(betterproto.Message):
    """Request payload for execute analysis workflow."""

    # Analysis id.
    id: int = betterproto.int64_field(1)


@dataclass(eq=False, repr=False)
class RunAnalysisResponse(betterproto.Message):
    """Response message execute analysis workflow returns empty message"""

    pass


@dataclass(eq=False, repr=False)
class PaginationHints(betterproto.Message):
    """
    Pagination hints which indicate if more data is available
    next_starting_cursor indicate the next id to be used for starting_after
    pagination parameter
    """

    has_more: bool = betterproto.bool_field(1)
    next_starting_cursor: Optional[int] = betterproto.message_field(
        2, wraps=betterproto.TYPE_INT64
    )


@dataclass(eq=False, repr=False)
class LatestAnalysisResultResponse(betterproto.Message):
    """Response payload for get LatestAnalysisResult."""

    # Analysis Result.
    analysis_result: "AnalysisResult" = betterproto.message_field(1)
    pagination_hints: "PaginationHints" = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class AnalysisResult(betterproto.Message):
    """Provides details of an analysis run."""

    # The run ID Analysis run. Run ID's are unique across analyses. example:
    # 102940
    id: int = betterproto.int64_field(1)
    # Indicates if analysis run completed successfully or not.
    run_status: "AnalysisResultRunStatus" = betterproto.enum_field(2)
    # Time at which run was kicked off.
    requested_at: datetime = betterproto.message_field(3)
    # Time at which analysis run completed.
    completed_at: datetime = betterproto.message_field(4)
    run_type: "AnalysisResultRunType" = betterproto.enum_field(5)
    key_driver_analysis_result: "KeyDriverAnalysisResult" = betterproto.message_field(
        6, group="run_result"
    )
    trend_analysis_result: "TrendAnalysisResult" = betterproto.message_field(
        7, group="run_result"
    )


@dataclass(eq=False, repr=False)
class KeyDriverAnalysisResult(betterproto.Message):
    """Provides details of a key driver analysis run."""

    # If subtype is TIME_COMPARISON, metadata about the time periods that are
    # compared.
    time_comparison: "KeyDriverAnalysisResultTimeComparison" = (
        betterproto.message_field(6, group="comparison")
    )
    # If subtype is GROUP_COMPARISON metadata about the groups that are being
    # compared.
    group_comparison: "KeyDriverAnalysisResultGroupComparison" = (
        betterproto.message_field(7, group="comparison")
    )
    # If the subtype is General_Performance.
    general_performance: "KeyDriverAnalysisResultGeneralPerformance" = (
        betterproto.message_field(8, group="comparison")
    )
    # Array of the subgroups selected by the key driver algorithm.
    subgroups: List["KeyDriverAnalysisResultSubgroup"] = betterproto.message_field(9)


@dataclass(eq=False, repr=False)
class KeyDriverAnalysisResultTimeComparison(betterproto.Message):
    """
    If subtype is TIME_COMPARISON, metadata about the time periods that are
    compared.
    """

    # The earlier of the two periods being compared.
    previous_period: "TimeRange" = betterproto.message_field(1)
    # The more recent of the two periods being compared.
    recent_period: "TimeRange" = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class KeyDriverAnalysisResultGroupComparison(betterproto.Message):
    """
    If subtype is GROUP_COMPARISON metadata about the groups that are being
    compared.
    """

    # The first group.
    group_a: "KeyDriverAnalysisResultGroupComparisonGroupDescription" = (
        betterproto.message_field(1)
    )
    # The second group.
    group_b: "KeyDriverAnalysisResultGroupComparisonGroupDescription" = (
        betterproto.message_field(2)
    )


@dataclass(eq=False, repr=False)
class KeyDriverAnalysisResultGroupComparisonGroupDescription(betterproto.Message):
    # The user-defined name corresponding to the first group.
    name: str = betterproto.string_field(1)


@dataclass(eq=False, repr=False)
class KeyDriverAnalysisResultGeneralPerformance(betterproto.Message):
    """If subtype is General Performance."""

    pass


@dataclass(eq=False, repr=False)
class KeyDriverAnalysisResultSubgroup(betterproto.Message):
    """Subgroup of a key driver analysis run."""

    # Unique ID corresponding to each subgroup, unique per analysis run.
    id: int = betterproto.int64_field(1)
    # Is top driver for this subgroup.
    is_top_driver: Optional[bool] = betterproto.message_field(
        2, wraps=betterproto.TYPE_BOOL
    )
    # The factors that define this subgroup, represented as a map of Dimension to
    # Value.
    factors: Dict[str, "Factor"] = betterproto.map_field(
        3, betterproto.TYPE_STRING, betterproto.TYPE_MESSAGE
    )
    group_comparison: "KeyDriverAnalysisResultSubgroupGroupComparisonPerformance" = (
        betterproto.message_field(4, group="details")
    )
    time_comparison: "KeyDriverAnalysisResultSubgroupTimeComparisonPerformance" = (
        betterproto.message_field(5, group="details")
    )
    general_performance: "KeyDriverAnalysisResultSubgroupGeneralPerformance" = (
        betterproto.message_field(6, group="details")
    )


@dataclass(eq=False, repr=False)
class KeyDriverAnalysisResultSubgroupGroupComparisonPerformance(betterproto.Message):
    """
    If analysis type is GROUP_COMPARISON the metric value and size of the
    compared subgroups.
    """

    # The size of this subgroup in the first group.
    group_a_size: Optional[float] = betterproto.message_field(
        1, wraps=betterproto.TYPE_DOUBLE
    )
    # The size of this subgroup in the second group.
    group_b_size: Optional[float] = betterproto.message_field(
        2, wraps=betterproto.TYPE_DOUBLE
    )
    # The value of the metric for this of this subgroup in the first group.
    group_a_value: Optional[float] = betterproto.message_field(
        3, wraps=betterproto.TYPE_DOUBLE
    )
    # The value of the metric for this of this subgroup in the second group.
    group_b_value: Optional[float] = betterproto.message_field(
        4, wraps=betterproto.TYPE_DOUBLE
    )


@dataclass(eq=False, repr=False)
class KeyDriverAnalysisResultSubgroupTimeComparisonPerformance(betterproto.Message):
    """
    If analysis type is TIME_COMPARISON,  the metric value and size of the
    compared subgroups.
    """

    # The size of this subgroup in the earlier of the compared periods.
    previous_period_size: Optional[float] = betterproto.message_field(
        1, wraps=betterproto.TYPE_DOUBLE
    )
    # The size of this subgroup in the more recent of the compared periods.
    recent_period_size: Optional[float] = betterproto.message_field(
        2, wraps=betterproto.TYPE_DOUBLE
    )
    # The value of the metric for this of this subgroup in the earlier of the
    # compared periods.
    previous_period_value: Optional[float] = betterproto.message_field(
        3, wraps=betterproto.TYPE_DOUBLE
    )
    # The value of the metric for this of this subgroup in the more recent of the
    # compared periods.
    recent_period_value: Optional[float] = betterproto.message_field(
        4, wraps=betterproto.TYPE_DOUBLE
    )


@dataclass(eq=False, repr=False)
class KeyDriverAnalysisResultSubgroupGeneralPerformance(betterproto.Message):
    """
    If analysis type is GENERAL_PERFORMANCE the metric value and size for this
    subgroup.
    """

    # The size (in percent) of this subgroup relative to the overall population.
    size: Optional[float] = betterproto.message_field(1, wraps=betterproto.TYPE_DOUBLE)
    # The metric value corresponding to this subgroup.
    value: Optional[float] = betterproto.message_field(2, wraps=betterproto.TYPE_DOUBLE)


@dataclass(eq=False, repr=False)
class TrendAnalysisResult(betterproto.Message):
    """Provides details of a Trend Analysis result."""

    # Metric level trends.
    overall_trends: List["TrendAnalysisResultTrend"] = betterproto.message_field(1)
    # Array of the subgroups in the trend.
    subgroups: List["TrendAnalysisResultSubgroup"] = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class TrendAnalysisResultTrend(betterproto.Message):
    """Provides fields that describes the trend."""

    # Inclusive start and exclusive end time range.
    time_range: "TimeRange" = betterproto.message_field(1)
    # Y-intersept of the trend.
    intercept: Optional[float] = betterproto.double_field(
        2, optional=True, group="_intercept"
    )
    # Steepness of trend.
    slope: Optional[float] = betterproto.double_field(3, optional=True, group="_slope")
    # The size (in percent) of this trend relative to the overall population.
    size: Optional[float] = betterproto.double_field(4, optional=True, group="_size")


@dataclass(eq=False, repr=False)
class TrendAnalysisResultSubgroup(betterproto.Message):
    """Subgroup of an trend analysis run."""

    # Unique ID corresponding to each subgroup, unique per analysis run.
    id: int = betterproto.int64_field(1)
    # The factors that define this subgroup, represented as a map of Dimension to
    # Value.
    factors: Dict[str, "Factor"] = betterproto.map_field(
        2, betterproto.TYPE_STRING, betterproto.TYPE_MESSAGE
    )
    # Trends for the subgroup.
    trends: List["TrendAnalysisResultTrend"] = betterproto.message_field(4)


@dataclass(eq=False, repr=False)
class TimeRange(betterproto.Message):
    """
    TimeRange start and end details with inclusive start and exclusive end.
    """

    start: datetime = betterproto.message_field(1)
    end: datetime = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class Factor(betterproto.Message):
    """(Dimension, Value) pairs that define a subgroup."""

    # Value, it is either string, int, boolean, float or timestamp type.
    value: "FactorValue" = betterproto.message_field(1, group="factor_type")
    # Keyword in a text dimension.
    keyword: "FactorKeyword" = betterproto.message_field(2, group="factor_type")
    # bin of a numerical dimension.
    bin: "FactorBin" = betterproto.message_field(3, group="factor_type")


@dataclass(eq=False, repr=False)
class FactorValue(betterproto.Message):
    """Value FactorType."""

    boolean_value: bool = betterproto.bool_field(1, group="value_type")
    integer_value: int = betterproto.int64_field(2, group="value_type")
    string_value: str = betterproto.string_field(3, group="value_type")
    float_value: float = betterproto.double_field(4, group="value_type")
    timestamp_value: datetime = betterproto.message_field(5, group="value_type")


@dataclass(eq=False, repr=False)
class FactorKeyword(betterproto.Message):
    """Keyword FactorType."""

    keyword: str = betterproto.string_field(1)


@dataclass(eq=False, repr=False)
class FactorBin(betterproto.Message):
    """Bin FactorType."""

    # The inclusive lower bound of the bin.
    lower_bound: Optional[float] = betterproto.message_field(
        1, wraps=betterproto.TYPE_DOUBLE
    )
    # The exclusive upper bound of the bin.
    upper_bound: Optional[float] = betterproto.message_field(
        2, wraps=betterproto.TYPE_DOUBLE
    )
    # The percentile of `lower_bound` within the factor's dimension.
    lower_bound_percentile: Optional[float] = betterproto.message_field(
        3, wraps=betterproto.TYPE_DOUBLE
    )
    # The percentile of `upper_bound` within the factor's dimension.
    upper_bound_percentile: Optional[float] = betterproto.message_field(
        4, wraps=betterproto.TYPE_DOUBLE
    )
