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

import os
from pysisu import PySisu

API_KEY = os.environ.get('SISU_API_KEY')
ANALYSIS_ID = 15245

sisu = PySisu(API_KEY)
filters = sisu.get_filters(ANALYSIS_ID)
print(filters)
resp = sisu.set_filters(ANALYSIS_ID, filters.to_dict())
print(resp)
