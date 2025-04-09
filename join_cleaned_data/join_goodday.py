import pandas as pd
import numpy as np
import os

dir = os.path.dirname(os.path.realpath(__file__)) + os.path.sep

source_df = pd.read_csv(dir + 'csv_files/goodday_cols.csv')

goodday_columns = source_df.iloc[:, -2:]


destination_df = pd.read_csv(dir + 'csv_files/ODI-2025-parsed.csv', sep=';')

goodday_columns.reset_index(drop=True, inplace=True)
destination_df.reset_index(drop=True, inplace=True)


destination_df = pd.concat([destination_df, goodday_columns], axis=1)

destination_df.to_csv(dir + 'csv_files/joined.csv', index=False)
