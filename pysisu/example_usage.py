from pysisu import PySisu
import os

API_KEY = os.environ.get('SISU_API_KEY')
ANALYSIS_ID = 13234

sisu = PySisu(API_KEY)
table = sisu.get_results(ANALYSIS_ID, {"top_drivers": "True"})
print(','.join([x.column_name for x in table.header]))
for row in table.rows:
    print(row)
