import pandas as pd
import os

# Paths to your two datasets
dataset1_path = os.path.join('..','data', 'FilteredDatasets', 'ModifiedNews-week-18aug5_English.csv')  # Replace with the actual path to the first dataset
dataset2_path = os.path.join('..','data', 'FilteredDatasets', 'ModifiedNews-week-18aug5_Non_English.csv')  # Replace with the actual path to the second dataset
output_path = os.path.join('..', 'data',  'ModifiedDatasets', 'ModifiedNews-week-18aug6.csv')  # Path to save the combined dataset

# Load the datasets
dataset1 = pd.read_csv(dataset1_path)  # Adjust delimiter if necessary
dataset2 = pd.read_csv(dataset2_path)  # Adjust delimiter if necessary

# Combine the datasets
combined_dataset = pd.concat([dataset1, dataset2], ignore_index=True)

# Save the combined dataset to a new file
combined_dataset.to_csv(output_path, index=False)

print(f"Combined dataset saved to {output_path}")