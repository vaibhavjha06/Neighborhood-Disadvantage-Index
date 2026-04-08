"""
Import packages
"""
from dotenv import load_dotenv
import os
import censusdis.data as ced
from censusdis.datasets import ACS5

"""
Call API key
"""
load_dotenv()
API_KEY = os.getenv("CENSUS_API_KEY")

df = ced.download(
    dataset=ACS5,
    vintage=2019,
    download_variables=['NAME', 'B01003_001E', 'B19013_001E'],
    state="24",
    county="*",
    tract="*",
    api_key=API_KEY
)

print(df)
