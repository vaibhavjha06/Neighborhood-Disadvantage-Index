"""
Import packages
"""
import pandas as pd


"""
Read in data
"""
df = pd.read_csv('/Users/vaibhavjha/Documents/Yale/Data/PLACES__Local_Data_for_Better_Health,_Census_Tract_Data_2021.csv')
print(df.head(10))
print(df['Year'].value_counts())