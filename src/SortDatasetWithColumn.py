import pandas as pd
import os

# Construct the relative path to the dataset
file_path = os.path.join('..', 'data', 'ModifiedDatasets', 'ModifiedGlobalNewsDataset10_MoveColumn.csv')
df = pd.read_csv(file_path)

# Specify the column to sort by
column_name = 'published_at'  # Replace with the actual column name

# Convert the 'created_date' column to datetime format
# df[column_name] = pd.to_datetime(df[column_name])

# For Weekly News Dataset
# df[column_name] = pd.to_datetime(df[column_name], format='%Y%m%d%H%M')

# Sort the DataFrame by the 'created_date' column in ascending order
sorted_df = df.sort_values(by=column_name, ascending=True)

# Print the sorted records
print(sorted_df)

# Optionally, save the sorted records to a new file
output_file = os.path.join('..', 'data', 'ModifiedDatasets', 'ModifiedGlobalNewsDataset10_sorted.csv')
sorted_df.to_csv(output_file, index=False)

print(f"Sorted records saved to {output_file}")