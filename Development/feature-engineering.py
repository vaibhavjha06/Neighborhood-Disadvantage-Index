"""
Import packages
"""
import pandas as pd
import numpy as np

"""
Read data
"""

df = pd.read_csv('/Users/vaibhavjha/Documents/Yale Project/Data/imputed_census.csv')
print(df.head())

"""
Define impute feature for division by zero exceptions in engineered features
"""


def impute_feature(df, col):
    """Replace inf with nan, then impute county → state → national median."""
    df[col] = df[col].replace([np.inf, -np.inf], np.nan)
    county_median = df.groupby(['STATE', 'COUNTY'])[col].transform('median')
    state_median  = df.groupby('STATE')[col].transform('median')
    nation_median = df[col].median()
    df[col] = df[col].fillna(county_median).fillna(state_median).fillna(nation_median)
    return df


"""
Education engineered features
"""

df['Education_1'] = (df['B06009_009E'] + df['B06009_015E']) / (df['B06009_007E'] + df['B06009_013E'])
df = impute_feature(df, 'Education_1')
df['Education_2'] = 1 - (df['B06009_030E'] / df['B06009_025E'])
df = impute_feature(df, 'Education_2')
df['Education_3'] = (df['B13014_010E'] + df['B13014_011E']) / df['B13014_002E']
df = impute_feature(df, 'Education_3')
df['Education_4'] = 1 - (df['B15011_023E'] + df['B15011_029E']) / (df['B15011_022E'] + df['B15011_028E'])
df = impute_feature(df, 'Education_4')
df['Education_5'] = df['B16010_021E'] / df['B16010_016E']
df = impute_feature(df, 'Education_5')
df['Education_6'] = (df['B17003_004E'] + df['B17003_005E'] + df['B17003_009E'] + df['B17003_010E']) / (df['B17003_003E'] + df['B17003_008E'])
df = impute_feature(df, 'Education_6')
df['Education_7'] = (df['B20004_006E'] - df['B20004_003E'])
df['Education_8'] = (df['B27019_011E'] + df['B27019_012E']) / df['B27019_008E']
df = impute_feature(df, 'Education_8')
df['Education_9'] = df['B28006_013E'] / df['B28006_008E']
df = impute_feature(df, 'Education_9')


"""
Employment engineered features
"""
df['Employment_1'] = 1 - (df['B08006_017E'] / df['B08006_001E'])
df = impute_feature(df, 'Employment_1')
df['Employment_2'] = 1 - (df['B08302_009E'] + df['B08302_010E'] + df['B08302_011E']) / df['B08302_001E']
df = impute_feature(df, 'Employment_2')
df['Employment_3'] = (df['B08134_070E'] + df['B08134_110E']) / df['B08134_010E']
df = impute_feature(df, 'Employment_3')
df['Employment_4'] = df['B08202_022E'] / df['B08202_018E']
df = impute_feature(df, 'Employment_4')
df['Employment_5'] = abs(df['B23013_001E'] - df['B23013_001E'].median()) / (df['B23013_001E'].quantile(0.75) - df['B23013_001E'].quantile(0.25))
df = impute_feature(df, 'Employment_5')
df['Employment_6'] = df['B23027_004E'] / df['B23027_002E']
df = impute_feature(df, 'Employment_6')
df['Employment_7'] = df['B23020_001E']
df['Employment_8'] = df['B28007_009E'] / df['B28007_002E']
df = impute_feature(df, 'Employment_8')
df['Employment_9'] = (df['C24050_002E'] + df['C24050_003E'] + df['C24050_004E'] + df['C24050_005E'] + df['C24050_006E'] + df['C24050_007E']) / df['C24050_001E']
df = impute_feature(df, 'Employment_9')


"""
Income & Poverty engineered features
"""
df['Income_1'] = (df['B19001_002E'] + df['B19001_003E'] + df['B19001_004E'] + df['B19001_005E'] + df['B19001_006E'] + df['B19001_007E'] + df['B19001_008E'] + df['B19001_009E'] + df['B19001_010E'] + df['B19001_011E']) / df['B19001_001E']
df = impute_feature(df, 'Income_1')
df['Income_2'] = df['B19057_002E'] / df['B19057_001E']
df = impute_feature(df, 'Income_2')
df['Income_3'] = df['B19083_001E']
df['Income_4'] = df['B19058_002E'] / df['B19058_001E']
df = impute_feature(df, 'Income_4')
df['Income_5'] = df['B22008_003E'] - df['B22008_002E']
df['Income_6'] = (df['B07012_010E'] / df['B07012_009E']) / (df['B07012_012E'] / df['B07012_009E'])
df = impute_feature(df, 'Income_6')


"""
Housing engineered features
"""
# Fixed
df['Housing_1'] = df['B25058_001E']

df['Housing_2'] = df['B25071_001E']
df['Housing_3'] = df['B25077_001E']
df['Housing_4'] = df['B25002_003E'] / df['B25002_001E']
df = impute_feature(df, 'Housing_4')
df['Housing_5'] = df['B25014_013E'] / df['B25014_008E']
df = impute_feature(df, 'Housing_5')
df['Housing_6'] = 1 - (df['B25003_002E'] - df['B25003_001E'])
df['Housing_7'] = 1 - (df['B11001_003E'] / df['B11001_001E'])
df = impute_feature(df, 'Housing_7')
df['Housing_8'] = 1 - df['B25035_001E']
df['Housing_9'] = df['B25051_003E'] / df['B25051_001E']
df = impute_feature(df, 'Housing_9')


"""
Verify nulls are taken care of
"""
eng_cols = [c for c in df.columns if any(c.startswith(p) for p in ['Education_', 'Employment_', 'Income_', 'Housing_'])]

remaining = df[eng_cols].isnull().sum()
remaining = remaining[remaining > 0]
print("Remaining nulls:" if len(remaining) > 0 else "✓ No nulls in engineered features")
if len(remaining) > 0:
    print(remaining)


"""
Return engineered features
"""
selected_df = df[['STATE', 'COUNTY', 'TRACT', 'NAME', 'tract_count',
                  'Education_1', 'Education_2', 'Education_3', 'Education_4',
                  'Education_5', 'Education_6', 'Education_7', 'Education_8',
                  'Education_9', 'Employment_1', 'Employment_2', 'Employment_3',
                  'Employment_4', 'Employment_5', 'Employment_6', 'Employment_7',
                  'Employment_8', 'Employment_9', 'Income_1', 'Income_2', 'Income_3',
                  'Income_4', 'Income_5', 'Income_6', 'Housing_1', 'Housing_2',
                  'Housing_3', 'Housing_4', 'Housing_5', 'Housing_6', 'Housing_7',
                  'Housing_8', 'Housing_9']]

selected_df.to_csv('/Users/vaibhavjha/Documents/Yale Project/Data/engineered_features.csv')
