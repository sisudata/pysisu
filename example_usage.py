import pysisu
import os

API_KEY = os.environ.get('SISU_API_KEY')
url = 'https://dev.sisu.ai'

table = pysisu.get_table(
    url, 7340, API_KEY, {"top_drivers": "False"}, True)
print(','.join([x.column_name for x in table.header]))
for row in table.rows:
    print(row)
