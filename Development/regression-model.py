"""
Import packages
"""
import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import r2_score
from sklearn.pipeline import Pipeline


"""
Read in data
"""
# Main covariate of interest
index = pd.read_csv('/Users/vaibhavjha/Documents/Yale Project/Data/index.csv')
index = index.drop(columns='Unnamed: 0')

# Outcomes
outcomes = pd.read_csv('/Users/vaibhavjha/Documents/Yale Project/Data/PLACES__Local_Data_for_Better_Health,_Census_Tract_Data_2021.csv')
# Isolate mental health measure
mental_health = outcomes[outcomes['Measure'] == 'Mental health not good for >=14 days among adults aged >=18 years']
mental_health = mental_health[['Year', 'LocationID', 'Data_Value']]
mental_health['LocationID'] = mental_health['LocationID'].astype(str)
# Isolate obesity measure
obesity = outcomes[outcomes['Measure'] == 'Obesity among adults aged >=18 years']
obesity = obesity[['Year', 'LocationID', 'Data_Value']]
obesity['LocationID'] = obesity['LocationID'].astype(str)

# Other variables for covariates in regression model
other = pd.read_csv('/Users/vaibhavjha/Documents/Yale Project/Data/othervars.csv')

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


"""
Fix other variables
"""
# Make state categorical
mental_health_master['STATE'] = mental_health_master['STATE'].astype('category')
obesity_master['STATE'] = obesity_master['STATE'].astype('category')

print(other.head())

other['female_prop'] = other['B01001_026E'] / other['B01001_001E']
other['minority_prop'] = (1 - (other['B02001_002E'] / other['B01003_001E']))
other['log_pop'] = np.log(other['B01003_001E'])


"""
Impute for missing values
"""
# Female prop
other['female_prop'] = other['female_prop'].replace([np.inf, -np.inf], np.nan)
other['female_prop'] = other['female_prop'].fillna(other.groupby('COUNTY')['female_prop'].transform('median'))

# Minority prop
other['minority_prop'] = other['minority_prop'].replace([np.inf, -np.inf], np.nan)
other['minority_prop'] = other['minority_prop'].fillna(other.groupby('COUNTY')['minority_prop'].transform('median'))

# Log pop
other['log_pop'] = other['log_pop'].replace([np.inf, -np.inf], np.nan)
other['log_pop'] = other['log_pop'].fillna(other.groupby('COUNTY')['log_pop'].transform('median'))

print(other['female_prop'].dtype)  # all floats, as intended


"""
Merge masters with other by State
"""


def add_geoid(df):
    df['STATE'] = df['STATE'].astype(str).str.zfill(2)
    df['COUNTY'] = df['COUNTY'].astype(str).str.zfill(3)
    df['TRACT'] = df['TRACT'].astype(str).str.zfill(6)

    df['GEOID'] = df['STATE'] + df['COUNTY'] + df['TRACT']
    return df


other = add_geoid(other)

mental_health_master = mental_health_master.merge(other, on=['STATE', 'COUNTY', 'TRACT'], how='left')
obesity_master = obesity_master.merge(other, on=['STATE', 'COUNTY', 'TRACT'], how='left')


"""
Remove duplicate tomorrow
"""
mental_health_master = mental_health_master.drop('GEOID_y', axis=1)
obesity_master = obesity_master.drop('GEOID_y', axis=1)


"""
Select and save each master
"""
mental_health_master = mental_health_master[['STATE', 'COUNTY', 'TRACT', 'NAME_x', 'tract_count', 'GEOID_x', 'index', 'mental_health', 'female_prop', 'minority_prop', 'log_pop']]
obesity_master = obesity_master[['STATE', 'COUNTY', 'TRACT', 'NAME_x', 'tract_count', 'GEOID_x', 'index', 'obesity', 'female_prop', 'minority_prop', 'log_pop']]

#mental_health_master.to_csv('/Users/vaibhavjha/Documents/Yale Project/Data/mental_health_master.csv')
#obesity_master.to_csv('/Users/vaibhavjha/Documents/Yale Project/Data/obesity_master.csv')


"""
Fit model: Mental Health
"""
numeric_cols = ['index', 'female_prop', 'minority_prop', 'log_pop']
cat_cols = ['STATE']

X = mental_health_master[numeric_cols + cat_cols]
y = mental_health_master['mental_health']

preprocessor = ColumnTransformer(transformers=[("num", StandardScaler(), numeric_cols),
                                               ("cat", OneHotEncoder(drop="first", handle_unknown="ignore"),  cat_cols),])

pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("model",        LinearRegression())])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)


"""
Assess model
"""
print(f"R² Score for mental health model: {r2_score(y_test, y_pred):.3f}")


"""
Mental health model WITHOUT index
"""
X_no_index = mental_health_master[numeric_cols]
X_train_ns, X_test_ns, y_train_ns, y_test_ns = train_test_split(X_no_index, y, test_size=0.2, random_state=42)

pipeline_no_index = Pipeline(steps=[
    ("scaler", StandardScaler()),
    ("model",  LinearRegression())
])

pipeline_no_index.fit(X_train_ns, y_train_ns)
y_pred_ns = pipeline_no_index.predict(X_test_ns)

print(f"R² WITH index    : {r2_score(y_test, y_pred):.3f}")
print(f"R² WITHOUT index : {r2_score(y_test_ns, y_pred_ns):.3f}")


"""
OLS assumptions
"""
residuals = y_test - y_pred

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Residuals vs fitted
axes[0].scatter(y_pred, residuals, alpha=0.5)
axes[0].axhline(0, color="red", linestyle="--")
axes[0].set_xlabel("Fitted values")
axes[0].set_ylabel("Residuals")
axes[0].set_title("Residuals vs Fitted")

# Q-Q plot
stats.probplot(residuals, plot=axes[1])
axes[1].set_title("Q-Q Plot (Normality of Residuals)")

plt.tight_layout()
plt.show()
plt.close()


"""
Fit model: Obesity
"""
numeric_cols = ['index', 'female_prop', 'minority_prop', 'log_pop']
cat_cols = ['STATE']

X = obesity_master[numeric_cols + cat_cols]
y = obesity_master['obesity']

preprocessor = ColumnTransformer(transformers=[("num", StandardScaler(), numeric_cols),
                                               ("cat", OneHotEncoder(drop="first", handle_unknown="ignore"),  cat_cols),])

pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("model",        LinearRegression())])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)


"""
Assess model
"""
print(f"R² Score for obesity model: {r2_score(y_test, y_pred):.3f}")


"""
OLS assumptions
"""
residuals = y_test - y_pred

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Residuals vs fitted
axes[0].scatter(y_pred, residuals, alpha=0.5)
axes[0].axhline(0, color="red", linestyle="--")
axes[0].set_xlabel("Fitted values")
axes[0].set_ylabel("Residuals")
axes[0].set_title("Residuals vs Fitted")

# Q-Q plot
stats.probplot(residuals, plot=axes[1])
axes[1].set_title("Q-Q Plot (Normality of Residuals)")

plt.tight_layout()
plt.show()
plt.close()


"""
Obesity model WITHOUT index
"""
X_no_index = obesity_master[numeric_cols]
X_train_ns, X_test_ns, y_train_ns, y_test_ns = train_test_split(X_no_index, y, test_size=0.2, random_state=42)

pipeline_no_index = Pipeline(steps=[
    ("scaler", StandardScaler()),
    ("model",  LinearRegression())
])

pipeline_no_index.fit(X_train_ns, y_train_ns)
y_pred_ns = pipeline_no_index.predict(X_test_ns)

print(f"R² WITH index    : {r2_score(y_test, y_pred):.3f}")
print(f"R² WITHOUT index : {r2_score(y_test_ns, y_pred_ns):.3f}")