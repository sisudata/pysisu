from pysisu import PySisu
import os
import gspread

# Sisu variables
API_KEY = os.environ.get('SISU_API_KEY')
ANALYSIS_ID = 165569
sisu = PySisu(API_KEY)

# GSheets variables
SPREADSHEET_NAME = "My Sisu Facts"
PATH_TO_CREDS = 'credentials.json'
PATH_TO_TOKEN = './token.json'

# Get facts from Sisu
sisu_table = sisu.get_results(ANALYSIS_ID, {"confidence_gte": "HIGH"})
print("Facts loaded")

# Connect to Google Drive
gc = gspread.oauth(credentials_filename=PATH_TO_CREDS, authorized_user_filename=PATH_TO_TOKEN)

# Create the spreadsheet
sh = gc.create(SPREADSHEET_NAME)
ws = sh.get_worksheet(0)

# Print facts to the terminal and insert into the spreadsheet
print(', '.join([x.column_name for x in sisu_table.header]))

data = []
row = []

# Add column headers to the list
for x in sisu_table.header:
    row.append(x.column_name)

# Add the column headers to the data set
data.append(row)
idx = 1

# Create rows for each individual fact, and add them to the data set
for fact_row in sisu_table.rows:
    print(fact_row)
    
    row=[]
    row.append(fact_row.subgroup_id)
    row.append(fact_row.confidence)
    row.append(fact_row.factor_0_dimension)
    row.append(fact_row.factor_0_value)
    row.append(fact_row.factor_1_dimension)
    row.append(fact_row.factor_1_value)
    row.append(fact_row.factor_2_dimension)
    row.append(fact_row.factor_2_value)
    row.append(fact_row.impact)
    row.append(fact_row.size)
    row.append(fact_row.value)

    data.append(row)

    print("Record inserted successfully into spreadsheet")

    idx = idx + 1

# Write the data set into the spreadsheet
range = 'A1:' + chr(ord('A')+len(row)) + str(idx)
ws.update(range, data)
