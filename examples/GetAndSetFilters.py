from ast import Expression
from pysisu import PySisu
from pysisu.proto.sisu.v1.api import SetAnalysisFiltersRequest
import os

def printBasicCondition(bc: dict, indent: str):
    print(indent + "I found a Basic Condition: " + bc['dimensionName'] + " " + bc['operator'] + " " + str(bc['literal'].popitem()[1]))

def processExps(d: dict, indent: str, type: str):
    exps = d['expressions']

    for exp in exps:
        if 'and' in exp:
            processExps(exp['and'], indent + "  ", 'AND')
        if 'or' in exp:
            processExps(exp['or'], indent + "  ", 'OR')
        if 'basicCondition' in exp:
            printBasicCondition(exp['basicCondition'], indent)
            print(indent + type)

# Sisu variables
API_KEY = os.environ.get('SISU_API_KEY')
SET_ANALYSIS_ID = 172783
GET_ANALYSIS_ID = 172960
sisu = PySisu(API_KEY)

filters = sisu.get_filters(GET_ANALYSIS_ID).to_dict()['filterExpression']

print("Retrieved filters! Let's see what we have...")

if 'and' in filters:
    processExps(filters['and'], "  ", 'AND')
if 'or' in filters:
    processExps(filters['or'], "  ", 'OR')
if 'basicCondition' in filters:
    printBasicCondition(filters['basicCondition'], "  ")

print("That's all I found!")
print("Moving on...")

# Create a dictionary that will set the filter to be:
#
#   ORDER_REFERRER != Google
#     AND
#   ORDER_ITEM_COUNT >= 2
#     AND
#   ORDER_VALUE >= 1.25
#     AND
#   ORDER_DATE >= 2018-12-01
#     AND
#       ORDER_CHANNEL = in_store
#         OR
#       ORDER_CHANNEL != digital_mobile

bc_ref = {'basicCondition': {'dimensionName': 'ORDER_REFERRER', 'operator': 'OPERATOR_NE', 'literal': {'string': 'Google'}}}
bc_ic = {'basicCondition': {'dimensionName': 'ORDER_ITEM_COUNT', 'operator': 'OPERATOR_GTE', 'literal': {'int': '2'}}}
bc_ov = {'basicCondition': {'dimensionName': 'ORDER_VALUE', 'operator': 'OPERATOR_GTE', 'literal': {'float': '1.25'}}}
bc_od = {'basicCondition': {'dimensionName': 'ORDER_DATE', 'operator': 'OPERATOR_GTE', 'literal': {'string': '2018-12-01'}}}
bc_ch1 = {'basicCondition': {'dimensionName': 'ORDER_CHANNEL', 'operator': 'OPERATOR_EQ', 'literal': {'string': 'in_store'}}}
bc_ch2 = {'basicCondition': {'dimensionName': 'ORDER_CHANNEL', 'operator': 'OPERATOR_NE', 'literal': {'string': 'digital_mobile'}}}

exp_ors = {'expressions': [bc_ch1, bc_ch2]}

exp_or = {'or': exp_ors}

exp_ands = {'expressions': [bc_ref, bc_ic, bc_ov, bc_od, exp_or]}

exp_and = {'and': exp_ands}

fe = {'filterExpression': exp_and}

sisu.set_filters(SET_ANALYSIS_ID, SetAnalysisFiltersRequest().from_dict(fe))

print("I set the filters!")
print("Googbye~")