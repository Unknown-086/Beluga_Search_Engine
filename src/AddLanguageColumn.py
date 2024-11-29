import pandas as pd
from langdetect import detect, DetectorFactory

# Ensure consistent results from langdetect
DetectorFactory.seed = 0

# Load the dataset (update the file path to your dataset)
file_path = "D:\\zDSA Project\\DataSets\\data.csv\\data.csv"  # Replace with the path to your dataset
df = pd.read_csv(file_path)

# Function to detect language
def detect_language(text):
    try:
        return detect(text)  # Detect language of the text
    except Exception:
        return "unknown"  # Handle cases where detection fails

# Apply language detection to the 'title' column and create a new 'language' column
df['language'] = df['title'].apply(detect_language)

# Save the updated dataset with the new 'language' column
output_file = "D:\\zDSA Project\\DataSets\\data.csv\\updated_dataset_with_languages.csv"
df.to_csv(output_file, index=False)

print(f"Updated dataset with language column saved to {output_file}")
