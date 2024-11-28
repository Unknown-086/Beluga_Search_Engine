import pandas as pd
from langdetect import detect, DetectorFactory, detect_langs
from langdetect.lang_detect_exception import LangDetectException
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
# file_path = "D:\zDSA Project\DataSets\Global_News_Dataset\Extracted_Data.csv"  # Replace with your dataset's file path
# dataset = pd.read_csv(file_path)
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


raw_text = "Î£Î¿ÎºÎ¬ÏÎ¿Ï…Î½ Î¿Î¹ Î¼Î±ÏÏ„Ï…ÏÎ¯ÎµÏ‚ Ï†Î¿Î¹Ï„Î·Ï„ÏŽÎ½ Î±Ï€ÏŒ Ï„Î¿ ÎÎµÏ€Î¬Î» Ï€Î¿Ï… Î²ÏÎ­Î¸Î·ÎºÎ±Î½ ÏƒÏ„Î· Î´Î¯Î½Î· Ï„Î¿Ï… Ï€Î¿Î»Î­Î¼Î¿Ï… ÏƒÏ„Î· ÎœÎ­ÏƒÎ· Î‘Î½Î±Ï„Î¿Î»Î® Î±Î½Î¬Î¼ÎµÏƒÎ± ÏƒÏ„Î¿ Î™ÏƒÏÎ±Î®Î» ÎºÎ±Î¹ Ï„Î¿Ï…Ï‚ Ï„ÏÎ¿Î¼Î¿ÎºÏÎ¬Ï„ÎµÏ‚ Ï„Î·Ï‚ Î§Î±Î¼Î¬Ï‚. ÎŸÎ¹ Ï†Î¿Î¹Ï„Î·Ï„Î­Ï‚ Î±Ï€ÏŒ Ï„Î¿ ÎÎµÏ€Î¬Î» ÎµÏ€Î­ÏƒÏ„ÏÎµÏˆÎ±Î½ Ï€Î¯ÏƒÏ‰ ÏƒÏ„Î·Î½ Ï€Î±Ï„ÏÎ¯Î´Î± Ï„Î¿Ï…Ï‚ Î¼Îµ Ï„Î·Î½ Ï€ÏÏŽÏ„Î· ÎµÎ¹Î´Î¹ÎºÎ® Ï€Ï„Î®ÏƒÎ· Î±Ï€ÏŒ Ï„Î¿ Î™ÏƒÏÎ±Î®Î», Î­Î³Î¹Î½Î±Î½ Î´ÎµÎºÏ„Î¿Î¯â€¦"

# Detect the language with probabilities
detected_language = detect(raw_text)
print(detected_language)  # Output includes all possible languages and their probabilities


# print(decode_text_safe(raw_text))


