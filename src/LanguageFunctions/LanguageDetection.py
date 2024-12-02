import pandas as pd
from langdetect import detect, DetectorFactory, detect_langs
from langdetect.lang_detect_exception import LangDetectException
import time
#
# # Ensure consistent results from langdetect
# DetectorFactory.seed = 0
#
#
# def detect_language(text):
#     """
#     Detect the language of a given text.
#
#     Args:
#         text (str): The input text.
#
#     Returns:
#         str: Detected language code (e.g., 'en', 'fr', etc.) or 'unknown' if detection fails.
#     """
#     try:
#         if pd.isnull(text) or not text.strip():  # Handle empty or NaN cases
#             return "unknown"
#         return detect(text)
#     except LangDetectException:
#         return "unknown"
#
#
# # Load your dataset
# file_path1 = "D:\zDSA Project\DataSets\Global_News_Dataset\Extracted_Data.csv"  # Replace with your dataset's file path
# dataset = pd.read_csv(file_path1)
#
# # Add a new column for detected language
# dataset['detected_language'] = dataset['headline_text'].apply(detect_language)
#
# # Save the updated dataset
# output_path = "dataset_with_languages.csv"
# dataset.to_csv(output_path, index=False)
# print(f"Dataset with detected languages saved to {output_path}")



# Example for decoding
# raw_text = "Привет мир"
# corrected_text = raw_text.encode('latin1').decode('utf-8')
# print(corrected_text)  # Decoded Chinese text



# def decode_text_safe(text):
#     try:
#         # Attempt to decode assuming it is incorrectly encoded
#         return text.encode('latin1').decode('utf-8')
#     except (UnicodeEncodeError, UnicodeDecodeError):
#         # If decoding fails, return the original text
#         return text

# Example for detecting language
# text = "å°¼æ³Šçˆ¾èŠ±è²»æ•¸ç™¾è¬ç¾Žå…ƒå»ºé€ ä¸€åº§æ–°æ©Ÿå ´ï¼Œå¸Œæœ›è—‰æ­¤æŽ¨å‹•æ—…éŠæ¥­â€”â€”ä½†æ˜¯æ©Ÿå ´å»ºå¥½äº†ï¼Œå»æ²’æœ‰äººä¾†ã€‚"

def detect_language(text):
    try:
        return detect(text)  # Detect language of the text
    except Exception:
        return "unknown"  # Handle cases where detection fails

        #  "ଗ୍ୟାସ୍-ଏସିଡିଟି ପାଇଁ ରାମବାଣ ପରି କାମ କରିବ ଏହି ୪ ଆସନ"
raw_text = "Aロンドン, 2023年10月27日 /PRNewswire/ -- Zambia External Bondholder Steering Committee（ザンビア外債保有者運営委員会、以下「委員会」）は、ザンビアの（1）7億5000万米ドル、金利5.375%、2022年満期債券（2）10億米ドル、金利8.500%、2024年満期債券（3）12億5000万米ドル、金利8.970%、2027年償還債（総称して..."

start = time.time()
# Detect the language with probabilities
detectedLanguage = detect_language(raw_text)
end = time.time()
print(detectedLanguage)  # Output includes all possible languages and their probabilities
print(end - start)

# print(decode_text_safe(raw_text))


