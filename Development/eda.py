"""
Import packages
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

"""
Read in data
"""
engineered_features = pd.read_csv('/Users/vaibhavjha/Documents/Yale Project/Data/engineered_features.csv')


"""
Histogram of tract counts per county
"""
sns.histplot(engineered_features['tract_count'])
median = engineered_features['tract_count'].median()
p75 = engineered_features['tract_count'].quantile(0.75)
plt.axvline(median, color='red', linestyle='--', label=f'Median: {median:,.0f}')
plt.axvline(p75, color='blue', linestyle='--', label=f'75th Percentile: {p75:,.0f}')

plt.xlim(0, 100)
plt.xlabel('Number of census tracts within a county')
plt.ylabel('Count')
plt.title('Histogram of Census Tracts Within Counties in the United States')
plt.suptitle('The count of census tracts per county skews heavily to the right, with figures up to 2,346.')
plt.legend()
#plt.show()
plt.close()


"""
Missingness analysis of engineered features
"""
id_cols = ['STATE', 'COUNTY', 'TRACT', 'NAME', 'tract_count']
feature_cols = [c for c in engineered_features.columns if c not in id_cols]
print(engineered_features[feature_cols].isnull().sum())


"""
Education engineered features
"""
# Education_1
# Theoretical range: [0, 1]
sns.histplot(engineered_features['Education_1'])
plt.xlabel('Proportion of natives whose highest education is high school')
plt.ylabel('Count')
plt.title('Proportion of native residents whose highest education attained \n is high school graduate equivalent / total native population')
#plt.show()
plt.close()

# Education_2
# Theoretical range: [0, 1]
sns.histplot(engineered_features['Education_2'])
plt.xlabel('Proportion of foreign-born non-graduate school graduates')
plt.ylabel('Count')
plt.title('Proportion of foreign-born non-graduate school graduates / total \n foreign-born population')
#plt.show()
plt.close()

# Education_3
# Theoretical range: [0, 1]
sns.histplot(engineered_features['Education_3'], bins=15)
plt.xlabel('Proportion of women who had a birth and are unmarried with \n high school education or less / all women who had a birth')
plt.ylabel('Count')
plt.title('Proportion of women who had a birth and are unmarried with \n high school education or less')
# plt.show()
plt.close()

# Education_4
# Theoretical range: [0, 1]
sns.histplot(engineered_features['Education_4'], bins=25)
plt.xlim(-10000, 1)
plt.xlabel('Proportion of women without science and engineering bachelors degrees \n aged between 25-64 / women with bachelors degrees aged between 25-64')
plt.ylabel('Count')
plt.title('Proportion of women without science and engineering bachelors degrees aged between 25-64')
plt.show()
plt.close()