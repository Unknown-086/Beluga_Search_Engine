import pandas as pd
import os

# Load the CSV file
file_path1 = os.path.join('..', 'data', 'FilteredDatasets', 'FilteredReddit_database3.csv')
# file_path2 = os.path.join('..', 'data', 'ModifiedDatasets', 'ModifiedGlobalNewsDataset7.csv')




file_paths = [
                os.path.join('..', 'data', 'ModifiedDatasets', 'ModifiedNews-week-17aug3.csv')
                # os.path.join('..', 'data', 'FilteredDatasets', 'FilteredNews-week-17aug24WithNUll.csv')
]

# column_name = 'headline_text'
list = []
number = 0
for file in file_paths:
    df = pd.read_csv(file)
    # df = df[df[column_name].isnull()]

    # Get the total number of rows
    total_rows = df.shape[0]
    list.insert(number, total_rows)
    number += 1
    print(f"Total number of rows in the {file} file: {total_rows}")

sum_count = 0
for i in list:
    sum_count += i

print(sum_count)