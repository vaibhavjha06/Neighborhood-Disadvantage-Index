"""
Import packages
"""
from dotenv import load_dotenv
import os
import pandas as pd
import censusdis.data as ced
from censusdis.datasets import ACS5
from censusdis.states import ALL_STATES_AND_DC


"""
Call API key
"""
load_dotenv()
API_KEY = os.getenv("CENSUS_API_KEY")


"""
Pull data from ACS 5-years estimates 2015-2019 for all states
"""
all_states = []
for state_fips in ALL_STATES_AND_DC:
    print(f"Downloading state {state_fips}...")
    df = ced.download(
        dataset=ACS5,
        vintage=2019,
        download_variables=['NAME', 'B01001_026E', 'B01001_001E', 'B02001_002E', 'B01003_001E'],
        state=state_fips,
        county="*",
        tract="*",
        api_key=API_KEY
    )
    all_states.append(df)

othervars = pd.concat(all_states, ignore_index=True)
print(othervars)
othervars.to_csv('/Users/vaibhavjha/Documents/Yale Project/Data/othervars.csv', index=False)


"""
Education raw features pulled

'B06009_007E', 'B06009_009E', 'B06009_013E', 'B06009_015E', 'B06009_019E',
'B06009_024E', 'B13014_002E', 'B13014_010E', 'B13014_011E', 'B15011_022E',
'B15011_023E', 'B15011_028E', 'B15011_029E','B16010_016E', 'B16010_021E',
'B17003_003E', 'B17003_004E', 'B17003_005E', 'B17003_008E', 'B17003_009E',
'B17003_010E', 'B20004_001E', 'B20004_003E', 'B20004_006E', 'B27019_008E',
'B27019_011E', 'B27019_012E', 'B28006_008E', 'B28006_013E'
"""

"""
Employment raw features pulled

'B08006_017E', 'B08006_001E', 'B08302_009E', 'B08302_010E',
'B08302_011E', 'B08302_001E', 'B08134_070E', 'B08134_110E', 'B08134_010E', 'B08202_022E',
'B08202_018E', 'B23013_001E', 'B23027_004E', 'B23027_002E', 'B23020_001E',
'B28007_009E', 'B28007_002E', 'C24050_002E', 'C24050_003E', 'C24050_004E',
'C24050_005E', 'C24050_006E', 'C24050_007E', 'C24050_001E'
"""

"""
Income and Poverty raw features pulled

'B19001_002E', 'B19001_003E', 'B19001_004E', 'B19001_005E', 'B19001_006E',
'B19001_007E', 'B19001_008E', 'B19001_009E', 'B19001_010E', 'B19001_011E',
'B19001_001E', 'B19057_002E', 'B19057_001E','B19083_001E',
'B19058_002E', 'B19058_001E', 'B22008_003E', 'B22008_002E', 'B07012_010E',
'B07012_009E', 'B07012_012E'
"""

"""
Housing raw features pulled

'B25058_001E', 'B25071_001E', 'B25077_001E', 'B25002_003E', 'B25002_001E',
'B25014_013E', 'B25014_008E', 'B25003_002E', 'B25003_001E', 'B11001_003E',
'B11001_001E','B25035_001E', 'B25051_003E', 'B25051_001E'
"""
