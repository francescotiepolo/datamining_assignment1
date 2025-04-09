import pandas as pd
import numpy as np
import os

# Get the directory of the script
dir = os.path.dirname(os.path.realpath(__file__)) + os.path.sep

# Read the source CSV file
source_df = pd.read_csv(dir + 'goodday_cols.csv')

# Extract the last two columns
goodday_columns = source_df.iloc[:, -2:]

# Read the destination CSV file
destination_df = pd.read_csv(dir + 'ODI-2025-parsed.csv', sep=';')

# Reset indices to ensure they align properly
goodday_columns.reset_index(drop=True, inplace=True)
destination_df.reset_index(drop=True, inplace=True)

# Check if the number of rows match between both DataFrames
if len(goodday_columns) != len(destination_df):
    print(f"Warning: Row count mismatch. 'goodday_columns' has {len(goodday_columns)} rows and 'destination_df' has {len(destination_df)} rows.")
    # Optionally: Handle this mismatch, e.g., truncate or pad the shorter DataFrame
else:
    # Merge the DataFrames using the index
    destination_df = pd.concat([destination_df, goodday_columns], axis=1)

    # Save the joined DataFrame to a CSV file in the same directory
    destination_df.to_csv(dir + 'joined.csv', index=False)

    print("The file has been saved as 'joined.csv' in the current directory.")
