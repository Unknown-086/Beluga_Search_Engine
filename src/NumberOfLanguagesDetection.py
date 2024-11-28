import pandas as pd
from langdetect import detect, DetectorFactory

# Ensure consistent results from langdetect
DetectorFactory.seed = 0

# Load the dataset (update the file path to your dataset)
file_path = "D:\\zDSA Project\\DataSets\\Global_News_Dataset\\Extracted_Data.csv" # Replace with your dataset file path
df = pd.read_csv(file_path)

# Function to detect language
def detect_language(text):
    try:
        return detect(text)  # Detect language of the text
    except Exception:
        return "unknown"  # Handle cases where detection fails

# Specify the column containing the text to analyze (e.g., 'title')
df['language'] = df['title'].apply(detect_language)  # Replace 'title' with the appropriate column name

# Find unique languages
unique_languages = df['language'].unique()

# Print results
print(f"Number of different languages: {len(unique_languages)}")
print(f"List of detected languages: {unique_languages}")
