import pandas as pd
import os

# Construct the relative path to the dataset
file_path = os.path.join('..', 'data', 'ModifiedDatasets', 'ModifiedGlobalNewsDataset10.csv')
df = pd.read_csv(file_path)

# Specify the column to move and its new position
column_to_move = 'published_at'  # Replace with the actual column name
new_position = 1  # New position (0-based index, so 1 mean second place)

# Get the list of columns
columns = list(df.columns)

# Remove the column to move from the list and insert it at the new position
columns.insert(new_position, columns.pop(columns.index(column_to_move)))

# Reorder the DataFrame columns
df = df[columns]

# Save the updated dataset to a new file
output_file = os.path.join('..', 'data', 'ModifiedDatasets', 'ModifiedGlobalNewsDataset10_MoveColumn.csv')
df.to_csv(output_file, index=False)

print(f"Updated dataset saved to {output_file}")