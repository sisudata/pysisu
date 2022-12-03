from pysisu import PySisu
import os

# Sisu variables
API_KEY = os.environ.get('SISU_API_KEY')
ANALYSIS_ID = 165569
sisu = PySisu(API_KEY)

# Duplicate the analysis
dupResult = sisu.duplicate_analysis(ANALYSIS_ID)

print('Duplicated the analysis ID: ' + str(ANALYSIS_ID) + '! The duplicate analysis ID is: ' + str(dupResult.id))

# Duplicate the analysis and give it a new name
dupResult = sisu.duplicate_analysis(ANALYSIS_ID, name='My New Analysis')

print('Duplicated the analysis ID: ' + str(ANALYSIS_ID) + '! The duplicate analysis ID with a new name is: ' + str(dupResult.id))