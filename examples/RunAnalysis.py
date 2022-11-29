from pysisu import PySisu
from pysisu.proto.sisu.v1.api import AnalysisResultRunStatus
from pysisu.formats import LatestAnalysisResultsFormats
from time import sleep
import os

# Sisu variables
API_KEY = os.environ.get('SISU_API_KEY')
ANALYSIS_ID = 165569
SYNCHRONOUS = True
sisu = PySisu(API_KEY)

if SYNCHRONOUS:
    # Run the analysis synchronously
    sisu.run(ANALYSIS_ID)
    print("Running Analysis Synchronously...")

    while True:
        run_status = sisu.get_results(ANALYSIS_ID, format = LatestAnalysisResultsFormats.PROTO).analysis_result.run_status
        
        print(f"status of ANALYSIS_ID={ANALYSIS_ID} is {run_status.name}")
        if run_status != AnalysisResultRunStatus.RUN_STATUS_COMPLETED:
            sleep(5)
        else:
            break
else:
    # Run the analysis asynchronously
    sisu.run(ANALYSIS_ID)
    print("Running Analysis Asynchronously...")

# Get facts from Sisu
sisu_table = sisu.get_results(ANALYSIS_ID, {"confidence_gte": "HIGH"})
print("Facts loaded")

# Print facts to the terminal and insert into the database
print(', '.join([x.column_name for x in sisu_table.header]))

for fact_row in sisu_table.rows:
    pg_row = (fact_row.subgroup_id, fact_row.confidence, fact_row.factor_0_dimension, fact_row.factor_0_value, fact_row.factor_1_dimension, fact_row.factor_1_value, fact_row.factor_2_dimension, fact_row.factor_2_value, fact_row.impact, fact_row.size, fact_row.value)
    print(pg_row)
