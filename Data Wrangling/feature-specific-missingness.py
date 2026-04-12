"""
Import packages
"""
import pandas as pd
from functools import reduce


"""
Define constants
"""
state_fips = {
    '01': 'Alabama', '02': 'Alaska', '04': 'Arizona', '05': 'Arkansas',
    '06': 'California', '08': 'Colorado', '09': 'Connecticut', '10': 'Delaware',
    '11': 'District of Columbia', '12': 'Florida', '13': 'Georgia', '15': 'Hawaii',
    '16': 'Idaho', '17': 'Illinois', '18': 'Indiana', '19': 'Iowa',
    '20': 'Kansas', '21': 'Kentucky', '22': 'Louisiana', '23': 'Maine',
    '24': 'Maryland', '25': 'Massachusetts', '26': 'Michigan', '27': 'Minnesota',
    '28': 'Mississippi', '29': 'Missouri', '30': 'Montana', '31': 'Nebraska',
    '32': 'Nevada', '33': 'New Hampshire', '34': 'New Jersey', '35': 'New Mexico',
    '36': 'New York', '37': 'North Carolina', '38': 'North Dakota', '39': 'Ohio',
    '40': 'Oklahoma', '41': 'Oregon', '42': 'Pennsylvania', '44': 'Rhode Island',
    '45': 'South Carolina', '46': 'South Dakota', '47': 'Tennessee', '48': 'Texas',
    '49': 'Utah', '50': 'Vermont', '51': 'Virginia', '53': 'Washington',
    '54': 'West Virginia', '55': 'Wisconsin', '56': 'Wyoming', '72': 'Puerto Rico'
}

education_features = ['B20004_006E', 'B20004_003E', 'B20004_001E']
employment_features = ['B23013_001E', 'B23020_001E']
income_poverty_features = ['B19083_001E', 'B22008_003E', 'B22008_002E']
housing_features = ['B25058_001E', 'B25071_001E', 'B25077_001E']

"""
Read in data
"""
census = pd.read_csv('/Users/vaibhavjha/Documents/Yale Project/Data/census.csv')


"""
Define functions
"""


def compute_state_missingness(df, group_cols, features, fips_map, save_path=None):
    """
    Compute state-level missingness for a group of features.

    Parameters:
        df: input dataframe
        group_cols: columns to group by (e.g. ['STATE'])
        features: list of feature columns to assess missingness
        fips_map: dictionary mapping FIPS codes to state names
        save_path: optional path to save CSV
    """
    # Get missingness percentage per state
    missingness = df.groupby(group_cols)[features].apply(
        lambda x: x.isna().mean() * 100, include_groups=False
    ).round(2).reset_index()

    # Normalize so each feature column sums to 1
    missingness[features] = missingness[features].div(
        missingness[features].sum(axis=0)
    ).mul(100).round(4)

    # Map state names
    missingness['STATE_NAME'] = missingness['STATE'].astype(str).str.zfill(2).map(fips_map)

    if save_path:
        missingness.to_csv(save_path, index=False)

    return missingness


def find_consistently_missing(df, feature_cols, threshold=0.95):
    """
    Find counties that are in the top 5% of missingness across all feature groups.
    threshold=0.95 means top 5% (i.e. above the 95th percentile).
    """
    results = {}
    for col in feature_cols:
        cutoff = df[col].quantile(threshold)
        results[col] = df[col] >= cutoff

    flags = pd.DataFrame(results)
    df['top5_count'] = flags.sum(axis=1)       # how many features they're top 5% in
    df['top5_pct'] = flags.mean(axis=1).round(2) # share of features they're top 5% in
    df['consistently_missing'] = flags.all(axis=1) # True only if top 10% in ALL features

    return df.sort_values('top5_count', ascending=False)


"""
State-level analysis
"""
state_education_missingness = compute_state_missingness(
    census, ['STATE'], education_features, state_fips)

state_employment_missingness = compute_state_missingness(
    census, ['STATE'], employment_features, state_fips)

state_income_poverty_missingness = compute_state_missingness(
    census, ['STATE'], income_poverty_features, state_fips)

state_housing_missingness = compute_state_missingness(
    census, ['STATE'], housing_features, state_fips)

"""
County-level analysis
"""
county_education_missingness = compute_state_missingness(
    census, ['STATE', 'COUNTY'], education_features, state_fips)

county_employment_missingness = compute_state_missingness(
    census, ['STATE', 'COUNTY'], employment_features, state_fips)

county_income_poverty_missingness = compute_state_missingness(
    census, ['STATE', 'COUNTY'], income_poverty_features, state_fips)

county_housing_missingness = compute_state_missingness(
    census, ['STATE', 'COUNTY'], housing_features, state_fips)


"""
Counties: identify counties are in top 10% of missingness at least 75% of the time
"""
# Merge all county-level missingness data
county_missingness_all = reduce(
    lambda left, right: left.merge(right, on=['STATE', 'COUNTY', 'STATE_NAME'], how='inner'),
    [county_education_missingness, county_employment_missingness, county_income_poverty_missingness, county_housing_missingness]
)

# Add tract counts
tract_counts = census.groupby(['STATE', 'COUNTY'])['TRACT'].count().reset_index(name='tract_count')
county_missingness_all = county_missingness_all.merge(tract_counts, on=['STATE', 'COUNTY'], how='left')

# Identify features of interest
feature_cols = [c for c in county_missingness_all.columns 
                if c not in ['STATE', 'COUNTY', 'STATE_NAME', 'tract_count']]

# Run function
result = find_consistently_missing(county_missingness_all, feature_cols)

# Counties in top 10% for every single feature
always_missing = result[result['consistently_missing']]
print(f"{len(always_missing)} counties consistently in top 5% missing across all features")
print(always_missing[['STATE_NAME', 'COUNTY', 'top5_count', 'top5_pct', 'tract_count']])

# Counties in top 10% for most (e.g. 75%+) features
mostly_missing = result[result['top5_pct'] >= 0.75]
print(f"\n{len(mostly_missing)} counties in top 5% for 75%+ of features")
print(mostly_missing[['STATE_NAME', 'COUNTY', 'top5_count', 'top5_pct', 'tract_count']])

# Export tables
#always_missing.to_csv('/Users/vaibhavjha/Documents/Yale Project/Data/Missingness/county_top_5_missing_always_data.csv', index=False)
#mostly_missing.to_csv('/Users/vaibhavjha/Documents/Yale Project/Data/Missingness/county_top_5_missing_mostly_data.csv', index=False)