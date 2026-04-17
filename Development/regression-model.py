"""
Import packages
"""
import pandas as pd


"""
Read in data
"""
index = pd.read_csv('/Users/vaibhavjha/Documents/Yale Project/Data/index.csv')
index = index.drop(columns='Unnamed: 0')

outcomes = pd.read_csv('/Users/vaibhavjha/Documents/Yale Project/Data/PLACES__Local_Data_for_Better_Health,_Census_Tract_Data_2021.csv')
# Isolate mental health measure
mental_health = outcomes[outcomes['Measure'] == 'Mental health not good for >=14 days among adults aged >=18 years']
mental_health = mental_health[['Year', 'LocationID', 'Data_Value']]
mental_health['LocationID'] = mental_health['LocationID'].astype(str)
# Isolate obesity measure
obesity = outcomes[outcomes['Measure'] == 'Obesity among adults aged >=18 years']
obesity = obesity[['Year', 'LocationID', 'Data_Value']]
obesity['LocationID'] = obesity['LocationID'].astype(str)

"""
Create GEOID from census data to merge with outcomes data
"""
index['STATE'] = index['STATE'].astype(str).str.zfill(2)
index['COUNTY'] = index['COUNTY'].astype(str).str.zfill(3)
index['TRACT'] = index['TRACT'].astype(str).str.zfill(6)

index['GEOID'] = (
    index['STATE'] +
    index['COUNTY'] +
    index['TRACT']
)


"""
Merge index with each outcome by census tract ID
"""
mental_health_master = index.merge(
    mental_health,
    left_on="GEOID",
    right_on="LocationID",
    how="inner"
)

obesity_master = index.merge(
    obesity,
    left_on="GEOID",
    right_on="LocationID",
    how="inner"
)


"""
Rename outcome columns
"""
mental_health_master = mental_health_master.rename(columns={
    'Data_Value': 'mental_health'
})

obesity_master = obesity_master.rename(columns={
    'Data_Value': 'obesity'
})


"""
Inspect new shape
"""
print(mental_health.shape)  # 70,228
print(mental_health_master.shape)  # 56,405

print(obesity.shape)  # 70,228
print(obesity_master.shape)  # 56,405

print(mental_health_master)