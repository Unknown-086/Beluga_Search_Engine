import pandas as pd
import os

# Construct the relative path to the dataset
file_path = os.path.join('..', 'data', 'ModifiedDatasets', 'ModifiedReddit_database3.csv')
df = pd.read_csv(file_path)

# Specify the column to get unique values from
column_name = 'subreddit'  # Replace with the actual column name

# # Get the list of unique values in the specified column
# unique_values = ['analytics', 'deeplearning' , 'datascience' , 'datasets',  'kaggle', 'learnmachinelearning' ,
#                  'MachineLearning' , 'statistics' , 'artificial', 'AskStatistics' , 'computerscience' , 'computervision'  ,
#                  'dataanalysis', 'dataengineering' , 'DataScienceJobs', 'datascienceproject',  'data',
#                  'MLQuestions' , 'rstats']

# Get the list of unique values in the specified column
unique_values = []

# Create a separate filtered file for each unique value
for value in unique_values:
    filtered_df = df[df[column_name] == value]
    output_file = os.path.join('..', 'data', 'FilteredDatasets', f'FilteredReddit_{value}.csv')
    filtered_df.to_csv(output_file, index=False)
    print(f"Filtered records for '{value}' saved to {output_file}")