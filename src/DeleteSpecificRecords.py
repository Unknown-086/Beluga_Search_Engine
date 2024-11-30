import pandas as pd
import os

# Construct the relative path to the dataset
file_path = os.path.join('..', 'data', 'ModifiedDatasets', 'FilteredGlobalNewsDatasetWithDocID.csv')
df = pd.read_csv(file_path)

# Specify the column name and the value to filter out
column_name = 'DocID'
value_to_delete = [117382, 117393, 117445, 117464, 117481]

# Filter out the rows that match the specific column values from the list
df_filtered = df
for value in value_to_delete:
    df_filtered = df_filtered[df_filtered[column_name] != value]

# Save the updated dataset to a new file
output_file = os.path.join('..', 'data', 'ModifiedDatasets', 'FilteredGlobalNewsDatasetWithDocID2.csv')
df_filtered.to_csv(output_file, index=False)

print(f"Rows with {column_name} = {value_to_delete} have been deleted and saved to {output_file}")