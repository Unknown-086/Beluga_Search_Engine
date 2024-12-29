import boto3
import time

# Initialize a session using Amazon Translate
translate = boto3.client('translate', region_name='us-east-1')  # Change region as needed

def translate_text(text, source_lang = 'auto', target_lang = 'en'):
    # Translate text
    response = translate.translate_text(
        Text=text,
        SourceLanguageCode=source_lang, # Detect source language automatically
        TargetLanguageCode=target_lang # Translate to English
    )
    return response['TranslatedText']

# Example usage
if __name__ == "__main__":
    start = time.time()
    source_text = "بھاڑ میں جاؤ"
    translated_text = translate_text(source_text)  # Korean to English
    end = time.time()
    print(f"Translated Text: {translated_text}")
    print(end - start)

