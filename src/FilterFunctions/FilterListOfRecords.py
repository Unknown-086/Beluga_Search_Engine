import pandas as pd
import os

# Construct the relative path to the dataset
file_path = os.path.join('../..', 'data', 'FilteredDatasets', 'FilteredNews-week-17aug1.csv')
df = pd.read_csv(file_path)

# Specify the range of rows and the column name
start_row = 0  # Replace with the starting row index (inclusive)
end_row = 14384   # Replace with the ending row index (exclusive)
column_name = 'DocID'  # Replace with the actual column name

# Get the list of values from the specified column for the specified range of rows
values_list = df.loc[start_row:end_row, column_name].tolist()

# Print the list of values
print(values_list)