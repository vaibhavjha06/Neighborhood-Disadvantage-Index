"""
Import packages
"""
import pandas as pd


"""
Read in data
"""
engineered_features = pd.read_csv('/Users/vaibhavjha/Documents/Yale Project/Data/engineered_features.csv')
print(engineered_features)


"""
Keep features following post-factor analysis feature selection
"""
final_features = engineered_features.drop(columns=['Unnamed: 0', 'Education_2', 'Education_3', 'Education_4', 'Education_5', 'Education_7',
                                                   'Employment_1', 'Employment_3', 'Employment_4', 'Employment_5', 'Employment_6', 'Employment_7',
                                                   'Income_1', 'Income_3', 'Income_5', 'Income_6',
                                                   'Housing_1', 'Housing_3', 'Housing_5', 'Housing_8'])
print(final_features.columns)


"""
Rename and reorder columns from final_features
"""
# Rename
final_features.rename(columns={
    'Education_8': 'ECON_1',
    'Employment_8': 'ECON_2',
    'Income_2': 'ECON_3',
    'Income_4': 'ECON_4',
    'Housing_2': 'ECON_5',
    'Housing_6': 'ECON_6',
    'Housing_7': 'ECON_7',
    'Education_1': 'LABOR_1',
    'Education_6': 'LABOR_2',
    'Employment_2': 'LABOR_3',
    'Employment_9': 'LABOR_4',
    'Education_9': 'INFRA_1',
    'Housing_4': 'INFRA_2',
    'Housing_9': 'INFRA_3'
}, inplace=True)

# Reorder
final_features = final_features[['STATE', 'COUNTY', 'TRACT', 'NAME', 'tract_count',
                                 'ECON_1', 'ECON_2', 'ECON_3', 'ECON_4', 'ECON_5', 'ECON_6', 'ECON_7',
                                 'LABOR_1', 'LABOR_2', 'LABOR_3', 'LABOR_4',
                                 'INFRA_1', 'INFRA_2', 'INFRA_3']]


"""
Standardize features
"""
id_cols = ['STATE', 'COUNTY', 'TRACT', 'NAME', 'tract_count']

feature_cols = ['ECON_1', 'ECON_2', 'ECON_3', 'ECON_4', 'ECON_5', 'ECON_6', 'ECON_7',
                'LABOR_1', 'LABOR_2', 'LABOR_3', 'LABOR_4',
                'INFRA_1', 'INFRA_2', 'INFRA_3']

final_features = final_features.copy()

final_features[feature_cols] = (
    final_features[feature_cols]
    - final_features[feature_cols].mean()
) / final_features[feature_cols].std()

print(final_features)


"""
Save standardized renamed features
"""
#final_features.to_csv('/Users/vaibhavjha/Documents/Yale Project/Data/final_eng_std_features.csv')


"""
Calculate domain scores
"""
final_features['ECON_score'] = (final_features['ECON_1'] + final_features['ECON_2'] + final_features['ECON_3'] + final_features['ECON_4'] + final_features['ECON_5'] + final_features['ECON_6'] + final_features['ECON_7']) / 7
final_features['LABOR_score'] = (final_features['LABOR_1'] + final_features['LABOR_2'] + final_features['LABOR_3'] + final_features['LABOR_4'] / 4)
final_features['INFRA_score'] = (final_features['INFRA_1'] + final_features['INFRA_2'] + final_features['INFRA_3'] / 3)

# Restandardize group scores
final_features['ECON_score'] = (final_features['ECON_score'] - final_features['ECON_score'].mean()) / final_features['ECON_score'].std()
final_features['LABOR_score'] = (final_features['LABOR_score'] - final_features['LABOR_score'].mean()) / final_features['LABOR_score'].std()
final_features['INFRA_score'] = (final_features['INFRA_score'] - final_features['INFRA_score'].mean()) / final_features['INFRA_score'].std()

#print(final_features[id_cols + ['ECON_score', 'LABOR_score', 'INFRA_score']])


"""
Calculate index with weights: 60, 25, 15
"""
final_features['index'] = (0.6*final_features['ECON_score'] + 0.25*final_features['LABOR_score'] + 0.15*final_features['INFRA_score']) / 3
final_features['index'] = final_features['index'].round(4)


"""
Save index
"""
final_output = final_features[['STATE', 'COUNTY', 'TRACT', 'NAME', 'tract_count', 'index']]
#final_output.to_csv('/Users/vaibhavjha/Documents/Yale Project/Data/index.csv')
print(final_output)
