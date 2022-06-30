# pysisu

`pysisu` is a Python package that will query the [Sisu API](https://docs.sisudata.com/docs/api/) and convert results into a tabular format.

# Overview and Example

Take a look at `example_usage.py` for a simple example.
```python
API_KEY = os.environ.get('SISU_API_KEY')
url = 'https://vip.sisudata.com'

table = sisu_api.get_table(
    url, 7340, API_KEY, {"top_drivers": "False"}, True)
print(','.join([x.column_name for x in table.header]))
for row in table.rows:
    print(row)
```

The API limits its response to 100 results per response, via pagination. However, there is a flag for `auto_paginate` that will continuously fetch for any limit you set.

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
