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
        download_variables=['NAME', 'B06009_007E', 'B06009_009E', 'B06009_013E', 'B06009_015E', 'B06009_019E', 'B06009_024E',
                            'B13014_002E', 'B13014_010E', 'B13014_011E',
                            'B15011_022E', 'B15011_023E', 'B15011_028E', 'B15011_029E',
                            'B16010_016E', 'B16010_021E',
                            'B17003_003E', 'B17003_004E', 'B17003_005E', 'B17003_008E', 'B17003_009E', 'B17003_010E',
                            'B20004_001E', 'B20004_003E', 'B20004_006E',
                            'B27019_008E', 'B27019_011E', 'B27019_012E',
                            'B28006_008E', 'B28006_013E'],
        state=state_fips,
        county="*",
        tract="*",
        api_key=API_KEY
    )
    all_states.append(df)

education = pd.concat(all_states, ignore_index=True)
print(education)
# education.to_csv('/Users/vaibhavjha/Documents/Yale Project/Data/education_data.csv', index=False)