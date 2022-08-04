from pysisu import PySisu
import os
import gspread

# Sisu variables
API_KEY = os.environ.get('SISU_API_KEY')
ANALYSIS_ID = 165576
sisu = PySisu(API_KEY)

# GSheets variables
SPREADSHEET_NAME = "My Sisu Facts"
PATH_TO_CREDS = 'credentials.json'
PATH_TO_TOKEN = './token.json'

# Get facts from Sisu
sisu_table = sisu.get_results(ANALYSIS_ID)
print("Facts loaded")

# Connect to Google Drive
gc = gspread.oauth(credentials_filename=PATH_TO_CREDS, authorized_user_filename=PATH_TO_TOKEN)

# Create the spreadsheet
sh = gc.create(SPREADSHEET_NAME)
ws = sh.get_worksheet(0)

# Print facts to the terminal and insert into the spreadsheet
print(', '.join([x.column_name for x in sisu_table.header]))

idx = 1

for x in sisu_table.header:
    ws.update_cell(1, idx, x.column_name)
    idx = idx+1

idx = 2

for fact_row in sisu_table.rows:
    print(fact_row)

    ws.update_cell(idx, 1, fact_row.subgroup_id)
    ws.update_cell(idx, 2, fact_row.is_top_driver)
    ws.update_cell(idx, 3, fact_row.factor_0_dimension)
    ws.update_cell(idx, 4, fact_row.factor_0_value)
    ws.update_cell(idx, 5, fact_row.factor_1_dimension)
    ws.update_cell(idx, 6, fact_row.factor_1_value)
    ws.update_cell(idx, 7, fact_row.factor_2_dimension)
    ws.update_cell(idx, 8, fact_row.factor_2_value)
    ws.update_cell(idx, 9, fact_row.group_a_size)
    ws.update_cell(idx, 10, fact_row.group_b_size)
    ws.update_cell(idx, 11, fact_row.group_a_value)
    ws.update_cell(idx, 12, fact_row.group_b_value)
    ws.update_cell(idx, 13, fact_row.group_a_name)
    ws.update_cell(idx, 14, fact_row.group_b_name)

    print("Record inserted successfully into spreadsheet")

    idx = idx + 1
