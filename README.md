# pysisu

`pysisu` is a Python package that will query the [Sisu API](https://docs.sisudata.com/docs/api/) and convert results into a tabular format.

## Overview and Example

Take a look at `example_usage.py` for a simple example.

```python
from pysisu import PySisu
import os

API_KEY = os.environ.get('SISU_API_KEY')
ANALYSIS_ID = 13234

sisu = PySisu(API_KEY)
sisu.run(ANALYSIS_ID)
table = sisu.get_results(ANALYSIS_ID)
table.to_csv()
```

The API limits its response to 10000 results per response, via pagination. However, there is a flag for `auto_paginate` that will continuously fetch for any limit you set.

## Contributing to protos

Currently (06/21/2022) betterproto only supports `optional` in beta, so please install the most recent beta version of better proto.

```bash
pip install betterproto==2.0.0b4
```

Follow the install instructions [here](https://grpc.io/docs/protoc-installation/).

Then to generate the proto api run the following command:

```bash
protoc -I . --python_betterproto_out=. api.proto
```

## Local development

```bash
python -m pip install -e .
export SISU_API_KEY=<key>
```

## Testing

Setup

```bash
python3 -m venv env
python -m pip install -e .
pip install -r requirements-dev.txt
```

There are example api responses in `tests/input_snapshots` and there are the expected parsing responses in `tests/output_snapshots`.

To updated the output snapshots whenever the input snapshots get updated, just run

```bash
pytest -k results_output --snapshot-update
```
