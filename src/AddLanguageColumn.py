import pandas as pd
from langdetect import detect, DetectorFactory
import os

# Ensure consistent results from langdetect
DetectorFactory.seed = 0

# Construct the relative path to the dataset
file_path = os.path.join('..', 'data', 'ModifiedDatasets', 'ModifiedGlobalNewsDatasetWithDocID.csv')
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
output_file = os.path.join('..', 'data', 'ModifiedDatasets', 'ModifiedGlobalNewsDatasetWithLanguage.csv')
df.to_csv(output_file, index=False)

print(f"Updated dataset with language column saved to {output_file}")