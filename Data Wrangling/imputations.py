"""
Import packages
"""

import pandas as pd
import numpy as np


"""
Read in data
"""
census = pd.read_csv('/Users/vaibhavjha/Documents/Yale Project/Data/census.csv')
id_cols = ['STATE', 'COUNTY', 'TRACT', 'NAME']


"""
Inspect data
"""
print(census.head())
print(census.columns)


"""
Remove Hawaii census tracts
"""
census = census[census['STATE'] != 15]


"""
Replace -666666666 from B25035_001E with nan
"""
census['B25035_001E'] = census['B25035_001E'].replace(-666666666, np.nan)


"""
Add column: number of tracts in that tract's county
"""
tract_counts = census.groupby(['STATE', 'COUNTY'])['TRACT'].count().reset_index(name='tract_count')
census = census.merge(tract_counts, on=['STATE', 'COUNTY'], how='left')


"""
Definition

Impute median of non-null tracts from the same county
If all tract data is missing in county, impute state-level median
"""


def impute_census(df, feature_cols):
    df = df.copy()

    for col in feature_cols:
        county_median = df.groupby(['STATE', 'COUNTY'])[col].transform('median')
        state_median = df.groupby('STATE')[col].transform('median')

        df[col] = df[col].fillna(county_median).fillna(state_median)

    return df


"""
Implementation
"""
feature_cols = [c for c in census.columns if c not in id_cols + ['tract_count']]
imputed_census = impute_census(census, feature_cols)
imputed_census.to_csv('/Users/vaibhavjha/Documents/Yale Project/Data/imputed_census.csv')

"""
Verify
"""
print(f"Missing before: {census[feature_cols].isnull().sum().sum()}")
print(f"Missing after:  {imputed_census[feature_cols].isnull().sum().sum()}")
