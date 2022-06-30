# pysisu

This repo contains a python package called `sisu_api` that will querying and convert all results into a Table format.

The Sisu api limits it's response to 100 results per response. The way we can fetch more than this limit is to paginate. This library allows us to auto_paginate.

Take a look at `example_usage.py` for a really simple example.
```python
API_KEY = os.environ.get('SISU_API_KEY')
url = 'https://vip.sisu.ai'

table = sisu_api.get_table(
    url, 7340, API_KEY, {"top_drivers": "False"}, True)
print(','.join([x.column_name for x in table.header]))
for row in table.rows:
    print(row)
```

The available parameters you can add are `top_drivers`, `starting_after`, and `limit`.

Additionally there is a flag for `auto_paginate` that will continuously fetch for any limit you set.

# Contributing to protos

Currently (06/21/2022) betterproto only supports `optional` in beta, so please install the most recent beta version of better proto.
```
pip install betterproto==2.0.0b4
```

Follow the install instructions here:
https://grpc.io/docs/protoc-installation/

Then to generate the proto api run the following command.
```
protoc -I . --python_betterproto_out=. api.proto
```

# Local development

```
python -m pip install -e .
export SISU_API_KEY=<key>
```

# Example

```python
import pysisu
import os

API_KEY = os.environ.get('SISU_API_KEY')
url = 'https://vip.sisudata.com'

table = pysisu.get_table(url, 7340, API_KEY, {"top_drivers": "False", "limit": 50}, True)
print(','.join([x.column_name for x in table.header]))
for row in table.rows:
    print(row)
```