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
from enum import Enum, auto
from typing import List, Type


@dataclass
class Table:
    header: List["HeaderColumn"]
    rows: List["Row"]

    def to_csv(self, delimiter : str = ',') -> str:
        header = delimiter.join(x.column_name for x in self.header)
        rows = '\n'.join(row.to_tabular_str(delimiter) for row in self.rows)
        return f'{header}\n{rows}'


@dataclass
class Row:
    def to_tabular_str(self, delimiter: str = ',') -> str:
        variables = []
        for x in vars(self).values():
            if x is None:
                variables.append('')
            elif isinstance(x, (int, float)):
                variables.append(x)
            else:
                variables.append(f"'{x}'")
        return delimiter.join([str(x).replace('\n', ' ') for x in variables])

    def __str__(self):
        return self.to_tabular_str()


@dataclass
class HeaderColumn:
    column_name: str
    column_type: Type


class LatestAnalysisResultsFormats(Enum):
    TABLE = auto()
    PROTO = auto()
