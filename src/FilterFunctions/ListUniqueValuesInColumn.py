import pandas as pd
import os

# Construct the relative path to the dataset
file_path = os.path.join('../..', 'data', 'ModifiedDatasets', 'ModifiedNews-week-17aug_Language_4.csv')
df = pd.read_csv(file_path)

# Specify the column to get unique values from
column_name = 'feed_code'  # Replace with the actual column name

# Get the list of unique values in the specified column
unique_values = df[column_name].unique()

# Print the list of unique values
print(unique_values)
print(len(unique_values))