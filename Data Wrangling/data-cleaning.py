"""
Import packages
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

"""
Constants
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

id_cols = ['STATE', 'COUNTY', 'TRACT', 'NAME']

data_paths = {
    'education':  '/Users/vaibhavjha/Documents/Yale Project/Data/education_data.csv',
    'employment': '/Users/vaibhavjha/Documents/Yale Project/Data/employment_data.csv',
    'income':     '/Users/vaibhavjha/Documents/Yale Project/Data/income_data.csv',
    'housing':    '/Users/vaibhavjha/Documents/Yale Project/Data/housing_data.csv',
}


"""
Loading data
"""


def load_and_merge(paths, export_path=None):
    datasets = {name: pd.read_csv(path) for name, path in paths.items()}
    base = datasets['education']
    for name in ['employment', 'income', 'housing']:
        base = base.merge(
            datasets[name].drop(columns=['NAME']),
            on=['STATE', 'COUNTY', 'TRACT'],
            how='inner'
        )
    if export_path:
        base.to_csv(export_path, index=False)
    return base


def inspect(df):
    print(f"Shape: {df.shape}")
    print(f"\nSummary statistics:\n{df.describe()}")
    print(f"\nMissingness:\n{df.isnull().sum()}")
    print(f"\nColumn info:"); df.info()


"""
Missingness
"""


def compute_missingness(df, group_cols, export_path=None):
    features = [c for c in df.columns if c not in id_cols]

    result = (
        df.groupby(group_cols)[features]
        .apply(lambda x: x.isnull().mean())
        .round(3)
        .reset_index()
    )
    result['mean_missingness'] = result[features].replace(0, np.nan).mean(axis=1).round(2)
    result['STATE_NAME'] = result['STATE'].astype(str).str.zfill(2).map(state_fips)

    tract_counts = df.groupby(group_cols)['TRACT'].count().reset_index(name='tract_count')
    result = result.merge(tract_counts, on=group_cols, how='left')

    if export_path:
        result.to_csv(export_path, index=False)
    return result


def summarize(df, group_cols, export_path=None):
    result = (
        df[group_cols + ['STATE_NAME', 'mean_missingness', 'tract_count']]
        .sort_values('mean_missingness', ascending=False)
    )
    if export_path:
        result.to_csv(export_path, index=False)
    return result


"""
Visualization
"""


def plot_missingness(df, title, suptitle, save_path=None):
    plt.figure(figsize=(10, 6))
    sns.kdeplot(df['mean_missingness'], fill=True)
    plt.title(title)
    plt.suptitle(suptitle)
    plt.xlabel('Proportion of features missing')
    if save_path:
        plt.savefig(save_path)
    else:
        plt.show()
    plt.close()


"""
Main
"""
BASE = '/Users/vaibhavjha/Documents/Yale Project/Data/Missingness'


def main():
    census = load_and_merge(data_paths, '/Users/vaibhavjha/Documents/Yale Project/Data/census.csv')
    inspect(census)

    for level, group_cols in [('State', ['STATE']), ('County', ['STATE', 'COUNTY'])]:
        missingness = compute_missingness(census, group_cols,
                                          export_path=f'{BASE}/{level.lower()}_missingness_pct.csv')
        summary = summarize(missingness, group_cols,
                            export_path=f'{BASE}/{level.lower()}_select_missingness_pct.csv')
        print(summary)

        plot_missingness(
            missingness,
            title=f'{level} missingness density plot',
            suptitle=f'Among missing features, there is variability in average census tract missingness at the {level.lower()} level.',
        )


if __name__ == '__main__':
    main()
