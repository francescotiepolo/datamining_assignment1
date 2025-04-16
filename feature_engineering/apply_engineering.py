import pandas as pd
import numpy as np
from datetime import datetime
import os

from engineering_funcs import normalize_column, sleep_deviation

dir = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + ".." + os.path.sep
df = pd.read_csv(dir + 'csv_files/filled.csv')

# Calculate the Sleep Deviation
df['SleepDeviation'] = df['Parsed Time you went to bed Yesterday'].apply(sleep_deviation)

# Normalize Sleep Deviation (inverted so lower deviation gets higher score)
df['Norm.SleepDeviation'] = normalize_column(df['SleepDeviation'], invert=True)

# Normalize Stress level (inverted as lower stress gets higher score)
df['Norm.Stress'] = normalize_column(df['Parsed What is your stress level (0-100)?'], invert=True)

# Normalize Sport hours
df['Norm.Sport'] = normalize_column(df['Parsed How many hours per week do you do sports (in whole hours)?'])

# Calculate the WellBeing score
df['WellBeing'] = (df['Norm.SleepDeviation'] + df['Norm.Stress'] + df['Norm.Sport']) / 3


print(df['WellBeing'].describe())
df.to_csv(dir + 'csv_files/well_being.csv', index=False)

import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(8, 5))
sns.histplot(df["WellBeing"], bins=20, kde=True, color="skyblue")
plt.title("Distribution of WellBeing Scores")
plt.xlabel("WellBeing Score")
plt.ylabel("Frequency")
plt.grid(True)
plt.savefig(dir + 'figs/well_being_distribution.png', dpi=300)