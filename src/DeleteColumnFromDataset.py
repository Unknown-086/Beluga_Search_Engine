import pandas as pd
import os

# Construct the relative path to the dataset
file_path = os.path.join('..', 'data', 'ModifiedDatasets', 'ModifiedGlobalNewsDataset5.csv')
df = pd.read_csv(file_path)

# Specify the column to be deleted
column_to_delete = 'DocID'  # Replace 'column_name' with the actual column name

# Delete the specified column
if column_to_delete in df.columns:
    df.drop(columns=[column_to_delete], inplace=True)
    print(f"Column '{column_to_delete}' has been deleted.")
else:
    print(f"Column '{column_to_delete}' does not exist in the dataset.")

# Save the updated dataset to a new file
output_file = os.path.join('..', 'data', 'ModifiedDatasets', 'ModifiedGlobalNewsDataset6.csv')
df.to_csv(output_file, index=False)

print(f"Updated dataset without the column saved to {output_file}")