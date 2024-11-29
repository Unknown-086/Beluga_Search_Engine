import pandas as pd

# Load the dataset with the 'language' column
file_path = "D:\\zDSA Project\\DataSets\data.csv\\updated_dataset_with_languages.csv"  # Replace with your file path
df = pd.read_csv(file_path)

# Count rows where the 'language' column has the value 'en'
english_count = df[df['language'] != 'en'].shape[0]

print(f"Number of rows with English language ('en'): {english_count}")
