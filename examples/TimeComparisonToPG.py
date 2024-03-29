from pysisu import PySisu
import psycopg2
import os

# Sisu variables
API_KEY = os.environ.get("SISU_API_KEY")
ANALYSIS_ID = 165193
sisu = PySisu(API_KEY)

# PG variables
DATABASE_NAME = "tyoung"
DATABASE_USER = "tyoung"
FACT_TABLE_NAME = "sisu_facts"

# Get facts from Sisu
sisu_table = sisu.get_results(ANALYSIS_ID, confidence_gte="HIGH")
print("Facts loaded")

# Connect to PG
pg_con = psycopg2.connect(dbname=DATABASE_NAME, user=DATABASE_USER)
pg_con.autocommit = True
pg_cur = pg_con.cursor()

# Truncate the table
sql_stmt = """TRUNCATE TABLE """ + FACT_TABLE_NAME + """;"""
pg_cur.execute(sql_stmt)

# Insert the facts
sql_stmt = (
    """INSERT INTO """
    + FACT_TABLE_NAME
    + """ (subgroup_id, confidence, factor_0_dimension, factor_0_value, factor_1_dimension, factor_1_value, factor_2_dimension, factor_2_value, impact, previous_period_size, recent_period_size, previous_period_value, recent_period_value, previous_period_start, previous_period_end, recent_period_start, recent_period_end) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
)

# Print facts to the terminal and insert into the database
print(", ".join([x.column_name for x in sisu_table.header]))

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
    pg_rs = pg_cur.execute(sql_stmt, (pg_row))
    print("Record inserted successfully into table")

# Clean up
pg_cur.close()
pg_con.close()
