import pandas as pd
import os

# Construct the relative path to the dataset
file_path = os.path.join('..', 'data', 'ModifiedDatasets', 'ModifiedGlobalNewsDatasetWithLanguage.csv')
df = pd.read_csv(file_path)

# Specify the column and the value to filter by
column_name = 'language'  # Replace with the actual column name
specific_value = 'unknown'  # Replace with the specific value you are looking for

# Get the records that have the specific value in the specified column
# filtered_df = df[df[column_name].isnull()]
filtered_df = df[df[column_name] == specific_value]

# Print the filtered records
print(filtered_df)

# Optionally, save the filtered records to a new file
output_file = os.path.join('..', 'data', 'FilteredDatasets', 'FilteredRecord2.csv')
filtered_df.to_csv(output_file, index=False)

print(f"Filtered records saved to {output_file}")