import pandas as pd
from src.WebTranslateAPI.AWSLanguageDetect import AWS_detect_language
from langdetect import detect, DetectorFactory
import os

# Ensure consistent results from langdetect
DetectorFactory.seed = 0

# Construct the relative path to the dataset
file_path = os.path.join('../..', 'data', 'FilteredDatasets', 'FilteredReddit_database5_Non_English.csv')
df = pd.read_csv(file_path)

# Function to detect language
def detect_language(text):
    try:
        return detect(text)  # Detect language of the text
    except Exception:
        return "unknown"  # Handle cases where detection fails

# Function to get the text for language detection
def get_text_for_language_detection(row):
    if pd.isna(row['post']):
        return row['title']
    return row['post']

# Apply language detection to the appropriate column and create a new 'detected_language' column
# df['language'] = df.apply(lambda row: AWS_detect_language(get_text_for_language_detection(row)), axis=1)

df['language'] = df.apply(lambda row: detect_language(get_text_for_language_detection(row)), axis=1)

# Filter the records by matching the detected language code with the language code in the dataset

# Save the filtered records to a new file
output_file = os.path.join('../..', 'data', 'FilteredDatasets', 'FilteredReddit_database5_Non_English_By_Post.csv')
df.to_csv(output_file, index=False)

print(f"Updates records saved to {output_file}")