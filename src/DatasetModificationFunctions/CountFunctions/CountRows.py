import pandas as pd
import os

# Load the CSV file
file_path1 = os.path.join('../../..', 'data', 'FilteredDatasets', 'FilteredReddit_database3.csv')
# file_path2 = os.path.join('..', 'data', 'ModifiedDatasets', 'ModifiedGlobalNewsDataset7.csv')




file_paths = [
                # os.path.join('..', 'data', 'FilteredDatasets', 'FilteredGlobalNewsDataset9_English.csv'),
                # os.path.join('..', 'data', 'FilteredDatasets', 'FilteredGlobalNewsDataset9_Non_English.csv'),
                #
                # os.path.join('..', 'data', 'FilteredDatasets', 'FilteredReddit_database7_English_Sorted_8.csv'),
                # os.path.join('..', 'data', 'FilteredDatasets', 'FilteredReddit_database7_Non_English.csv'),
                #
                # os.path.join('..', 'data', 'FilteredDatasets', 'FilteredNews-week-18aug4_English_5.csv'),
                # os.path.join('..', 'data', 'FilteredDatasets', 'FilteredNews-week-18aug4_Non_English_5.csv'),
                #
                # os.path.join('..', 'data', 'FilteredDatasets', 'FilteredNews-week-17aug5_English_6.csv'),
                # os.path.join('..', 'data', 'FilteredDatasets', 'FilteredNews-week-17aug5_Non_English_6.csv')

                #
                # os.path.join('../../..', 'data', 'FilteredDatasets', 'ModifiedGlobalNewsDataset13_Language_English_Langauge.csv'),
                # os.path.join('../../..', 'data', 'FilteredDatasets', 'ModifiedReddit_database11_English.csv'),
                os.path.join('../../..', 'data', 'FilteredDatasets', 'ModifiedGlobalNewsDataset13_Language_English_Langauge.csv'),
                # os.path.join('../../..', 'data', 'FilteredDatasets', 'ModifiedNews-week-18aug7_Non_English.csv')

                # os.path.join('../../..', 'data', 'ModifiedDatasets', 'ModifiedNews-week-18aug7.csv'),
                # os.path.join('../../..', 'data', 'ModifiedDatasets', 'ModifiedReddit_database100.csv'),
                # os.path.join('../../..', 'data', 'ModifiedDatasets', 'ModifiedNews-week-17aug100.csv'),
                # os.path.join('../../..', 'data', 'ModifiedDatasets', 'ModifiedNews-week-18aug100.csv')

                # os.path.join('../../..', 'data', 'FilteredDatasets', 'ModifiedNews-week-18aug7_Non_English.csv')

                # os.path.join('../..', 'data', 'ModifiedDatasets', 'ModifiedNews-week-17aug6.csv'),
                #
                # os.path.join('../..', 'data', 'ModifiedDatasets', 'ModifiedNews-week-18aug5.csv')
                # os.path.join('..', 'data', 'ModifiedDatasets', 'ModifiedReddit_database7.csv')
]

column_name = 'language'
value = 'en'

list = []
number = 0

for file in file_paths:
    df = pd.read_csv(file)
    # df = df[df[column_name].isnull()]
    # df = df[df[column_name] != value]


    # Get the total number of rows
    total_rows = df.shape[0]
    list.insert(number, total_rows)
    number += 1
    print(f"Total number of rows in the {file} file: {total_rows}")

sum_count = 0
for i in list:
    sum_count += i

print(sum_count)