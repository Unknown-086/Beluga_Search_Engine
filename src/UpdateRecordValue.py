from CrawlingWebLinks import CrawlUrl
import pandas as pd
import os

# Construct the relative path to the dataset
file_path = os.path.join('..', 'data', 'ModifiedDatasets', 'ModifiedGlobalNewsDatasetWithLanguage.csv')
df = pd.read_csv(file_path)

# Specify the condition to locate the record and the new value

# new_value = 'new_value'  # Replace with the new value you want to set

# updating the title of the record with DocIDs List
# DocIDs = [179410]
# for ID in DocIDs:
#     condition = (df['DocID'] == ID)  # Replace 'column_name' and 'specific_value' with actual values
#     url = df[condition]['url'].values[0]
#     new_value = CrawlUrl.crawl_url(url, 'title')  # Replace with the new value you want to set
#
#     # Update the record value
#     df.loc[condition, 'title'] = new_value  # Replace 'column_to_update' with the actual column name

condition = (df['DocID'] == ID)
df.loc[condition, 'title'] = new_value  # Replace 'column_to_update' with the actual column name

# Save the updated DataFrame back to the CSV file
df.to_csv(file_path, index=False)

print(f"Record updated and saved to {file_path}")