from pysisu import PySisu
import csv
import os

# Sisu variables
API_KEY = os.environ.get("SISU_API_KEY")
ANALYSIS_ID = 165193
sisu = PySisu(API_KEY)

# CSV variables
FILE_NAME = "sisu_facts.csv"

# Get facts from Sisu
sisu_table = sisu.get_results(ANALYSIS_ID, confidence_gte="HIGH")
print("Facts loaded")

# Open the CSV file
file = open(FILE_NAME, "w")
writer = csv.writer(file)
header = []

# Add column headers to the list
for x in sisu_table.header:
    header.append(x.column_name)

writer.writerow(header)

for fact_row in sisu_table.rows:
    pg_row = (
        fact_row.subgroup_id,
        fact_row.confidence,
        fact_row.factor_0_dimension,
        fact_row.factor_0_value,
        fact_row.factor_1_dimension,
        fact_row.factor_1_value,
        fact_row.factor_2_dimension,
        fact_row.factor_2_value,
        fact_row.impact,
        fact_row.previous_period_size,
        fact_row.recent_period_size,
        fact_row.previous_period_value,
        fact_row.recent_period_value,
        fact_row.previous_period_start_date_inclusive,
        fact_row.previous_period_end_date_inclusive,
        fact_row.recent_period_start_date_inclusive,
        fact_row.recent_period_end_date_inclusive,
    )
    print(pg_row)
    writer.writerow(pg_row)
    print("Record written to CSV file")

# Clean up
file.close()
