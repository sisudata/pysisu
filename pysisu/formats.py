from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Type


@dataclass
class Table:
    header: List["HeaderColumn"]
    rows: List["Row"]


@dataclass
class Row:
    pass


@dataclass
class HeaderColumn:
    column_name: str
    column_type: Type


class LatestAnalysisResultsFormats(Enum):
    TABLE = auto()
    PROTO = auto()
