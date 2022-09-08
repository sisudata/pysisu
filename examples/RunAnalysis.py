from pysisu import PySisu
import os

# Sisu variables
API_KEY = os.environ.get('SISU_API_KEY')
ANALYSIS_ID = 165569
sisu = PySisu(API_KEY)

# Run the analysis
sisu.run(ANALYSIS_ID)
print("Running Analysis...")

# Get facts from Sisu
sisu_table = sisu.get_results(ANALYSIS_ID, {"top_drivers": "True"})
print("Facts loaded")

# Print facts to the terminal and insert into the database
print(', '.join([x.column_name for x in sisu_table.header]))

for fact_row in sisu_table.rows:
    pg_row = (fact_row.subgroup_id, fact_row.is_top_driver, fact_row.factor_0_dimension, fact_row.factor_0_value, fact_row.factor_1_dimension, fact_row.factor_1_value, fact_row.factor_2_dimension, fact_row.factor_2_value, fact_row.impact, fact_row.size, fact_row.value)
    print(pg_row)
