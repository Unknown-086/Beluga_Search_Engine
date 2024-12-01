import pandas as pd
import os

# Construct the relative path to the dataset
file_path = os.path.join('../..', 'data', 'FilteredDatasets', 'ModifiedGlobalNewsDataset13_English.csv')
df = pd.read_csv(file_path)

# Specify the range of rows and the column name
start_row = 103130  # Replace with the starting row index (inclusive)
end_row = 14384   # Replace with the ending row index (exclusive)
column_name = 'DocID'  # Replace with the actual column name

# Get the list of values from the specified column for the specified range of rows
# values_list = df.loc[start_row:end_row, column_name].tolist()
df = df.loc[start_row:]

# Print the list of values
output_path = os.path.join('../..', 'data', 'FilteredDatasets', 'FilteredGlobalNewsDataset13_English.csv')
df.to_csv(output_path, index=False)
# print(values_list)