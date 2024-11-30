import pandas as pd
import os

# Construct the relative path to the dataset
file_path = os.path.join('..', 'data', 'ModifiedDatasets', 'ModifiedNews-week-17aug2.csv')
df = pd.read_csv(file_path)

# Specify the column and the value to filter by
column_name = 'headline_text'  # Replace with the actual column name
specific_value = 'w3-meneame'  # Replace with the specific year you are looking for

# Convert the 'created_date' column to datetime format

# Get the records that have the specific year in the column
filtered_df = df[df[column_name].isnull()]
# filtered_df = df[df[column_name] == specific_value]

####  For Filtering the Create_date Column In Reddit Dataset
# df[column_name] = pd.to_datetime(df[column_name])
# filtered_df = df[df[column_name].dt.year == int(specific_value)]

# Print the filtered records
print(filtered_df)

# Optionally, save the filtered records to a new file
output_file = os.path.join('..', 'data', 'FilteredDatasets', 'FilteredNews-week-17aug3.csv')
filtered_df.to_csv(output_file, index=False)

print(f"Filtered records saved to {output_file}")