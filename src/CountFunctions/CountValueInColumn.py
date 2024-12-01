import pandas as pd

# Load the dataset with the 'language' column
file_path = "D:\\zDSA Project\\PartOne\\Search_Engine_DSA_project\\data\\Datasets\\news-week-17aug24.csv"  # Replace with your file path
df = pd.read_csv(file_path)

# Count rows where the 'language' column has the value 'en'
english_count = df[df['feed_code'] == 'w3-meneame'].shape[0]

print(f"Number of rows with English language ('en'): {english_count}")
