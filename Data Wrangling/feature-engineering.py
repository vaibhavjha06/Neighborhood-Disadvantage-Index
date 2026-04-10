"""
Import packages
"""
import pandas as pd

"""
Read in data
"""
education = pd.read_csv('/Users/vaibhavjha/Documents/Yale Project/Data/education_data.csv')

"""
Inspect data
"""
print(education.head())
print(education.describe())
print(education.info())
print(education.shape)

"""
There appears to be missing values for:
B20004_001E, B20004_003E, B20004_006E
These are features from measuring median income difference between degree earners
"""
