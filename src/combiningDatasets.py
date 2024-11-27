import pandas as pd

# Paths to your two datasets
dataset1_path = "D:\\zDSA Project\\DataSets\\dataverse_files\\extracted_dataset1.csv"  # Replace with the actual path to the first dataset
dataset2_path = "D:\\zDSA Project\\DataSets\\dataverse_files\\extracted_dataset2.csv"  # Replace with the actual path to the second dataset
output_path = "D:\\zDSA Project\\DataSets\\dataverse_files\\combined_dataset.csv"  # Path to save the combined dataset

# Load the datasets
dataset1 = pd.read_csv(dataset1_path)  # Adjust delimiter if necessary
dataset2 = pd.read_csv(dataset2_path)  # Adjust delimiter if necessary

# Combine the datasets
combined_dataset = pd.concat([dataset1, dataset2], ignore_index=True)

# Save the combined dataset to a new file
combined_dataset.to_csv(output_path, index=False)

print(f"Combined dataset saved to {output_path}")
