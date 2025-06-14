import time

import pandas as pd
from src.WebTranslateAPI import AWSLanguageDetect
from langdetect import detect, DetectorFactory
import os

# Ensure consistent results from langdetect
DetectorFactory.seed = 0

start = time.time()

# Construct the relative path to the dataset
file_path = os.path.join('../../..', 'data', 'FilteredDatasets', 'ModifiedGlobalNewsDataset13_Language_English_withoutLangauge.csv')
df = pd.read_csv(file_path)

# Function to detect language
def detect_language(text):
    try:
        return detect(text)  # Detect language of the text
    except Exception:
        return "unknown"  # Handle cases where detection fails

# Function to get the text for language detection
def get_text_for_language_detection(row):
    if pd.isna(row['title']):
        return row['description']
    return row['title']

# Apply language detection to the appropriate column and create a new 'language' column
df['language'] = df.apply(lambda row: detect_language(get_text_for_language_detection(row)), axis=1)

# Apply language detection to the 'title' column and create a new 'language' column
# df['language'] = df['headline_text'].apply(detect_language)

# Save the updated dataset with the new 'language' column
output_file = os.path.join('../../..', 'data', 'FilteredDatasets', 'ModifiedGlobalNewsDataset13_Language_English_Langauge.csv')
df.to_csv(output_file, index=False)

end = time.time()
print(f"Updated dataset with language column saved to {output_file}")
print(f"Time taken: {end - start:.2f} seconds")
