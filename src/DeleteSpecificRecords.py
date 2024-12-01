import pandas as pd
import os

# Construct the relative path to the dataset
file_path = os.path.join('..', 'data', 'FilteredDatasets', 'FilteredNews-week-17aug5_Non_English.csv')
df = pd.read_csv(file_path)

# Specify the column name and the value to filter out
column_name = 'language'
value = 'unknown'
# value_to_delete = [106574]

# Filter out the rows that match the specific column values from the list
# for value in value_to_delete:
# df_filtered = df[df[column_name] != value]
# df_filtered = df[df[column_name].notnull()]


# Specify the interval for deleting records and the target length
N = 3

#  For Deleting Every Nth Record giving   1/N * records
df_filtered = df.iloc[::N]

#  For Deleting Every Nth Record giving   N-1/N * records
# df_filtered = df.drop(df.index[::N])

print(len(df_filtered))
# Save the updated dataset to a new file
output_file = os.path.join('..', 'data', 'FilteredDatasets', 'FilteredNews-week-17aug5_Non_English_6.csv')
df_filtered.to_csv(output_file, index=False)

# print(f"Rows with {column_name} = {value} have been deleted and saved to {output_file}")
print(f"Filtered dataset saved to {output_file} By deleting Every {N}th Record")