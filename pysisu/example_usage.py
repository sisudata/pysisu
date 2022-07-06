import pysisu
import os

API_KEY = os.environ.get('SISU_API_KEY')
ANALYSIS_ID = 128998

table = pysisu.get_results(ANALYSIS_ID, API_KEY, {"top_drivers": "False"})
print(','.join([x.column_name for x in table.header]))
for row in table.rows:
    print(row)
