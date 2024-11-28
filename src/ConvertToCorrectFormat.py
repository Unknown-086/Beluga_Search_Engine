import chardet  # To detect encoding
from langdetect import detect, DetectorFactory

# # Ensure consistent results for language detection
# DetectorFactory.seed = 0
#
# # Step 1: Raw text (incorrectly encoded)
# raw_text = "Î£Î¿ÎºÎ¬ÏÎ¿Ï…Î½ Î¿Î¹ Î¼Î±ÏÏ„Ï…ÏÎ¯ÎµÏ‚ Ï†Î¿Î¹Ï„Î·Ï„ÏŽÎ½ Î±Ï€ÏŒ Ï„Î¿ ÎÎµÏ€Î¬Î» Ï€Î¿Ï… Î²ÏÎ­Î¸Î·ÎºÎ±Î½ ÏƒÏ„Î· Î´Î¯Î½Î· Ï„Î¿Ï… Ï€Î¿Î»Î­Î¼Î¿Ï… ÏƒÏ„Î· ÎœÎ­ÏƒÎ· Î‘Î½Î±Ï„Î¿Î»Î® Î±Î½Î¬Î¼ÎµÏƒÎ± ÏƒÏ„Î¿ Î™ÏƒÏÎ±Î®Î» ÎºÎ±Î¹ Ï„Î¿Ï…Ï‚ Ï„ÏÎ¿Î¼Î¿ÎºÏÎ¬Ï„ÎµÏ‚ Ï„Î·Ï‚ Î§Î±Î¼Î¬Ï‚. ÎŸÎ¹ Ï†Î¿Î¹Ï„Î·Ï„Î­Ï‚ Î±Ï€ÏŒ Ï„Î¿ ÎÎµÏ€Î¬Î» ÎµÏ€Î­ÏƒÏ„ÏÎµÏˆÎ±Î½ Ï€Î¯ÏƒÏ‰ ÏƒÏ„Î·Î½ Ï€Î±Ï„ÏÎ¯Î´Î± Ï„Î¿Ï…Ï‚ Î¼Îµ Ï„Î·Î½ Ï€ÏÏŽÏ„Î· ÎµÎ¹Î´Î¹ÎºÎ® Ï€Ï„Î®ÏƒÎ· Î±Ï€ÏŒ Ï„Î¿ Î™ÏƒÏÎ±Î®Î», Î­Î³Î¹Î½Î±Î½ Î´ÎµÎºÏ„Î¿Î¯â€¦"
#
# # raw_text = "Μέση Ανατολή: Σοκαριστικές μαρτυρίες φοιτητών του Νεπάλ, που επέστρεψαν στην πατρίδα τους"# Step 2: Convert text to the correct format
# def fix_encoding(text):
#     # Detect the likely encoding of the text
#     detected_encoding = chardet.detect(text.encode())['encoding']
#     # Decode and re-encode the text to fix the format
#     return text.encode(detected_encoding).decode('utf-8')
#
# try:
#     corrected_text = fix_encoding(raw_text)
# except Exception as e:
#     print("Encoding error:", e)
#     corrected_text = raw_text  # Use raw text if decoding fails
#
# print("Corrected Text:")
# print(corrected_text)
#
# # Step 3: Detect the language
# def detect_language(text):
#     try:
#         language = detect(text)
#         return language
#     except Exception as e:
#         return "unknown"
#
# detected_language = detect_language(corrected_text)
# print("Detected Language:", detected_language)



# Sample text (incorrectly encoded text)
raw_text = "Î£Î¿ÎºÎ¬ÏÎ¿Ï…Î½ Î¿Î¹ Î¼Î±ÏÏ„Ï…ÏÎ¯ÎµÏ‚ Ï†Î¿Î¹Ï„Î·Ï„ÏŽÎ½"

# Step 1: Fix the encoding for the sentence
def fix_encoding(text):
    try:
        # Attempt to decode the text from latin1 and then re-encode it to UTF-8
        fixed_text = text.encode('latin2').decode('utf-8')
        return fixed_text
    except Exception as e:
        print(f"Error fixing encoding: {e}")
        return text  # Return original text if something goes wrong

# Step 2: Apply the encoding fix
corrected_text = fix_encoding(raw_text)

# Step 3: Print the corrected text
print("Corrected Text:")
print(corrected_text)
