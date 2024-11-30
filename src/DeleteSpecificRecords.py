import pandas as pd
import os

from src.FilterWithList import value

# Construct the relative path to the dataset
file_path = os.path.join('..', 'data', 'ModifiedDatasets', 'ModifiedNews-week-17aug2.csv')
df = pd.read_csv(file_path)

# Specify the column name and the value to filter out
column_name = 'headline_text'
value = 'w3-meneame'
# value_to_delete = [106574]

# Filter out the rows that match the specific column values from the list
# for value in value_to_delete:
# df_filtered = df[df[column_name] != value]
df_filtered = df[df[column_name].notnull()]

# Save the updated dataset to a new file
output_file = os.path.join('..', 'data', 'ModifiedDatasets', 'ModifiedNews-week-17aug3.csv')
df_filtered.to_csv(output_file, index=False)

print(f"Rows with {column_name} = {value} have been deleted and saved to {output_file}")