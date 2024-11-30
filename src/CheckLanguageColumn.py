import pandas as pd
from WebTranslateAPI import AWSLanguageDetect
from langdetect import detect, DetectorFactory
import os

# Ensure consistent results from langdetect
DetectorFactory.seed = 0

# Construct the relative path to the dataset
file_path = os.path.join('..', 'data', 'FilteredDatasets', 'FilteredGlobalNewsDataset_Not_english.csv')
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

# Apply language detection to the appropriate column and create a new 'detected_language' column
df['detected_language'] = df.apply(lambda row: detect_language(get_text_for_language_detection(row)), axis=1)

# Filter the records by matching the detected language code with the language code in the dataset
filtered_df = df[df['language'] != df['detected_language']]

# Save the filtered records to a new file
output_file = os.path.join('..', 'data', 'FilteredDatasets', 'FilteredGlobalNewsDataset_Not_english2.csv')
filtered_df.to_csv(output_file, index=False)

print(f"Filtered records saved to {output_file}")