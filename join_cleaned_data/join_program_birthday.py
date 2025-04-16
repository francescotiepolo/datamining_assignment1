import pandas as pd
import os

# Set up directory paths
script_dir = os.path.dirname(os.path.realpath(__file__))
base_dir = os.path.join(script_dir, "..")
csv_dir = os.path.join(base_dir, "csv_files")

COLUMNS_TO_SUBSTITUTE = {
    'What programme are you in?': 'What programme are you in?',
    'When is your birthday (date)?': 'When is your birthday (date)?'
}

source_path = os.path.join(csv_dir, 'cleaned_program_and_birthday.csv')
source_df = pd.read_csv(source_path)

dest_path = os.path.join(csv_dir, 'joined.csv')
destination_df = pd.read_csv(dest_path, sep=',')

for src_col, dest_col in COLUMNS_TO_SUBSTITUTE.items():
    destination_df[dest_col] = source_df[src_col]
    
output_path = os.path.join(csv_dir, 'joined.csv')
destination_df.to_csv(output_path, index=False, sep=',')