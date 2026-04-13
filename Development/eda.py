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
Visualization: Histogram of tract counts per county
"""
sns.histplot(engineered_features['tract_count'])
median = engineered_features['tract_count'].median()
p75 = engineered_features['tract_count'].quantile(0.75)
plt.axvline(median, color='red', linestyle='--', label=f'Median: {median:,.0f}')
plt.axvline(p75, color='blue', linestyle='--', label=f'75th Percentile: {p75:,.0f}')

plt.xlim(0, 500)
plt.xlabel('Number of census tracts within a county')
plt.ylabel('Count')
plt.title('Histogram of Census Tracts Within Counties in the United States')
plt.suptitle('The count of census tracts per county skews heavily to the right, with figures up to 2,346.')
plt.legend()
#plt.show()
plt.close()


"""
Visualization: Education engineered features
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
plt.title('Proportion of women who had a birth and are unmarried with \n high school education or less / all women who had a birth')
plt.ylabel('Count')
plt.xlabel('Proportion of women who had a birth and are unmarried with \n high school education or less')
#plt.show()
plt.close()

# Education_4
# Theoretical range: [0, 1]
sns.histplot(engineered_features['Education_4'], bins=25)
plt.xlim(0, 1)
plt.title('Proportion of women without science and engineering bachelors degrees \n aged between 25-64 / women with bachelors degrees aged between 25-64')
plt.ylabel('Count')
plt.xlabel('Proportion of women without science and engineering bachelors degrees aged between 25-64')
#plt.show()
plt.close()

# Education_5
# Theoretical range: [0, 1]
sns.histplot(engineered_features['Education_5'], bins=25)
plt.xlim(0, 1)
plt.title('Proportion of high school graduate equivalents in labor force who speak \n other languages >= 25 years old/ all high school graduate equivalents in labor force >= 25 years old')
plt.ylabel('Count')
plt.xlabel('Proportion of high school graduate equivalents in labor force who speak \n other languages >= 25 years old')
#plt.show()
plt.close()

# Education_6
# Theoretical range: [0, 1]
sns.histplot(engineered_features['Education_6'], bins=25)
plt.xlim(0, 1)
plt.title('Proportion of high school graduate equivalents or less whose income in \n the past 12 months is below poverty level / all high school graduate equivalents')
plt.ylabel('Count')
plt.xlabel('Proportion of high school graduate equivalents or less whose income in \n the past 12 months is below poverty level')
#plt.show()
plt.close()

# Education_7
# Theoretical range: (-inf, inf)
sns.histplot(engineered_features['Education_7'], bins=25)
#plt.xlim(-5, 5)
plt.title('Median income difference between high school graduate equivalents and \n graduate or professional degree earners')
plt.ylabel('Count')
plt.xlabel('Median income difference between high school graduate equivalents and \n graduate or professional degree earners')
#plt.show()
plt.close()

# Education_8
# Theoretical range: [0, 1]
sns.histplot(engineered_features['Education_8'], bins=25)
#plt.xlim(-5, 5)
plt.title('Proportion: high school graduate equivalents between 26-64 years old \n who are on public health insurance or not on any health insurance / \n high school graduate equivalents between 26-64 years old')
plt.ylabel('Count')
plt.xlabel('Proportion of high school graduate equivalents between 26-64 years old \n who are on public health insurance or not on any health insurance')
#plt.show()
plt.close()

# Education_9
# Theoretical range: [0, 1]
sns.histplot(engineered_features['Education_9'], bins=25)
#plt.xlim(-5, 5)
plt.title("Proportion: high school graduate equivalent or some college or associate's \n degree individuals who do not have a computer / all high school \n graduate equivalents or some college or associate's degree individuals")
plt.ylabel('Count')
plt.xlabel("Proportion of high school graduate equivalent or some college or associate's \n degree individuals who do not have a computer")
#plt.show()
plt.close()


"""
Visualization: Employment engineered features
"""
# Employment_1
# Theoretical range: [0, 1]
sns.histplot(engineered_features['Employment_1'], bins=25)
#plt.xlim(-5, 5)
plt.title("Proportion: workers that do not work from home")
plt.ylabel('Count')
plt.xlabel("Proportion of workers that do not work from home")
#plt.show()
plt.close()

# Employment_2
# Theoretical range: [0, 1]
sns.histplot(engineered_features['Employment_2'], bins=25)
#plt.xlim(-5, 5)
plt.title("Proportion: those whose travel time to work is not between 8-10 am / those whose travel time to work overall")
plt.ylabel('Count')
plt.xlabel("Proportion of those whose travel time to work is not between 8-10 am / those whose travel time to work overall")
#plt.show()
plt.close()

# Employment_3
# Theoretical range: [0, 1]
sns.histplot(engineered_features['Employment_3'], bins=20)
#plt.xlim(-5, 5)
plt.title("Proportion: individuals who take public transportation or walk to work \n for more than 60 minutes / all individuals who take more than \n 60 minutes to get to work")
plt.ylabel('Count')
plt.xlabel("Proportion of individuals who take public transportation or walk to work \n for more than 60 minutes")
#plt.show()
plt.close()

# Employment_4
# Theoretical range: [0, 1]
sns.histplot(engineered_features['Employment_4'], bins=20)
#plt.xlim(-5, 5)
plt.title("Proportion: 4-or-more person households that have 3 or more workers / \n all 4-or-more person households")
plt.ylabel('Count')
plt.xlabel("Proportion of 4-or-more person households that have 3 or more workers")
#plt.show()
plt.close()

# Employment_5
# Theoretical range: (-inf, inf)
sns.histplot(engineered_features['Employment_5'], bins=20)
#plt.xlim(-5, 5)
plt.title("IQR-based distance of median age for census tract working compared to \n national median age for working")
plt.ylabel('Count')
plt.xlabel("IQR-based distance")
#plt.show()
plt.close()

# Employment_6
# Theoretical range: [0, 1]
sns.histplot(engineered_features['Employment_6'], bins=20)
#plt.xlim(-5, 5)
plt.title("Proportion: individuals working full-time, year-round at 16-19 years old / \n all individuals at 16-19 years old")
plt.ylabel('Count')
plt.xlabel("Proportion of individuals working full-time, year-round at 16-19 years old")
#plt.show()
plt.close()

# Employment_7
# Theoretical range: [-inf, inf]
sns.histplot(engineered_features['Employment_7'], bins=20)
#plt.xlim(-5, 5)
plt.title("Mean usual hours worked in past 12 months for workers aged 16-64")
plt.ylabel('Count')
plt.xlabel("Mean usual hours worked in past 12 months for workers aged 16-64")
#plt.show()
plt.close()

# Employment_8
# Theoretical range: (0, 1)
sns.histplot(engineered_features['Employment_8'], bins=20)
#plt.xlim(-5, 5)
plt.title("Proportion: civilian labor force that is unemployed / total civilian labor force")
plt.ylabel('Count')
plt.xlabel("Unemployment rate")
#plt.show()
plt.close()

# Employment_9
# Theoretical range: (0, 1)
sns.histplot(engineered_features['Employment_9'], bins=20)
#plt.xlim(-5, 5)
plt.title("Proportion: blue-collar industry workers / all workers")
plt.ylabel('Count')
plt.xlabel("Proportion of blue-collar industry workers")
#plt.show()
plt.close()