# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: v1/api.public.proto
# plugin: python-betterproto
from dataclasses import dataclass
from datetime import datetime
from typing import (
    TYPE_CHECKING,
    Dict,
    List,
    Optional,
)

import betterproto
import grpclib
from betterproto.grpc.grpclib_server import ServiceBase


if TYPE_CHECKING:
    import grpclib.server
    from betterproto.grpc.grpclib_client import MetadataLike
    from grpclib.metadata import Deadline


class AnalysisType(betterproto.Enum):
    """Type of Analysis eg. KEY_DRIVER."""

    ANALYSIS_TYPE_UNKNOWN = 0
    ANALYSIS_TYPE_KEY_DRIVER = 1
    ANALYSIS_TYPE_TREND = 2


class SqlDataType(betterproto.Enum):
    """Represents a datatype of a specific column."""

    SQL_DATA_TYPE_UNKNOWN = 0
    SQL_DATA_TYPE_STRING = 1
    SQL_DATA_TYPE_FLOAT = 2
    SQL_DATA_TYPE_TIMESTAMP = 3
    SQL_DATA_TYPE_INT = 4
    SQL_DATA_TYPE_BOOLEAN = 5


class AnalysisResultRunStatus(betterproto.Enum):
    """Status of running an analysis."""

    RUN_STATUS_UNKNOWN = 0
    RUN_STATUS_IN_FLIGHT = 1
    """Analysis is currently running."""

    RUN_STATUS_FAILED = 2
    """Analysis finished running but had errors."""

    RUN_STATUS_COMPLETED = 3
    """Analysis ran successfully."""


class AnalysisResultRunType(betterproto.Enum):
    """Either SCHEDULED or MANUAL."""

    RUN_TYPE_UNKNOWN = 0
    RUN_TYPE_SCHEDULED = 1
    RUN_TYPE_MANUAL = 2


class MetricDesiredDirection(betterproto.Enum):
    """Type of metric direction."""

    DESIRED_DIRECTION_UNKNOWN = 0
    DESIRED_DIRECTION_INCREASE = 1
    DESIRED_DIRECTION_DECREASE = 2


class MetricMetricType(betterproto.Enum):
    """
    Type of metric calculation that is used to evaluate the metric's dimension.
    """

    METRIC_TYPE_UNKNOWN = 0
    METRIC_TYPE_AVERAGE = 1
    """Average of a single metric column(e.g., average order value)."""

    METRIC_TYPE_SUM = 2
    """Sum of a single metric column(e.g., total revenue)."""

    METRIC_TYPE_WEIGHTED_SUM = 3
    """
    Sum of a metric column weighted by a weight column(e.g., price per share).
    """

    METRIC_TYPE_WEIGHTED_AVERAGE = 4
    """
    Average of a metric column weighted by a weight column(e.g., price per
    share).
    """

    METRIC_TYPE_CATEGORICAL_COUNT = 5
    """
    Count of a matching condition in a metric column(e.g., number of churns).
    """

    METRIC_TYPE_CATEGORICAL_RATE = 6
    """Rate of a matching condition in a metric column(e.g., churn rate)."""

    METRIC_TYPE_COUNT_DISTINCT = 7
    """
    Count of a matching condition in a metric column(e.g., number of churns).
    """

    METRIC_TYPE_NUMERICAL_COUNT = 8
    """Count of the rows of a single metric column(e.g., number of orders)."""

    METRIC_TYPE_NUMERICAL_RATE = 9
    """
    A metric column divided by a denominator column(e.g., lead conversion
    rate).
    """


class DataSourceDataSourceType(betterproto.Enum):
    DATA_SOURCE_TYPE_UNKNOWN = 0
    DATA_SOURCE_TYPE_REDSHIFT = 1
    DATA_SOURCE_TYPE_POSTGRESQL = 2
    DATA_SOURCE_TYPE_SNOWFLAKE = 3
    DATA_SOURCE_TYPE_SQLSERVER = 4
    DATA_SOURCE_TYPE_BIGQUERY = 5
    DATA_SOURCE_TYPE_VERTICA = 6
    DATA_SOURCE_TYPE_AWSATHENA = 7
    DATA_SOURCE_TYPE_SPARK = 8
    DATA_SOURCE_TYPE_DATABRICKS = 9
    DATA_SOURCE_TYPE_SAP = 10


class DatasetDatasetType(betterproto.Enum):
    DATASET_TYPE_UNKNOWN = 0
    DATASET_TYPE_TABLE = 1
    """Data is sourced from a single table."""

    DATASET_TYPE_QUERY = 2
    """Data is sourced from a user-defined query."""


@dataclass(eq=False, repr=False)
class AnalysisRunResultsRequest(betterproto.Message):
    """Request parameters for get analysis results."""

    limit: Optional[int] = betterproto.message_field(1, wraps=betterproto.TYPE_UINT64)
    """
    A limit on the number of objects to be returned, between 1 and 10000.
    Default value is 100.
    """

    starting_after: Optional[int] = betterproto.message_field(
        2, wraps=betterproto.TYPE_INT64
    )
    """
    starting_after is an object ID that defines your place in the list. For
    instance, if you make a analysis list request and receive 100, ending with
    id = 89, your subsequent call can include starting_after=89 in order to
    fetch the next page of the list.
    """

    top_drivers: Optional[str] = betterproto.message_field(
        3, wraps=betterproto.TYPE_STRING
    )
    """filter by only top driver results."""

    id: Optional[int] = betterproto.message_field(4, wraps=betterproto.TYPE_INT64)
    """Analysis Id."""


@dataclass(eq=False, repr=False)
class AnalysesListRequest(betterproto.Message):
    """Request parameters for get analysis list."""

    analysis_type: "AnalysisType" = betterproto.enum_field(1)
    """
    What type of analyses to include in the results. If not set all types will
    be returned.
    """

    limit: Optional[int] = betterproto.message_field(2, wraps=betterproto.TYPE_UINT64)
    """
    A limit on the number of objects to be returned, between 1 and 10000.
    Default value is 100.
    """

    starting_after: Optional[int] = betterproto.message_field(
        3, wraps=betterproto.TYPE_INT64
    )
    """
    starting_after is an object ID that defines your place in the list. For
    instance, if you make a analysis list request and receive 100, ending with
    id = 89, your subsequent call can include starting_after=89 in order to
    fetch the next page of the list.
    """


@dataclass(eq=False, repr=False)
class AnalysesListResponse(betterproto.Message):
    """AnalysesListResponse provides list of Analyses."""

    analyses: List["Analysis"] = betterproto.message_field(1)
    """List of analyses."""

    pagination_hints: "PaginationHints" = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class Analysis(betterproto.Message):
    """Provides detailed information about an analysis."""

    id: int = betterproto.int64_field(1)
    """Analysis id."""

    name: str = betterproto.string_field(2)
    """Analysis name."""

    type: "AnalysisType" = betterproto.enum_field(3)
    """Type of Analysis eg. TYPE_KEY_DRIVER."""

    created_at: datetime = betterproto.message_field(4)
    """Timestamp when the analysis was created."""

    metric_id: int = betterproto.uint64_field(5)
    """Metric id corresponding to the analysis."""


@dataclass(eq=False, repr=False)
class RunAnalysisRequest(betterproto.Message):
    """Request payload for execute analysis workflow."""

    id: int = betterproto.int64_field(1)
    """Analysis id."""


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
class AnalysisRunResultsResponse(betterproto.Message):
    """Response payload for get LatestAnalysisResult."""

    analysis_result: "AnalysisResult" = betterproto.message_field(1)
    """Analysis Result."""

    pagination_hints: "PaginationHints" = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class AnalysisResult(betterproto.Message):
    """Provides details of an analysis run."""

    id: int = betterproto.int64_field(1)
    """
    The run ID Analysis run. Run ID's are unique across analyses. example:
    102940
    """

    run_status: "AnalysisResultRunStatus" = betterproto.enum_field(2)
    """Indicates if analysis run completed successfully or not."""

    requested_at: datetime = betterproto.message_field(3)
    """Time at which run was kicked off."""

    completed_at: datetime = betterproto.message_field(4)
    """Time at which analysis run completed."""

    run_type: "AnalysisResultRunType" = betterproto.enum_field(5)
    key_driver_analysis_result: "KeyDriverAnalysisResult" = betterproto.message_field(
        6, group="run_result"
    )
    trend_analysis_result: "TrendAnalysisResult" = betterproto.message_field(
        7, group="run_result"
    )
    metric_id: int = betterproto.uint64_field(8)
    """Metric ID for the analysis."""


@dataclass(eq=False, repr=False)
class KeyDriverAnalysisResult(betterproto.Message):
    """Provides details of a key driver analysis run."""

    time_comparison: "KeyDriverAnalysisResultTimeComparison" = (
        betterproto.message_field(6, group="comparison")
    )
    """
    If subtype is TIME_COMPARISON, metadata about the time periods that are
    compared.
    """

    group_comparison: "KeyDriverAnalysisResultGroupComparison" = (
        betterproto.message_field(7, group="comparison")
    )
    """
    If subtype is GROUP_COMPARISON metadata about the groups that are being
    compared.
    """

    general_performance: "KeyDriverAnalysisResultGeneralPerformance" = (
        betterproto.message_field(8, group="comparison")
    )
    """If the subtype is General_Performance."""

    subgroups: List["KeyDriverAnalysisResultSubgroup"] = betterproto.message_field(9)
    """Array of the subgroups selected by the key driver algorithm."""


@dataclass(eq=False, repr=False)
class KeyDriverAnalysisResultTimeComparison(betterproto.Message):
    """
    If subtype is TIME_COMPARISON, metadata about the time periods that are
    compared.
    """

    previous_period: "TimeRange" = betterproto.message_field(1)
    """The earlier of the two periods being compared."""

    recent_period: "TimeRange" = betterproto.message_field(2)
    """The more recent of the two periods being compared."""


@dataclass(eq=False, repr=False)
class KeyDriverAnalysisResultGroupComparison(betterproto.Message):
    """
    If subtype is GROUP_COMPARISON metadata about the groups that are being
    compared.
    """

    group_a: "KeyDriverAnalysisResultGroupComparisonGroupDescription" = (
        betterproto.message_field(1)
    )
    """The first group."""

    group_b: "KeyDriverAnalysisResultGroupComparisonGroupDescription" = (
        betterproto.message_field(2)
    )
    """The second group."""


@dataclass(eq=False, repr=False)
class KeyDriverAnalysisResultGroupComparisonGroupDescription(betterproto.Message):
    name: str = betterproto.string_field(1)
    """The user-defined name corresponding to the first group."""


@dataclass(eq=False, repr=False)
class KeyDriverAnalysisResultGeneralPerformance(betterproto.Message):
    """If subtype is General Performance."""

    pass


@dataclass(eq=False, repr=False)
class KeyDriverAnalysisResultSubgroup(betterproto.Message):
    """Subgroup of a key driver analysis run."""

    id: int = betterproto.int64_field(1)
    """Unique ID corresponding to each subgroup, unique per analysis run."""

    is_top_driver: Optional[bool] = betterproto.message_field(
        2, wraps=betterproto.TYPE_BOOL
    )
    """Is top driver for this subgroup."""

    factors: Dict[str, "Factor"] = betterproto.map_field(
        3, betterproto.TYPE_STRING, betterproto.TYPE_MESSAGE
    )
    """
    The factors that define this subgroup, represented as a map of Dimension to
    Value.
    """

    group_comparison: "KeyDriverAnalysisResultSubgroupGroupComparisonPerformance" = (
        betterproto.message_field(4, group="details")
    )
    time_comparison: "KeyDriverAnalysisResultSubgroupTimeComparisonPerformance" = (
        betterproto.message_field(5, group="details")
    )
    general_performance: "KeyDriverAnalysisResultSubgroupGeneralPerformance" = (
        betterproto.message_field(6, group="details")
    )
    impact: Optional[float] = betterproto.message_field(
        7, wraps=betterproto.TYPE_DOUBLE
    )
    """
    How much this subgroup contributes to the overall value of the metric
    calculation.
    """


@dataclass(eq=False, repr=False)
class KeyDriverAnalysisResultSubgroupGroupComparisonPerformance(betterproto.Message):
    """
    If analysis type is GROUP_COMPARISON the metric value and size of the
    compared subgroups.
    """

    group_a_size: Optional[float] = betterproto.message_field(
        1, wraps=betterproto.TYPE_DOUBLE
    )
    """The size of this subgroup in the first group."""

    group_b_size: Optional[float] = betterproto.message_field(
        2, wraps=betterproto.TYPE_DOUBLE
    )
    """The size of this subgroup in the second group."""

    group_a_value: Optional[float] = betterproto.message_field(
        3, wraps=betterproto.TYPE_DOUBLE
    )
    """
    The value of the metric for this of this subgroup in the first group.
    """

    group_b_value: Optional[float] = betterproto.message_field(
        4, wraps=betterproto.TYPE_DOUBLE
    )
    """
    The value of the metric for this of this subgroup in the second group.
    """


@dataclass(eq=False, repr=False)
class KeyDriverAnalysisResultSubgroupTimeComparisonPerformance(betterproto.Message):
    """
    If analysis type is TIME_COMPARISON,  the metric value and size of the
    compared subgroups.
    """

    previous_period_size: Optional[float] = betterproto.message_field(
        1, wraps=betterproto.TYPE_DOUBLE
    )
    """The size of this subgroup in the earlier of the compared periods."""

    recent_period_size: Optional[float] = betterproto.message_field(
        2, wraps=betterproto.TYPE_DOUBLE
    )
    """
    The size of this subgroup in the more recent of the compared periods.
    """

    previous_period_value: Optional[float] = betterproto.message_field(
        3, wraps=betterproto.TYPE_DOUBLE
    )
    """
    The value of the metric for this of this subgroup in the earlier of the
    compared periods.
    """

    recent_period_value: Optional[float] = betterproto.message_field(
        4, wraps=betterproto.TYPE_DOUBLE
    )
    """
    The value of the metric for this of this subgroup in the more recent of the
    compared periods.
    """


@dataclass(eq=False, repr=False)
class KeyDriverAnalysisResultSubgroupGeneralPerformance(betterproto.Message):
    """
    If analysis type is GENERAL_PERFORMANCE the metric value and size for this
    subgroup.
    """

    size: Optional[float] = betterproto.message_field(1, wraps=betterproto.TYPE_DOUBLE)
    """
    The size (in percent) of this subgroup relative to the overall population.
    """

    value: Optional[float] = betterproto.message_field(2, wraps=betterproto.TYPE_DOUBLE)
    """The metric value corresponding to this subgroup."""


@dataclass(eq=False, repr=False)
class TrendAnalysisResult(betterproto.Message):
    """Provides details of a Trend Analysis result."""

    overall_trends: List["TrendAnalysisResultTrend"] = betterproto.message_field(1)
    """Metric level trends."""

    subgroups: List["TrendAnalysisResultSubgroup"] = betterproto.message_field(2)
    """Array of the subgroups in the trend."""


@dataclass(eq=False, repr=False)
class TrendAnalysisResultTrend(betterproto.Message):
    """Provides fields that describes the trend."""

    time_range: "TimeRange" = betterproto.message_field(1)
    """Inclusive start and exclusive end time range."""

    intercept: Optional[float] = betterproto.double_field(
        2, optional=True, group="_intercept"
    )
    """Y-intersept of the trend."""

    slope: Optional[float] = betterproto.double_field(3, optional=True, group="_slope")
    """Steepness of trend."""

    size: Optional[float] = betterproto.double_field(4, optional=True, group="_size")
    """
    The size (in percent) of this trend relative to the overall population.
    """


@dataclass(eq=False, repr=False)
class TrendAnalysisResultSubgroup(betterproto.Message):
    """Subgroup of an trend analysis run."""

    id: int = betterproto.int64_field(1)
    """Unique ID corresponding to each subgroup, unique per analysis run."""

    factors: Dict[str, "Factor"] = betterproto.map_field(
        2, betterproto.TYPE_STRING, betterproto.TYPE_MESSAGE
    )
    """
    The factors that define this subgroup, represented as a map of Dimension to
    Value.
    """

    trends: List["TrendAnalysisResultTrend"] = betterproto.message_field(4)
    """Trends for the subgroup."""

    impact: Optional[float] = betterproto.message_field(
        5, wraps=betterproto.TYPE_DOUBLE
    )
    """
    How much this subgroup contributes to the overall value of the metric
    calculation.
    """


@dataclass(eq=False, repr=False)
class TimeRange(betterproto.Message):
    """
    TimeRange start and end details with inclusive start and exclusive end.
    """

    start: datetime = betterproto.message_field(1)
    end: datetime = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class Value(betterproto.Message):
    """Represent different possible primitive data types."""

    boolean_value: bool = betterproto.bool_field(1, group="value_type")
    integer_value: int = betterproto.int64_field(2, group="value_type")
    string_value: str = betterproto.string_field(3, group="value_type")
    float_value: float = betterproto.double_field(4, group="value_type")
    timestamp_value: datetime = betterproto.message_field(5, group="value_type")


@dataclass(eq=False, repr=False)
class Factor(betterproto.Message):
    """(Dimension, Value) pairs that define a subgroup."""

    value: "Value" = betterproto.message_field(1, group="factor_type")
    """Value, it is either string, int, boolean, float or timestamp type."""

    keyword: "FactorKeyword" = betterproto.message_field(2, group="factor_type")
    """Keyword in a text dimension."""

    bin: "FactorBin" = betterproto.message_field(3, group="factor_type")
    """bin of a numerical dimension."""


@dataclass(eq=False, repr=False)
class FactorKeyword(betterproto.Message):
    """Keyword FactorType."""

    keyword: str = betterproto.string_field(1)


@dataclass(eq=False, repr=False)
class FactorBin(betterproto.Message):
    """Bin FactorType."""

    lower_bound: Optional[float] = betterproto.message_field(
        1, wraps=betterproto.TYPE_DOUBLE
    )
    """The inclusive lower bound of the bin."""

    upper_bound: Optional[float] = betterproto.message_field(
        2, wraps=betterproto.TYPE_DOUBLE
    )
    """The exclusive upper bound of the bin."""

    lower_bound_percentile: Optional[float] = betterproto.message_field(
        3, wraps=betterproto.TYPE_DOUBLE
    )
    """The percentile of `lower_bound` within the factor's dimension."""

    upper_bound_percentile: Optional[float] = betterproto.message_field(
        4, wraps=betterproto.TYPE_DOUBLE
    )
    """The percentile of `upper_bound` within the factor's dimension."""


@dataclass(eq=False, repr=False)
class MetricsListRequest(betterproto.Message):
    """Request payload for get metrics."""

    pass


@dataclass(eq=False, repr=False)
class MetricsListResponse(betterproto.Message):
    """ListMetricsResponse provides list of Metrics."""

    metrics: List["Metric"] = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class Metric(betterproto.Message):
    """Detailed information about a metric."""

    id: int = betterproto.uint64_field(1)
    """Metric id."""

    name: str = betterproto.string_field(2)
    """Metric name."""

    weight_dimension_name: str = betterproto.string_field(3)
    """
    The name of the weight dimension. A weight dimension is used to increases
    the importance of a given row in an analysis.
    """

    time_dimension_name: str = betterproto.string_field(4)
    """
    The name of metric's time dimension which represnts the date range of the
    metric.
    """

    desired_direction: "MetricDesiredDirection" = betterproto.enum_field(5)
    """
    Specifies whether the metric's goal is to increase or decrease the kpi
    value.
    """

    metric_dimension: "MetricMetricDimension" = betterproto.message_field(6)
    """The dimension which defines the metric's goal."""

    type: "MetricMetricType" = betterproto.enum_field(8)
    """Type of metric calculation."""

    created_at: datetime = betterproto.message_field(9)
    """Timestamp when the metric was created."""

    dataset_id: int = betterproto.uint64_field(10)
    """Id of the metric data set."""


@dataclass(eq=False, repr=False)
class MetricMetricDimension(betterproto.Message):
    """A dimension in a metric."""

    name: str = betterproto.string_field(1)
    """The name of the dimension."""

    value: "Value" = betterproto.message_field(2)
    """Value, it is either string, int, boolean, float or timestamp type."""


@dataclass(eq=False, repr=False)
class AnalysisDimensionsListRequest(betterproto.Message):
    """Request for a list of dimensions for a given `analysis_id`."""

    analysis_id: int = betterproto.int64_field(1)
    """Unique ID corresponding to the analysis containing the dimensions."""

    is_selected: Optional[str] = betterproto.message_field(
        2, wraps=betterproto.TYPE_STRING
    )
    """
    Will return only active or non active dimensions for a given analysis.
    """


@dataclass(eq=False, repr=False)
class DataSetDimensionsListRequest(betterproto.Message):
    """Request for a list of dimensions for a given `dimension_id`."""

    data_set_id: int = betterproto.int64_field(1)
    """Unique ID corresponding to the dataset containing the dimensions."""


@dataclass(eq=False, repr=False)
class Dimension(betterproto.Message):
    """Represents a dimension (column) within a specfic `Dataset`."""

    name: str = betterproto.string_field(1)
    """
    A string literal corresponding to a column selected in the dataset. It is
    either a column name or a column alias for a computed SQL function over a
    column ( for example, `upper(email) as 'UPPER_EMAIL'` ex: `red` in `SELECT
    roja as red`.
    """

    dataset_id: int = betterproto.uint64_field(2)
    """Refers to the dataset that this dimension is associated with."""

    dimension_type: "SqlDataType" = betterproto.enum_field(3)
    """
    Refers to the column type of this dimension as it exists within the data
    warehouse
    """


@dataclass(eq=False, repr=False)
class DataSetDimensionsListResponse(betterproto.Message):
    """
    DataSetDimensionsListResponse provides list of Dimensions for a given
    data_set.
    """

    dimensions: List["Dimension"] = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class AnalysisDimensionsListResponse(betterproto.Message):
    """
    AnalysisDimensionsListResponse provides list of Dimensions for a given
    analysis.
    """

    dimensions: List["Dimension"] = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class DataSourceListRequest(betterproto.Message):
    """Request payload for get datasources."""

    pass


@dataclass(eq=False, repr=False)
class DataSourceListResponse(betterproto.Message):
    """Response payload for get datasources."""

    data_sources: List["DataSource"] = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class DataSource(betterproto.Message):
    id: int = betterproto.uint64_field(1)
    """Id of a given data source."""

    name: str = betterproto.string_field(2)
    """Represents the table or query name of a data source."""

    data_source_type: "DataSourceDataSourceType" = betterproto.enum_field(3)
    """Type of the data source."""

    created_at: datetime = betterproto.message_field(4)
    """Time when the data source was created."""

    created_by: str = betterproto.string_field(5)
    """Data source creator's user email info."""

    connection_uri: str = betterproto.string_field(6)
    """JDBC connection URI to the data source location."""


@dataclass(eq=False, repr=False)
class DataSetsRequest(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class DataSetsResponse(betterproto.Message):
    datasets: List["Dataset"] = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class Dataset(betterproto.Message):
    """Dataset contains instructions on how to query a data source."""

    id: int = betterproto.uint64_field(1)
    """Id of a given dataset."""

    name: str = betterproto.string_field(2)
    """
    Represents the table name for DATASET_TYPE_TABLE or user-defined for
    DATASET_TYPE_QUERY.
    """

    dataset_type: "DatasetDatasetType" = betterproto.enum_field(3)
    """Dataset type represents how data has been obtained."""

    query_string: str = betterproto.string_field(4)
    """A SQL query string for a datasete of type query."""

    last_modified: datetime = betterproto.message_field(5)
    """Last time the data set was modified."""

    created_at: datetime = betterproto.message_field(6)
    """Time when the data set was created."""

    data_source_id: int = betterproto.uint64_field(7)
    """Data Source id of the data set."""


class AnalysesServiceStub(betterproto.ServiceStub):
    async def analyses_list(
        self,
        analyses_list_request: "AnalysesListRequest",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "AnalysesListResponse":
        return await self._unary_unary(
            "/sisu.v1.api.AnalysesService/AnalysesList",
            analyses_list_request,
            AnalysesListResponse,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def run_analysis(
        self,
        run_analysis_request: "RunAnalysisRequest",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "RunAnalysisResponse":
        return await self._unary_unary(
            "/sisu.v1.api.AnalysesService/RunAnalysis",
            run_analysis_request,
            RunAnalysisResponse,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def analysis_run_results(
        self,
        analysis_run_results_request: "AnalysisRunResultsRequest",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "AnalysisRunResultsResponse":
        return await self._unary_unary(
            "/sisu.v1.api.AnalysesService/AnalysisRunResults",
            analysis_run_results_request,
            AnalysisRunResultsResponse,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def analysis_dimensions_list(
        self,
        analysis_dimensions_list_request: "AnalysisDimensionsListRequest",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "AnalysisDimensionsListResponse":
        return await self._unary_unary(
            "/sisu.v1.api.AnalysesService/AnalysisDimensionsList",
            analysis_dimensions_list_request,
            AnalysisDimensionsListResponse,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )


class MetricServiceStub(betterproto.ServiceStub):
    async def metrics_list(
        self,
        metrics_list_request: "MetricsListRequest",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "MetricsListResponse":
        return await self._unary_unary(
            "/sisu.v1.api.MetricService/MetricsList",
            metrics_list_request,
            MetricsListResponse,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )


class DatasetServiceStub(betterproto.ServiceStub):
    async def data_sets(
        self,
        data_sets_request: "DataSetsRequest",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "DataSetsResponse":
        return await self._unary_unary(
            "/sisu.v1.api.DatasetService/DataSets",
            data_sets_request,
            DataSetsResponse,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def data_set_dimensions_list(
        self,
        data_set_dimensions_list_request: "DataSetDimensionsListRequest",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "DataSetDimensionsListResponse":
        return await self._unary_unary(
            "/sisu.v1.api.DatasetService/DataSetDimensionsList",
            data_set_dimensions_list_request,
            DataSetDimensionsListResponse,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )


class DataSourcesServiceStub(betterproto.ServiceStub):
    async def data_source_list(
        self,
        data_source_list_request: "DataSourceListRequest",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "DataSourceListResponse":
        return await self._unary_unary(
            "/sisu.v1.api.DataSourcesService/DataSourceList",
            data_source_list_request,
            DataSourceListResponse,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )


class AnalysesServiceBase(ServiceBase):
    async def analyses_list(
        self, analyses_list_request: "AnalysesListRequest"
    ) -> "AnalysesListResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def run_analysis(
        self, run_analysis_request: "RunAnalysisRequest"
    ) -> "RunAnalysisResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def analysis_run_results(
        self, analysis_run_results_request: "AnalysisRunResultsRequest"
    ) -> "AnalysisRunResultsResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def analysis_dimensions_list(
        self, analysis_dimensions_list_request: "AnalysisDimensionsListRequest"
    ) -> "AnalysisDimensionsListResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def __rpc_analyses_list(
        self, stream: "grpclib.server.Stream[AnalysesListRequest, AnalysesListResponse]"
    ) -> None:
        request = await stream.recv_message()
        response = await self.analyses_list(request)
        await stream.send_message(response)

    async def __rpc_run_analysis(
        self, stream: "grpclib.server.Stream[RunAnalysisRequest, RunAnalysisResponse]"
    ) -> None:
        request = await stream.recv_message()
        response = await self.run_analysis(request)
        await stream.send_message(response)

    async def __rpc_analysis_run_results(
        self,
        stream: "grpclib.server.Stream[AnalysisRunResultsRequest, AnalysisRunResultsResponse]",
    ) -> None:
        request = await stream.recv_message()
        response = await self.analysis_run_results(request)
        await stream.send_message(response)

    async def __rpc_analysis_dimensions_list(
        self,
        stream: "grpclib.server.Stream[AnalysisDimensionsListRequest, AnalysisDimensionsListResponse]",
    ) -> None:
        request = await stream.recv_message()
        response = await self.analysis_dimensions_list(request)
        await stream.send_message(response)

    def __mapping__(self) -> Dict[str, grpclib.const.Handler]:
        return {
            "/sisu.v1.api.AnalysesService/AnalysesList": grpclib.const.Handler(
                self.__rpc_analyses_list,
                grpclib.const.Cardinality.UNARY_UNARY,
                AnalysesListRequest,
                AnalysesListResponse,
            ),
            "/sisu.v1.api.AnalysesService/RunAnalysis": grpclib.const.Handler(
                self.__rpc_run_analysis,
                grpclib.const.Cardinality.UNARY_UNARY,
                RunAnalysisRequest,
                RunAnalysisResponse,
            ),
            "/sisu.v1.api.AnalysesService/AnalysisRunResults": grpclib.const.Handler(
                self.__rpc_analysis_run_results,
                grpclib.const.Cardinality.UNARY_UNARY,
                AnalysisRunResultsRequest,
                AnalysisRunResultsResponse,
            ),
            "/sisu.v1.api.AnalysesService/AnalysisDimensionsList": grpclib.const.Handler(
                self.__rpc_analysis_dimensions_list,
                grpclib.const.Cardinality.UNARY_UNARY,
                AnalysisDimensionsListRequest,
                AnalysisDimensionsListResponse,
            ),
        }


class MetricServiceBase(ServiceBase):
    async def metrics_list(
        self, metrics_list_request: "MetricsListRequest"
    ) -> "MetricsListResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def __rpc_metrics_list(
        self, stream: "grpclib.server.Stream[MetricsListRequest, MetricsListResponse]"
    ) -> None:
        request = await stream.recv_message()
        response = await self.metrics_list(request)
        await stream.send_message(response)

    def __mapping__(self) -> Dict[str, grpclib.const.Handler]:
        return {
            "/sisu.v1.api.MetricService/MetricsList": grpclib.const.Handler(
                self.__rpc_metrics_list,
                grpclib.const.Cardinality.UNARY_UNARY,
                MetricsListRequest,
                MetricsListResponse,
            ),
        }


class DatasetServiceBase(ServiceBase):
    async def data_sets(
        self, data_sets_request: "DataSetsRequest"
    ) -> "DataSetsResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def data_set_dimensions_list(
        self, data_set_dimensions_list_request: "DataSetDimensionsListRequest"
    ) -> "DataSetDimensionsListResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def __rpc_data_sets(
        self, stream: "grpclib.server.Stream[DataSetsRequest, DataSetsResponse]"
    ) -> None:
        request = await stream.recv_message()
        response = await self.data_sets(request)
        await stream.send_message(response)

    async def __rpc_data_set_dimensions_list(
        self,
        stream: "grpclib.server.Stream[DataSetDimensionsListRequest, DataSetDimensionsListResponse]",
    ) -> None:
        request = await stream.recv_message()
        response = await self.data_set_dimensions_list(request)
        await stream.send_message(response)

    def __mapping__(self) -> Dict[str, grpclib.const.Handler]:
        return {
            "/sisu.v1.api.DatasetService/DataSets": grpclib.const.Handler(
                self.__rpc_data_sets,
                grpclib.const.Cardinality.UNARY_UNARY,
                DataSetsRequest,
                DataSetsResponse,
            ),
            "/sisu.v1.api.DatasetService/DataSetDimensionsList": grpclib.const.Handler(
                self.__rpc_data_set_dimensions_list,
                grpclib.const.Cardinality.UNARY_UNARY,
                DataSetDimensionsListRequest,
                DataSetDimensionsListResponse,
            ),
        }


class DataSourcesServiceBase(ServiceBase):
    async def data_source_list(
        self, data_source_list_request: "DataSourceListRequest"
    ) -> "DataSourceListResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def __rpc_data_source_list(
        self,
        stream: "grpclib.server.Stream[DataSourceListRequest, DataSourceListResponse]",
    ) -> None:
        request = await stream.recv_message()
        response = await self.data_source_list(request)
        await stream.send_message(response)

    def __mapping__(self) -> Dict[str, grpclib.const.Handler]:
        return {
            "/sisu.v1.api.DataSourcesService/DataSourceList": grpclib.const.Handler(
                self.__rpc_data_source_list,
                grpclib.const.Cardinality.UNARY_UNARY,
                DataSourceListRequest,
                DataSourceListResponse,
            ),
        }
