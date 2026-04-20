"""
Import packages
"""
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from factor_analyzer import FactorAnalyzer
from factor_analyzer.factor_analyzer import calculate_bartlett_sphericity


"""
Read in data
"""
engineered_features = pd.read_csv('/Users/vaibhavjha/Documents/Yale Project/Data/engineered_features.csv')

# Isolate individual features from labels
features = engineered_features.iloc[:, 6:]

# Iteration after removing features

final_features = features.drop(columns=['Education_2', 'Education_3', 'Education_5', 'Education_7',
                                        'Employment_1', 'Employment_3', 'Employment_5', 'Employment_6', 'Employment_7',
                                        'Income_1', 'Income_5', 'Income_6',
                                        'Housing_1', 'Housing_3', 'Housing_5', 'Housing_8'])


"""
Determine whether data are suitable for factor analysis
"""
# Assess correlation between columns (features)

corr = final_features.corr()
mask = np.triu(np.ones_like(corr, dtype=bool))  # hide upper triangle

labels = corr.applymap(lambda x: f'{x:.2f}' if abs(x) >= 0.3 else '')  # annotate correlations where abs value is >= 0.3
plt.figure(figsize=(12, 10))
sns.heatmap(corr, mask=mask, annot=labels, fmt='', cmap='coolwarm', center=0)
plt.title("Correlation Matrix")
plt.tight_layout()
plt.show()
plt.close()

print(corr.round(2))

# Conduct Bartlett's sphericity test
chi_square, p_value = calculate_bartlett_sphericity(final_features)
print(f'Barlett p-value: {p_value}')
# Output: 0.0


"""
Load factors
"""
n_factors = 3
fa = FactorAnalyzer(n_factors=n_factors, rotation='oblimin')  # maybe consider varimax/oblimin if we believe factors are uncorrelated/correlated
fa.fit(final_features)


# Kaiser criterion
ev, cf = fa.get_eigenvalues()
print(ev)

# Proportion of variance by factor
variance, prop_var, cumulative_var = fa.get_factor_variance()

x = np.arange(1, len(ev) + 1)

# Scree plot
plt.figure(figsize=(10, 6))
plt.plot(x[:8], ev[:8], marker='o', linewidth=2)
plt.plot(x[3:], ev[3:], marker='o', linewidth=2, color='0.65')
plt.axhline(y=1, color='r', linestyle='--', linewidth=1.8)

plt.xlabel('Factor Number')
plt.xticks(range(1, 18))
plt.ylabel('Eigenvalue')
plt.title('Scree Plot - Oblique Rotation')
plt.text(10.5, 1.05, 'Kaiser criterion', color='r')

plt.show()
plt.close()


"""
Visualization: cumulative proportion of variance explained with each added factor
"""

plt.plot(range(1, len(cumulative_var) + 1), cumulative_var, marker='o')
plt.xlabel('Factor Number')
plt.xticks(range(1, 4))
plt.ylabel('Cumulative Proportion of Variance Explained')
plt.title('Cumulative Proportion of Variance Explained Across Factors')
plt.suptitle('Three factors explain approx. 42% of the variance.',
             y=0.98)
plt.show()
plt.close()

print(cumulative_var)


"""
Visualization: factor loadings heatmap
"""
loadings = pd.DataFrame(fa.loadings_, index=final_features.columns,
                        columns=[f'Factor {i+1}' for i in range(n_factors)])

plt.figure(figsize=(10, 8))
ax = sns.heatmap(loadings, annot=True, fmt='.2f',
                 cmap='coolwarm', center=0, vmin=-1, vmax=1, annot_kws={"size": 11})
plt.xlabel('Factors')
plt.ylabel('Engineered Features')
plt.title('Factor Loadings Heatmap')
#plt.suptitle('The factor loadings for the first seven factors align with the behavioral cohorts we developed.', y=0.98)
plt.show()
plt.close()